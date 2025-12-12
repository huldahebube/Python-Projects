Bever Hill Bird Observatory – Migration Analysis & Streamlit App

This project analyzes multi-year bird migration data from the Bever Hill Bird Observatory and provides an interactive Streamlit web app that helps users explore species behavior, habitat use, and seasonal migration trends.

The goal is to make bird movement data easy to understand for researchers, conservationists, and the public.

✅ Project Summary

Cleaned and prepared raw bird observation data

Generated temporal, behavioral, and geospatial features

Explored migration patterns through visualizations

Built machine learning models to understand and predict bird signal strength

Developed a Streamlit app with filtering tools, summary statistics, and visual dashboards

🛠 Libraries Used

Data & Processing:

pandas

numpy

Visualization:

matplotlib

seaborn

plotly

Modeling:

scikit-learn

Random Forest Regressor

XGBoost / LightGBM (if used)

App Framework:

streamlit

🤖 Models Used

Used primarily to predict signal strength and understand influencing factors:

Random Forest Regressor

XGBoost

Evaluation metrics:

RMSE

MAE

R² Score

These metrics helped measure how well the models captured migration patterns and bird behavior.

🔍 Key Insights

Migration activity changes significantly across seasons

Habitat type strongly affects detection and movement

Species show distinct temporal movement patterns (daily + seasonal)

Adding engineered features (lag values, rolling windows, time-based features) improved model accuracy

Streamlit app allows users to dynamically explore:

Bird IDs

Habitat types

Date ranges

Summary statistics

🧠 Skills Demonstrated

Data cleaning & feature engineering

Geospatial and temporal data analysis

Building regression models

Creating interactive dashboards

Deploying a Streamlit application

Communicating findings for both technical and non-technical users
