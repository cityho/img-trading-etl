import glob
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from utils.args import parse_args
from utils.log import LOGGER
from utils.data import get_files_of, get_all_dates
from data.img.config import NUM_DATA_PATH


def load_num_data(market, d: int):
    assert market in ["kospi", "kosdaq"], "marekt 오타 같은데용?"
    f_path = f"/locdisk/data/hoseung2/{market}/price_data_raw_{d}.csv"
    df = pd.read_csv(f_path)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df = df[
        [c for c in df.columns if not c.startswith('Unnamed')]
    ]

    start_time = pd.to_datetime('09:00:00').time()
    end_time = pd.to_datetime('15:30:00').time()
    df = df.between_time(start_time, end_time, include_start=True, include_end=True)
    df.reset_index(inplace=True)
    df.set_index(["stock_code", "date"], inplace=True)
    return df


def get_files_of(market):
    assert market in ["kospi", "kosdaq"], "marekt 오타 같은데용?"
    f_path = f"/locdisk/data/hoseung2/{market}"
    files = glob.glob(f"{f_path}/*.csv")
    return sorted(files)


# input은 close 로 통일
# todo !! 현지언니가 준 함수 추가해야함
class IndexCalculator:
    @staticmethod
    def calculate_rsi(data, window=14):
        delta = data.diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rs

    @staticmethod
    def calculate_ma15(data):
        return data.rolling(window=15).mean()

    @staticmethod
    def calculate_ma60(data):
        return data.rolling(window=60).mean()


func_dict = {
    "RSI": IndexCalculator.calculate_rsi,
    "MA15": IndexCalculator.calculate_ma15,
    "MA60": IndexCalculator.calculate_ma60
}


def idx_to_file(market, d):
    df = load_num_data(market, d)
    stocks = df.index.get_level_values(0).unique()
    all_stocks_df = []
    for s in stocks:
        tmp = df.loc[s]  # 특정 종목의 하루치 데이터 호출

        for c, func in func_dict.items():
            tmp[c] = func(tmp["Close"])

        tmp.reset_index(inplace=True)
        tmp["stock_code"] = s
        all_stocks_df.append(tmp)
    df = pd.concat(all_stocks_df)
    df.to_csv(
        NUM_DATA_PATH.format(market=market, d=d)
    )


def run(args):
    for m in args.market:
        LOGGER.info(f"START {m.upper()}")
        dates = get_all_dates(m)
        dates = [d for d in dates if int(args.start) < int(d) < int(args.end)]
        if args.thread:
            with ThreadPoolExecutor(max_workers=4) as executor:
                for d in dates:
                    executor.submit(idx_to_file, m, d)
        else:
            for d in dates:
                idx_to_file(m, d)


if __name__ == '__main__':
    args = parse_args()
    run(args)
