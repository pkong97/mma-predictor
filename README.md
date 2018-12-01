# mma-predictor
A predictor for MMA fights!
The data was gathered from fightmetric.com using Beautiful Soup and munged with NumPy and pandas. scikit-learn was used to fit a logistic regression model to the data and predict the outcome of a fight.

# Predictions
UFC Fight Night: Dos Santos vs. Tuivasa

| Fighter1  | Fighter2 | Predicted Winner | Correct? |
| --------- | -------- | ---------------- | |
| Junior Dos Santos  | Tai Tuivasa  | Fighter1 | |
| Mauricio Rua | Tyson Pedro  | Fighter1 | |
| Mark Hunt | Justin Willis | Fighter2 | |
| Jake Matthews | Anthony Rocco Martin | Fighter1 | |
| Jimmy Crute | Paul Craig | Fighter1 | |
| Yushin Okami | Aleksei Kunchenko | Fighter1 | |
| Wilson Reis | Ben Nguyen | Fighter2 | |
| Keita Nakamura | Salim Touahri | Fighter1 | |
| Mizuto Hirota | Christos Giagos | Fighter2 | |

# TODO
- [ ] Chain together scripts with workflow engine
- [ ] Get data on betting odds
