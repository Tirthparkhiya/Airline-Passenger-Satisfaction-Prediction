from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split

import pandas as pd
from config.path_config import *
from src.exception import CustomException
from src.logger import get_logger
import matplotlib.pyplot as plt
import time
import sys

from torch.utils.tensorboard import SummaryWriter

logger=get_logger(__name__)

class ModelSelection:
    def __init__(self,data_path):
        self.data_path=data_path
        run_id=time.strftime("%Y%m%d-%H%M%S")
        self.writer=SummaryWriter(log_dir=f"tensorboard_logs/run_{run_id}")
        
        self.models={
            'Ada Boost':AdaBoostClassifier(n_estimators=50),
            'Gradient Boosting':GradientBoostingClassifier(n_estimators=50),
            'Logistic Regression':LogisticRegression(),
            'KNNeighbors':KNeighborsClassifier(),
            'GaussianNB':GaussianNB(),
            'Random Forest':RandomForestClassifier(n_estimators=50,n_jobs=-1),
            'Decision tree':DecisionTreeClassifier(),
            'xgboost':xgb.XGBClassifier(eval_metric='mlogloss'),
            'lightgbm':lgb.LGBMClassifier()
        }
        self.result={}
    
    def load_data(self):
        try:
            logger.info("loading CSV file")
            df=pd.read_csv(self.data_path) #100% == df
            df_sample=df.sample(frac=0.25,random_state=42) #25% of the 100%  == df_sample   
            x=df_sample.drop(columns='satisfaction')
            y=df_sample['satisfaction'] 
            logger.info("data loaded and sampled Successfully")                
            return x,y
        except Exception as e:
            raise CustomException("Error while loading data",sys)
        
    def split_data(self,x,y):
        try:
            logger.info("splitting data")
            return train_test_split(x,y,test_size=0.2,random_state=42)
        except Exception as e:
            raise CustomException("Error while spiting data",sys)
    
    def log_confusion_matrix(self,y_true,y_pred,step,model_name):
        cm=confusion_matrix(y_true,y_pred)
        fig,ax=plt.subplots(figsize=(5,5))
        ax.matshow(cm,cmap=plt.cm.Blues,alpha=0.7)
        
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(x=j,y=i,s=cm[i,j],va="center",ha="center")
                
        plt.xlabel("Predicted Labels")
        plt.ylabel("True/Actual Labels")
        plt.title(f"Confusion matrix for {model_name}")
        self.writer.add_figure(f"Confusion_Matrix/{model_name}",fig,global_step=step)
        plt.close(fig)
        
    def train_and_evaluate(self,x_train,x_test,y_train,y_test):
        try:
            logger.info("training and evaluation started")
            for idx,(name,model) in enumerate(self.models.items()):
                model.fit(x_train,y_train)
                y_pred=model.predict(x_test)
                accuracy=accuracy_score(y_test,y_pred)
                precision=precision_score(y_test,y_pred,average="weighted",zero_division=0)
                recall=recall_score(y_test,y_pred,average="weighted",zero_division=0)
                f1=f1_score(y_test,y_pred,average="weighted",zero_division=0)
                confusion=confusion_matrix(y_test,y_pred)
                
                self.result[name]={
                    "accuracy":accuracy,
                    "precision score":precision,
                    'recall score':recall,
                    "f1 score":f1,
                }
                logger.info(f"{name} trained successfully"
                            f"Metrics: Accuracy:{accuracy},Precision Score:{precision},Recall Score:{recall},f1 Score:{f1}")
                self.writer.add_scalar(f"Accuracy/{name}",accuracy,idx)
                self.writer.add_scalar(f"Precision Score/{name}",precision,idx)
                self.writer.add_scalar(f"Recall Score/{name}",recall,idx)
                self.writer.add_scalar(f"f1 Score/{name}",f1,idx)
                
                self.writer.add_text(f"Model Details/{name}",f"Metrics: Name:{name}, Accuracy:{accuracy},Precision Score:{precision},Recall Score:{recall},f1 Score:{f1}")
                self.log_confusion_matrix(y_test,y_pred,idx,name)
            
            self.writer.close()    
        except Exception as e:
            raise CustomException("Error while Training and evalution",sys)   
        
    def run(self):     
        try:
            logger.info("Starting Model selection Pipeline")
            x,y=self.load_data()
            x_train,y_train,x_test,y_test=self.split_data(x,y)
            self.train_and_evaluate(x_train,y_train,x_test,y_test)
            logger.info("Model Selection Pipeline completed successfully")
        except Exception as e:
            logger.error("Error in the Pipeline")
            raise CustomException("Error in Pipeline",sys)
        
               
if __name__=="__main__":
    Model_selection=ModelSelection(ENGINEERED_DATA_PATH)
    Model_selection.run()            
            