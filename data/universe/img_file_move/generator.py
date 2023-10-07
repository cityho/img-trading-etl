"""
당일의 True, False 를 기반으로 이미지를 이동하는 경우 해당 코드를 임포트 하여 사용한다.
"""


import os

import traceback
import shutil
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor
from data.universe.config import RESULT_PATH

# ImageDataGenerator 에 들어갈 파일들을 폴더 구조 별로 mv 하는 코드

BASE_IMG_PATH = Path("/locdisk/data/hoseung2/img/img_w_ma")
PNGS = list(BASE_IMG_PATH.rglob('*.png'))
sceanrio, folder_name, sceanrio_idx = None, None, None


def files_cp_to_folder(f):
    tmp_col = f.name.replace(".png", "")
    tmp_idx_no_dash = f.parent.name
    tmp_idx_dash = f"{tmp_idx_no_dash[:4]}-{tmp_idx_no_dash[4:6]}-{tmp_idx_no_dash[6:]}"
    try:
        sceanrio.at[tmp_idx_dash, tmp_col]
    except KeyError:
        return  # 여기 없어용~

    dest = sceanrio.at[tmp_idx_dash, tmp_col]

    if dest:
        try:
            shutil.copy(f, folder_name + f"/{tmp_idx_no_dash}_{tmp_col}.png")
        except:
            print("Error", f, dest)
            print(traceback.format_exc())
            return


def run(setting):
    global sceanrio
    sceanrio = pd.read_csv(
        setting["scenario"]
    ).set_index("FILE DATE", drop=True)
    sceanrio = sceanrio.isna()

    global folder_name
    folder_name = setting["scenario"].replace(".csv", "").replace("/home/hoseung2/", RESULT_PATH) +"/img"
    os.makedirs(folder_name, exist_ok=True)

    # for i in tqdm(range(len(PNGS)), desc="파일 이동 진행 중"):
    #     files_cp_to_folder(PNGS[i])

    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in tqdm(range(len(PNGS)), desc="파일 이동 진행 중"):
            executor.submit(files_cp_to_folder, PNGS[i])

