# Falsification `falsify-rediscovery_chomp4-20261013T143152Z-20261013T143202Z`

Mining run: `rediscovery_chomp4-20261013T143152Z` · 17.55 s

Rule: refuted if violated on any sequence in scope; survived if it holds on all and at least one has new terms; otherwise untestable.

| Dataset | Window | Scale factor | Candidates |
|---|---|---|---|
| `chomp4_n1000` | `{'a': 100}` | `{'a': 10.0}` | 73 |

Overall: {'survived': 69, 'refuted': 4}

| Kind | Status counts |
|---|---|
| additive_periodic | {'survived': 69, 'refuted': 4} |

## Refuted (4)

| Sequence | Statement | Detail |
|---|---|---|
| `chomp4_n1000/data|a~b|c=20,d=19|raw` | s(n + 1) = s(n) + 1 for all n >= 51 | n=81: observed 101, predicted 100 |
| `chomp4_n1000/data|a~b|c=21,d=4|raw` | s(n + 1) = s(n) + 1 for all n >= 60 | n=106: observed 119, predicted 118 |
| `chomp4_n1000/data|a~b|c=21,d=21|raw` | s(n + 1) = s(n) + 1 for all n >= 50 | n=81: observed 102, predicted 101 |
| `chomp4_n1000/data|a~b|c=29,d=21|raw` | s(n + 1) = s(n) + 1 for all n >= 46 | n=130: observed 156, predicted 155 |

## Survived (69)

