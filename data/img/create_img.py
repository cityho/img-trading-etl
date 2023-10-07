import pandas as pd
import mplfinance as mpf
from mplfinance import _styles
import pandas as pd
import os
from PIL import Image
import numpy as np
import glob

from data.img.config import NUM_DATA_PATH
from utils.args import parse_args
from utils.log import LOGGER
from utils.data import get_files_of, get_all_dates, img_upload_to_s3
from data.img.config import NUM_DATA_PATH, IMG_DATA_PATH
from concurrent.futures import ThreadPoolExecutor


daily_df = None


"""
현재는 ma만 지원합니다~
"""

def load_num_data(market, d: int):
    assert market in ["kospi", "kosdaq"], "marekt 오타 같은데용?"
    f_path = NUM_DATA_PATH.format(market=market, d=d)
    df = pd.read_csv(f_path)
    df = df[
        [c for c in df.columns if not c.startswith('Unnamed')]
    ]
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    start_time = pd.to_datetime('09:00:00').time()
    end_time = pd.to_datetime('15:30:00').time()
    df = df.between_time(start_time, end_time, include_start=True, include_end=True)
    df.reset_index(inplace=True)
    df.set_index(["stock_code", "date"], inplace=True)
    return df


def data_to_img(
    tmp, stock_code=None, for_threding=False, market=None, d=None
):
    if for_threding:
        global daily_df
        tmp = daily_df.loc[stock_code]

    folder = IMG_DATA_PATH.format(market=market, d=d)
    if not os.path.exists(folder):
        os.makedirs(folder)

    f_name = folder+f"/{stock_code}.png"
    if os.path.exists(f_name):
        return
    print(f_name)
    mpf.plot(
        tmp,
        type='candle',
        mav=(15, 60),
        volume=True,
        scale_padding={'left': 0, 'top': 0, 'right': 0, 'bottom': 0},
        style='yahoo',
        savefig=dict(
            fname=f_name,
        ),
        figsize=(4, 2),
        axisoff=True,  # 사이즈 및 여백 조절
    )

    s3_path = f"img_w_ma/{market}/{d}/{stock_code}.png"
    img_upload_to_s3(folder+f"{d}_{stock_code}.png", s3_path)


def run(args):
    for m in args.market:
        LOGGER.info(f"START {m.upper()}")
        dates = get_all_dates(m)
        dates = [d for d in dates if int(args.start) < int(d) < int(args.end)]
        for d in dates:
            LOGGER.info(f"IMG_PROCESSING_START {d.upper()}")
            global daily_df
            daily_df = load_num_data(m, d)
            stocks = daily_df.index.get_level_values(0).unique()

            if args.thread:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    for stock_code in stocks:
                        executor.submit(data_to_img, daily_df, stock_code, True, m, d)
            else:
                for c in stocks:
                    tmp = daily_df.loc[c]
                    data_to_img(
                        tmp, stock_code=c, for_threding=False, market=m, d=d
                    )
            LOGGER.info(f"IMG_PROCESSING_END {d.upper()}")


if __name__ == '__main__':
    args = parse_args()
    run(args)
