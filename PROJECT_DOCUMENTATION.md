# End-to-End Data Science Project Documentation

## 1. Project Overview
This project is an end-to-end machine learning pipeline built to predict student performance, specifically the `math_score`, using other student-related features such as gender, race/ethnicity, parental education level, lunch type, test preparation status, reading score, and writing score.

The project follows a standard ML lifecycle:
1. Read the raw data from a database or a local CSV fallback.
2. Split the dataset into training and testing sets.
3. Preprocess categorical and numerical features.
4. Train and compare multiple regression models.
5. Select the best model based on test performance.
6. Save the trained model and preprocessing object.
7. Log metrics and model artifacts through MLflow when available.

The main goal is not only to build a model, but also to organize the workflow in a clean production-style structure.

---

## 2. Problem Statement
The task is a regression problem:
- **Input:** student demographic and academic features
- **Output:** predicted `math_score`

Since `math_score` is continuous, the project uses regression models instead of classification models.

---

## 3. Dataset Description
The dataset contains the following features:

- `gender`
- `race_ethnicity`
- `parental_level_of_education`
- `lunch`
- `test_preparation_course`
- `reading_score`
- `writing_score`
- `math_score` (target)

### Target Variable
- `math_score` is the value the model learns to predict.

### Feature Types
- **Categorical features:** `gender`, `race_ethnicity`, `parental_level_of_education`, `lunch`, `test_preparation_course`
- **Numerical features:** `reading_score`, `writing_score`

---

## 4. Folder Structure Explanation

```text
app.py
Dockerfile
README.md
requirements.txt
setup.py
template.py
artifacts/
logs/
mlruns/
notebook/
src/data_science_project/
```

### Root Files
- **app.py**: Main entry point of the project.
- **Dockerfile**: Used to containerize the application.
- **README.md**: Short project overview.
- **requirements.txt**: Python dependencies.
- **setup.py**: Package setup for installation.
- **template.py**: Project scaffolding helper.

### `artifacts/`
Stores generated outputs:
- raw dataset copy
- train/test splits
- preprocessing object
- trained model

### `logs/`
Stores log files created during execution.

### `mlruns/`
Stores MLflow run artifacts and experiment metadata.

### `notebook/`
Contains exploratory and training notebooks.

### `src/data_science_project/`
Contains the actual application code.

---

## 5. Main Execution Flow

The application starts from `app.py`.

### Step-by-step flow
1. `DataIngestion` reads the data.
2. The data is split into train and test sets.
3. `DataTransformation` preprocesses the data.
4. `ModelTrainer` trains multiple models.
5. Best model is selected using test `r2_score`.
6. The final model is saved in `artifacts/model.pkl`.
7. The evaluation metric is printed to the console.

---

## 6. File-by-File Explanation

### 6.1 `app.py`
This is the application launcher.

#### What it does
- Bootstraps the local virtual environment automatically if available.
- Imports the main pipeline classes.
- Runs ingestion, transformation, and model training in order.
- Prints the final `r2_score`.

#### Important behavior
If MLflow logging fails because of permissions or registry issues, the training step still completes and returns the score.

---

### 6.2 `src/data_science_project/components/data_ingestion.py`
This file handles loading and splitting the raw data.

#### Responsibilities
- Read data from the source using `read_sql_data()`.
- Save a raw CSV copy in `artifacts/raw.csv`.
- Split the data into:
  - `artifacts/train.csv`
  - `artifacts/test.csv`

#### Why it matters
Data ingestion prepares the input data for the rest of the pipeline and makes the workflow reproducible.

---

### 6.3 `src/data_science_project/components/data_transformation.py`
This file handles preprocessing.

#### Responsibilities
- Identify categorical and numerical columns.
- Build separate preprocessing pipelines.
- Apply imputation, encoding, and scaling.
- Save the fitted preprocessor as `artifacts/preprocessor.pkl`.

#### Numerical pipeline
- Median imputation
- Standard scaling

#### Categorical pipeline
- Most-frequent imputation
- One-hot encoding
- Scaling with `with_mean=False`

#### Output
- Transformed training and testing arrays
- Saved preprocessing object

---

### 6.4 `src/data_science_project/components/model_trainer.py`
This file trains and evaluates multiple regression models.

