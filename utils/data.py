import os
import glob

import boto3

from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

S3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def get_files_of(market, base_path=None):
    assert market in ["kospi", "kosdaq"], "marekt 오타 같은데용?"
    if os.getlogin() == "hoseung2":
        f_path = f"/locdisk/data/hoseung2/price_volume_w_index/{market}" # my wls local path
    else:
        f_path = f"/content/drive/MyDrive/dfmba_img_rl_trading/data/price_volume/{market}" # gdrive

    if base_path:
        f_path = base_path

    files = glob.glob(f"{f_path}/*.csv")
    return sorted(files)


def get_all_dates(market):
    assert market in ["kospi", "kosdaq"], "marekt 오타 같은데용?"
    all_files = [f.split("/")[-1] for f in get_files_of(market)]
    dates = [f.replace("price_data_idx_", "").replace(".csv", "") for f in all_files]
    return sorted(list(set(dates)))


def img_upload_to_s3(img_path, s3_path):
    # s3 upload_file bucket name: dfmba-img-trading, s3_path: img_w_ma/
    S3.upload_file(img_path, 'dfmba-img-trading', s3_path)
    os.remove(img_path)


def file_upload_to_s3(file_path, s3_path):
    S3.upload_file(file_path, 'dfmba-img-trading', s3_path)
