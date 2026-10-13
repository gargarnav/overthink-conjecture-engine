# Falsification `falsify-rediscovery2_chomp4-20261013T150627Z-20261013T150640Z`

Mining run: `rediscovery2_chomp4-20261013T150627Z` · 2.5 s

Rule: refuted if violated on any sequence in scope; survived if it holds on all and at least one has new terms; otherwise untestable.

| Dataset | Tested against | Window | Scale factor | Candidates |
|---|---|---|---|---|
| `chomp4_a3000_c60` | `chomp4_a3000_c60` | `{'a': 300}` | `{'a': 10.0}` | 176 |

Overall: {'survived': 167, 'refuted': 9}

| Kind | Status counts |
|---|---|
| additive_periodic | {'survived': 163, 'refuted': 9} |
| functional_dependency | {'survived': 4} |

## Refuted (9)

| Sequence | Statement | Detail |
|---|---|---|
| `chomp4_a3000_c60/data|a~b|c=27,d=6|raw` | s(n + 1) = s(n) + 1 for all n >= 261 | n=282: observed 301, predicted 299 |
| `chomp4_a3000_c60/data|a~b|c=29,d=21|raw` | s(n + 1) = s(n) + 1 for all n >= 132 | n=303: observed 329, predicted 328 |
| `chomp4_a3000_c60/data|a~b|c=30,d=6|raw` | s(n + 1) = s(n) + 1 for all n >= 261 | n=290: observed 311, predicted 308 |
| `chomp4_a3000_c60/data|a~b|c=35,d=5|raw` | s(n + 2) = s(n) + 2 for all n >= 250 | n=285: observed 307, predicted 305 |
| `chomp4_a3000_c60/data|a~b|c=43,d=41|raw` | s(n + 1) = s(n) + 1 for all n >= 122 | n=428: observed 470, predicted 469 |
| `chomp4_a3000_c60/data|a~b|c=43,d=43|raw` | s(n + 1) = s(n) + 1 for all n >= 121 | n=673: observed 717, predicted 716 |
| `chomp4_a3000_c60/data|a~b|c=48,d=46|raw` | s(n + 1) = s(n) + 1 for all n >= 87 | n=2181: observed 2229, predicted 2228 |
| `chomp4_a3000_c60/data|a~b|c=55,d=9|raw` | s(n + 1) = s(n) + 1 for all n >= 199 | n=270: observed 305, predicted 304 |
| `chomp4_a3000_c60/data|a~b|c=56,d=55|raw` | s(n + 4) = s(n) + 4 for all n >= 108 | n=391: observed 447, predicted 443 |

## Survived (167)

