import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from src.logger import get_logger
from src.exception import CustomException
from utils.helpers import label_encode
from config.path_config import *

logger=get_logger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.data_path=PROCESSED_DATA_PATH
        self.df=None
        self.label_mapping={}
        
    def load_data(self):
        try:
            logger.info("loading data")
            self.df=pd.read_csv(self.data_path)
            logger.info("data loaded successfully")
        except Exception as e:
            logger.error(f"error while loading data {e}")
            raise CustomException("Error while loading data",sys)     
        
    def feature_construction(self):
        try:
            logger.info("Doing feature construction")
            self.df['Total Delay']=self.df['Departure Delay in Minutes']+self.df['Arrival Delay in Minutes']
            self.df['Delay Ratio']=self.df['Total Delay']/(self.df['Flight Distance']+1)    
            logger.info("Feature construction done successfully")
        except Exception as e:
            logger.error(f"error while Feature construction {e}")
            raise CustomException("Error while Feature construction",sys)         
        
    def bin_age(self):
        try:
            logger.info("Starting binning of age column")
            self.df['Age Group']=pd.cut(self.df['Age'],bins=[0,18,30,50,100],labels=['Child','Youngster','Adult','Senior'])
            logger.info("Binning of age column successfull")  
        except Exception as e:
            logger.error(f"error while Binning of age column {e}")
            raise CustomException("Error while Binning of age column",sys)  
    
    def label_encoding(self):
        try:
            columns_to_encode=['Gender','Customer Type','Type of Travel','Class','satisfaction','Age Group']
            logger.info(f"Performing label encoding on {columns_to_encode}")
            
            self.df,self.label_mapping=label_encode(self.df,columns_to_encode)
            for col,mapping in self.label_mapping.items():
                logger.info(f"mapping for {col} : {mapping}")
            logger.info("label encoding successfull")    
        
        except Exception as e:
            logger.error(f"error while doing label Encoding {e}")
            raise CustomException("Error while doing label Encoding",sys)
        
    def feature_selection(self):
        try:
            logger.info("Starting Feature Selection")
            x=self.df.drop(columns='satisfaction')
            y=self.df['satisfaction'] 
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
            mutual_info=mutual_info_classif(x_train,y_train,discrete_features=True)
            mutual_info_df=pd.DataFrame({
                'Feature': x.columns,
                'Mutual Information':mutual_info
            }).sort_values(by='Mutual Information',ascending=False)
            
            logger.info(f"Matual Information Tabel is : \n{mutual_info_df}")
            top_features=mutual_info_df.head(12)['Feature'].tolist()
            self.df=self.df[top_features+['satisfaction']]
            logger.info(f"Top Features : {top_features}")
            logger.info("Feature selection successfull")
        except Exception as e:
            logger.error(f"error while doing feature selection {e}")
            raise CustomException("Error while doing feature selection",sys)    
        
    def save_data(self):
        try:
            logger.info("saving your data..")
            os.makedirs(ENGINEERED_DIR,exist_ok=True)
            self.df.to_csv(ENGINEERED_DATA_PATH,index=False)
            logger.info(f"Data saved successfully as {ENGINEERED_DATA_PATH}")
        except Exception as e:
            logger.error(f"error while saveing data {e}")
            raise CustomException("Error while saveing data",sys)
    
    def run(self):
        try:
            logger.info("starting the pipeline of data procesing")
            self.load_data()
            self.feature_construction()
            self.bin_age()
            self.label_encoding()
            self.feature_selection()
            self.save_data()
            logger.info("Feature Engineering Pipeline completed successfully")
        except CustomException as e:
            logger.error(f"Error occured in data processing pipeline : {str(e)}") 
         
        finally:
            logger.info("End of FE pipeline")        
            
if __name__=='__main__':
    Feature_Engineer=FeatureEngineer()
    Feature_Engineer.run()        
        
            