
import pandas as pd
import os



def load_orders(engine):
    query = "SELECT * FROM orders_clean"
    df = pd.read_sql(query,engine)
    return df

def load_ads(engine):
    query = "SELECT * FROM ad_campaigns_clean"
    ad_df = pd.read_sql(query,engine)
    return ad_df

def load_country_metrics(engine):
    query = "SELECT * FROM country_metrics"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        metrics_df = pd.read_sql(query,engine)
        return metrics_df

    except Exception as e:
        fallback = os.path.join(BASE_DIR, "outputs", "country_metrics.csv")
        return pd.read_csv(fallback)
