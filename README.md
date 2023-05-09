# ReadMe - Improving NYC Rideshare Prediction Accuracy

This repository contains the code and data for a project focused on improving the prediction accuracy of rideshare demand in New York City during the Covid-19 pandemic.

## Project Overview

We sought to answer four essential questions and test our hypotheses related to rideshare demand in NYC, specifically for Lyft and Uber. The questions are:

1. Which rideshare company experienced the most growth in demand since the beginning of the Covid-19 pandemic?
2. What is the relationship between exogenous variables, such as Covid-19 cases, hospitalizations, deaths, vaccinations, temperature, precipitation, and rideshare demand?
3. Which predictive algorithm and exogenous variables achieve the best forecast in rideshare demand?
4. What is the forecasted growth for Lyft and Uber through the second quarter of 2022?

## Dataset

The dataset used in this project is split into four key phases: pre-pandemic, shutdown, reopening, and vaccination. It contains daily trip counts for both Lyft and Uber, along with variables like temperature, precipitation, Covid-19 cases, hospitalizations, deaths, and vaccinations.

## Methods

We employed descriptive statistics, Pearson Correlation Coefficient calculations, and predictive models (SARIMAX, Prophet, and XGBoost) to analyze the data and make forecasts. We trained our models with data from Feb. 1, 2019, through Apr. 30, 2021, and performed cross-validation tests from May 1, 2021, through Mar. 31, 2022.

## Findings

Our findings suggest that during different phases of the pandemic, both Lyft and Uber experienced varying levels of growth and decline in demand. We also found that vaccinations were the best predictor for Lyft demand, while temperature was the best predictor for Uber demand. The predictive models forecasted that Lyft would experience a 10.23% increase in demand, while Uber would see a 3.86% increase in demand during the second quarter of 2022.

## Limitations

Limitations of the study include the smaller sample size of precipitation and Covid-19 vaccinations data, which led to less reliable R-values, and the lack of more specific vaccination data, which could introduce biases into the predictive models.

## Proposed Actions

To address the observed trends and forecasted growth, we recommend that both Lyft and Uber:

1. Increase marketing spending during warmer months to boost demand.
2. Explore economic variables that may impact rideshare demand and improve the quality of predictive models for future quarters.

## Expected Benefits

Our research can benefit small businesses looking to optimize their forecasting models by introducing exogenous variables into their predictive algorithms, potentially increasing accuracy and helping them better meet customer demand.

## Repository Structure

- `data/`: Contains the dataset used in the project.
- `src/`: Contains the source code for data processing, analysis, and modeling.
- `notebooks/`: Contains Jupyter notebooks used for data exploration, analysis, and visualization.
- `results/`: Contains tables and figures generated from the analysis and modeling.
- `LICENSE`: The license file for the project.
- `README.md`: This ReadMe file with an overview of the project.

## How to Run

1. Install the required Python packages: `pip install -r requirements.txt`.
2. Run the Jupyter notebooks in the `notebooks/` folder for data exploration, analysis, and visualization.
3. Run the source code in the `src/` folder for data processing, analysis, and modeling.
