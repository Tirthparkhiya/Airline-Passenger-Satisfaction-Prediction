import os
import csv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config.db_config import DB_CONFIG
from src.logger import get_logger
from src.exception import CustomException

logger=get_logger(__name__)

class MongoDbExtractor:
    def __init__(self,db_config):
        self.host=db_config["host"]
        self.port=db_config["port"]
        self.database_name=db_config["database"]
        self.collection_name=db_config["collection_name"]
        self.client=None
        self.database=None
        self.collection=None
        
        logger.info("Your Database configuration has been set up")
        
    def connect(self):
        try:
            self.client=MongoClient(self.host,self.port)
            self.database=self.client[self.database_name]
            self.collection=self.database[self.collection_name]
            logger.info("succesfull connected to the database")
        except PyMongoError as e:
            raise CustomException(f"Error while connecting to the database: {e}")
    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected to the database")       
    
    def extract_to_csv(self,output_folder="./artifacts/raw"):
        try:
            if not self.client:
                self.connect()
                
            data=list(self.collection.find({},{"_id":0}))
            if not data:
                logger.warning("No data found in collection.")
                return
            
            columns=set()
            for doc in data:
                columns.update(doc.keys())
            columns=list(columns)    
            logger.info("Data fetched Succesfully !!")
            
            os.makedirs(output_folder,exist_ok=True)
            csv_file_path=os.path.join(output_folder,"data.csv")
            
            with open(csv_file_path,mode="w",newline="",encoding="utf-8") as file:
                writer=csv.DictWriter(file,fieldnames=columns)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            logger.info(f"Data Succesfully saved to {csv_file_path}")
                
        except PyMongoError as e:
            raise CustomException(f"Error in extracting DB due to SQL : {e}")
        
        except CustomException as ce:
            logger.error(str(ce))
        
        finally:
            self.disconnect()
          
if __name__=='__main__':
    try:
        extractor=MongoDbExtractor(DB_CONFIG)
        extractor.extract_to_csv()
    except CustomException as ce:
        logger.error(str(ce))                                     