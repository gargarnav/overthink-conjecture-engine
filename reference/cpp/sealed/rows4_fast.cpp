// rows4_fast.cpp - b-outer Byrnes-row solver for 4xn Chomp with sliding windows.
//
// Same recursion as rows4.cpp (see there for the move analysis), but the loop
// order is b (outer) -> c -> d, so every exclusion set is a small bitset
// relative to b:
//   S[d]  = { a_q(b) : q = (j,min(d,j)), j < c }     (row-c moves)
//   FS[d] = { a_q(j) : q = (j,min(d,j)), j < c }     (row-b moves, F_p)
//   T     = { a_(c,j)(b) : j < d }                   (row-d moves)
//   used_p (ring buffer, a mod WB)                   (row-b moves within pair)
// All candidate a lie in [b, b+WB); the program aborts if that is violated.
// Memory is O(pairs * WB) bits, independent of A.
//
// Per pair it records: status, diagonal, first a, #never-used a (>= max(c,1),
// <= A: equals the mean eventual shift for live pairs), max unused a,
// and the last TL deltas (b in (A-TL, A]) for period detection.
// With a periods file (pass 2) it also records, for each pair with period
// pi, the last b with delta(b) != delta(b-pi)  -> pre-period end.
//
// usage: rows4_fast C A WB TL out_prefix [periods.csv]
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <chrono>
#include <algorithm>
using namespace std;

static int C, A, WB, WW, TL;
static inline size_t pidx(int c, int d) { return (size_t)c * (c + 1) / 2 + d; }

