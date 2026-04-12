import os
import sys
from src.data_science_project.exception import CustomException
from src.data_science_project.logger import logging
import pandas as pd

from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')
    source_data_path:str=os.path.join('notebook','data','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            ##reading the data from mysql
            candidate_paths = [
                os.environ.get("DATA_SOURCE_PATH"),
                self.ingestion_config.source_data_path,
                os.path.join("data", "raw.csv"),
            ]
            source_path = next((p for p in candidate_paths if p and os.path.exists(p)), None)

            if source_path is None:
                raise FileNotFoundError(
                    "Raw data file not found. Add a CSV at notebook/data/raw.csv or data/raw.csv, "
                    "or set DATA_SOURCE_PATH to your CSV file path."
                )

            df=pd.read_csv(source_path)
            logging.info("Reading completed mysql database")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            train_set=df.sample(frac=0.8,random_state=42)
            test_set=df.drop(train_set.index)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Data Ingestion is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path


            )


        except Exception as e:
            raise CustomException(e,sys)