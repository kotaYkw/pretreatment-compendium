import numpy as np
import pandas as pd
import pyproj
from pyproj import Transformer
from geopy.distance import geodesic

def convert_to_continuous(x: float) -> float:
    x_min = (x * 100 - int(x * 100)) * 100
    x_sec = (x - int(x) - x_min / 10000) * 100
    return int(x) + x_sec / 60 + x_min / 60 / 60

def main():
    # データ読み込み
    reserve_df = pd.read_csv('input/reserve.csv')
    hotel_df = pd.read_csv('input/hotel.csv')
    hotel_df['hotel_latitude'] = hotel_df['hotel_latitude'].apply(lambda x: convert_to_continuous(x))
    hotel_df['hotel_longitude'] = hotel_df['hotel_longitude'].apply(lambda x: convert_to_continuous(x))
    customer_df = pd.read_csv('input/customer.csv')
    customer_df['home_latitude'] = customer_df['home_latitude'].apply(lambda x: convert_to_continuous(x))
    customer_df['home_longitude'] = customer_df['home_longitude'].apply(lambda x: convert_to_continuous(x))
    # 日本測地系を世界測地系に変換
    transformer = Transformer.from_crs("epsg:4326", "epsg:4301")
    home_position = customer_df[['home_latitude', 'home_longitude']]\
        .apply(lambda x: transformer.transform(x[0], x[1]), axis=1)
    customer_df['home_latitude'] = [x[0] for x in home_position]
    customer_df['home_longitude'] = [x[1] for x in home_position]
    hotel_position = hotel_df[['hotel_latitude', 'hotel_longitude']]\
        .apply(lambda x: transformer.transform(x[0], x[1]), axis=1)
    hotel_df['hotel_latitude'] = [x[0] for x in hotel_position]
    hotel_df['hotel_longitude'] = [x[1] for x in hotel_position]

    # DataFrameを結合
    reserve_df = pd.merge(reserve_df, customer_df, on='customer_id', how='inner')
    reserve_df = pd.merge(reserve_df, hotel_df, on='hotel_id', how='inner')

    # 家とホテルの緯度経度の情報を取得
    home_and_hotel_points = reserve_df.loc[:, ['home_longitude', 'home_latitude',
                                               'hotel_longitude', 'hotel_latitude']]

    # 距離計算
    home_to_hotel = home_and_hotel_points\
        .apply(lambda x: geodesic((x[1], x[0]), (x[3], x[2])), axis=1)
    print(home_to_hotel)

if __name__ == "__main__":
    main()
