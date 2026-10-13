// krow_brute.cpp - brute-force P/N solver for k-row Chomp in a k x N box.
// Positions: non-increasing tuples r[0]>=...>=r[k-1]>=0 with r[0]>=1.
// Move: pick row i, column j < r[i], (i,j) != (0,0): r[t] = min(r[t], j) for t>=i.
// Output: all P-positions, one per line, space separated.
//
// usage: krow_brute k N > out.txt
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

int K, N;
vector<vector<int>> all;

void gen(vector<int>& cur, int i, int maxv) {
    if (i == K) { if (cur[0] >= 1) all.push_back(cur); return; }
    for (int v = 0; v <= maxv; ++v) { cur[i] = v; gen(cur, i + 1, v); }
}

static inline uint64_t enc(const vector<int>& r) {  // base N+1, checked to fit in 63 bits
    uint64_t h = 0;
    for (int x : r) h = h * (uint64_t)(N + 1) + x;
    return h;
}

int main(int argc, char** argv) {
    K = atoi(argv[1]); N = atoi(argv[2]);
    { long double cap = 1; for (int i = 0; i < K; ++i) cap *= (N + 1);
      if (cap >= 9.2e18L) { fprintf(stderr, "(N+1)^k too large for 64-bit key\n"); return 1; } }
    vector<int> cur(K);
    gen(cur, 0, N);
    sort(all.begin(), all.end(), [](const vector<int>& x, const vector<int>& y) {
        int sx = 0, sy = 0; for (int v : x) sx += v; for (int v : y) sy += v; return sx < sy; });
    unordered_map<uint64_t, char> isP;
    isP.reserve(all.size() * 2);
    vector<int> nxt(K);
    for (auto& r : all) {
        bool P = true;
        for (int i = 0; i < K && P; ++i)
            for (int j = (i == 0 ? 1 : 0); j < r[i] && P; ++j) {
                for (int t = 0; t < K; ++t) nxt[t] = t >= i ? min(r[t], j) : r[t];
                if (isP[enc(nxt)]) P = false;
            }
        isP[enc(r)] = P;
        if (P) { for (int t = 0; t < K; ++t) printf("%d%c", r[t], t + 1 < K ? ' ' : '\n'); }
    }
    return 0;
}
