# NPRI Project
📊 NPRI Pollution Trends Forecasting Project

Time Series Regression | Environmental Data Analysis | Machine Learning

📌 Project Overview

This project analyzes historical pollutant release data from Canada’s National Pollutant Release Inventory (NPRI) to understand industry-level pollution trends and forecast future emissions over the next five years.
The goal is to identify industries with rising environmental risk and those showing meaningful reductions, supporting data-driven environmental monitoring and policy decisions.

❓ Problem Statement

Based on NPRI data, which industry is predicted to have the highest growth in pollutant releases over the next five years, and which industry is expected to experience the largest decline?

🗂️ Data Description

The NPRI dataset tracks pollutant releases across Canada from 2000 to 2020, covering emissions to air, water, and land.

Key Fields Used

NAICS Code – Industry classification

Company & Facility – Source of emissions

Releases – Total pollutant quantities

Province & Employees – Location and scale indicators

Year – Time dimension for trend analysis

⚙️ Methodology
Phase 1: Pollution Level Classification

Industries were categorized into Low, Medium, and High pollution levels.

Pollution categories were encoded numerically to support modeling.

Phase 2: Time Series Regression

Built regression models to forecast long-term emission trends by industry.

Used historical release patterns and prior-year growth values as predictors.

🧹 Data Preparation

Cleaned missing and infinite values

Encoded categorical variables (region, estimation method)

Scaled numerical features using StandardScaler

Removed incomplete records to ensure model reliability

📈 Modeling Approach

Regression-based forecasting

Features included:

Previous year pollution levels

Previous year growth rates

Encoded pollution categories

Focused on trend direction and relative change, not short-term volatility

🔍 Key Findings

Bituminous coal mining is projected to show the highest growth in emissions over the next five years.

Non-ferrous metal smelting (except aluminum) is forecasted to experience the largest decline, indicating effective emissions control.

Most industries show relatively stable trends, but a small number of outliers drive significant environmental impact.

🌍 Implications

Forecasting tools like this help prioritize high-risk industries for regulatory focus.

Industries with increasing emissions may require targeted interventions.

Sectors with declining trends can serve as benchmarks for best practices in emissions management.

The approach supports evidence-based environmental policy and planning.

🛠️ Tools & Technologies

Python

Pandas & NumPy

Scikit-learn

Time Series Regression

StandardScaler

PowerPoint (technical communication & presentation)
