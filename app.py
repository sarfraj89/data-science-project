import os
import sys


if os.environ.get("DATA_SCIENCE_PROJECT_BOOTSTRAPPED") != "1":
    project_python = os.path.join(os.path.dirname(__file__), ".venv", "bin", "python")
    if sys.executable != project_python and os.path.exists(project_python):
        os.environ["DATA_SCIENCE_PROJECT_BOOTSTRAPPED"] = "1"
        os.execv(project_python, [project_python] + sys.argv)


from src.data_science_project.logger import logging
from src.data_science_project.exception import CustomException
from src.data_science_project.components.data_ingestion import DataIngestion
from src.data_science_project.components.data_ingestion import DataIngestionConfig
from src.data_science_project.components.data_transformation import DataTransformation, DataTransformationConfig
from src.data_science_project.components.model_trainer import ModelTrainerConfig, ModelTrainer
import sys


if __name__=="__main__":
    logging.info("The execution has started")

    try:
        #data_ingestion_config=DataIngestionConfig()
        data_ingestion=DataIngestion()
        train_data_path,test_data_path=data_ingestion.initiate_data_ingestion()

        #data_transformation_config=DataTransformationConfig()
        data_transformation=DataTransformation()
        train_arr,test_arr,_=data_transformation.initiate_data_transormation(train_data_path,test_data_path)

        ## Model Training

        model_trainer=ModelTrainer()
        print(model_trainer.initiate_model_trainer(train_arr,test_arr))
        
    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e,sys)