#### Models used
- Random Forest Regressor
- Decision Tree Regressor
- Gradient Boosting Regressor
- Linear Regression
- XGBRegressor
- CatBoost Regressor
- AdaBoost Regressor

#### What it does
- Splits arrays into `X_train`, `y_train`, `X_test`, `y_test`
- Runs model comparison using `evaluate_models()`
- Finds the best model based on test `r2_score`
- Saves the best model in `artifacts/model.pkl`
- Logs metrics to MLflow if available

#### Evaluation metrics
- RMSE
- MAE
- R2 Score

#### Final output
- Returns the test `r2_score` of the best model.

---

### 6.5 `src/data_science_project/utils.py`
This file contains reusable helper functions.

#### `read_sql_data()`
- Tries to read data from MySQL using environment variables.
- If DB credentials are missing, it falls back to local CSV data.
- If SQL connection fails, it also falls back to local data when available.

#### `save_object()`
- Saves Python objects using `pickle`.
- Used for the trained model and preprocessing object.

#### `evaluate_models()`
- Runs GridSearchCV for each model.
- Fits the best parameters.
- Calculates test `r2_score` for every model.
- Returns a report dictionary.

---

### 6.6 `src/data_science_project/logger.py`
This file sets up application logging.

#### Responsibilities
- Creates a timestamped log file inside `logs/`
- Configures the logging format
- Helps track the execution flow and errors

---

### 6.7 `src/data_science_project/exception.py`
This file defines custom exception handling.

#### Responsibilities
- Captures detailed error context
- Includes file name and line number in the error message
- Makes debugging easier

#### Why it is useful
Instead of getting a vague Python error, the project reports where the error happened.

---

### 6.8 `setup.py`
This file makes the project installable as a Python package.

#### Responsibilities
- Defines package metadata
- Loads dependencies from `requirements.txt`
- Supports `pip install -e .`

---

### 6.9 `requirements.txt`
Lists the external libraries used in the project.

#### Main dependencies
- `numpy`
- `pandas`
- `scikit-learn`
- `catboost`
- `xgboost`
- `mlflow`
- `pymysql`
- `python-dotenv`

---

### 6.10 `Dockerfile`
Used to package the application in a Docker container.

#### Why it matters
- Makes the project portable
- Helps deploy the project consistently across environments

---

### 6.11 `notebook/`
Contains notebook-based exploration and experimentation.

#### Files
- EDA notebook
- Model training notebook

These notebooks are useful for experimentation, but the production-like flow lives in the `src/` folder and `app.py`.

---

## 7. Data Flow in Simple Words
1. Get the raw data.
2. Clean and split it.
3. Convert categorical data into numbers.
4. Scale the features.
5. Train several regression models.
6. Compare their scores.
7. Save the best one.
8. Print the final R2 score.

---

## 8. Why Preprocessing Is Needed
Machine learning models cannot directly learn from text categories like:
- `male`
- `female`
- `group A`
- `standard`

So preprocessing is required to:
- convert categories into numeric features
- handle missing values
- standardize numerical columns

This improves model learning and consistency.

---

## 9. Why Multiple Models Are Used
Different models behave differently on the same dataset.

### Benefits of testing multiple models
- Better chance of finding the strongest algorithm
- Helps compare linear and non-linear approaches
- Makes the solution more reliable

### In this project
The best model is selected by comparing test `r2_score`.

---

## 10. Understanding the R2 Score
`R2 score` tells how well the model explains the variance in the target variable.

### Interpretation
- Closer to `1.0`: very good fit
- Around `0.0`: weak predictive power
- Negative: worse than a simple baseline

A higher `r2_score` is better for this project.

---

## 11. MLflow Integration
MLflow is used to track:
- parameters
- metrics
- trained model artifacts

### What happens in the project
- It logs RMSE, MAE, and R2
- It attempts to register the model in MLflow
- If registry access fails, the project now continues and still returns the result

### Why this is helpful
You can compare experiments and track the best model across runs.

---

## 12. Local Fallback Behavior
The project is designed to be flexible.

### If the database is unavailable
- It reads from `notebook/data/raw.csv` or `artifacts/raw.csv`

