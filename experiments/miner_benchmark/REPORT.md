# Miner benchmark (n=200 per family, seed=7, scale 10x)

Config: `experiments/configs/mining/dev_subtraction_wythoff.yaml`

| Family | n | recovered | exact | wrong | other_true | silent | candidates |
|---|---|---|---|---|---|---|---|
| periodic | 200 | 200 | 200 | 0 | 2 | 0 | 202 |
| additive_periodic | 200 | 200 | 200 | 0 | 0 | 0 | 200 |
| periodic_long_preperiod | 200 | 200 | 200 | 0 | 0 | 0 | 200 |
| linear_recurrence | 200 | 200 | 0 | 0 | 0 | 0 | 206 |
| polynomial | 200 | 200 | 0 | 0 | 0 | 0 | 200 |
| quasi_polynomial | 200 | 200 | 0 | 0 | 0 | 0 | 200 |
| floor_linear | 200 | 200 | 0 | 19 | 0 | 0 | 322 |
| negative_uniform | 200 | 0 | 0 | 0 | 0 | 200 | 0 |
| negative_random_walk | 200 | 0 | 0 | 0 | 0 | 200 | 0 |
| negative_noisy_periodic | 200 | 0 | 0 | 111 | 0 | 89 | 111 |
