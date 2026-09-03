from vnstock import Quote
from datetime import datetime
from pathlib import Path
import time
from tenacity import RetryError

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

SYMBOL = 'VNM'
SOURCE = 'kbs'
START_DATE = '2026-01-01'
END_DATE = datetime.now().strftime("%Y-%m-%d") #Ngày cuối lấy dữ liệu
RUN_DATE = datetime.now().strftime("%Y-%m-%d") #Ngày chạy 
MAX_RETRIES = 4


def get_data():

    q = Quote(symbol=SYMBOL, source=SOURCE)
    df = q.history(start=START_DATE, end=END_DATE, interval='1D')

    return df


def get_data_safe():

    for i in range(MAX_RETRIES):
        try:
            data_raw = get_data()
            if data_raw is None or data_raw.empty:
                print('Khong co du lieu tra ve')
                return None
            return data_raw        

        except ValueError:
            print("Ma sai dinh dang") 
            return None
        
        except RetryError as e:
            loi_goc = e.last_attempt.exception()

            if isinstance(loi_goc, ValueError):
                print("Ma sai dinh dang ( ValueError tu retry cuoi cung )")
                return None
            
            print(f"Lan {i+1} that bai (RetryError): {loi_goc}")
            if i < (MAX_RETRIES - 1):
                time.sleep(2 ** (i + 1))              
            
        except Exception as e:        
            print(f'Lan {i+1} that bai : {e}')
            if i<(MAX_RETRIES-1):                
                time.sleep(2 ** (i+1))
    return None


def save_raw(df, symbol):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ten = f'{RUN_DATE}_{symbol}.parquet'
    duong_dan = RAW_DIR/ten
    df.to_parquet(duong_dan, index=False)

    return duong_dan



if __name__ == "__main__":
    price_df = get_data_safe()
    if price_df is not None and not price_df.empty:
        print(f"Kich thuoc DataFrame: {price_df.shape}")
        print(f"Danh sach cot: {price_df.columns.tolist()}")
        print(price_df.head())
        print(price_df.tail(10))
        if "time" in price_df.columns:
            print(f"Khoang thoi gian: {price_df['time'].min()} -> {price_df['time'].max()}")
        raw = save_raw(price_df, SYMBOL)
        print(f'Du lieu raw da luu trong {raw}, voi {len(price_df)} dong')
    else:
        print("Qua trinh lay du lieu that bai hoac khong co du lieu")


