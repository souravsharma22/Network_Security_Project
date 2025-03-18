import os
import sys
import mlflow
from mlflow.sklearn import log_model
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.entity.artifact_entity import ClassificationMetricArtifact, ModelTrainerArtifact, DataTransformationArtifact
from NetworkSecurity.entity.config_entity import ModelTrainerConfig

from NetworkSecurity.utils.main_utils.utils import  save_object,load_object,load_numpy_array_data, evaluate_model
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

import dagshub
dagshub.init(repo_owner='souravbgp2210', repo_name='Network_Security_Project', mlflow=True)



class ModelTraier:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("MOdel Trainer is called")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model, classificationmetric):
        try:
            with mlflow.start_run():
                f1score = classificationmetric.f1_score
                precision_score = classificationmetric.precision_score
                recall_score = classificationmetric.recall_score

                mlflow.log_metric("f1_score",f1score)
                mlflow.log_metric("recall_score",recall_score)
                mlflow.log_metric("precision_score",precision_score)

                mlflow.sklearn.log_model(best_model,"model")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def train_model(self, x_train,y_train,x_test,y_test):
        try:
            logging.info("Model Training started")
            models = {
                "Random Forest":RandomForestClassifier(verbose=1)
                , "Decision Tree": DecisionTreeClassifier(),
               ## "Kneighbour":KNeighborsClassifier(),
                "Gradient Boosting":GradientBoostingClassifier(verbose=1),
                "AdaBoost":AdaBoostClassifier(),
                "Logistic Regression":LogisticRegression(verbose=1)
            }

            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.05,.001],
                'subsample':[0.6,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            }
            model_report:dict = evaluate_model(x_train,y_train,x_test,y_test,models,params)

            best_model_score = max(sorted(model_report.values()))

            best_model_name  = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]
            y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)

            classification_train_metric= get_classification_score(y_true=y_train,y_pred=y_train_pred)
            classification_test_metric= get_classification_score(y_true=y_test,y_pred=y_test_pred)
            
            #TRacking the experiment mlflow
            self.track_mlflow(best_model=best_model,classificationmetric=classification_train_metric)
            self.track_mlflow(best_model=best_model,classificationmetric=classification_test_metric)


            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            Network_model = NetworkModel(preprocessor,best_model)
            save_object(self.model_trainer_config.trained_model_file_path,obj=Network_model)

            #saving bes model
            save_object("final_models/model.pkl",best_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            logging.info(f"Model Trainer Artifact {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info("Loading training and test array")
            train_arr= load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            logging.info("Creating xtrain and xtest ")
            x_train, y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact = self.train_model(x_train=x_train,x_test=x_test,y_train=y_train,y_test=y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)