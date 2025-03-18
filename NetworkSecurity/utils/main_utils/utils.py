import yaml
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import os,sys
import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    


def save_numpy_array_data(file_path:str,array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file :
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path:str, obj:object)->None:
    try:
        logging.info("saving the object in main utils")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file:
            pickle.dump(obj,file)
        logging.info("Pickeling has been done")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_object(file_path:str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file :{file_path} does not exist")
        with open(file_path,'rb') as f:
            print(f)
            logging.info("Loading the pickle file")
            return pickle.load(f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as f:
            return np.load(f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report ={}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_true=y_train,y_pred=y_train_pred)
            test_model_score  = r2_score(y_true=y_test,y_pred=y_test_pred)

            report[list(models.keys())[i]] = test_model_score
            return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)