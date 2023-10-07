"""
특정 종목만 추출한다.
특정 종목의 전 기간에 대해 합친 하나의 csv 파일을 만든다!
"""

import os

import traceback
import shutil
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor

from data.universe.config import RESULT_PATH
from utils.args import parse_args


BASE_IMG_PATH = Path("/locdisk/data/hoseung2/img/img_w_ma")
TOTAL_DATA = list()

sceanrio, folder_name, sceanrio_idx = None, None, None


# 유니버스 별로 파일을 날짜별로 만드는 과정
def files_cp_to_folder(f, stock):
    tmp_col = f.name.replace(".png", "")
    try:
        shutil.copy(f, folder_name + f"/{f.parent.name}_{tmp_col}.png")
    except:
        print(traceback.format_exc())
        return


def run(stocks):
    global folder_name
    f_name = "_".join(stocks)
    folder_name = RESULT_PATH + f"specific/img/{f_name}"
    os.makedirs(folder_name, exist_ok=True)
    for s in stocks:
        pngs = list(BASE_IMG_PATH.rglob(f'{s}.png'))
        with ThreadPoolExecutor(max_workers=3) as executor:
            for i in tqdm(range(len(pngs)), desc="파일 이동 진행 중"):
                executor.submit(files_cp_to_folder, pngs[i], stocks)
        print(f"{s} 끝~!")


if __name__ == '__main__':
    args = parse_args()
    run(args.stock_code)
