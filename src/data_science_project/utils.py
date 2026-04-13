import os
import sys
from src.data_science_project.exception import CustomException
from src.data_science_project.logger import logging
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import pymysql

import pickle
import numpy as np

load_dotenv()

host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
db=os.getenv('db')
local_raw_data_candidates = [
    os.path.join("notebook", "data", "raw.csv"),
    os.path.join("artifacts", "raw.csv"),
]


def _get_local_raw_data_path():
    for candidate in local_raw_data_candidates:
        if os.path.exists(candidate):
            return candidate
    return None



def read_sql_data():
    logging.info("Reading SQL database started")
    try:
        local_raw_data_path = _get_local_raw_data_path()

        if local_raw_data_path is not None and not all([host, user, password, db]):
            logging.info("Database credentials are missing; reading local raw data instead")
            return pd.read_csv(local_raw_data_path)

        mydb=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        logging.info("Connection Established",mydb)
        df=pd.read_sql_query('Select * from students',mydb)
        print(df.head())

        return df



    except Exception as ex:
        local_raw_data_path = _get_local_raw_data_path()
        if local_raw_data_path is not None:
            logging.info("Falling back to local raw data after SQL connection failed")
            return pd.read_csv(local_raw_data_path)
        raise CustomException(ex, sys)
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)