| Sequence | Statement | Detail |
|---|---|---|
| `chomp4_a3000_c60/data|a~b|c=0,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 0 | 2999 checks, range [0, 2999] (10.0x) |
| `chomp4_a3000_c60/data|a~b|c=2,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 2 | 2996 checks, range [2, 2998] (10.09x) |
| `chomp4_a3000_c60/data|a~b|c=3,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 7 | 2990 checks, range [3, 2997] (10.15x) |
| `chomp4_a3000_c60/data|a~b|c=4,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 7 | 2988 checks, range [4, 2996] (10.22x) |
| `chomp4_a3000_c60/data|a~b|c=4,d=3|raw` | s(n + 2) = s(n) + 2 for all n >= 8 | 2987 checks, range [4, 2996] (10.22x) |
| `chomp4_a3000_c60/data|a~b|c=4,d=4|raw` | s(n + 2) = s(n) + 2 for all n >= 8 | 2985 checks, range [4, 2994] (10.28x) |
| `chomp4_a3000_c60/data|a~b|c=5,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 7 | 2989 checks, range [5, 2996] (10.25x) |
| `chomp4_a3000_c60/data|a~b|c=5,d=3|raw` | s(n + 4) = s(n) + 4 for all n >= 9 | 2982 checks, range [5, 2994] (10.31x) |
| `chomp4_a3000_c60/data|a~b|c=6,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 10 | 2977 checks, range [6, 2994] (10.31x) |
| `chomp4_a3000_c60/data|a~b|c=6,d=4|raw` | s(n + 8) = s(n) + 8 for all n >= 9 | 2979 checks, range [6, 2995] (10.31x) |
| `chomp4_a3000_c60/data|a~b|c=6,d=5|raw` | s(n + 8) = s(n) + 8 for all n >= 19 | 2968 checks, range [6, 2994] (10.34x) |
| `chomp4_a3000_c60/data|a~b|c=7,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 10 | 2985 checks, range [7, 2995] (10.34x) |
| `chomp4_a3000_c60/data|a~b|c=7,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 20 | 2968 checks, range [7, 2995] (10.34x) |
| `chomp4_a3000_c60/data|a~b|c=7,d=6|raw` | s(n + 8) = s(n) + 8 for all n >= 21 | 2965 checks, range [7, 2993] (10.44x) |
| `chomp4_a3000_c60/data|a~b|c=8,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 12 | 2982 checks, range [8, 2994] (10.41x) |
| `chomp4_a3000_c60/data|a~b|c=8,d=3|raw` | s(n + 16) = s(n) + 16 for all n >= 20 | 2958 checks, range [8, 2993] (10.48x) |
| `chomp4_a3000_c60/data|a~b|c=8,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 20 | 2956 checks, range [8, 2991] (10.47x) |
| `chomp4_a3000_c60/data|a~b|c=8,d=7|raw` | s(n + 16) = s(n) + 16 for all n >= 23 | 2954 checks, range [8, 2992] (10.47x) |
| `chomp4_a3000_c60/data|a~b|c=8,d=8|raw` | s(n + 16) = s(n) + 16 for all n >= 23 | 2953 checks, range [8, 2991] (10.54x) |
| `chomp4_a3000_c60/data|a~b|c=9,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 12 | 2982 checks, range [9, 2994] (10.44x) |
| `chomp4_a3000_c60/data|a~b|c=9,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 18 | 2958 checks, range [9, 2991] (10.54x) |
| `chomp4_a3000_c60/data|a~b|c=9,d=6|raw` | s(n + 16) = s(n) + 16 for all n >= 32 | 2945 checks, range [9, 2992] (10.47x) |
| `chomp4_a3000_c60/data|a~b|c=9,d=9|raw` | s(n + 16) = s(n) + 16 for all n >= 27 | 2948 checks, range [9, 2990] (10.61x) |
| `chomp4_a3000_c60/data|a~b|c=10,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 14 | 2979 checks, range [10, 2993] (10.51x) |
| `chomp4_a3000_c60/data|a~b|c=10,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 15 | 2962 checks, range [10, 2992] (10.54x) |
| `chomp4_a3000_c60/data|a~b|c=10,d=6|raw` | s(n + 16) = s(n) + 16 for all n >= 35 | 2941 checks, range [10, 2991] (10.57x) |
| `chomp4_a3000_c60/data|a~b|c=10,d=8|raw` | s(n + 16) = s(n) + 16 for all n >= 52 | 2925 checks, range [10, 2992] (10.5x) |
| `chomp4_a3000_c60/data|a~b|c=10,d=10|raw` | s(n + 16) = s(n) + 16 for all n >= 60 | 2913 checks, range [10, 2988] (10.68x) |
| `chomp4_a3000_c60/data|a~b|c=11,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 19 | 2974 checks, range [11, 2993] (10.54x) |
| `chomp4_a3000_c60/data|a~b|c=11,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 22 | 2955 checks, range [11, 2992] (10.61x) |
| `chomp4_a3000_c60/data|a~b|c=11,d=6|raw` | s(n + 32) = s(n) + 32 for all n >= 32 | 2928 checks, range [11, 2991] (10.65x) |
| `chomp4_a3000_c60/data|a~b|c=11,d=8|raw` | s(n + 32) = s(n) + 32 for all n >= 64 | 2897 checks, range [11, 2992] (10.57x) |
| `chomp4_a3000_c60/data|a~b|c=11,d=9|raw` | s(n + 32) = s(n) + 32 for all n >= 68 | 2891 checks, range [11, 2990] (10.72x) |
| `chomp4_a3000_c60/data|a~b|c=12,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 16 | 2976 checks, range [12, 2992] (10.61x) |
| `chomp4_a3000_c60/data|a~b|c=12,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 25 | 2950 checks, range [12, 2990] (10.64x) |
| `chomp4_a3000_c60/data|a~b|c=12,d=8|raw` | s(n + 32) = s(n) + 32 for all n >= 50 | 2909 checks, range [12, 2990] (10.75x) |
| `chomp4_a3000_c60/data|a~b|c=13,d=2|raw` | s(n + 4) = s(n) + 4 for all n >= 20 | 2968 checks, range [13, 2991] (10.68x) |
| `chomp4_a3000_c60/data|a~b|c=13,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 27 | 2948 checks, range [13, 2990] (10.75x) |
| `chomp4_a3000_c60/data|a~b|c=13,d=8|raw` | s(n + 32) = s(n) + 32 for all n >= 103 | 2857 checks, range [13, 2991] (10.79x) |
| `chomp4_a3000_c60/data|a~b|c=13,d=9|raw` | s(n + 32) = s(n) + 32 for all n >= 115 | 2841 checks, range [13, 2987] (10.66x) |
| `chomp4_a3000_c60/data|a~b|c=13,d=10|raw` | s(n + 32) = s(n) + 32 for all n >= 125 | 2834 checks, range [13, 2990] (10.87x) |
| `chomp4_a3000_c60/data|a~b|c=14,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 20 | 2971 checks, range [14, 2991] (10.71x) |
| `chomp4_a3000_c60/data|a~b|c=14,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 18 | 2971 checks, range [14, 2989] (10.78x) |
| `chomp4_a3000_c60/data|a~b|c=14,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 22 | 2954 checks, range [14, 2991] (10.75x) |
| `chomp4_a3000_c60/data|a~b|c=14,d=5|raw` | s(n + 16) = s(n) + 16 for all n >= 80 | 2893 checks, range [14, 2988] (10.82x) |
| `chomp4_a3000_c60/data|a~b|c=14,d=9|raw` | s(n + 32) = s(n) + 32 for all n >= 154 | 2803 checks, range [14, 2988] (10.86x) |
| `chomp4_a3000_c60/data|a~b|c=14,d=10|raw` | s(n + 32) = s(n) + 32 for all n >= 156 | 2800 checks, range [14, 2987] (10.78x) |
| `chomp4_a3000_c60/data|a~b|c=15,d=4|raw` | s(n + 16) = s(n) + 16 for all n >= 26 | 2950 checks, range [15, 2991] (10.79x) |
| `chomp4_a3000_c60/data|a~b|c=15,d=6|raw` | s(n + 64) = s(n) + 64 for all n >= 34 | 2892 checks, range [15, 2989] (10.78x) |
| `chomp4_a3000_c60/data|a~b|c=16,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 29 | 2961 checks, range [16, 2990] (10.82x) |
| `chomp4_a3000_c60/data|a~b|c=16,d=3|raw` | s(n + 3) = s(n) + 3 for all n >= 29 | 2958 checks, range [16, 2989] (10.85x) |
| `chomp4_a3000_c60/data|a~b|c=16,d=4|raw` | s(n + 48) = s(n) + 48 for all n >= 45 | 2897 checks, range [16, 2989] (10.85x) |
| `chomp4_a3000_c60/data|a~b|c=17,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 24 | 2965 checks, range [17, 2989] (10.89x) |
| `chomp4_a3000_c60/data|a~b|c=17,d=3|raw` | s(n + 3) = s(n) + 3 for all n >= 29 | 2956 checks, range [17, 2987] (10.96x) |
| `chomp4_a3000_c60/data|a~b|c=17,d=5|raw` | s(n + 48) = s(n) + 48 for all n >= 138 | 2801 checks, range [17, 2986] (10.96x) |
| `chomp4_a3000_c60/data|a~b|c=19,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 27 | 2961 checks, range [19, 2988] (11.0x) |
| `chomp4_a3000_c60/data|a~b|c=19,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 28 | 2958 checks, range [19, 2987] (11.04x) |
| `chomp4_a3000_c60/data|a~b|c=19,d=4|raw` | s(n + 48) = s(n) + 48 for all n >= 56 | 2884 checks, range [19, 2987] (11.04x) |
| `chomp4_a3000_c60/data|a~b|c=20,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 28 | 2958 checks, range [20, 2987] (11.07x) |
| `chomp4_a3000_c60/data|a~b|c=20,d=3|raw` | s(n + 6) = s(n) + 6 for all n >= 40 | 2941 checks, range [20, 2986] (11.11x) |
| `chomp4_a3000_c60/data|a~b|c=21,d=4|raw` | s(n + 48) = s(n) + 48 for all n >= 34 | 2907 checks, range [21, 2988] (11.07x) |
| `chomp4_a3000_c60/data|a~b|c=22,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 31 | 2955 checks, range [22, 2986] (11.19x) |
| `chomp4_a3000_c60/data|a~b|c=22,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 41 | 2932 checks, range [22, 2984] (11.27x) |
| `chomp4_a3000_c60/data|a~b|c=24,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 34 | 2951 checks, range [24, 2985] (11.31x) |
| `chomp4_a3000_c60/data|a~b|c=24,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 34 | 2950 checks, range [24, 2985] (11.31x) |
| `chomp4_a3000_c60/data|a~b|c=25,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 37 | 2948 checks, range [25, 2985] (11.34x) |
| `chomp4_a3000_c60/data|a~b|c=26,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 36 | 2948 checks, range [26, 2984] (11.42x) |
| `chomp4_a3000_c60/data|a~b|c=26,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 40 | 2943 checks, range [26, 2983] (11.47x) |
| `chomp4_a3000_c60/data|a~b|c=27,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 39 | 2933 checks, range [27, 2983] (11.51x) |
| `chomp4_a3000_c60/data|a~b|c=27,d=27|raw` | s(n + 1) = s(n) + 1 for all n >= 50 | 2923 checks, range [27, 2973] (11.93x) |
| `chomp4_a3000_c60/data|a~b|c=28,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 39 | 2944 checks, range [28, 2983] (11.55x) |
| `chomp4_a3000_c60/data|a~b|c=28,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 42 | 2928 checks, range [28, 2981] (11.63x) |
| `chomp4_a3000_c60/data|a~b|c=28,d=28|raw` | s(n + 1) = s(n) + 1 for all n >= 52 | 2920 checks, range [28, 2972] (12.02x) |
| `chomp4_a3000_c60/data|a~b|c=29,d=3|raw` | s(n + 24) = s(n) + 24 for all n >= 74 | 2884 checks, range [29, 2981] (11.67x) |
| `chomp4_a3000_c60/data|a~b|c=30,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 43 | 2938 checks, range [30, 2981] (11.71x) |
| `chomp4_a3000_c60/data|a~b|c=30,d=3|raw` | s(n + 24) = s(n) + 24 for all n >= 62 | 2895 checks, range [30, 2980] (11.76x) |
| `chomp4_a3000_c60/data|a~b|c=31,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 44 | 2937 checks, range [31, 2981] (11.76x) |
| `chomp4_a3000_c60/data|a~b|c=31,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 104 | 2864 checks, range [31, 2979] (11.84x) |
| `chomp4_a3000_c60/data|a~b|c=32,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 48 | 2932 checks, range [32, 2980] (11.84x) |
| `chomp4_a3000_c60/data|a~b|c=32,d=4|raw` | s(n + 1) = s(n) + 1 for all n >= 49 | 2932 checks, range [32, 2981] (11.8x) |
| `chomp4_a3000_c60/data|a~b|c=32,d=31|raw` | s(n + 1) = s(n) + 1 for all n >= 60 | 2909 checks, range [32, 2969] (12.34x) |
| `chomp4_a3000_c60/data|a~b|c=33,d=2|raw` | s(n + 3) = s(n) + 3 for all n >= 48 | 2930 checks, range [33, 2980] (11.89x) |
| `chomp4_a3000_c60/data|a~b|c=34,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 48 | 2931 checks, range [34, 2979] (11.98x) |
| `chomp4_a3000_c60/data|a~b|c=34,d=4|raw` | s(n + 2) = s(n) + 2 for all n >= 59 | 2920 checks, range [34, 2980] (11.93x) |
| `chomp4_a3000_c60/data|a~b|c=35,d=4|raw` | s(n + 1) = s(n) + 1 for all n >= 50 | 2929 checks, range [35, 2979] (12.02x) |
| `chomp4_a3000_c60/data|a~b|c=35,d=34|raw` | s(n + 1) = s(n) + 1 for all n >= 65 | 2900 checks, range [35, 2965] (12.69x) |
| `chomp4_a3000_c60/data|a~b|c=35,d=35|raw` | s(n + 1) = s(n) + 1 for all n >= 66 | 2898 checks, range [35, 2964] (12.74x) |
| `chomp4_a3000_c60/data|a~b|c=36,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 50 | 2928 checks, range [36, 2978] (12.11x) |
| `chomp4_a3000_c60/data|a~b|c=36,d=2|raw` | s(n + 12) = s(n) + 12 for all n >= 50 | 2916 checks, range [36, 2977] (12.16x) |
| `chomp4_a3000_c60/data|a~b|c=36,d=3|raw` | s(n + 24) = s(n) + 24 for all n >= 96 | 2857 checks, range [36, 2976] (12.2x) |
| `chomp4_a3000_c60/data|a~b|c=36,d=35|raw` | s(n + 1) = s(n) + 1 for all n >= 66 | 2899 checks, range [36, 2965] (12.74x) |
| `chomp4_a3000_c60/data|a~b|c=37,d=4|raw` | s(n + 1) = s(n) + 1 for all n >= 56 | 2922 checks, range [37, 2978] (12.16x) |
| `chomp4_a3000_c60/data|a~b|c=37,d=5|raw` | s(n + 1) = s(n) + 1 for all n >= 53 | 2922 checks, range [37, 2975] (12.3x) |
| `chomp4_a3000_c60/data|a~b|c=37,d=37|raw` | s(n + 1) = s(n) + 1 for all n >= 68 | 2894 checks, range [37, 2962] (12.95x) |
| `chomp4_a3000_c60/data|a~b|c=38,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 56 | 2921 checks, range [38, 2977] (12.25x) |
| `chomp4_a3000_c60/data|a~b|c=38,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 56 | 2919 checks, range [38, 2976] (12.3x) |
| `chomp4_a3000_c60/data|a~b|c=38,d=38|raw` | s(n + 2) = s(n) + 2 for all n >= 70 | 2890 checks, range [38, 2961] (13.05x) |
| `chomp4_a3000_c60/data|a~b|c=39,d=2|raw` | s(n + 12) = s(n) + 12 for all n >= 56 | 2909 checks, range [39, 2976] (12.34x) |
| `chomp4_a3000_c60/data|a~b|c=39,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 92 | 2873 checks, range [39, 2976] (12.34x) |
| `chomp4_a3000_c60/data|a~b|c=39,d=4|raw` | s(n + 6) = s(n) + 6 for all n >= 74 | 2899 checks, range [39, 2978] (12.25x) |
| `chomp4_a3000_c60/data|a~b|c=40,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 60 | 2916 checks, range [40, 2976] (12.39x) |
| `chomp4_a3000_c60/data|a~b|c=40,d=5|raw` | s(n + 3) = s(n) + 3 for all n >= 60 | 2913 checks, range [40, 2975] (12.44x) |
| `chomp4_a3000_c60/data|a~b|c=41,d=2|raw` | s(n + 12) = s(n) + 12 for all n >= 62 | 2902 checks, range [41, 2975] (12.49x) |
| `chomp4_a3000_c60/data|a~b|c=41,d=40|raw` | s(n + 1) = s(n) + 1 for all n >= 76 | 2883 checks, range [41, 2959] (13.33x) |
| `chomp4_a3000_c60/data|a~b|c=41,d=41|raw` | s(n + 2) = s(n) + 2 for all n >= 79 | 2878 checks, range [41, 2958] (13.39x) |
| `chomp4_a3000_c60/data|a~b|c=42,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 63 | 2912 checks, range [42, 2975] (12.54x) |
| `chomp4_a3000_c60/data|a~b|c=42,d=4|raw` | s(n + 6) = s(n) + 6 for all n >= 77 | 2894 checks, range [42, 2976] (12.49x) |
| `chomp4_a3000_c60/data|a~b|c=43,d=4|raw` | s(n + 12) = s(n) + 12 for all n >= 82 | 2883 checks, range [43, 2976] (12.54x) |
| `chomp4_a3000_c60/data|a~b|c=43,d=5|raw` | s(n + 1) = s(n) + 1 for all n >= 64 | 2909 checks, range [43, 2973] (12.69x) |
| `chomp4_a3000_c60/data|a~b|c=44,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 62 | 2912 checks, range [44, 2974] (12.69x) |
| `chomp4_a3000_c60/data|a~b|c=44,d=5|raw` | s(n + 1) = s(n) + 1 for all n >= 66 | 2906 checks, range [44, 2972] (12.79x) |
| `chomp4_a3000_c60/data|a~b|c=44,d=6|raw` | s(n + 2) = s(n) + 2 for all n >= 66 | 2904 checks, range [44, 2971] (12.84x) |
| `chomp4_a3000_c60/data|a~b|c=45,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 63 | 2910 checks, range [45, 2973] (12.79x) |
| `chomp4_a3000_c60/data|a~b|c=45,d=4|raw` | s(n + 12) = s(n) + 12 for all n >= 80 | 2881 checks, range [45, 2972] (12.84x) |
| `chomp4_a3000_c60/data|a~b|c=46,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 66 | 2905 checks, range [46, 2971] (12.95x) |
| `chomp4_a3000_c60/data|a~b|c=46,d=6|raw` | s(n + 12) = s(n) + 12 for all n >= 80 | 2881 checks, range [46, 2972] (12.89x) |
| `chomp4_a3000_c60/data|a~b|c=47,d=3|raw` | s(n + 2) = s(n) + 2 for all n >= 71 | 2898 checks, range [47, 2970] (13.05x) |
| `chomp4_a3000_c60/data|a~b|c=48,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 67 | 2904 checks, range [48, 2971] (13.05x) |
| `chomp4_a3000_c60/data|a~b|c=48,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 67 | 2902 checks, range [48, 2970] (13.11x) |
| `chomp4_a3000_c60/data|a~b|c=48,d=5|raw` | s(n + 6) = s(n) + 6 for all n >= 84 | 2881 checks, range [48, 2970] (13.11x) |
| `chomp4_a3000_c60/data|a~b|c=49,d=49|raw` | s(n + 1) = s(n) + 1 for all n >= 91 | 2862 checks, range [49, 2953] (14.17x) |
| `chomp4_a3000_c60/data|a~b|c=50,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 73 | 2896 checks, range [50, 2970] (13.22x) |
| `chomp4_a3000_c60/data|a~b|c=50,d=5|raw` | s(n + 12) = s(n) + 12 for all n >= 80 | 2877 checks, range [50, 2968] (13.33x) |
| `chomp4_a3000_c60/data|a~b|c=51,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 73 | 2896 checks, range [51, 2969] (13.33x) |
| `chomp4_a3000_c60/data|a~b|c=51,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 76 | 2891 checks, range [51, 2967] (13.44x) |
| `chomp4_a3000_c60/data|a~b|c=51,d=4|raw` | s(n + 1) = s(n) + 1 for all n >= 74 | 2896 checks, range [51, 2970] (13.27x) |
| `chomp4_a3000_c60/data|a~b|c=52,d=4|raw` | s(n + 1) = s(n) + 1 for all n >= 78 | 2891 checks, range [52, 2969] (13.39x) |
| `chomp4_a3000_c60/data|a~b|c=52,d=5|raw` | s(n + 12) = s(n) + 12 for all n >= 78 | 2878 checks, range [52, 2967] (13.5x) |
| `chomp4_a3000_c60/data|a~b|c=52,d=51|raw` | s(n + 1) = s(n) + 1 for all n >= 94 | 2854 checks, range [52, 2948] (14.71x) |
| `chomp4_a3000_c60/data|a~b|c=52,d=52|raw` | s(n + 2) = s(n) + 2 for all n >= 96 | 2850 checks, range [52, 2947] (14.78x) |
| `chomp4_a3000_c60/data|a~b|c=53,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 75 | 2893 checks, range [53, 2968] (13.5x) |
| `chomp4_a3000_c60/data|a~b|c=53,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 75 | 2892 checks, range [53, 2968] (13.5x) |
| `chomp4_a3000_c60/data|a~b|c=53,d=3|raw` | s(n + 6) = s(n) + 6 for all n >= 76 | 2886 checks, range [53, 2967] (13.56x) |
| `chomp4_a3000_c60/data|a~b|c=53,d=5|raw` | s(n + 6) = s(n) + 6 for all n >= 84 | 2876 checks, range [53, 2965] (13.68x) |
| `chomp4_a3000_c60/data|a~b|c=54,d=3|raw` | s(n + 3) = s(n) + 3 for all n >= 81 | 2884 checks, range [54, 2967] (13.62x) |
| `chomp4_a3000_c60/data|a~b|c=54,d=51|raw` | s(n + 1) = s(n) + 1 for all n >= 96 | 2853 checks, range [54, 2949] (14.78x) |
| `chomp4_a3000_c60/data|a~b|c=54,d=54|raw` | s(n + 1) = s(n) + 1 for all n >= 103 | 2842 checks, range [54, 2945] (15.06x) |
| `chomp4_a3000_c60/data|a~b|c=55,d=4|raw` | s(n + 1) = s(n) + 1 for all n >= 82 | 2886 checks, range [55, 2968] (13.62x) |
| `chomp4_a3000_c60/data|a~b|c=55,d=52|raw` | s(n + 2) = s(n) + 2 for all n >= 98 | 2848 checks, range [55, 2947] (14.99x) |
| `chomp4_a3000_c60/data|a~b|c=56,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 79 | 2887 checks, range [56, 2966] (13.8x) |
| `chomp4_a3000_c60/data|a~b|c=56,d=5|raw` | s(n + 12) = s(n) + 12 for all n >= 84 | 2871 checks, range [56, 2966] (13.8x) |
| `chomp4_a3000_c60/data|a~b|c=56,d=53|raw` | s(n + 1) = s(n) + 1 for all n >= 102 | 2844 checks, range [56, 2946] (15.14x) |
| `chomp4_a3000_c60/data|a~b|c=57,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 81 | 2884 checks, range [57, 2965] (13.92x) |
| `chomp4_a3000_c60/data|a~b|c=58,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 82 | 2883 checks, range [58, 2965] (13.98x) |
| `chomp4_a3000_c60/data|a~b|c=58,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 81 | 2883 checks, range [58, 2965] (13.98x) |
| `chomp4_a3000_c60/data|a~b|c=58,d=3|raw` | s(n + 6) = s(n) + 6 for all n >= 84 | 2874 checks, range [58, 2963] (14.11x) |
| `chomp4_a3000_c60/data|a~b|c=58,d=4|raw` | s(n + 4) = s(n) + 4 for all n >= 82 | 2881 checks, range [58, 2966] (13.92x) |
| `chomp4_a3000_c60/data|a~b|c=59,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 84 | 2879 checks, range [59, 2964] (14.11x) |
| `chomp4_a3000_c60/data|a~b|c=59,d=5|raw` | s(n + 12) = s(n) + 12 for all n >= 95 | 2859 checks, range [59, 2965] (14.04x) |
| `chomp4_a3000_c60/data|a~b|c=60,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 84 | 2880 checks, range [60, 2964] (14.17x) |
| `chomp4_a3000_c60/data|a~b|c=60,d=5|raw` | s(n + 12) = s(n) + 12 for all n >= 96 | 2856 checks, range [60, 2963] (14.24x) |
| `chomp4_a3000_c60/data|b~a|c=0,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 1 | 2999 checks, range [1, 3000] (10.0x) |
| `chomp4_a3000_c60/data|b~a|c=2,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 4 | 2996 checks, range [4, 3000] (10.09x) |
| `chomp4_a3000_c60/data|b~a|c=4,d=2|raw` | s(n + 2) = s(n) + 2 for all n >= 10 | 2989 checks, range [7, 3000] (10.18x) |
| `chomp4_a3000_c60/data|b~a|c=4,d=4|raw` | s(n + 2) = s(n) + 2 for all n >= 14 | 2985 checks, range [9, 3000] (10.25x) |
| `chomp4_a3000_c60/data|b~a|c=5,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 11 | 2989 checks, range [9, 3000] (10.25x) |
| `chomp4_a3000_c60/data|b~a|c=5,d=3|raw` | s(n + 4) = s(n) + 4 for all n >= 15 | 2982 checks, range [10, 3000] (10.28x) |
| `chomp4_a3000_c60/data|b~a|c=7,d=0|raw` | s(n + 1) = s(n) + 1 for all n >= 15 | 2985 checks, range [12, 3000] (10.34x) |
| `chomp4_a3000_c60/data|b~a|c=7,d=3|raw` | s(n + 8) = s(n) + 8 for all n >= 24 | 2969 checks, range [12, 3000] (10.34x) |
| `chomp4_a3000_c60/data|b~a|c=8,d=3|raw` | s(n + 16) = s(n) + 16 for all n >= 24 | 2961 checks, range [13, 3000] (10.38x) |
| `chomp4_a3000_c60/data|b~a|c=12,d=2|raw` | s(n + 1) = s(n) + 1 for all n >= 24 | 2976 checks, range [20, 3000] (10.61x) |
| `chomp4_a3000_c60/data|b~a|c=26,d=3|raw` | s(n + 1) = s(n) + 1 for all n >= 57 | 2943 checks, range [43, 3000] (11.47x) |
| `chomp4_a3000_c60/data|b~a|c=27,d=3|raw` | s(n + 12) = s(n) + 12 for all n >= 56 | 2933 checks, range [44, 3000] (11.51x) |
| `chomp4_a3000_c60/data|FD:a<-(b,c,d)` | In chomp4_a3000_c60/data, a is determined by (b, c, d): no two rows share (b, c, d) with different a |  |
| `chomp4_a3000_c60/data|FD:b<-(a,c,d)` | In chomp4_a3000_c60/data, b is determined by (a, c, d): no two rows share (a, c, d) with different b |  |
| `chomp4_a3000_c60/data|FD:c<-(a,b,d)` | In chomp4_a3000_c60/data, c is determined by (a, b, d): no two rows share (a, b, d) with different c |  |
| `chomp4_a3000_c60/data|FD:d<-(a,b,c)` | In chomp4_a3000_c60/data, d is determined by (a, b, c): no two rows share (a, b, c) with different d |  |
