# mma-predictor
A predictor for MMA fights!

Mixed Martial Arts is a very unpredictable sport. There exists a large number of variables from stemming from the multitude of styles and attacks allowed in the sport. So I've created this mma-predictor to try and make sense of all the chaos and hopefully glimpse into the future!

The data was gathered from [fightmetric](https://www.fightmetric.com) using Beautiful Soup and cleaned with NumPy and pandas. Scikit-learn was used to fit a logistic regression model to the data and predict the outcome of a fight. 

Initial testing with logistic regression, decision tree classifier, and random forest classifier classifier models yielded prediction rates of 89.93%, 72.48%, and 79.87% respectively.

To use the predictor, clone the repository and execute the "run-predictor.sh" script. Currently the tool only predicts the next upcoming UFC event. However, I plan to add functionality that will allow for the user to input any two fighters.

# Real-time Predictions

UFC 231: Holloway vs. Ortega
----------------------------
Dec. 08, 2018

8/13 (61.5%) of fights predicted correctly

Expected ROI* = +11.1%

| Fighter1  | Fighter2 | Predicted Winner | Correct? |
| --------- | -------- | ---------------- | -- |
| Max Holloway  | Brian Ortega  | Fighter1 | Y |
| Valentina Shevchenko | Joanna Jedrzejczyk | Fighter2 | N |
| Alex Oliveira | Gunnar Nelson | Fighter1 | N |
| Hakeem Dawodu | Kyle Bochniak | Fighter1 | Y |
| Jimi Manuwa | Thiago Santos | Fighter2 | Y |
| Claudia Gadehla | Nina Ansaroff | Fighter2 | Y |
| Olivier Aubin-Mercier | Gilbert Burns | Fighter1 | N |
| Katlyn Chookagian | Jessica Eye | Fighter1 | N |
| Elias Theodorou | Eryk Anders | Fighter1 | Y |
| Brad Katona | Matthew Lopez | Fighter1 | Y |
| Chad Laprise | Dhiega Lima | Fighter1 | N |
| Diego Ferreira | Kyle Nelson | Fighter1 | Y |
| Devin Clark | Aleksandar Rakic | Fighter2 | Y |

UFC Fight Night: Dos Santos vs. Tuivasa
---------------------------------------
Dec. 01, 2018

6/9 (66.6%) of fights predicted correctly

Exected ROI* = +36.0%

| Fighter1  | Fighter2 | Predicted Winner | Correct? |
| --------- | -------- | ---------------- | -- |
| Junior Dos Santos  | Tai Tuivasa  | Fighter1 | Y |
| Mauricio Rua | Tyson Pedro  | Fighter1 | Y |
| Mark Hunt | Justin Willis | Fighter2 | Y |
| Jake Matthews | Anthony Rocco Martin | Fighter1 | N |
| Jimmy Crute | Paul Craig | Fighter1 | Y |
| Yushin Okami | Aleksei Kunchenko | Fighter1 | N |
| Wilson Reis | Ben Nguyen | Fighter2 | N |
| Keita Nakamura | Salim Touahri | Fighter1 | Y |
| Mizuto Hirota | Christos Giagos | Fighter2 | Y |

*The expected ROI is calculated by assuming an identical wager is placed on each match.

# TODO
- [ ] Get data on betting odds
- [ ] Additional feature engineering to improve accuracy
- [X] Migrate data to PostgreSQL
