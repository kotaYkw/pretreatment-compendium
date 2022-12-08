import numpy as np
import pandas as pd
from pyproj import Transformer

def convert_to_continuous(x: float) -> float:
    x_min = (x * 100 - int(x * 100) * 100)
    x_sec = (x - int(x) - x_min / 10000) * 100
    return int(x) + x_sec / 60 + x_min / 60 / 60

def main():
    df = pd.read_csv('input/customer.csv')
    print('=== row ===')
    print(df.head())
    df['home_latitude'] = df['home_latitude'].apply(lambda x: convert_to_continuous(x))
    df['home_longitude'] = df['home_longitude'].apply(lambda x: convert_to_continuous(x))
    print('=== convert_to_continuous ===')
    print(df.head())
    # 日本測地系を世界測地系に変換
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    home_position = df[['home_latitude', 'home_longitude']]\
        .apply(lambda x: transformer.transform(x[0], x[1]), axis=1)
    df['home_latitude'] = [x[0] for x in home_position]
    df['home_longitude'] = [x[1] for x in home_position]
    print('=== pyproj.Proj ===')
    print(df.head())

if __name__ == "__main__":
    main()
