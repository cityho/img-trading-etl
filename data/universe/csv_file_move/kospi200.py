from data.universe.csv_file_move.generator import run

if __name__ == '__main__':
    setting = dict(
        scenario="/locdisk/data/hoseung2/universe/kospi200_constituent.csv",
    )
    run(setting)
