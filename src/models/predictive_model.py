import os
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = "database/ecommerce.db"
QUERY_PATH = os.path.join("src", "queries", "prediction_data.sql")

class DeliveryRatingPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.r2_score = 0.0
        
    def _fetch_training_data(self):
        
        with open(QUERY_PATH, "r", encoding="utf-8") as f:
            sql_script = f.read()
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(sql_script, conn)

    def train(self):
        
        df = self._fetch_training_data()
        
        
        X = df[['delay_days']]
        y = df['satisfaction']
        
      
        self.model.fit(X, y)
        
 
        self.r2_score = self.model.score(X, y)
        return self.r2_score

    def predict_score(self, days_of_delay):
        """Predicts what rating a client will give based on simulated delay days."""
       
        input_data = pd.DataFrame({'delay_days': [days_of_delay]})
        
        prediction = self.model.predict(input_data)
        
    
        return max(1.0, min(5.0, float(prediction[0])))
