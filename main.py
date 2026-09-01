from vnstock import Quote
from datetime import datetime

SYMBOL = 'VNM'
SOURCE = 'VCI'
START_DATE = '2025-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')

def get_data():

    q = Quote(symbol=SYMBOL, source=SOURCE)
    df = q.history(start=START_DATE, end=END_DATE, interval='1D')
    #df = df[(df["time"] >= START_DATE) & (df["time"] <= END_DATE)]
    
    return df

if __name__ == "__main__":
    test = get_data()    
    print(test.shape)
    print(test.columns.tolist())
    print(test.head())
    print(test["time"].min(), test["time"].max())