
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    host = os.getenv("DB_HOST","localhost")
    user = os.getenv("DB_USER","root")
    password = os.getenv("DB_PASSWORD","")
    database = os.getenv("DB_NAME","cross_border_ecommerce_db")

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}"
    )
    return engine