import argparse
from datetime import datetime


def check_settings(settings):
    common = [
        "data_dir", "img_size",
        "file_name", "batch_size",
        "class_num"
    ]
    assert all(
        [
            k in common for k in settings.keys()
        ]
    ),  "'data_dir', 'img_size' is required in settings"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    default_date = datetime.today().date().strftime("%Y%m%d")
    parser.add_argument(
        "--start", default=default_date, type=str
    )
    parser.add_argument(
        "--end", default=default_date, type=str
    )

    parser.add_argument("--market", default=["kosdaq", "kospi"], type=str, nargs="+")
    parser.add_argument("--thread", default=False, action="store_true")

    return parser.parse_args()