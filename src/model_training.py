import os
import pandas as pd
import sys
import joblib
import json
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split,RandomizedSearchCV
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
import lightgbm as lgb
from src.logger import get_logger
from src.exception import CustomException
from config.path_config import *

logger=get_logger(__name__)

class ModelTraining:
    def __init__(self,data_path,params_path,model_save_path,experiment_name="Model_Training_Experiment"):
        self.data_path=data_path
        self.params_path=params_path
        self.model_save_path=model_save_path
        self.experiment_name=experiment_name
        
        self.best_model=None
        self.metrics=None
        
    def load_data(self):
        try:
            logger.info("Data Loading for Model Training")
            data=pd.read_csv(self.data_path)
            logger.info("Data loaded Successfully")
            return data
        except Exception as e:
            raise CustomException("Error while loading data", sys)
        
    def split_data(self,data):
        try:
            logger.info("data spliting started")
            x=data.drop(columns='satisfaction')
            y=data['satisfaction'] 
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
            logger.info("Data spliting done")
            return x_train,x_test,y_train,y_test       
        except Exception as e:
            raise CustomException("Error while spliting data", sys)
    
    def train_model(self,x_train,y_train,params):
        try:
            logger.info("Training model started")
            lgbm=lgb.LGBMClassifier()
            random_search=RandomizedSearchCV(estimator=lgbm,param_distributions=params,cv=3,scoring='accuracy',random_state=42)
            random_search.fit(x_train,y_train)            
            logger.info("Model Training Completed")
            self.best_model=random_search.best_estimator_
            
            return random_search.best_params_
        except Exception as e:
            raise CustomException("Error while training model", sys)
        
    def evaluate_model(self,x_test,y_test):
        try:
            logger.info("model evaluation started")
            y_pred=self.best_model.predict(x_test)    
            self.metrics={
                "accuracy":accuracy_score(y_test,y_pred),
                "precision":precision_score(y_test,y_pred,average="weighted"),
                "recall":recall_score(y_test,y_pred,average="weighted"),
                "f1_score":f1_score(y_test,y_pred,average="weighted"),
                "confusion_matrix":confusion_matrix(y_test,y_pred).tolist()
            }
            logger.info(f"Evaluation metrics : {self.metrics}")
            return self.metrics
        except Exception as e:
            raise CustomException("Error while evaluating model ", sys)
        
    def save_model(self):
        try:
            logger.info("saving model")
            os.makedirs(os.path.dirname(self.model_save_path),exist_ok=True) 
            joblib.dump(self.best_model,self.model_save_path)   
            logger.info("model saved successfully")
        except Exception as e:
            raise CustomException("Error while saving model ", sys)
        
    def run(self):
        try:
            mlflow.set_experiment(self.experiment_name)
            with mlflow.start_run():
                data=self.load_data()
                x_train,x_test,y_train,y_test=self.split_data(data) 
                with open(self.params_path,"r") as f:
                    params=json.load(f)
                
                logger.info(f"Loaded hyperparameters : {params}")
                mlflow.log_params({f"random_{key}":value for key , value in params.items()})
                best_params=self.train_model(x_train,y_train,params)
                logger.info(f"Best hyperparameters are : {best_params}")
                
                mlflow.log_params({f"best_{key}":value for key , value in best_params.items()})
                
                metrics=self.evaluate_model(x_test,y_test)
                
                for metric,value in metrics.items():
                    if metric != "confusion_matrix":
                        mlflow.log_metric(metric,value)
                        
                self.save_model()
                mlflow.sklearn.log_model(self.best_model,name="Model")
                
        except CustomException as ce:
            logger.error(str(ce))
            mlflow.end_run(status='FAILED')
            
            
if __name__ == "__main__":
    Model_Training=ModelTraining(data_path=ENGINEERED_DATA_PATH,
                                 params_path=PARAMS_PATH,
                                 model_save_path=MODEL_SAVE_PATH)
    Model_Training.run()                               