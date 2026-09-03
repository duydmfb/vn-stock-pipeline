from vnstock import Quote
from datetime import datetime
from pathlib import Path


SYMBOL = 'VNM'
SOURCE = 'kbs'
START_DATE = '2026-01-01'
END_DATE = datetime.now().strftime("%Y-%m-%d") #Ngày cuối lấy dữ liệu
RAW_DIR = Path("data/raw")
RUN_DATE = datetime.now().strftime("%Y-%m-%d") #Ngày chạy 

def get_data():

    q = Quote(symbol=SYMBOL, source=SOURCE)
    df = q.history(start=START_DATE, end=END_DATE, interval='1D')

    return df


def save_raw(df, symbol):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ten = f'{RUN_DATE}_{symbol}.parquet'
    duong_dan = RAW_DIR/ten
    df.to_parquet(duong_dan, index=False)

    return duong_dan

if __name__ == "__main__":
    price_df = get_data()    
    print(price_df.shape)
    print(price_df.columns.tolist())
    print(price_df.head())
    print(price_df.tail(10))
    print(price_df["time"].min(), price_df["time"].max())
    raw = save_raw(price_df, SYMBOL)
    print(f'Du lieu raw đa luu trong {raw}, voi {len(price_df)} dong')

