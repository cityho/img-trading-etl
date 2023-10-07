"""
특정 종목만 추출한다.
특정 종목의 전 기간에 대해 합친 하나의 csv 파일을 만든다!
"""

import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from data.universe.config import RESULT_PATH
from utils.args import parse_args


FTYPE = ".csv"
BASE_DATA_PATH = Path("/locdisk/data/hoseung2/price_volume_w_index")
CSVS = list(BASE_DATA_PATH.rglob(f'*{FTYPE}'))
TOTAL_DATA = list()

sceanrio, folder_name, sceanrio_idx = None, None, None
a = 0


# 유니버스 별로 파일을 날짜별로 만드는 과정
def store_data(f, stocks):
    global TOTAL_DATA
    global a
    a += 1
    data = pd.read_csv(f, index_col=0).set_index("date")

    tmp = data[
        data.stock_code.isin(stocks)
    ]
    TOTAL_DATA.append(tmp)
    print(f"a: {a}, data: {len(TOTAL_DATA)}")


def run(stocks):
    global folder_name
    folder_name = RESULT_PATH + "specific/csv/"
    os.makedirs(folder_name, exist_ok=True)

    # global 변수를 쓰기 때문에 여기서는 그냥 스레드로 진행 구다사이
    for i in tqdm(range(len(CSVS)), desc="파일 이동 진행 중"):
        store_data(CSVS[i], stocks)


    f_name = "_".join(stocks)
    pd.concat(TOTAL_DATA).to_csv(folder_name + "/" + f_name + FTYPE)


if __name__ == '__main__':
    args = parse_args()
    run(args.stock_code)
