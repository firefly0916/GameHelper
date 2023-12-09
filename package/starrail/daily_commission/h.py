import time

from he_cheng_yi_ci_cai_liao import HeChengYiCiCaiLiao
from go_assignment import GoAssignment
from he_cheng_yi_ci_xiao_hao_pin import HeChengYiCiXiaoHaoPin


class DailyCommission(object):
    def __init__(self):
        pass

    @staticmethod
    def he_cheng_yi_ci_cai_liao():
        commission = HeChengYiCiCaiLiao()
        commission.run()

    @staticmethod
    def he_cheng_yi_ci_xiao_hao_pin():
        commission = HeChengYiCiXiaoHaoPin()
        commission.run()

    @staticmethod
    def go_assignment():
        commission = GoAssignment()
        commission.run()


if __name__ == "__main__":
    dailyCommission = DailyCommission()
    time.sleep(1)
    dailyCommission.he_cheng_yi_ci_xiao_hao_pin()
