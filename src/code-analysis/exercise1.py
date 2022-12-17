import numpy as np
import pandas as pd

def to_age_rank(age: int) -> str:
    """年齢を年代に変換。

    Args:
        age (int): 年齢

    Returns:
        str: 年代
    """
    if 20 <= age < 30:
        return '20代'
    elif 30 <= age < 40:
        return '30代'
    elif 40 <= age < 50:
        return '40代'
    elif 50 <= age < 60:
        return '50代'
    elif 60 <= age:
        return '60以上'
    else:
        raise Exception(f'{age} is a illegal age.')


def main():
    # データ読み込み
    reserve_df = pd.read_csv('input/reserve.csv')
    customer_df = pd.read_csv('input/customer.csv')
    # 年齢を年代へと変換
    customer_df['age_rank'] = customer_df['age'].apply(to_age_rank)
    # 結合
    df = pd.merge(reserve_df, customer_df, how='left')
    print(df.info())

    # 年代×性別で集計
    # 該当人数
    customer_cnt = df.groupby(['age_rank', 'sex']).customer_id.nunique()
    print(customer_cnt)
    # 合計予約回数
    rsv_cnt = df.groupby(['age_rank', 'sex']).count()['reserve_id']
    print(rsv_cnt)
    # 平均予約人数
    people_num_avg = df.groupby(['age_rank', 'sex']).mean()['people_num']
    print(people_num_avg)
    # 平均予約単価
    total_price_avg = df.groupby(['age_rank', 'sex']).apply(lambda x: np.mean(x['total_price'] / x['people_num']))
    print(total_price_avg)


if __name__ == "__main__":
    main()
