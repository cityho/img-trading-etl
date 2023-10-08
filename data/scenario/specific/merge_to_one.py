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

adj_factor = pd.read_csv("/home/hoseung2/adj_factor.csv").set_index("Unnamed: 0")
adj_factor.index = pd.to_datetime(adj_factor.index)


def run(setting):
    all_df = []
    for csv_f in Path(setting["universe"]).rglob("*.csv"):
        d = csv_f.name.replace(".csv", "").split("_")[-1]
        d = datetime.strptime(d, "%Y%m%d")

        tmp_data = pd.read_csv(csv_f).set_index("date")
        if tmp_data.empty:
            continue
        tmp_data.index = pd.to_datetime(tmp_data.index)
        s = tmp_data.stock_code.unique()[0]

        try:
            tmp_data = tmp_data[['Close', 'Open', 'Low', 'High', "Volume"]]
        except KeyError:
            continue
        tmp_data["Adj Close"] = tmp_data["Close"] * adj_factor.at[d, s]
        all_df.append(tmp_data)
    print(f"/locdisk/data/hoseung2/universe/specific/{s}.csv")
    pd.concat(all_df).to_csv(f"/locdisk/data/hoseung2/universe/specific/{s}.csv")


if __name__ == '__main__':
    setting = dict(
        universe="/locdisk/data/hoseung2/universe/specific/csv",
        label=[0, 1, 2]
    )
    run(setting)