# LoL Draft Analyzer

## Description

Project that aims to research if you can predict the League of Legends games result base only on the draft.

#### Technologies
  - pytorch
  - sklearn
  - skorch
  - jupyter notebook
  - xgboost

## Parts of the project
### Data Scraping

Data scraping part was realized with requests to RIOT API which results were later saved into the database.

### Preprocessing

- Creating Training, Valid and Test sets.
- Creating custom transformers and Pipelines

### ML models

- Linear Regression
- sklearn random forest
- xgboost
- vote classifier

### Neural Networks

- CNN
- FCNN

### Conclusions

Given that the best result was 5% better than the baseline, quick conclusion is that bare draft
provides to little information to make accurate prediction.