### If MLflow registry is unavailable
- It skips registry logging
- It still trains the model and returns the score

This makes the project more reliable during local development.

---

## 13. How to Run the Project

### Install dependencies
```bash
pip install -r requirements.txt
```

### Install the local package
```bash
pip install -e .
```

### Run the application
```bash
python app.py
```

### Expected output
- Best model name
- Final `r2_score`
- Saved model inside `artifacts/`

---

## 14. Outputs Generated by the Project
After a successful run, these files are usually created or updated:

- `artifacts/raw.csv`
- `artifacts/train.csv`
- `artifacts/test.csv`
- `artifacts/preprocessor.pkl`
- `artifacts/model.pkl`
- log files in `logs/`
- MLflow artifacts in `mlruns/`

---

## 15. Common Interview Explanation
If someone asks you to explain this project in an interview, you can say:

> I built an end-to-end machine learning pipeline to predict student math scores. The project starts by ingesting data from a database or local CSV, then it preprocesses categorical and numerical features, trains multiple regression models, evaluates them using R2 score, and saves the best model. I also added logging, custom exception handling, and MLflow tracking to make the project production-friendly.

---

## 16. Interview Section

### 16.1 How to introduce this project
You can say:

> This is an end-to-end student performance prediction project. It predicts math scores based on demographic and academic inputs. I structured it into ingestion, transformation, training, and evaluation modules so the pipeline is modular and production-ready.

### 16.2 Why did you choose regression?
Because the target variable, `math_score`, is continuous. Regression is the correct learning task for numeric prediction.

### 16.3 Why do you use preprocessing?
Because the dataset contains categorical variables and possible missing values. Preprocessing ensures the model receives clean numeric inputs.

### 16.4 Why use one-hot encoding?
One-hot encoding converts categorical values into a machine-readable format without introducing fake ordering.

### 16.5 Why use StandardScaler?
Scaling helps models that are sensitive to feature magnitude and ensures consistent input ranges.

### 16.6 Why compare multiple models?
Different algorithms perform differently depending on the dataset. Comparing multiple models improves the chance of selecting the best one.

### 16.7 Why use R2 score?
R2 is a standard regression metric that shows how much variance the model explains. It is easy to interpret and suitable for comparing models.

### 16.8 What is the role of MLflow?
MLflow tracks experiments, metrics, and models. It helps with reproducibility and model management.

### 16.9 What is the role of custom exception handling?
It provides clearer error messages with file names and line numbers, which makes debugging easier.

### 16.10 What is the role of logging?
Logging records the execution flow and helps diagnose problems after the pipeline runs.

### 16.11 How would you deploy this project?
I would package it with Docker and expose inference through an API or web app. The trained model and preprocessor can be loaded to serve predictions.

### 16.12 How would you improve the project further?
Possible improvements:
- add hyperparameter tuning for more models
- create a prediction API
- add automated tests
- improve model explainability
- add data validation checks
- deploy to cloud services

---

## 17. Possible Interview Questions and Short Answers

### Q1. What problem does this project solve?
It predicts student math scores using other student features.

### Q2. What type of ML task is this?
It is a regression problem.

### Q3. Why did you use `train_test_split` logic manually?
To keep the pipeline simple and explicitly store train/test artifacts.

### Q4. How did you handle missing values?
With median imputation for numeric features and most-frequent imputation for categorical features.

### Q5. Why save the preprocessing object?
So the same transformations can be applied consistently during inference.

### Q6. How do you select the best model?
By comparing test R2 scores from multiple trained models.

### Q7. Why is custom logging useful?
It helps trace execution and debug failures.

### Q8. What happens if MLflow fails?
The training still completes and returns the final score.

### Q9. Why is `app.py` important?
It is the entry point that runs the full pipeline.

### Q10. What makes this project end-to-end?
It includes ingestion, preprocessing, model training, evaluation, saving artifacts, and experiment tracking.

---

## 18. Final Summary
This project is a complete example of how to build a structured machine learning workflow in Python. It is modular, easy to understand, and suitable for both learning and interview discussion. The code is organized in a way that separates responsibilities clearly, which is a strong software engineering practice for data science projects.

If you want, I can also turn this into a more polished README-style document or add a dedicated section for deployment and API prediction flow.
