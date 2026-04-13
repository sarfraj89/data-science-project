# End-to-End Data Science Project

This project predicts a student's `math_score` using demographic and academic features. It is built as a modular machine learning pipeline with data ingestion, preprocessing, model training, evaluation, logging, custom exceptions, and optional MLflow tracking.

## Project Highlights
- End-to-end regression pipeline for student performance prediction
- Automatic fallback to local CSV data when database credentials are unavailable
- Multiple regression models compared with cross-validation and test `R2` score
- Saved preprocessing and model artifacts in `artifacts/`
- Logging and custom exception handling for easier debugging

## Project Structure
- `app.py` — main entry point that runs the full pipeline
- `src/data_science_project/components/` — ingestion, transformation, trainer modules
- `src/data_science_project/utils.py` — shared helpers for reading data, saving objects, and model evaluation
- `src/data_science_project/logger.py` — application logging setup
- `src/data_science_project/exception.py` — custom exception wrapper
- `notebook/` — EDA and training notebooks
- `artifacts/` — saved datasets, preprocessor, and trained model

## Setup

### 1. Create and activate the virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

## Run the Project
```bash
python app.py
```

### What happens when you run it
1. Data is loaded from the database or local CSV fallback.
2. Train/test split files are created in `artifacts/`.
3. Features are preprocessed and saved.
4. Multiple regression models are trained and compared.
5. The best model is saved as `artifacts/model.pkl`.
6. The final `R2` score is printed to the console.

## Output Files
- `artifacts/raw.csv`
- `artifacts/train.csv`
- `artifacts/test.csv`
- `artifacts/preprocessor.pkl`
- `artifacts/model.pkl`

## Metrics Used
- `R2 score` — primary metric for model comparison
- `RMSE` — root mean squared error
- `MAE` — mean absolute error

## MLflow
The project supports MLflow experiment logging. If registry access is not available, training still completes and returns the final metric.

## Full Documentation
For a complete explanation of every file, the pipeline flow, and interview-ready notes, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md).

## Interview Tip
If you are asked to explain this project in an interview, focus on the pipeline design, preprocessing choices, model comparison, and how you made the project production-friendly with logging, custom exceptions, and artifact saving.
End to End Data Science Project