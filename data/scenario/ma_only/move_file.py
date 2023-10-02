import os
import shutil
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor

# ImageDataGenerator 에 들어갈 파일들을 폴더 구조 별로 mv 하는 코드

BASE_IMG_PATH = Path("/locdisk/data/hoseung2/img/img_w_ma/")
PNGS = list(BASE_IMG_PATH.rglob('*.png'))
sceanrio, folders, sceanrio_idx = None, None, None


def files_cp_to_folder(f):
    tmp_col = f.name.replace(".png", "")
    tmp_idx_no_dash = f.parent.name
    tmp_idx_dash = f"{tmp_idx_no_dash[:4]}-{tmp_idx_no_dash[4:6]}-{tmp_idx_no_dash[6:]}"

    i = sceanrio_idx.index(tmp_idx_dash) - 1
    tmp_idx_dash = sceanrio_idx[i]
    tmp_idx_no_dash = tmp_idx_dash.replace("-", "")

    if i < 0:  # 전일의 데이터가 아니므로 학습대상 아님
        return

    try:
        dest = sceanrio.at[tmp_idx_dash, tmp_col]
    except KeyError:
        return
    try:
        shutil.copy(f, folders[dest] + f"/{tmp_idx_no_dash}_{tmp_col}.png")
    except:
        print("Error", f, dest)
        import traceback
        print(traceback.format_exc())
        return


def run(setting):
    global sceanrio
    sceanrio = pd.read_csv(
        setting["scenario"]
    ).set_index("Unnamed: 0", drop=True)

    global sceanrio_idx
    sceanrio_idx = sceanrio.index.tolist()

    folder_name = setting["scenario"].replace(".csv", "")
    os.makedirs(folder_name, exist_ok=True)

    global folders
    folders = {l: f"{folder_name}/{l}" for l in setting["label"]}

    for l in folders.values():
        os.makedirs(l, exist_ok=True)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in tqdm(range(len(PNGS)), desc="파일 이동 진행 중"):
            executor.submit(files_cp_to_folder, PNGS[i])


"""
todo : 데이터 생성 속도가 느려서 일단 코스피만 있음!!! (총 14만장)
"""
if __name__ == '__main__':
    setting = dict(
        scenario="/locdisk/data/hoseung2/scenario/jongga_tomorrow_ma_only_krx.csv",
        label=[1, 0],
        validate_from="20191101"
    )
    run(setting)
