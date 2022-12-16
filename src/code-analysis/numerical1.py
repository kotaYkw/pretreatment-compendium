import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


def main():
    # データ読み込み
    reserve_df = pd.read_csv('input/reserve.csv')
    customer_df = pd.read_csv('input/customer.csv')
    production_df = pd.read_csv('input/production.csv')
    # 対数化
    reserve_df['total_price'] = np.log10(reserve_df['total_price']/1000)
    # カテゴリ化
    customer_df['age_rank'] = (customer_df['age']//10*10).astype('category')
    # 正規化
    ss = StandardScaler()
    reserve_df[['people_num', 'total_price']] = ss.fit_transform(reserve_df[['people_num', 'total_price']])
    # 外れ値除去
    reserve_df = reserve_df[(abs(reserve_df['total_price']-np.mean(reserve_df['total_price']))/
                             np.std(reserve_df['total_price']) <= 3)].reset_index()
    # 主成分分析
    pca = PCA(n_components=2)
    pca_values = pca.fit_transform(production_df[['length', 'thickness']])
    print(f'累積寄与率: {sum(pca.explained_variance_ratio_)}')
    print(f'各次元の寄与率: {sum(pca.explained_variance_ratio_)}')
    # 欠損値の補完
    production_df.replace('None', np.nan, inplace=True)
    production_df['thickness'].fillna(production_df['thickness'].mean(), inplace=True)
    print(production_df['thickness'])
    # PMMによる多重代入
    production_df[['length', 'thickness']] = IterativeImputer().fit_transform(production_df[['length', 'thickness']])


if __name__ == "__main__":
    main()
