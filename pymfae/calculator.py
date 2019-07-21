import pandas as pd
import datetime as dt
import numpy as np

def get_mae(order_type: str, 
            entry_time: dt.datetime or int, exit_time: dt.datetime or int, \
            price_data: pd.DataFrame or pd.Series or np.array or list):
    '''
    parameters:
        order_type: str, 做多或做空 ('long' 或 'short')
        entry_time: dt.datetime 或 int, 進場時間 (若有OHLC資料，則視為open進場)
        exit_time: dt.datetime 或 int, 出場時間 (若有OHLC資料，則視為close出場)
        price_data: pd.DataFrame 或 pd.Series, 以datetime為index的價格資料
                    np.array 或 list, 以陣列紀錄的價格資料
                    (DataFrame為OHLC資料；Series、Array或List則為Tick或Close資料)

    return:
        mae: float, 交易期間最大回徹
        mae_time: dt.datetime 或 int, MAE發生時間
    '''
    mae = 0.0
    mae_time = None
    
    if type(price_data) == pd.DataFrame:
        data = price_data.loc[entry_time : exit_time]
        entry_price = data['open'].loc[entry_time]
        for index, values in data.iterrows():
            if order_type == 'long':
                drawdown = values['low'] - entry_price
            elif order_type == 'short':
                drawdown = entry_price - values['high']
            if mae > drawdown:
                mae = drawdown
                mae_time = index

    elif type(price_data) == pd.Series:
        data = price_data.loc[entry_time : exit_time]
        entry_price = data.loc[entry_time]
        for index, values in enumerate(data):
            if order_type == 'long':
                drawdown = values - entry_price
            elif order_type == 'short':
                drawdown = entry_price - values
            if mae > drawdown:
                mae = drawdown
                mae_time = index

    elif type(price_data) == np.array or type(price_data) == list:
        entry_price = price_data[entry_time]
        for index, values in enumerate(price_data[entry_time : exit_time+1]):
            if order_type == 'long':
                drawdown = values - entry_price
            elif order_type == 'short':
                drawdown = entry_price - values
            if mae > drawdown:
                mae = drawdown
                mae_time = entry_time + index

    return mae, mae_time


def get_mfe(order_type: str, 
            entry_time: dt.datetime or int, exit_time: dt.datetime or int, \
            price_data: pd.DataFrame or pd.Series or np.array or list):
    '''
    parameters:
        order_type: str, 做多或做空 ('long' 或 'short')
        entry_time: dt.datetime 或 int, 進場時間 (若有OHLC資料，則視為open進場)
        exit_time: dt.datetime 或 int, 出場時間 (若有OHLC資料，則視為close出場)
        price_data: pd.DataFrame 或 pd.Series, 以datetime為index的價格資料
                    np.array 或 list, 以陣列紀錄的價格資料
                    (DataFrame為OHLC資料；Series、Array或List則為Tick或Close資料)

    return:
        mfe: float, 交易期間最大回徹
        mfe_time: dt.datetime 或 int, MAE發生時間
    '''
    mfe = 0.0
    mfe_time = None
    
    if type(price_data) == pd.DataFrame:
        data = price_data.loc[entry_time : exit_time]
        entry_price = data['open'].loc[entry_time]
        for index, values in data.iterrows():
            if order_type == 'long':
                profit = values['high'] - entry_price
            elif order_type == 'short':
                profit = entry_price - values['low']
            if mfe < profit:
                mfe = profit
                mfe_time = index

    elif type(price_data) == pd.Series:
        data = price_data.loc[entry_time : exit_time]
        entry_price = data.loc[entry_time]
        for index, values in enumerate(data):
            if order_type == 'long':
                profit = values - entry_price
            elif order_type == 'short':
                profit = entry_price - values
            if mfe < profit:
                mfe = profit
                mfe_time = index

    elif type(price_data) == np.array or type(price_data) == list:
        entry_price = price_data[entry_time]
        for index, values in enumerate(price_data[entry_time : exit_time+1]):
            if order_type == 'long':
                profit = values - entry_price
            elif order_type == 'short':
                profit = entry_price - values
            if mfe < profit:
                mfe = profit
                mfe_time = entry_time + index

    return mfe, mfe_time


def mae_mfe_pair(order: list, 
                price_data: pd.DataFrame or pd.Series or np.array or list, \
                mae_first: bool=True):
    '''
    parameters:
        order: list, 所有交易紀錄，交易紀錄為dict
                交易紀錄格式:
                {
                    'order_type': str,
                    'entry_time': dt.datetime 或 int,
                    'exit_time': dt.datetime 或 int
                }
        price_data: pd.DataFrame 或 pd.Series, 以datetime為index的價格資料
                    np.array 或 list, 以陣列紀錄的價格資料
                    (DataFrame為OHLC資料；Series、Array或List則為Tick或Close資料)
        mae_first: bool (預設為True), MFE是否出現在MAE之前

    return:
        results: list, 所有交易紀錄結果，交易紀錄結果為dict
                交易紀錄結果格式:
                {
                    'mae': float,
                    'mfe': float,
                    'mae_time': dt.datetime 或 int,
                    'mfe_time': dt.datetime 或 int
                }
    '''
    results = []
    for this_order in order:
        mae, mae_time = get_mae(this_order['order_type'], \
                                this_order['entry_time'], \
                                this_order['exit_time'], \
                                price_data)
        
        if mae_first:
            mfe, mfe_time = get_mfe(this_order['order_type'], \
                                    this_order['entry_time'], \
                                    mae_time, \
                                    price_data)
        else:
            mfe, mfe_time = get_mfe(this_order['order_type'], \
                                    this_order['entry_time'], \
                                    this_order['exit_time'], \
                                    price_data)
        
        results.append({
            'mae': mae, 'mfe': mfe, \
            'mae_time': mae_time, 'mfe_time': mfe_time
        })

    return results


                            