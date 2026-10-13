// rows3_fast.cpp - fast Byrnes-row solver for 3xn Chomp (b outer, c inner).
//
// Row c: P-positions (a_c(b), b, c), b >= c.  a_c(b) = least a >= max(b,1) with
//   a not used in row c at smaller b         (row-b move within row c)
//   a not in F_c = { a_j(j) : j < c }         (row-b move to (a,j,j))
//   a not in { a_j(b) : j < c }               (row-c move to (a,b,j))
// and no P once row c had a diagonal a_c(x) = x with x < b.
// All three exclusion sets are bitsets; the scan is word-parallel.
//
// Output (text): per row c <= C
//   c status x firstA unused maxUnused      status: A(live) / D(dead at x)
// where unused = #{a in [max(c,1), A] never used in row c}  (= mean eventual
// shift for live rows, once A is well beyond 2c).
//
// usage: rows3_fast C A out.txt
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <chrono>
using namespace std;

int main(int argc, char** argv) {
    int C = atoi(argv[1]), A = atoi(argv[2]);
    const char* outp = argv[3];
    const int W = (A + 64) / 64 + 1;
    vector<uint64_t> used((size_t)(C + 1) * W, 0);   // used[c][word]
    auto U = [&](int w, int c) -> uint64_t& { return used[(size_t)c * W + w]; };
    auto isU = [&](int a, int c) -> bool { return (U(a >> 6, c) >> (a & 63)) & 1; };
    vector<int> pos(C + 1, 1);   // pos[c] = least a >= 1 not used in row c (all of [b,pos) used)
    vector<uint64_t> mark(W, 0), fset(W, 0);
    vector<int> dead(C + 1, -1), firstA(C + 1, -1);
    auto t0 = chrono::steady_clock::now();
    for (int b = 0; b <= A; ++b) {
        // per-b bitsets: mark = {a_j(b) : j < c}, fset = F_c ; both grow with c
        int wlo = b >> 6;
        memset(&mark[wlo], 0, (W - wlo) * 8);
        memset(&fset[wlo], 0, (W - wlo) * 8);
        int cmax = b < C ? b : C;
        for (int c = 0; c <= cmax; ++c) {
            if (c > 0) {
                int f = firstA[c - 1];
                if (f >= b) fset[f >> 6] |= 1ULL << (f & 63);
            }
            if (dead[c] >= 0 && dead[c] < b) continue;
            int a = b < 1 ? 1 : b;
            if (pos[c] < a) { pos[c] = a; while (pos[c] <= A && isU(pos[c], c)) ++pos[c]; }
            a = pos[c];   // every value in [max(b,1), pos[c]) is already used in row c
            if (a > A) continue;
            int w = a >> 6;
            uint64_t ex = (mark[w] | fset[w] | U(w, c)) | ((1ULL << (a & 63)) - 1);
            while (ex == ~0ULL && w + 1 < W) { ++w; ex = mark[w] | fset[w] | U(w, c); }
            if (ex == ~0ULL) continue;
            a = (w << 6) + __builtin_ctzll(~ex);
            if (a > A) continue;
            U(a >> 6, c) |= 1ULL << (a & 63);
            if (a == pos[c]) while (pos[c] <= A && isU(pos[c], c)) ++pos[c];
            mark[a >> 6] |= 1ULL << (a & 63);
            if (b == c) firstA[c] = a;
            if (a == b) dead[c] = b;
        }
        if (b % 5000 == 0) {
            double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
            fprintf(stderr, "b=%d %.1fs\n", b, el);
        }
    }
    FILE* f = fopen(outp, "w");
    fprintf(f, "c,status,x,firstA,unused,maxUnused\n");
    vector<long long> cnt(C + 1, 0);
    vector<int> mx(C + 1, -1);
    for (int w = 0; w < W; ++w) {
        int base = w << 6;
        for (int c = 0; c <= C; ++c) {
            int lo = c < 1 ? 1 : c;                       // count a in [lo, A]
            uint64_t bits = ~U(w, c);
            if (base + 63 < lo || base > A) continue;
            if (lo > base) bits &= ~0ULL << (lo - base);
            if (A < base + 63) bits &= (A - base == 63) ? ~0ULL : ((1ULL << (A - base + 1)) - 1);
            if (bits) { cnt[c] += __builtin_popcountll(bits); mx[c] = base + 63 - __builtin_clzll(bits); }
        }
    }
    for (int c = 0; c <= C; ++c)
        fprintf(f, "%d,%c,%d,%d,%lld,%d\n", c, dead[c] >= 0 ? 'D' : 'A', dead[c], firstA[c], cnt[c], mx[c]);
    fclose(f);
    return 0;
}
