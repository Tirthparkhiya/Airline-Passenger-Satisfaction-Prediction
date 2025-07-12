import pandas as pd
from config.path_config import *
from src.logger import get_logger
from src.exception import CustomException
import sys
 
logger=get_logger(__name__)

class DataProcessor:
    def __init__(self):
        self.train_path=TRAIN_DATA_PATH
        self.processed_data_path=PROCESSED_DATA_PATH
        
    def load_data(self):
        try:
            logger.info("Data Processing Started")
            df=pd.read_csv(self.train_path)
            logger.info(f"Data read successfull Data shape : {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while Loading data")
            raise CustomException("Error while Loading data: ",sys)

    def drop_unnecessary_cols(self,df,columns):
        try:
            logger.info(f"dropping Unnecesary columns : {columns}")
            df=df.drop(columns=columns,axis=1)
            logger.info(f"columns droped successfully shape= {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while dropping columns")
            raise CustomException("Error while dropping columns: ",sys)
        
    def handle_outliers(self,df,columns):
        try:
            logger.info(f"handling outliers columns={columns}") 
            for col in columns:
                Q1=df[col].quantile(0.25)
                Q3=df[col].quantile(0.75)
                IQR=Q3-Q1

                lower_bound=Q1-1.5*IQR
                upper_bound=Q3+1.5*IQR
                df[col]=df[col].clip(lower=lower_bound,upper=upper_bound)
            logger.info(f"Outliers handled successfully : {df.shape}")    
            return df   
        except Exception as e:
            logger.error("Problem while handling outliers ")
            raise CustomException("Error while handling outliers: ",sys)
        
    def handel_null_values(self,df,columns):
        try:
            logger.info(f"handel null values")
            df[columns]=df[columns].fillna(df[columns].median())
            logger.info(f"null values handled successfully : {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while handling null values ")
            raise CustomException("Error while handling null values: ",sys)
    
    def save_data(self,df):
        try:
            os.makedirs(PROCESSED_DIR,exist_ok=True)    
            df.to_csv(self.processed_data_path,index=False)
            logger.info("Processed data saved successfully")
        except Exception as e:
            logger.error("Problem while saving data ")
            raise CustomException("Error while saving data: ",sys)
        
    def run(self):
        try:
            logger.info("starting the pipeline of data procesing")
            df=self.load_data()
            df=self.drop_unnecessary_cols(df,['index','id'])
            cols_to_handel=['Flight Distance','Checkin service','Departure Delay in Minutes','Arrival Delay in Minutes']
            df=self.handle_outliers(df,cols_to_handel)
            df=self.handel_null_values(df,['Arrival Delay in Minutes'])    
            self.save_data(df)
            logger.info("Data Processing Pipeline completed successfully")
        except CustomException as e:
            logger.error(f"Error occured in data processing pipeline : {str(e)}")
                
if __name__=="__main__":
    processor=DataProcessor()
    processor.run()        