// rows4.cpp - "Byrnes-row" solver for 4xn Chomp.
//
// A position is (a,b,c,d), a>=b>=c>=d>=0, a>=1 (row lengths, a = poisoned row).
// Fix the pair of short rows (c,d). Moves from (a,b,c,d) are:
//
//   same pair (c,d):
//     row a, col j in [b, a)   -> (j, b, c, d)
//     row a, col j in [c, b)   -> (j, j, c, d)          "diagonal" move (j>=1)
//     row b, col j in [c, b)   -> (a, j, c, d)
//   lower pairs:
//     row a, col j in [1, c)   -> (j, j, j, min(d,j))   constant position
//     row b, col j in [0, c)   -> (a, j, j, min(d,j))   pair (j,min(d,j)) at b'=j
//     row c, col j in [0, c)   -> (a, b, j, min(d,j))   pair (j,min(d,j)) at same b
//     row d, col j in [0, d)   -> (a, b, c, j)          pair (c,j)        at same b
//
// So for each pair p=(c,d) the P-positions form a partial function
//      b -> a_p(b)   (b >= c),
// computed greedily in b: a_p(b) = least a >= max(b,1) that is not
//   * already used by a smaller b in this pair,
//   * in F_p = { a_q(j) : q=(j,min(d,j)), j<c },
//   * equal to a_q(b) for a lower pair q (row-c / row-d moves),
// and no P exists at all once a diagonal P (x,x,c,d) with x<b appeared,
// or if some constant position (j,j,j,min(d,j)), 1<=j<c, is P.
//
// Pairs are processed along anti-diagonals s=c+d (all dependencies have
// smaller s), each anti-diagonal in parallel.
//
// Output (binary, little endian):
//   int32 C, int32 A
//   for c=0..C, d=0..c:  (A-c+1) x uint16  delta = a-b  (0xFFFF = none <= A)
//
// Usage: rows4 C A out.bin [threads]

#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <thread>
#include <atomic>
#include <chrono>
#include <algorithm>

using namespace std;

static int C, A;
static vector<uint16_t*> rowp;           // rowp[idx(c,d)][b-c] = a-b or NONE
static const uint16_t NONE = 0xFFFF;

static inline size_t pidx(int c, int d) { return (size_t)c * (c + 1) / 2 + d; }

static inline int getA(int c, int d, int b) {  // a_p(b) or -1
    uint16_t v = rowp[pidx(c, d)][b - c];
    return v == NONE ? -1 : b + v;
}

static void solve_pair(int c, int d, vector<int>& mark, vector<uint8_t>& used) {
    uint16_t* out = rowp[pidx(c, d)];
    int len = A - c + 1;
    // constant-position kill
    for (int j = 1; j < c; ++j) {
        if (getA(j, min(d, j), j) == j) {
            for (int i = 0; i < len; ++i) out[i] = NONE;
            return;
        }
    }
    fill(used.begin(), used.end(), 0);
    for (int j = 0; j < c; ++j) {
        int a = getA(j, min(d, j), j);
        if (a >= 0) used[a] = 1;
    }
    // lower pair list for row-c and row-d moves
    vector<const uint16_t*> lp;
    vector<int> lc;
    for (int j = 0; j < c; ++j) { lp.push_back(rowp[pidx(j, min(d, j))]); lc.push_back(j); }
    for (int j = 0; j < d; ++j) { lp.push_back(rowp[pidx(c, j)]); lc.push_back(c); }
    const int nl = (int)lp.size();

    bool dead = false;
    for (int b = c; b <= A; ++b) {
        if (dead) { out[b - c] = NONE; continue; }
        for (int k = 0; k < nl; ++k) {
            uint16_t v = lp[k][b - lc[k]];
            if (v != NONE) mark[b + v] = b;
        }
        int a = max(b, 1);
        while (a <= A && (used[a] || mark[a] == b)) ++a;
        if (a > A) { out[b - c] = NONE; continue; }
        out[b - c] = (uint16_t)(a - b);
        used[a] = 1;
        if (a == b) dead = true;  // diagonal P (b,b,c,d): kills all larger b
    }
}

int main(int argc, char** argv) {
    if (argc < 4) { fprintf(stderr, "usage: rows4 C A out.bin [threads]\n"); return 1; }
    C = atoi(argv[1]); A = atoi(argv[2]);
    const char* outpath = argv[3];
    int T = argc >= 5 ? atoi(argv[4]) : (int)thread::hardware_concurrency();
    if (A >= 65535) { fprintf(stderr, "A must be < 65535\n"); return 1; }
    size_t npairs = pidx(C, C) + 1;
    size_t total = 0;
    for (int c = 0; c <= C; ++c) total += (size_t)(c + 1) * (A - c + 1);
    fprintf(stderr, "pairs=%zu  storage=%.1f MB  threads=%d\n", npairs, total * 2.0 / 1048576, T);
    uint16_t* store = (uint16_t*)malloc(total * sizeof(uint16_t));
    if (!store) { fprintf(stderr, "alloc failed\n"); return 1; }
    rowp.resize(npairs);
    size_t off = 0;
    for (int c = 0; c <= C; ++c)
        for (int d = 0; d <= c; ++d) { rowp[pidx(c, d)] = store + off; off += A - c + 1; }

    auto t0 = chrono::steady_clock::now();
    vector<vector<int>> marks(T, vector<int>(A + 2, -1));
    vector<vector<uint8_t>> useds(T, vector<uint8_t>(A + 2, 0));
    for (int s = 0; s <= 2 * C; ++s) {
        vector<pair<int, int>> todo;
        for (int d = 0; d <= s / 2; ++d) { int c = s - d; if (c <= C && d <= c) todo.push_back({c, d}); }
        atomic<int> next(0);
        auto worker = [&](int t) {
            for (;;) {
                int i = next.fetch_add(1);
                if (i >= (int)todo.size()) break;
                fill(marks[t].begin(), marks[t].end(), -1);
                solve_pair(todo[i].first, todo[i].second, marks[t], useds[t]);
            }
        };
        int nt = min<int>(T, todo.size());
        vector<thread> th;
        for (int t = 0; t < nt; ++t) th.emplace_back(worker, t);
        for (auto& x : th) x.join();
        if (s % 20 == 0) {
            double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
            fprintf(stderr, "s=%d/%d  %.1fs\n", s, 2 * C, el);
        }
    }
    FILE* f = fopen(outpath, "wb");
    int32_t hdr[2] = {C, A};
    fwrite(hdr, sizeof(int32_t), 2, f);
    fwrite(store, sizeof(uint16_t), total, f);
    fclose(f);
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    fprintf(stderr, "done %.1fs -> %s\n", el, outpath);
    return 0;
}
