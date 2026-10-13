// scan_twostep.c - stream a P-position CSV (a,b,c,d,n) and emit every
// "two-step" P-position: (a,j,j,j) T1, (a,a,j,j) T2, (a,a,a,j) T3 with j<a.
// usage: scan_twostep < p_positions.csv > twostep.csv
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    static char buf[1 << 16];
    printf("a,type,j\n");
    long long n = 0;
    while (fgets(buf, sizeof buf, stdin)) {
        if (buf[0] < '0' || buf[0] > '9') continue;
        int v[4] = {0, 0, 0, 0}, k = 0;
        for (char* p = buf; *p && k < 4; ++p) {
            if (*p >= '0' && *p <= '9') v[k] = v[k] * 10 + (*p - '0');
            else if (*p == ',') ++k;
        }
        int a = v[0], b = v[1], c = v[2], d = v[3];
        if (b == c && c == d && b < a) printf("%d,T1,%d\n", a, b);
        else if (a == b && c == d && c < a) printf("%d,T2,%d\n", a, c);
        else if (a == b && b == c && d < a) printf("%d,T3,%d\n", a, d);
        ++n;
    }
    fprintf(stderr, "scanned %lld rows\n", n);
    return 0;
}
