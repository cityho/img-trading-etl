from datetime import datetime
from pathlib import Path
import numpy as np
import h5py
import time
import tensorflow as tf
import pandas as pd
from itertools import product
from utils.log import LOGGER
import gc

from concurrent.futures import ThreadPoolExecutor


from data.scenario.common.test_data import get_basic_model, y_label_convertor

def to_tensor(x: pd.DataFrame, y):
    print("test")
    # 2시간만 자고 일어나서 보자...
    x.values
    y_label_convertor([y], 3)
    y
    pass

def run(setting):
    scenario = pd.read_csv(setting["scenario"]).set_index("Unnamed: 0")
    scenario.index = pd.to_datetime(scenario.index)
    all_df = []
    for csv_f in Path(setting["universe"]).rglob("*.csv"):
        d = csv_f.name.replace(".csv", "").split("_")[-1]
        d = datetime.strptime(d, "%Y%m%d")

        tmp_data = pd.read_csv(csv_f).set_index("date")
        tmp_data.index = pd.to_datetime(tmp_data.index)
        stocks = tmp_data.stock_code.unique()
        print("test")
        for s, tmp in tmp_data.groupby("stock_code"):
            tmp_ = tmp[['Close', 'Open', 'Low', 'High', "Volume"]]
            # tmp_l = int(scenario.at[d, s])
            all_df.append(tmp)


            # 그러니까 챗gpt 코드를 바탕으로, min, max를 기반으로 정규화하고,dataset = tf.data.Dataset.from_tensor_slices((data_normalized, labels)) 하면 된다는듯?

    model = get_basic_model()
    model.fit(numeric_features, target, epochs=15, batch_size=BATCH_SIZE)


if __name__ == '__main__':
    setting = dict(
        scenario="/locdisk/data/hoseung2/scenario/jongga_tomorrow_trenary.csv",
        universe="/locdisk/data/hoseung2/universe/kospi200_constituent/csv",
        label=[0, 1, 2]
    )
    run(setting)


    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     for i in tqdm(range(len(PNGS)), desc="파일 이동 진행 중"):
    #         executor.submit(files_cp_to_folder, PNGS[i])