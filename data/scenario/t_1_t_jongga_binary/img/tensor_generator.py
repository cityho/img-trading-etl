from data.scenario.common.dataset_maker import run

"""
데이터 시나리오:
- 전일의 분봉 데이터 추이를 바탕으로 다음날짜의 종가를 예측한다
투자 시나리오
- 전일의 분봉 차트를 확인
- 장전시간외매매로 매수 (전일 종가로 매수)
- 장종료 후 매매로 매도 (당일 종가로 매도)
- 매수 혹은 매도 2개로 분류
"""

if __name__ == '__main__':
    setting = {
        "data_dir": "/locdisk/data/hoseung2/scenario/jongga_tomorrow_ma_only_krx/",
        "img_size": (400, 200),
        "file_name": "/locdisk/data/hoseung2/scenario/jongga_tomorrow_ma_only_krx.h5",
        "batch_size": 100,
        "class_num": 2
    }
    run(setting)
