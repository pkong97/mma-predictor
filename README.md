# mma-predictor
A predictor for MMA fights!
The data was gathered from fightmetric.com using Beautiful Soup and munged with NumPy and pandas. scikit-learn was used to fit a logistic regression model to the data and predict the outcome of a fight.

# Predictions
UFC Fight Night: Dos Santos vs. Tuivasa

| Fighter1  | Fighter2 | Predicted Winner |
| --------- | -------- | ---------------- |
| Junior Dos Santos  | Tai Tuivasa  | 1 |
| Mauricio Rua | Tyson Pedro  | 1 |
| Mark Hunt | Justin Willis | 2 | 
| Jake Matthews | Anthony Rocco Martin | 1 |
| Jimmy Crute | Paul Craig | 1 |
| Yushin Okami | Aleksei Kunchenko | 1 |
| Wilson Reis | Ben Nguyen | 2 |
| Keita Nakamura | Salim Touahri | 1 |
| Mizuto Hirota | Christos Giagos | 2 |

# TODO
- [ ] Chain together scripts with workflow engine
- [ ] Get data on betting odds
