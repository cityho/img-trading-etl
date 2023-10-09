if __name__ == '__main__':
    from data.scenario.t_1_t_jongga_ternary.img.move_file import run
    setting = dict(
        scenario="/locdisk/data/hoseung2/scenario/jongga_tomorrow_trenary.csv",
        universe="/locdisk/data/hoseung2/universe/kosdaq150_constituent/img",
        label=[0, 1, 2]
    )
    run(setting)