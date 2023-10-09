def is_gics(g, x):
    if "," in g:
        return any([str(x).startswith(a) for a in g.split(",")])
    return str(x).startswith(g)


# gics = pd.read_csv("/home/hoseung2/gics_krx.csv").set_index("Unnamed: 0")
# gics.index = pd.to_datetime(gics.index)
# for g in IDX_CODE_NAME.keys():
#     univ = gics.applymap(lambda x: is_gics(g, x))
#     univ.to_csv(f"/locdisk/data/hoseung2/universe/gics_{g}.csv")

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
            print(folder_name + f"/{tmp_idx_no_dash}_{tmp_col}.png")
        except:
            print("Error", f, dest)
            print(traceback.format_exc())
            return


def run(setting):
    global sceanrio
    sceanrio = pd.read_csv(
        setting["scenario"]
    )
    try:
        sceanrio.set_index("FILE DATE", drop=True, inplace=True)
    except KeyError:
        sceanrio.set_index("Unnamed: 0", drop=True, inplace=True)

    global folder_name
    folder_name = setting["scenario"].replace(".csv", "").replace("/home/hoseung2/", RESULT_PATH) +"/img"
    os.makedirs(folder_name, exist_ok=True)

    for idx in sceanrio.index:
        break
        d_tmp = sceanrio.loc[idx]
        trues = d_tmp[d_tmp==True]
        if trues.empty:
            continue

    for i in tqdm(range(len(PNGS)), desc="파일 이동 진행 중 for 루프"):
        files_cp_to_folder(PNGS[i])


if __name__ == '__main__':
    IDX_CODE_NAME = {
        "4520": "Technology Hardware & Equipment",
        "4530": "Semiconductors & Semiconductor Equipment",
        "1510": "Materials",
        "5020": "Media & Entertainment",
        "2510": "Automobiles & Components",
        "4010": "Banks",
        "3520": "Pharmaceuticals, Biotechnology & Life Sciences",
        "2010": "Capital Goods",
        "2520": "Consumer Durables & Apparel",
        "3020": "Food, Beverage & Tobacco",
        "1010": "Energy",
        "5010": "Telecommunication Services",
        "3030": "Household & Personal Products",
        "4030": "Insurance",
        "5510": "Utilities",
        "2030": "Transportation",
        "4510": "Software & Services",
        "2530": "Consumer Services",
        "2550": "Retailing",
        "4020": "Diversified Financials",
        "3010": "Food & Staples Retailing",
        "2020": "Commercial & Professional Services",
        "3510": "Health Care Equipment & Services",
        "6010,6020": "Real Estate",
    }

    for g in IDX_CODE_NAME.keys():
        print(g)
        setting = dict(
            scenario=f"/locdisk/data/hoseung2/universe/gics_{g}.csv",
        )
        run(setting)
        print("*"*50)