| Sequence | Statement | Detail |
|---|---|---|
| `chomp4_n1000/data|a~b|c=0,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 0 | 999 checks, range [0, 999] (10.0x) |
| `chomp4_n1000/data|a~b|c=2,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 2 | 996 checks, range [2, 998] (10.28x) |
| `chomp4_n1000/data|a~b|c=3,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 7 | 990 checks, range [3, 997] (10.47x) |
| `chomp4_n1000/data|a~b|c=4,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 7 | 988 checks, range [4, 996] (10.68x) |
| `chomp4_n1000/data|a~b|c=4,d=3|raw` | s(n + 2) = s(n) + 2 for all n >= 8 | 987 checks, range [4, 996] (10.68x) |
| `chomp4_n1000/data|a~b|c=4,d=4|raw` | s(n + 2) = s(n) + 2 for all n >= 8 | 985 checks, range [4, 994] (10.89x) |
| `chomp4_n1000/data|a~b|c=5,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 7 | 989 checks, range [5, 996] (10.78x) |
| `chomp4_n1000/data|a~b|c=5,d=3|raw` | s(n + 4) = s(n) + 4 for all n >= 9 | 982 checks, range [5, 994] (11.0x) |
| `chomp4_n1000/data|a~b|c=6,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 10 | 977 checks, range [6, 994] (10.99x) |
| `chomp4_n1000/data|a~b|c=6,d=4|raw` | s(n + 8) = s(n) + 8 for all n >= 9 | 979 checks, range [6, 995] (11.0x) |
| `chomp4_n1000/data|a~b|c=6,d=5|raw` | s(n + 8) = s(n) + 8 for all n >= 19 | 968 checks, range [6, 994] (11.11x) |
| `chomp4_n1000/data|a~b|c=7,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 10 | 985 checks, range [7, 995] (11.11x) |
| `chomp4_n1000/data|a~b|c=7,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 20 | 968 checks, range [7, 995] (11.11x) |
| `chomp4_n1000/data|a~b|c=7,d=6|raw` | s(n + 8) = s(n) + 8 for all n >= 21 | 965 checks, range [7, 993] (11.48x) |
| `chomp4_n1000/data|a~b|c=8,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 12 | 982 checks, range [8, 994] (11.34x) |
| `chomp4_n1000/data|a~b|c=8,d=3|raw` | s(n + 16) = s(n) + 16 for all n >= 20 | 958 checks, range [8, 993] (11.6x) |
| `chomp4_n1000/data|a~b|c=8,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 20 | 956 checks, range [8, 991] (11.58x) |
| `chomp4_n1000/data|a~b|c=8,d=7|raw` | s(n + 16) = s(n) + 16 for all n >= 23 | 954 checks, range [8, 992] (11.45x) |
| `chomp4_n1000/data|a~b|c=8,d=8|raw` | s(n + 16) = s(n) + 16 for all n >= 23 | 953 checks, range [8, 991] (11.71x) |
| `chomp4_n1000/data|a~b|c=9,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 12 | 982 checks, range [9, 994] (11.47x) |
| `chomp4_n1000/data|a~b|c=9,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 18 | 958 checks, range [9, 991] (11.84x) |
| `chomp4_n1000/data|a~b|c=9,d=6|raw` | s(n + 16) = s(n) + 16 for all n >= 32 | 945 checks, range [9, 992] (11.58x) |
| `chomp4_n1000/data|a~b|c=9,d=9|raw` | s(n + 16) = s(n) + 16 for all n >= 27 | 948 checks, range [9, 990] (11.98x) |
| `chomp4_n1000/data|a~b|c=10,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 14 | 979 checks, range [10, 993] (11.71x) |
| `chomp4_n1000/data|a~b|c=10,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 15 | 962 checks, range [10, 992] (11.7x) |
| `chomp4_n1000/data|a~b|c=10,d=6|raw` | s(n + 16) = s(n) + 16 for all n >= 35 | 941 checks, range [10, 991] (11.83x) |
| `chomp4_n1000/data|a~b|c=11,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 19 | 974 checks, range [11, 993] (11.84x) |
| `chomp4_n1000/data|a~b|c=11,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 22 | 955 checks, range [11, 992] (12.12x) |
| `chomp4_n1000/data|a~b|c=12,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 16 | 976 checks, range [12, 992] (12.11x) |
| `chomp4_n1000/data|a~b|c=12,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 25 | 950 checks, range [12, 990] (12.39x) |
| `chomp4_n1000/data|a~b|c=13,d=2|raw` | s(n + 4) = s(n) + 4 for all n >= 20 | 968 checks, range [13, 991] (12.39x) |
| `chomp4_n1000/data|a~b|c=13,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 27 | 948 checks, range [13, 990] (12.54x) |
| `chomp4_n1000/data|a~b|c=14,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 20 | 971 checks, range [14, 991] (12.54x) |
| `chomp4_n1000/data|a~b|c=14,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 18 | 971 checks, range [14, 989] (12.84x) |
| `chomp4_n1000/data|a~b|c=14,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 22 | 954 checks, range [14, 991] (12.7x) |
| `chomp4_n1000/data|a~b|c=15,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 26 | 950 checks, range [15, 991] (13.03x) |
| `chomp4_n1000/data|a~b|c=16,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 29 | 961 checks, range [16, 990] (13.0x) |
| `chomp4_n1000/data|a~b|c=16,d=3|raw` | s(n + 3) = s(n) + 3 for all n >= 29 | 957 checks, range [16, 988] (13.33x) |
| `chomp4_n1000/data|a~b|c=17,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 24 | 965 checks, range [17, 989] (13.33x) |
| `chomp4_n1000/data|a~b|c=17,d=3|raw` | s(n + 3) = s(n) + 3 for all n >= 29 | 957 checks, range [17, 988] (13.5x) |
| `chomp4_n1000/data|a~b|c=19,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 27 | 961 checks, range [19, 988] (13.86x) |
| `chomp4_n1000/data|a~b|c=19,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 28 | 958 checks, range [19, 987] (14.04x) |
| `chomp4_n1000/data|a~b|c=20,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 28 | 958 checks, range [20, 987] (14.24x) |
| `chomp4_n1000/data|a~b|c=20,d=3|raw` | s(n + 6) = s(n) + 6 for all n >= 40 | 941 checks, range [20, 986] (14.43x) |
| `chomp4_n1000/data|a~b|c=22,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 31 | 955 checks, range [22, 986] (14.85x) |
| `chomp4_n1000/data|a~b|c=22,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 41 | 933 checks, range [22, 985] (15.06x) |
| `chomp4_n1000/data|a~b|c=24,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 34 | 951 checks, range [24, 985] (15.52x) |
| `chomp4_n1000/data|a~b|c=24,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 34 | 950 checks, range [24, 985] (15.52x) |
| `chomp4_n1000/data|a~b|c=25,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 37 | 948 checks, range [25, 985] (15.75x) |
| `chomp4_n1000/data|a~b|c=26,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 36 | 948 checks, range [26, 984] (16.25x) |
| `chomp4_n1000/data|a~b|c=26,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 40 | 943 checks, range [26, 983] (16.52x) |
| `chomp4_n1000/data|a~b|c=27,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 39 | 932 checks, range [27, 982] (17.07x) |
| `chomp4_n1000/data|a~b|c=27,d=27|raw` | s(n + 1) = s(n) + 1 for all n >= 50 | 923 checks, range [27, 973] (20.15x) |
| `chomp4_n1000/data|a~b|c=28,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 39 | 944 checks, range [28, 983] (17.07x) |
| `chomp4_n1000/data|a~b|c=28,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 42 | 930 checks, range [28, 983] (17.07x) |
| `chomp4_n1000/data|a~b|c=28,d=28|raw` | s(n + 1) = s(n) + 1 for all n >= 52 | 920 checks, range [28, 972] (21.0x) |
| `chomp4_n1000/data|a~b|c=30,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 43 | 938 checks, range [30, 981] (18.31x) |
| `chomp4_n1000/data|b~a|c=0,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 1 | 999 checks, range [1, 1000] (10.0x) |
| `chomp4_n1000/data|b~a|c=2,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 4 | 996 checks, range [4, 1000] (10.28x) |
| `chomp4_n1000/data|b~a|c=4,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 10 | 989 checks, range [7, 1000] (10.57x) |
| `chomp4_n1000/data|b~a|c=4,d=4|raw` | s(n + 2) = s(n) + 2 for all n >= 14 | 985 checks, range [9, 1000] (10.78x) |
| `chomp4_n1000/data|b~a|c=5,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 11 | 989 checks, range [9, 1000] (10.78x) |
| `chomp4_n1000/data|b~a|c=5,d=3|raw` | s(n + 4) = s(n) + 4 for all n >= 15 | 982 checks, range [10, 1000] (10.89x) |
| `chomp4_n1000/data|b~a|c=7,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 15 | 985 checks, range [12, 1000] (11.11x) |
| `chomp4_n1000/data|b~a|c=7,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 24 | 969 checks, range [12, 1000] (11.11x) |
| `chomp4_n1000/data|b~a|c=8,d=3|raw` | s(n + 16) = s(n) + 16 for all n >= 24 | 961 checks, range [13, 1000] (11.23x) |
| `chomp4_n1000/data|b~a|c=12,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 24 | 976 checks, range [20, 1000] (12.11x) |
| `chomp4_n1000/data|b~a|c=26,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 57 | 943 checks, range [43, 1000] (16.52x) |
| `chomp4_n1000/data|b~a|c=27,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 56 | 933 checks, range [44, 1000] (16.79x) |
