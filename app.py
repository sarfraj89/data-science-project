from src.data_science_project.logger import logging
from src.data_science_project.exception import CustomException
from src.data_science_project.pipelines.training_pipeline import TrainPipeline
import sys

if __name__ == "__main__":
    logging.info("The execution has started.")

    try:
        train_data_path, test_data_path = TrainPipeline().run_pipeline()
        logging.info("Training data created at: %s", train_data_path)
        logging.info("Test data created at: %s", test_data_path)
    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e, sys)