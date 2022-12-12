import pandas as pd
import datetime


def to_season(month_num: int) -> str:
    """月を季節に変換する。

    Args:
        month_num (int): 月

    Returns:
        str: 季節名
    """
    match month_num:
        case 3 | 4 | 5:
            return 'spring'
        case 6 | 7 | 8:
            return 'summer'
        case 9 | 10 | 11:
            return 'autumn'
        case 12 | 1 | 2:
            return 'winter'
        case x:
            raise Exception(f'{x} is a illegal month.')


def main():
    # データ読み込み
    reserve_df = pd.read_csv('input/reserve.csv')
    # datetime型に変換
    reserve_df['reserve_datetime'] = pd.to_datetime(reserve_df['reserve_datetime'],
                                                    format='%Y-%m-%d %H:%M:%S')
    reserve_df['checkin_datetime'] = pd.to_datetime(reserve_df['checkin_date']+reserve_df['checkin_time'],
                                                    format='%Y-%m-%d%H:%M:%S')
    # 日付情報取得
    reserve_df['reserve_date'] = reserve_df['reserve_datetime'].dt.date
    reserve_df['checkin_date'] = reserve_df['checkin_datetime'].dt.date

    # 日時の抽出
    dt_column_list = ['reserve_datetime', 'reserve_date', 'month', 'day_in_month', 'weekdays',
                      'hour', 'minute', 'second', 'format_str']
    reserve_df['month'] = reserve_df['reserve_datetime'].dt.month
    reserve_df['day_in_month'] = reserve_df['reserve_datetime'].dt.day
    reserve_df['weekdays'] = reserve_df['reserve_datetime'].dt.dayofweek
    reserve_df['hour'] = reserve_df['reserve_datetime'].dt.hour
    reserve_df['minute'] = reserve_df['reserve_datetime'].dt.minute
    reserve_df['second'] = reserve_df['reserve_datetime'].dt.second
    reserve_df['format_str'] = reserve_df['reserve_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 差分変換
    dt_column_list = ['reserve_datetime', 'checkin_datetime', 'diff_year', 'diff_month', 'diff_day', 'diff_hour',
                      'diff_min', 'diff_sec']
    r_dt = reserve_df['reserve_datetime']
    c_dt = reserve_df['checkin_datetime']
    reserve_df['diff_year'] = r_dt.dt.year - c_dt.dt.year
    reserve_df['diff_month'] = (r_dt.dt.year * 12 + r_dt.dt.month) - \
                               (c_dt.dt.year * 12 + c_dt.dt.month)
    reserve_df['diff_day'] = (r_dt - c_dt).astype('timedelta64[D]')
    reserve_df['diff_hour'] = (r_dt - c_dt).astype('timedelta64[h]')
    reserve_df['diff_min'] = (r_dt - c_dt).astype('timedelta64[m]')
    reserve_df['diff_sec'] = (r_dt - c_dt).astype('timedelta64[s]')

    # 日時増減
    dt_column_list = ['reserve_datetime', 'add_day', 'add_hour', 'add_min', 'add_sec']
    reserve_df['add_day'] = r_dt + datetime.timedelta(days=1)
    reserve_df['add_hour'] = r_dt + datetime.timedelta(hours=1)
    reserve_df['add_min'] = r_dt + datetime.timedelta(minutes=1)
    reserve_df['add_sec'] = r_dt + datetime.timedelta(seconds=1)

    # 季節への変換
    dt_column_list = ['reserve_datetime', 'season']
    reserve_df['season'] = r_dt.dt.month.apply(to_season)

    # 平日・休日への変換
    dt_column_list = ['checkin_datetime', 'holidayday_flg', 'nextday_is_holiday_flg']
    holiday_df = pd.read_csv('input/holiday_mst.csv')
    holiday_df['target_day'] = pd.to_datetime(holiday_df['target_day']).dt.date
    reserve_df = pd.merge(reserve_df, holiday_df, left_on='checkin_date', right_on='target_day')
    print(reserve_df[dt_column_list])


if __name__ == "__main__":
    main()