int main(int argc, char** argv) {
    if (argc < 6) { fprintf(stderr, "usage: rows4_fast C A WB TL out_prefix [periods.csv]\n"); return 1; }
    C = atoi(argv[1]); A = atoi(argv[2]); WB = atoi(argv[3]); TL = atoi(argv[4]);
    const char* pre = argv[5];
    const char* perfile = argc > 6 ? argv[6] : nullptr;
    WW = WB / 64;
    if (WB % 64 || (WB & (WB - 1))) { fprintf(stderr, "WB must be a power of two >= 64\n"); return 1; }
    const size_t NP = pidx(C, C) + 1;
    vector<uint64_t> ring(NP * WW, 0);
    vector<int> curA(NP, -1), firstA(NP, -1), diag(NP, -1), maxUnused(NP, -1);
    vector<char> empty(NP, 0);
    vector<long long> unused(NP, 0);
    vector<uint16_t> tail(NP * (size_t)TL, 0xFFFF);
    // pass-2 period tracking
    vector<int> per(NP, 0), lastMis(NP, -1);
    vector<uint16_t> hist;  // ring of deltas of length HL per pair
    int HL = 0;
    if (perfile) {
        FILE* pf = fopen(perfile, "r");
        int c, d, p;
        char line[256];
        fgets(line, sizeof line, pf);
        while (fscanf(pf, "%d,%d,%d", &c, &d, &p) == 3) { per[pidx(c, d)] = p; HL = max(HL, p); }
        fclose(pf);
        HL = max(HL, 1);
        hist.assign(NP * (size_t)HL, 0xFFFF);
    }
    vector<uint64_t> S((size_t)(C + 1) * WW), FS((size_t)(C + 1) * WW), T(WW);
    const uint64_t RMASK = (uint64_t)WB - 1;

    auto ringword = [&](const uint64_t* r, int s) -> uint64_t {  // 64 bits from bit s (mod WB)
        int w = (s >> 6) % WW, sh = s & 63;
        uint64_t lo = r[w] >> sh;
        if (sh) lo |= r[(w + 1) % WW] << (64 - sh);
        return lo;
    };

    auto t0 = chrono::steady_clock::now();
    for (int b = 0; b <= A + 1; ++b) {
        // retire value v=b-1 (final for every pair)
        if (b >= 1) {
            int v = b - 1;
            int cm = min(v, C);
            for (int c = 0; c <= cm; ++c)
                for (int d = 0; d <= c; ++d) {
                    size_t p = pidx(c, d);
                    uint64_t* r = &ring[p * WW];
                    int bit = v & RMASK;
                    bool u = (r[bit >> 6] >> (bit & 63)) & 1;
                    if (!u && !empty[p] && diag[p] < 0 && v >= max(c, 1)) { ++unused[p]; maxUnused[p] = v; }
                    r[bit >> 6] &= ~(1ULL << (bit & 63));
                }
        }
        if (b > A) break;
        const int cmax = min(b, C);
        memset(S.data(), 0, S.size() * 8);
        memset(FS.data(), 0, FS.size() * 8);
        for (int c = 0; c <= cmax; ++c) {
            memset(T.data(), 0, WW * 8);
            for (int d = 0; d <= c; ++d) {
                size_t p = pidx(c, d);
                if (b == c) {  // pair created: constant-position kill
                    for (int j = 1; j < c; ++j)
                        if (firstA[pidx(j, min(d, j))] == j) { empty[p] = 1; break; }
                }
                int a = -1;
                if (!empty[p] && !(diag[p] >= 0 && diag[p] < b)) {
                    const uint64_t* sd = &S[(size_t)d * WW];
                    const uint64_t* fd = &FS[(size_t)d * WW];
                    const uint64_t* r = &ring[p * WW];
                    int i0 = (b == 0) ? 1 : 0;
                    int k = 0;
                    uint64_t ex = sd[0] | fd[0] | T[0] | ringword(r, b & RMASK);
                    ex |= (1ULL << i0) - 1;
                    while (ex == ~0ULL) {
                        if (++k >= WW) { fprintf(stderr, "window overflow at b=%d c=%d d=%d\n", b, c, d); return 2; }
                        ex = sd[k] | fd[k] | T[k] | ringword(r, (b + 64 * k) & RMASK);
                    }
                    int i = 64 * k + __builtin_ctzll(~ex);
                    if (i >= WB - 64) { fprintf(stderr, "window near-overflow at b=%d c=%d d=%d\n", b, c, d); return 2; }
                    a = b + i;
                    if (a > A) a = -1;
                }
                curA[p] = a;
                if (a >= 0) {
                    int i = a - b;
                    uint64_t* r = &ring[p * WW];
                    int bit = a & RMASK;
                    r[bit >> 6] |= 1ULL << (bit & 63);
                    T[i >> 6] |= 1ULL << (i & 63);
                    if (b == c) firstA[p] = a;
                    if (a == b) diag[p] = b;
                }
                uint16_t dv = a >= 0 ? (uint16_t)(a - b) : 0xFFFF;
                if (b > A - TL) tail[p * TL + (b - (A - TL + 1))] = dv;
                if (perfile && per[p] > 0 && dv != 0xFFFF) {  // NONE = truncated (a > A): ignore
                    int pi = per[p];
                    uint16_t* h = &hist[p * HL];
                    int slot = (b - c) % pi;
                    if (b - c >= pi && h[slot] != dv) lastMis[p] = b;
                    h[slot] = dv;
                }
            }
            // row c finished: extend S[d], FS[d] with pair (c, min(c,d))
            for (int d = 0; d <= C; ++d) {
                size_t q = pidx(c, min(c, d));
                int aq = curA[q];
                if (aq >= 0) { int i = aq - b; S[(size_t)d * WW + (i >> 6)] |= 1ULL << (i & 63); }
                int fq = firstA[q];
                if (fq >= b && fq - b < WB) { int i = fq - b; FS[(size_t)d * WW + (i >> 6)] |= 1ULL << (i & 63); }
            }
        }
        if (b % 5000 == 0) {
            double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
            fprintf(stderr, "b=%d %.1fs\n", b, el);
        }
    }
    char path[512];
    snprintf(path, sizeof path, "%s_pairs.csv", pre);
    FILE* f = fopen(path, "w");
    fprintf(f, "c,d,status,diag,firstA,unused,maxUnused%s\n", perfile ? ",period,lastMismatch" : "");
    for (int c = 0; c <= C; ++c)
        for (int d = 0; d <= c; ++d) {
            size_t p = pidx(c, d);
            const char* st = empty[p] ? "EMPTY" : (diag[p] >= 0 ? "DEAD" : "ALIVE");
            fprintf(f, "%d,%d,%s,%d,%d,%lld,%d", c, d, st, diag[p], firstA[p], unused[p], maxUnused[p]);
            if (perfile) fprintf(f, ",%d,%d", per[p], lastMis[p]);
            fprintf(f, "\n");
        }
    fclose(f);
    snprintf(path, sizeof path, "%s_tail.bin", pre);
    f = fopen(path, "wb");
    int32_t hdr[3] = {C, A, TL};
    fwrite(hdr, 4, 3, f);
    fwrite(tail.data(), 2, tail.size(), f);
    fclose(f);
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    fprintf(stderr, "done %.1fs\n", el);
    return 0;
}
