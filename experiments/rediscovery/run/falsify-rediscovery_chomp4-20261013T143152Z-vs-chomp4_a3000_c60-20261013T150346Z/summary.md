# Falsification `falsify-rediscovery_chomp4-20261013T143152Z-vs-chomp4_a3000_c60-20261013T150346Z`

Mining run: `rediscovery_chomp4-20261013T143152Z` · 0.98 s

Rule: refuted if violated on any sequence in scope; survived if it holds on all and at least one has new terms; otherwise untestable.

| Dataset | Tested against | Window | Scale factor | Candidates |
|---|---|---|---|---|
| `chomp4_n1000` | `chomp4_a3000_c60` | `{'a': 100}` | `{'a': 30.0}` | 73 |

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
| `chomp4_n1000/data|a~b|c=0,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 0 | 2999 checks, range [0, 2999] (30.0x) |
| `chomp4_n1000/data|a~b|c=2,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 2 | 2996 checks, range [2, 2998] (30.9x) |
| `chomp4_n1000/data|a~b|c=3,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 7 | 2990 checks, range [3, 2997] (31.53x) |
| `chomp4_n1000/data|a~b|c=4,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 7 | 2988 checks, range [4, 2996] (32.18x) |
| `chomp4_n1000/data|a~b|c=4,d=3|raw` | s(n + 2) = s(n) + 2 for all n >= 8 | 2987 checks, range [4, 2996] (32.18x) |
| `chomp4_n1000/data|a~b|c=4,d=4|raw` | s(n + 2) = s(n) + 2 for all n >= 8 | 2985 checks, range [4, 2994] (32.87x) |
| `chomp4_n1000/data|a~b|c=5,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 7 | 2989 checks, range [5, 2996] (32.52x) |
| `chomp4_n1000/data|a~b|c=5,d=3|raw` | s(n + 4) = s(n) + 4 for all n >= 9 | 2982 checks, range [5, 2994] (33.22x) |
| `chomp4_n1000/data|a~b|c=6,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 10 | 2977 checks, range [6, 2994] (33.21x) |
| `chomp4_n1000/data|a~b|c=6,d=4|raw` | s(n + 8) = s(n) + 8 for all n >= 9 | 2979 checks, range [6, 2995] (33.22x) |
| `chomp4_n1000/data|a~b|c=6,d=5|raw` | s(n + 8) = s(n) + 8 for all n >= 19 | 2968 checks, range [6, 2994] (33.58x) |
| `chomp4_n1000/data|a~b|c=7,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 10 | 2985 checks, range [7, 2995] (33.58x) |
| `chomp4_n1000/data|a~b|c=7,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 20 | 2968 checks, range [7, 2995] (33.58x) |
| `chomp4_n1000/data|a~b|c=7,d=6|raw` | s(n + 8) = s(n) + 8 for all n >= 21 | 2965 checks, range [7, 2993] (34.73x) |
| `chomp4_n1000/data|a~b|c=8,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 12 | 2982 checks, range [8, 2994] (34.33x) |
| `chomp4_n1000/data|a~b|c=8,d=3|raw` | s(n + 16) = s(n) + 16 for all n >= 20 | 2958 checks, range [8, 2993] (35.13x) |
| `chomp4_n1000/data|a~b|c=8,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 20 | 2956 checks, range [8, 2991] (35.11x) |
| `chomp4_n1000/data|a~b|c=8,d=7|raw` | s(n + 16) = s(n) + 16 for all n >= 23 | 2954 checks, range [8, 2992] (34.71x) |
| `chomp4_n1000/data|a~b|c=8,d=8|raw` | s(n + 16) = s(n) + 16 for all n >= 23 | 2953 checks, range [8, 2991] (35.52x) |
| `chomp4_n1000/data|a~b|c=9,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 12 | 2982 checks, range [9, 2994] (34.72x) |
| `chomp4_n1000/data|a~b|c=9,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 18 | 2958 checks, range [9, 2991] (35.94x) |
| `chomp4_n1000/data|a~b|c=9,d=6|raw` | s(n + 16) = s(n) + 16 for all n >= 32 | 2945 checks, range [9, 2992] (35.11x) |
| `chomp4_n1000/data|a~b|c=9,d=9|raw` | s(n + 16) = s(n) + 16 for all n >= 27 | 2948 checks, range [9, 2990] (36.37x) |
| `chomp4_n1000/data|a~b|c=10,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 14 | 2979 checks, range [10, 2993] (35.52x) |
| `chomp4_n1000/data|a~b|c=10,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 15 | 2962 checks, range [10, 2992] (35.51x) |
| `chomp4_n1000/data|a~b|c=10,d=6|raw` | s(n + 16) = s(n) + 16 for all n >= 35 | 2941 checks, range [10, 2991] (35.93x) |
| `chomp4_n1000/data|a~b|c=11,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 19 | 2974 checks, range [11, 2993] (35.94x) |
| `chomp4_n1000/data|a~b|c=11,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 22 | 2955 checks, range [11, 2992] (36.81x) |
| `chomp4_n1000/data|a~b|c=12,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 16 | 2976 checks, range [12, 2992] (36.8x) |
| `chomp4_n1000/data|a~b|c=12,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 25 | 2950 checks, range [12, 2990] (37.71x) |
| `chomp4_n1000/data|a~b|c=13,d=2|raw` | s(n + 4) = s(n) + 4 for all n >= 20 | 2968 checks, range [13, 2991] (37.71x) |
| `chomp4_n1000/data|a~b|c=13,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 27 | 2948 checks, range [13, 2990] (38.18x) |
| `chomp4_n1000/data|a~b|c=14,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 20 | 2971 checks, range [14, 2991] (38.18x) |
| `chomp4_n1000/data|a~b|c=14,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 18 | 2971 checks, range [14, 2989] (39.16x) |
| `chomp4_n1000/data|a~b|c=14,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 22 | 2954 checks, range [14, 2991] (38.68x) |
| `chomp4_n1000/data|a~b|c=15,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 26 | 2950 checks, range [15, 2991] (39.69x) |
| `chomp4_n1000/data|a~b|c=16,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 29 | 2961 checks, range [16, 2990] (39.67x) |
| `chomp4_n1000/data|a~b|c=16,d=3|raw` | s(n + 3) = s(n) + 3 for all n >= 29 | 2958 checks, range [16, 2989] (40.74x) |
| `chomp4_n1000/data|a~b|c=17,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 24 | 2965 checks, range [17, 2989] (40.73x) |
| `chomp4_n1000/data|a~b|c=17,d=3|raw` | s(n + 3) = s(n) + 3 for all n >= 29 | 2956 checks, range [17, 2987] (41.26x) |
| `chomp4_n1000/data|a~b|c=19,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 27 | 2961 checks, range [19, 2988] (42.43x) |
| `chomp4_n1000/data|a~b|c=19,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 28 | 2958 checks, range [19, 2987] (43.03x) |
| `chomp4_n1000/data|a~b|c=20,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 28 | 2958 checks, range [20, 2987] (43.65x) |
| `chomp4_n1000/data|a~b|c=20,d=3|raw` | s(n + 6) = s(n) + 6 for all n >= 40 | 2941 checks, range [20, 2986] (44.28x) |
| `chomp4_n1000/data|a~b|c=22,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 31 | 2955 checks, range [22, 2986] (45.62x) |
| `chomp4_n1000/data|a~b|c=22,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 41 | 2932 checks, range [22, 2984] (46.3x) |
| `chomp4_n1000/data|a~b|c=24,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 34 | 2951 checks, range [24, 2985] (47.77x) |
| `chomp4_n1000/data|a~b|c=24,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 34 | 2950 checks, range [24, 2985] (47.77x) |
| `chomp4_n1000/data|a~b|c=25,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 37 | 2948 checks, range [25, 2985] (48.54x) |
| `chomp4_n1000/data|a~b|c=26,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 36 | 2948 checks, range [26, 2984] (50.15x) |
| `chomp4_n1000/data|a~b|c=26,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 40 | 2943 checks, range [26, 2983] (51.0x) |
| `chomp4_n1000/data|a~b|c=27,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 39 | 2933 checks, range [27, 2983] (52.8x) |
| `chomp4_n1000/data|a~b|c=27,d=27|raw` | s(n + 1) = s(n) + 1 for all n >= 50 | 2923 checks, range [27, 2973] (62.7x) |
| `chomp4_n1000/data|a~b|c=28,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 39 | 2944 checks, range [28, 2983] (52.79x) |
| `chomp4_n1000/data|a~b|c=28,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 42 | 2928 checks, range [28, 2981] (52.75x) |
| `chomp4_n1000/data|a~b|c=28,d=28|raw` | s(n + 1) = s(n) + 1 for all n >= 52 | 2920 checks, range [28, 2972] (65.44x) |
| `chomp4_n1000/data|a~b|c=30,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 43 | 2938 checks, range [30, 2981] (56.77x) |
| `chomp4_n1000/data|b~a|c=0,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 1 | 2999 checks, range [1, 3000] (30.0x) |
| `chomp4_n1000/data|b~a|c=2,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 4 | 2996 checks, range [4, 3000] (30.9x) |
| `chomp4_n1000/data|b~a|c=4,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 10 | 2989 checks, range [7, 3000] (31.85x) |
| `chomp4_n1000/data|b~a|c=4,d=4|raw` | s(n + 2) = s(n) + 2 for all n >= 14 | 2985 checks, range [9, 3000] (32.52x) |
| `chomp4_n1000/data|b~a|c=5,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 11 | 2989 checks, range [9, 3000] (32.52x) |
| `chomp4_n1000/data|b~a|c=5,d=3|raw` | s(n + 4) = s(n) + 4 for all n >= 15 | 2982 checks, range [10, 3000] (32.87x) |
| `chomp4_n1000/data|b~a|c=7,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 15 | 2985 checks, range [12, 3000] (33.58x) |
| `chomp4_n1000/data|b~a|c=7,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 24 | 2969 checks, range [12, 3000] (33.58x) |
| `chomp4_n1000/data|b~a|c=8,d=3|raw` | s(n + 16) = s(n) + 16 for all n >= 24 | 2961 checks, range [13, 3000] (33.95x) |
| `chomp4_n1000/data|b~a|c=12,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 24 | 2976 checks, range [20, 3000] (36.8x) |
| `chomp4_n1000/data|b~a|c=26,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 57 | 2943 checks, range [43, 3000] (51.0x) |
| `chomp4_n1000/data|b~a|c=27,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 56 | 2933 checks, range [44, 3000] (51.88x) |
