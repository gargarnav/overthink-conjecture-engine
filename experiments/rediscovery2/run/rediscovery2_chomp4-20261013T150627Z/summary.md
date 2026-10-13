# Mining run `rediscovery2_chomp4-20261013T150627Z`

Config: `experiments/configs/mining/rediscovery2_chomp4.yaml` · git `c33c7c17ac1f482f09b14b117817eb6311ae4323` · 2.92 s

| Dataset | Window | Rows | Sequences | 2nd-order | Candidates |
|---|---|---|---|---|---|
| `chomp4_a3000_c60` | `{'a': 300}` | 172,092 | 1546 | 0 | 176 |

Candidates by kind: additive_periodic 172, functional_dependency 4

All candidates are **unverified proposals** until the falsifier has tested them.

## chomp4_a3000_c60

| Sequence | Kind | Statement | Support |
|---|---|---|---|
| `chomp4_a3000_c60/data|a~b|c=0,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 0 | 299 |
| `chomp4_a3000_c60/data|a~b|c=2,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 2 | 296 |
| `chomp4_a3000_c60/data|a~b|c=3,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 7 | 290 |
| `chomp4_a3000_c60/data|a~b|c=4,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 7 | 288 |
| `chomp4_a3000_c60/data|a~b|c=4,d=3|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 8 | 287 |
| `chomp4_a3000_c60/data|a~b|c=4,d=4|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 8 | 285 |
| `chomp4_a3000_c60/data|a~b|c=5,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 7 | 289 |
| `chomp4_a3000_c60/data|a~b|c=5,d=3|raw` | additive_periodic | s(n + 4) = s(n) + 4 for all n >= 9 | 282 |
| `chomp4_a3000_c60/data|a~b|c=6,d=3|raw` | additive_periodic | s(n + 8) = s(n) + 8 for all n >= 10 | 278 |
| `chomp4_a3000_c60/data|a~b|c=6,d=4|raw` | additive_periodic | s(n + 8) = s(n) + 8 for all n >= 9 | 279 |
| `chomp4_a3000_c60/data|a~b|c=6,d=5|raw` | additive_periodic | s(n + 8) = s(n) + 8 for all n >= 19 | 268 |
| `chomp4_a3000_c60/data|a~b|c=7,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 10 | 285 |
| `chomp4_a3000_c60/data|a~b|c=7,d=3|raw` | additive_periodic | s(n + 8) = s(n) + 8 for all n >= 20 | 268 |
| `chomp4_a3000_c60/data|a~b|c=7,d=6|raw` | additive_periodic | s(n + 8) = s(n) + 8 for all n >= 21 | 264 |
| `chomp4_a3000_c60/data|a~b|c=8,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 12 | 282 |
| `chomp4_a3000_c60/data|a~b|c=8,d=3|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 20 | 257 |
| `chomp4_a3000_c60/data|a~b|c=8,d=5|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 20 | 257 |
| `chomp4_a3000_c60/data|a~b|c=8,d=7|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 23 | 254 |
| `chomp4_a3000_c60/data|a~b|c=8,d=8|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 23 | 252 |
| `chomp4_a3000_c60/data|a~b|c=9,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 12 | 282 |
| `chomp4_a3000_c60/data|a~b|c=9,d=5|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 18 | 258 |
| `chomp4_a3000_c60/data|a~b|c=9,d=6|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 32 | 246 |
| `chomp4_a3000_c60/data|a~b|c=9,d=9|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 27 | 247 |
| `chomp4_a3000_c60/data|a~b|c=10,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 14 | 279 |
| `chomp4_a3000_c60/data|a~b|c=10,d=4|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 15 | 262 |
| `chomp4_a3000_c60/data|a~b|c=10,d=6|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 35 | 241 |
| `chomp4_a3000_c60/data|a~b|c=10,d=8|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 52 | 226 |
| `chomp4_a3000_c60/data|a~b|c=10,d=10|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 60 | 213 |
| `chomp4_a3000_c60/data|a~b|c=11,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 19 | 274 |
| `chomp4_a3000_c60/data|a~b|c=11,d=4|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 22 | 254 |
| `chomp4_a3000_c60/data|a~b|c=11,d=6|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 32 | 227 |
| `chomp4_a3000_c60/data|a~b|c=11,d=8|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 64 | 197 |
| `chomp4_a3000_c60/data|a~b|c=11,d=9|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 68 | 189 |
| `chomp4_a3000_c60/data|a~b|c=12,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 16 | 276 |
| `chomp4_a3000_c60/data|a~b|c=12,d=5|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 25 | 251 |
| `chomp4_a3000_c60/data|a~b|c=12,d=8|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 50 | 207 |
| `chomp4_a3000_c60/data|a~b|c=13,d=2|raw` | additive_periodic | s(n + 4) = s(n) + 4 for all n >= 20 | 268 |
| `chomp4_a3000_c60/data|a~b|c=13,d=5|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 27 | 247 |
| `chomp4_a3000_c60/data|a~b|c=13,d=8|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 103 | 154 |
| `chomp4_a3000_c60/data|a~b|c=13,d=9|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 115 | 145 |
| `chomp4_a3000_c60/data|a~b|c=13,d=10|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 125 | 130 |
| `chomp4_a3000_c60/data|a~b|c=14,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 20 | 271 |
| `chomp4_a3000_c60/data|a~b|c=14,d=3|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 18 | 271 |
| `chomp4_a3000_c60/data|a~b|c=14,d=4|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 22 | 253 |
| `chomp4_a3000_c60/data|a~b|c=14,d=5|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 80 | 193 |
| `chomp4_a3000_c60/data|a~b|c=14,d=9|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 154 | 102 |
| `chomp4_a3000_c60/data|a~b|c=14,d=10|raw` | additive_periodic | s(n + 32) = s(n) + 32 for all n >= 156 | 102 |
| `chomp4_a3000_c60/data|a~b|c=15,d=4|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 26 | 249 |
| `chomp4_a3000_c60/data|a~b|c=15,d=6|raw` | additive_periodic | s(n + 64) = s(n) + 64 for all n >= 34 | 193 |
| `chomp4_a3000_c60/data|a~b|c=16,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 29 | 261 |
| `chomp4_a3000_c60/data|a~b|c=16,d=3|raw` | additive_periodic | s(n + 3) = s(n) + 3 for all n >= 29 | 258 |
| `chomp4_a3000_c60/data|a~b|c=16,d=4|raw` | additive_periodic | s(n + 48) = s(n) + 48 for all n >= 45 | 197 |
| `chomp4_a3000_c60/data|a~b|c=17,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 24 | 265 |
| `chomp4_a3000_c60/data|a~b|c=17,d=3|raw` | additive_periodic | s(n + 3) = s(n) + 3 for all n >= 29 | 256 |
| `chomp4_a3000_c60/data|a~b|c=17,d=5|raw` | additive_periodic | s(n + 48) = s(n) + 48 for all n >= 138 | 102 |
| `chomp4_a3000_c60/data|a~b|c=19,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 27 | 261 |
| `chomp4_a3000_c60/data|a~b|c=19,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 28 | 258 |
| `chomp4_a3000_c60/data|a~b|c=19,d=4|raw` | additive_periodic | s(n + 48) = s(n) + 48 for all n >= 56 | 184 |
| `chomp4_a3000_c60/data|a~b|c=20,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 28 | 258 |
| `chomp4_a3000_c60/data|a~b|c=20,d=3|raw` | additive_periodic | s(n + 6) = s(n) + 6 for all n >= 40 | 241 |
| `chomp4_a3000_c60/data|a~b|c=21,d=4|raw` | additive_periodic | s(n + 48) = s(n) + 48 for all n >= 34 | 207 |
| `chomp4_a3000_c60/data|a~b|c=22,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 31 | 255 |
| `chomp4_a3000_c60/data|a~b|c=22,d=3|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 41 | 232 |
| `chomp4_a3000_c60/data|a~b|c=24,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 34 | 251 |
| `chomp4_a3000_c60/data|a~b|c=24,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 34 | 250 |
| `chomp4_a3000_c60/data|a~b|c=25,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 37 | 248 |
| `chomp4_a3000_c60/data|a~b|c=26,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 36 | 248 |
| `chomp4_a3000_c60/data|a~b|c=26,d=3|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 40 | 243 |
| `chomp4_a3000_c60/data|a~b|c=27,d=3|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 39 | 233 |
| `chomp4_a3000_c60/data|a~b|c=27,d=6|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 261 | 20 |
| `chomp4_a3000_c60/data|a~b|c=27,d=27|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 50 | 223 |
| `chomp4_a3000_c60/data|a~b|c=28,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 39 | 244 |
| `chomp4_a3000_c60/data|a~b|c=28,d=3|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 42 | 228 |
| `chomp4_a3000_c60/data|a~b|c=28,d=28|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 52 | 220 |
| `chomp4_a3000_c60/data|a~b|c=29,d=3|raw` | additive_periodic | s(n + 24) = s(n) + 24 for all n >= 74 | 184 |
| `chomp4_a3000_c60/data|a~b|c=29,d=21|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 132 | 143 |
| `chomp4_a3000_c60/data|a~b|c=30,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 43 | 238 |
| `chomp4_a3000_c60/data|a~b|c=30,d=3|raw` | additive_periodic | s(n + 24) = s(n) + 24 for all n >= 62 | 195 |
| `chomp4_a3000_c60/data|a~b|c=30,d=6|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 261 | 21 |
| `chomp4_a3000_c60/data|a~b|c=31,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 44 | 237 |
| `chomp4_a3000_c60/data|a~b|c=31,d=3|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 104 | 164 |
| `chomp4_a3000_c60/data|a~b|c=32,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 48 | 232 |
| `chomp4_a3000_c60/data|a~b|c=32,d=4|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 49 | 232 |
| `chomp4_a3000_c60/data|a~b|c=32,d=31|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 60 | 209 |
| `chomp4_a3000_c60/data|a~b|c=33,d=2|raw` | additive_periodic | s(n + 3) = s(n) + 3 for all n >= 48 | 230 |
| `chomp4_a3000_c60/data|a~b|c=34,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 48 | 231 |
| `chomp4_a3000_c60/data|a~b|c=34,d=4|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 59 | 220 |
| `chomp4_a3000_c60/data|a~b|c=35,d=4|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 50 | 229 |
| `chomp4_a3000_c60/data|a~b|c=35,d=5|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 250 | 28 |
| `chomp4_a3000_c60/data|a~b|c=35,d=34|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 65 | 200 |
| `chomp4_a3000_c60/data|a~b|c=35,d=35|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 66 | 198 |
| `chomp4_a3000_c60/data|a~b|c=36,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 50 | 228 |
| `chomp4_a3000_c60/data|a~b|c=36,d=2|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 50 | 216 |
| `chomp4_a3000_c60/data|a~b|c=36,d=3|raw` | additive_periodic | s(n + 24) = s(n) + 24 for all n >= 96 | 157 |
| `chomp4_a3000_c60/data|a~b|c=36,d=35|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 66 | 199 |
| `chomp4_a3000_c60/data|a~b|c=37,d=4|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 56 | 222 |
| `chomp4_a3000_c60/data|a~b|c=37,d=5|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 53 | 222 |
| `chomp4_a3000_c60/data|a~b|c=37,d=37|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 68 | 194 |
| `chomp4_a3000_c60/data|a~b|c=38,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 56 | 221 |
| `chomp4_a3000_c60/data|a~b|c=38,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 56 | 219 |
| `chomp4_a3000_c60/data|a~b|c=38,d=38|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 70 | 190 |
| `chomp4_a3000_c60/data|a~b|c=39,d=2|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 56 | 209 |
| `chomp4_a3000_c60/data|a~b|c=39,d=3|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 92 | 173 |
| `chomp4_a3000_c60/data|a~b|c=39,d=4|raw` | additive_periodic | s(n + 6) = s(n) + 6 for all n >= 74 | 199 |
| `chomp4_a3000_c60/data|a~b|c=40,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 60 | 216 |
| `chomp4_a3000_c60/data|a~b|c=40,d=5|raw` | additive_periodic | s(n + 3) = s(n) + 3 for all n >= 60 | 213 |
| `chomp4_a3000_c60/data|a~b|c=41,d=2|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 62 | 202 |
| `chomp4_a3000_c60/data|a~b|c=41,d=40|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 76 | 183 |
| `chomp4_a3000_c60/data|a~b|c=41,d=41|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 79 | 178 |
| `chomp4_a3000_c60/data|a~b|c=42,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 63 | 212 |
| `chomp4_a3000_c60/data|a~b|c=42,d=4|raw` | additive_periodic | s(n + 6) = s(n) + 6 for all n >= 77 | 194 |
| `chomp4_a3000_c60/data|a~b|c=43,d=4|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 82 | 183 |
| `chomp4_a3000_c60/data|a~b|c=43,d=5|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 64 | 209 |
| `chomp4_a3000_c60/data|a~b|c=43,d=41|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 122 | 137 |
| `chomp4_a3000_c60/data|a~b|c=43,d=43|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 121 | 136 |
| `chomp4_a3000_c60/data|a~b|c=44,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 62 | 212 |
| `chomp4_a3000_c60/data|a~b|c=44,d=5|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 66 | 206 |
| `chomp4_a3000_c60/data|a~b|c=44,d=6|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 66 | 204 |
| `chomp4_a3000_c60/data|a~b|c=45,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 63 | 210 |
| `chomp4_a3000_c60/data|a~b|c=45,d=4|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 80 | 181 |
| `chomp4_a3000_c60/data|a~b|c=46,d=3|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 66 | 205 |
| `chomp4_a3000_c60/data|a~b|c=46,d=6|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 80 | 181 |
| `chomp4_a3000_c60/data|a~b|c=47,d=3|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 71 | 198 |
| `chomp4_a3000_c60/data|a~b|c=48,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 67 | 204 |
| `chomp4_a3000_c60/data|a~b|c=48,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 67 | 202 |
| `chomp4_a3000_c60/data|a~b|c=48,d=5|raw` | additive_periodic | s(n + 6) = s(n) + 6 for all n >= 84 | 181 |
| `chomp4_a3000_c60/data|a~b|c=48,d=46|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 87 | 166 |
| `chomp4_a3000_c60/data|a~b|c=49,d=49|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 91 | 162 |
| `chomp4_a3000_c60/data|a~b|c=50,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 73 | 196 |
| `chomp4_a3000_c60/data|a~b|c=50,d=5|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 80 | 177 |
| `chomp4_a3000_c60/data|a~b|c=51,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 73 | 196 |
| `chomp4_a3000_c60/data|a~b|c=51,d=3|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 76 | 191 |
| `chomp4_a3000_c60/data|a~b|c=51,d=4|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 74 | 196 |
| `chomp4_a3000_c60/data|a~b|c=52,d=4|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 78 | 191 |
| `chomp4_a3000_c60/data|a~b|c=52,d=5|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 78 | 178 |
| `chomp4_a3000_c60/data|a~b|c=52,d=51|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 94 | 154 |
| `chomp4_a3000_c60/data|a~b|c=52,d=52|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 96 | 150 |
| `chomp4_a3000_c60/data|a~b|c=53,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 75 | 193 |
| `chomp4_a3000_c60/data|a~b|c=53,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 75 | 192 |
| `chomp4_a3000_c60/data|a~b|c=53,d=3|raw` | additive_periodic | s(n + 6) = s(n) + 6 for all n >= 76 | 186 |
| `chomp4_a3000_c60/data|a~b|c=53,d=5|raw` | additive_periodic | s(n + 6) = s(n) + 6 for all n >= 84 | 176 |
| `chomp4_a3000_c60/data|a~b|c=54,d=3|raw` | additive_periodic | s(n + 3) = s(n) + 3 for all n >= 81 | 184 |
| `chomp4_a3000_c60/data|a~b|c=54,d=51|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 96 | 153 |
| `chomp4_a3000_c60/data|a~b|c=54,d=54|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 103 | 142 |
| `chomp4_a3000_c60/data|a~b|c=55,d=4|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 82 | 186 |
| `chomp4_a3000_c60/data|a~b|c=55,d=9|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 199 | 67 |
| `chomp4_a3000_c60/data|a~b|c=55,d=52|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 98 | 148 |
| `chomp4_a3000_c60/data|a~b|c=56,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 79 | 187 |
| `chomp4_a3000_c60/data|a~b|c=56,d=5|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 84 | 171 |
| `chomp4_a3000_c60/data|a~b|c=56,d=53|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 102 | 144 |
| `chomp4_a3000_c60/data|a~b|c=56,d=55|raw` | additive_periodic | s(n + 4) = s(n) + 4 for all n >= 108 | 133 |
| `chomp4_a3000_c60/data|a~b|c=57,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 81 | 184 |
| `chomp4_a3000_c60/data|a~b|c=58,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 82 | 183 |
| `chomp4_a3000_c60/data|a~b|c=58,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 81 | 183 |
| `chomp4_a3000_c60/data|a~b|c=58,d=3|raw` | additive_periodic | s(n + 6) = s(n) + 6 for all n >= 84 | 174 |
| `chomp4_a3000_c60/data|a~b|c=58,d=4|raw` | additive_periodic | s(n + 4) = s(n) + 4 for all n >= 82 | 181 |
| `chomp4_a3000_c60/data|a~b|c=59,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 84 | 179 |
| `chomp4_a3000_c60/data|a~b|c=59,d=5|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 95 | 159 |
| `chomp4_a3000_c60/data|a~b|c=60,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 84 | 180 |
| `chomp4_a3000_c60/data|a~b|c=60,d=5|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 96 | 156 |
| `chomp4_a3000_c60/data|b~a|c=0,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 1 | 299 |
| `chomp4_a3000_c60/data|b~a|c=2,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 4 | 296 |
| `chomp4_a3000_c60/data|b~a|c=4,d=2|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 10 | 289 |
| `chomp4_a3000_c60/data|b~a|c=4,d=4|raw` | additive_periodic | s(n + 2) = s(n) + 2 for all n >= 14 | 285 |
| `chomp4_a3000_c60/data|b~a|c=5,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 11 | 289 |
| `chomp4_a3000_c60/data|b~a|c=5,d=3|raw` | additive_periodic | s(n + 4) = s(n) + 4 for all n >= 15 | 282 |
| `chomp4_a3000_c60/data|b~a|c=7,d=0|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 15 | 285 |
| `chomp4_a3000_c60/data|b~a|c=7,d=3|raw` | additive_periodic | s(n + 8) = s(n) + 8 for all n >= 24 | 269 |
| `chomp4_a3000_c60/data|b~a|c=8,d=3|raw` | additive_periodic | s(n + 16) = s(n) + 16 for all n >= 24 | 261 |
| `chomp4_a3000_c60/data|b~a|c=12,d=2|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 24 | 276 |
| `chomp4_a3000_c60/data|b~a|c=26,d=3|raw` | additive_periodic | s(n + 1) = s(n) + 1 for all n >= 57 | 243 |
| `chomp4_a3000_c60/data|b~a|c=27,d=3|raw` | additive_periodic | s(n + 12) = s(n) + 12 for all n >= 56 | 233 |
| `chomp4_a3000_c60/data|FD:a<-(b,c,d)` | functional_dependency | In chomp4_a3000_c60/data, a is determined by (b, c, d): no two rows share (b, c, d) with different a | 172092 |
| `chomp4_a3000_c60/data|FD:b<-(a,c,d)` | functional_dependency | In chomp4_a3000_c60/data, b is determined by (a, c, d): no two rows share (a, c, d) with different b | 172092 |
| `chomp4_a3000_c60/data|FD:c<-(a,b,d)` | functional_dependency | In chomp4_a3000_c60/data, c is determined by (a, b, d): no two rows share (a, b, d) with different c | 172092 |
| `chomp4_a3000_c60/data|FD:d<-(a,b,c)` | functional_dependency | In chomp4_a3000_c60/data, d is determined by (a, b, c): no two rows share (a, b, c) with different d | 172092 |
