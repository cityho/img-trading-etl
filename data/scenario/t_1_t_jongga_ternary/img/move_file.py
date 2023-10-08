# ImageDataGenerator 에 들어갈 파일들을 폴더 구조 별로 mv 하는 코드

import os
import shutil
import random
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from data.scenario.config import RESULT_PATH

BASE_IMG_PATH = None
PNGS = None
sceanrio = None
folders = dict()
sceanrio_idx = None
data_count = 0
total_data = 0


def files_cp_to_folder(f):
    global data_count
    global sceanrio_idx

    tmp_idx_no_dash, tmp_col = f.name.replace(".png", "").split("_")
    tmp_idx_dash = f"{tmp_idx_no_dash[:4]}-{tmp_idx_no_dash[4:6]}-{tmp_idx_no_dash[6:]}"
    i = sceanrio_idx.index(tmp_idx_dash) - 1
    bef_tmp_idx_dash = sceanrio_idx[i]
    bef_tmp_idx_no_dash = bef_tmp_idx_dash.replace("-", "")

    if i < 0:  # 전일의 데이터가 아니므로 학습대상 아님
        return

    try:
        dest = int(sceanrio.at[bef_tmp_idx_dash, tmp_col])
    except KeyError:
        return
    try:
        if data_count > 0.8*total_data:
            print("start test")
            shutil.copy(
                str(f).replace(tmp_idx_no_dash, bef_tmp_idx_no_dash),
                folders[f"test_{dest}"] + f"/{bef_tmp_idx_no_dash}_{tmp_col}.png"
            )
        else:
            shutil.copy(
                str(f).replace(tmp_idx_no_dash, bef_tmp_idx_no_dash),
                folders[f"train_{dest}"] + f"/{bef_tmp_idx_no_dash}_{tmp_col}.png"
            )
            data_count += 1
    except:
        print("Error", f, dest)
        import traceback
        print(traceback.format_exc())
        return


def run(setting):
    global BASE_IMG_PATH
    global PNGS
    global total_data
    global sceanrio
    global sceanrio_idx

    BASE_IMG_PATH = Path(setting["universe"])
    PNGS = list(BASE_IMG_PATH.rglob('*.png'))
    random.shuffle(PNGS)
    total_data = len(PNGS)
    sceanrio = pd.read_csv(setting["scenario"]).set_index("Unnamed: 0", drop=True)
    sceanrio_idx = sceanrio.index.tolist()

    scen_name = setting["scenario"].replace(".csv", "").split("/")[-1]
    univ_name = setting["universe"].split("/")[-2]
    folder_name = RESULT_PATH+scen_name+"_"+univ_name
    os.makedirs(folder_name, exist_ok=True)

    global folders
    folders.update({f"train_{l}": f"{folder_name}/img/train/{l}" for l in setting["label"]})
    folders.update({f"test_{l}": f"{folder_name}/img/test/{l}" for l in setting["label"]})

    for l in folders.values():
        os.makedirs(l, exist_ok=True)
        print(l)

    # for i in tqdm(range(len(PNGS)), desc="파일 이동 진행 중"):
    #     files_cp_to_folder(PNGS[i])

    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in tqdm(range(len(PNGS)), desc="파일 이동 진행 중"):
            executor.submit(files_cp_to_folder, PNGS[i])


if __name__ == '__main__':
    setting = dict(
        scenario="/locdisk/data/hoseung2/scenario/jongga_tomorrow_trenary.csv",
        universe="/locdisk/data/hoseung2/universe/kospi200_constituent/img",
        label=[0, 1, 2]
    )
    run(setting)
