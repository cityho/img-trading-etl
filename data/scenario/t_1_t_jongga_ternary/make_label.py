import pandas as pd


def run():
    df = pd.read_csv("/home/hoseung2/price_close.csv").set_index("Unnamed: 0")
    df = df.pct_change()
    tmp = df.copy()
    tmp[df == 0] = 0
    tmp[df > 0] = 2
    tmp[df < 0] = 1
    tmp.to_csv("/locdisk/data/hoseung2/scenario/jongga_tomorrow_trenary.csv")


if __name__ == '__main__':
    run()