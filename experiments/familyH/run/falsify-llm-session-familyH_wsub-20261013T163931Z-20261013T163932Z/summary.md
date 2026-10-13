# Falsification `falsify-llm-session-familyH_wsub-20261013T163931Z-20261013T163932Z`

Mining run: `llm-session-familyH_wsub-20261013T163931Z` · 16.47 s

Rule: refuted if violated on any sequence in scope; survived if it holds on all and at least one has new terms; otherwise untestable.

| Dataset | Tested against | Window | Scale factor | Candidates |
|---|---|---|---|---|
| `wsub_subsets5_n1000` | `wsub_subsets5_n1000` | `{'x': 99, 'y': 99}` | `{'x': 10.09, 'y': 10.09}` | 19 |

Overall: {'survived': 19}

| Kind | Status counts |
|---|---|
| claim_predicate | {'survived': 19} |

## Survived (19)

| Sequence | Statement | Detail |
|---|---|---|
| `wsub_subsets5_n1000/data|claim:e0a4450718` | For every S consisting of odd numbers with 1 in S (here {1}, {1,3}, {1,5}, {1,3,5}), the Grundy value is G(x,y) = 0 if x,y both even; 2 if both odd; for mixed parity 1 if the odd coordinate is the larger one, else 3. |  |
| `wsub_subsets5_n1000/data|claim:a87ec015eb` | If 1 and 2 are in S and no element of S is divisible by 3 (here {1,2}, {1,2,4}, {1,2,5}, {1,2,4,5}), then G(x,y) = (x + y) mod 3. |  |
| `wsub_subsets5_n1000/data|claim:c841507145` | Scaling: for S = {2}, G(x,y) = G_{1}(floor(x/2), floor(y/2)) with G_{1} the formula of H01. |  |
| `wsub_subsets5_n1000/data|claim:a8fbb6e618` | Scaling: for S = {3}, G(x,y) = G_{1}(floor(x/3), floor(y/3)) with G_{1} the formula of H01. |  |
| `wsub_subsets5_n1000/data|claim:15aa0ce868` | Scaling: for S = {4}, G(x,y) = G_{1}(floor(x/4), floor(y/4)) with G_{1} the formula of H01. |  |
| `wsub_subsets5_n1000/data|claim:71dca76b54` | Scaling: for S = {5}, G(x,y) = G_{1}(floor(x/5), floor(y/5)) with G_{1} the formula of H01. |  |
| `wsub_subsets5_n1000/data|claim:723a9fb66f` | Scaling: for S = {2,4}, G(x,y) = (floor(x/2) + floor(y/2)) mod 3. |  |
| `wsub_subsets5_n1000/data|claim:a50bd1183c` | For S = {1,2,3} and S = {1,2,3,5}: (x,y) is a P-position iff (x mod 4, y mod 4) is one of (0,0), (1,2), (2,1), i.e. a Wythoff P-position with both coordinates < 4. |  |
| `wsub_subsets5_n1000/data|claim:956837e395` | For S = {1,2,3,4}: (x,y) is a P-position iff (x mod 5, y mod 5) is a Wythoff P-position with both coordinates < 5: (0,0), (1,2), (2,1). |  |
| `wsub_subsets5_n1000/data|claim:c1738b11d7` | For S = {1,2,3,4,5}: (x,y) is a P-position iff (x mod 6, y mod 6) is a Wythoff P-position with both coordinates < 6: (0,0), (1,2), (2,1), (3,5), (5,3). Conjecturally W({1..k}) reduces to Wythoff modulo k+1 for every k. |  |
| `wsub_subsets5_n1000/data|claim:5b058d006e` | For S = {2,3}: (x,y) is a P-position iff with m = 5: x mod m < 2 and y mod m < 2, or (x mod m, y mod m) is (2,4) or (4,2). Conjecturally this holds for every pair {a, a+1} (a = 1 gives (x+y) mod 3 = 0). |  |
| `wsub_subsets5_n1000/data|claim:35990c1ed4` | For S = {3,4}: (x,y) is a P-position iff with m = 7: x mod m < 3 and y mod m < 3, or (x mod m, y mod m) is (3,6) or (6,3). Conjecturally this holds for every pair {a, a+1} (a = 1 gives (x+y) mod 3 = 0). |  |
| `wsub_subsets5_n1000/data|claim:dfec26cdc2` | For S = {4,5}: (x,y) is a P-position iff with m = 9: x mod m < 4 and y mod m < 4, or (x mod m, y mod m) is (4,8) or (8,4). Conjecturally this holds for every pair {a, a+1} (a = 1 gives (x+y) mod 3 = 0). |  |
| `wsub_subsets5_n1000/data|claim:e2f269e20b` | For S = {2,3,4,5} and S = {2,3,5}: the P-positions are exactly the (x,y) with (x mod 7, y mod 7) in {0,1}x{0,1} or in {(2,4),(2,5),(3,5),(3,6),(4,2),(5,2),(5,3),(6,3)}. |  |
| `wsub_subsets5_n1000/data|claim:77719221b3` | For S = {3,5}: (x,y) is a P-position iff (x mod 8, y mod 8) is in {0,1,2}^2, {3,4}x{6,7} or {6,7}x{3,4}. |  |
| `wsub_subsets5_n1000/data|claim:c514592809` | For S = {1,4}: with u = min(x,y), v = max(x,y), (x,y) is a P-position iff (u mod 5, v mod 5) is in {(0,0),(0,2),(1,4),(2,2),(3,1),(3,4),(4,3)}. The pattern is periodic with period 5 on each side of the diagonal but not symmetric across it. |  |
| `wsub_subsets5_n1000/data|claim:20f5e6bda7` | For S = {2,3,4}: with u = min(x,y), v = max(x,y), (x,y) is a P-position iff (u mod 6, v mod 6) is in {0,1}x{0,1} or {(2,4),(2,5),(3,5),(4,2),(5,3)}. |  |
| `wsub_subsets5_n1000/data|claim:be762f7d6b` | For S = {3,4,5}: with u = min(x,y), v = max(x,y), (x,y) is a P-position iff (u mod 8, v mod 8) is in {0,1,2}^2 or {(3,6),(3,7),(4,7),(6,3),(7,4)}. |  |
| `wsub_subsets5_n1000/data|claim:8bcf65b750` | For S = {1,3,4}, away from the diagonal (max(x,y) >= 2 min(x,y)): (x,y) is a P-position iff (u mod 7, v mod 7) is in {(0,0),(0,2),(1,4),(1,6),(2,1),(2,3),(3,6),(4,1),(4,3),(5,5),(5,0),(6,4)} with u = min, v = max. Near the diagonal the pattern is different. |  |
