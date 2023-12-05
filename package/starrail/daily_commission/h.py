import time

from he_cheng_yi_ci_cai_liao import HeChengYiCiCaiLiao
from go_assignment import GoAssignment


class DailyCommission(object):
    def __init__(self):
        pass

    @staticmethod
    def he_cheng_yi_ci_cai_liao():
        commission = HeChengYiCiCaiLiao()
        commission.run()

    @staticmethod
    def go_assignment():
        commission = GoAssignment()
        commission.run()


if __name__ == "__main__":
    dailyCommission = DailyCommission()
    time.sleep(1)
    dailyCommission.go_assignment()
