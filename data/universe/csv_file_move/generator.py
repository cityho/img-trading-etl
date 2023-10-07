"""
당일의 True, False 를 기반으로 csv를 concat한다..
"""
from datetime import datetime

import os

import traceback
import shutil
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor
from data.universe.config import RESULT_PATH

# ImageDataGenerator 에 들어갈 파일들을 폴더 구조 별로 mv 하는 코드

FTYPE = ".csv"
BASE_DATA_PATH = Path("/locdisk/data/hoseung2/price_volume_w_index/kospi")
CSVS = list(BASE_DATA_PATH.rglob(f'*{FTYPE}'))

sceanrio, folder_name, sceanrio_idx = None, None, None


# 유니버스 별로 파일을 날짜별로 만드는 과정
def store_data(f):
    DATA_TO_STORE = []
    global folder_name

    data = pd.read_csv(f, index_col=0).set_index("date")

    univ_name = folder_name.split("/")[-2]
    f_name = f.name.replace(FTYPE, "").replace("price_data_idx", univ_name)

    d = datetime.strptime(f_name.split("_")[-1], "%Y%m%d")
    tmp_idx_no_dash = d.strftime("%Y%m%d")
    tmp_idx_dash = d.strftime("%Y-%m-%d")

    # 하루씩이기 때문에 종목코드만으로 groupby 해도 됨
    for s, tmp in data.groupby(["stock_code"]):
        if s not in sceanrio.columns:
            continue

        try:
            dest = sceanrio.at[tmp_idx_dash, s]
        except KeyError:
            continue  # 여기 없어용~

        if dest:
            try:
                DATA_TO_STORE.append(tmp)
            except:
                print("Error", f, dest)
                print(traceback.format_exc())
                continue

    pd.concat(DATA_TO_STORE).to_csv(folder_name + "/" + f_name + FTYPE)


def run(setting):
    global sceanrio
    sceanrio = pd.read_csv(
        setting["scenario"]
    ).set_index("FILE DATE", drop=True)
    sceanrio = sceanrio.isna()

    global folder_name
    folder_name = setting["scenario"].replace(".csv", "").replace("/home/hoseung2/", RESULT_PATH) + "/csv"
    os.makedirs(folder_name, exist_ok=True)

    # for i in tqdm(range(len(CSVS)), desc="파일 이동 진행 중"):
    #     store_data(CSVS[i])

    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in tqdm(range(len(CSVS)), desc="파일 이동 진행 중"):
            executor.submit(store_data, CSVS[i])
