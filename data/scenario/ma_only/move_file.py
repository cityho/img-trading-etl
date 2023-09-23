from data.scenario.common.move_file import run


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
