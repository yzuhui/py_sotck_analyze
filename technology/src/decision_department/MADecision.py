from pandas import DataFrame
from src.analysis_department.CurveDeterminer import CurveDeterminer

"""
    均线决策
"""


class MADecision(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def decision(self, analysis_days: int, df: DataFrame):
        # 倒序排列5日均价数据
        end = 7 if len(df) >= 7 and analysis_days < 7 else analysis_days
        ma5_list = list(df['5日均价'])[0:end][::-1]
        close_list = list(df['收盘价'])[0:end][::-1]
        size = len(ma5_list)
        # TODO
        '''
            对于短时趋势，5日均线存在延后的问题，因此暂时使用每日收盘价作为判断依据
        '''
        # return CurveDeterminer().curveUnevennessJudgment(ma5_list)
        return CurveDeterminer().curveUnevennessJudgment(close_list)


    # 规则一：（找跃领 这类突然拔地而起的）
    # 条件1：最近5个交易日累计涨幅15%以上，
    # 条件2：五个交易日前的四十五个交易日内最高价和最低价落差20%以内
    def ruleOne(self, df: DataFrame):
        if (len(df) <= 5) :
            return "不符合"
        build_list = list(df['涨跌幅（%）'])[0:5][::1]
        if (len(df) > 50):
            end = 50
        else:
            end = len(df)
        # 五日涨跌幅度
        sum_build = sum(build_list)
        close_list = list(df['收盘价'])[5:end][::1]
        max_num = max(close_list)
        min_num = min(close_list)
        sort = (max_num - min_num)/max_num
        if (sum_build >= 15 and sort <= 0.2):
            return "符合"
        else:
            return "不符合"
    # （找启明，京城这类拉升一个平台后在盘整的）
    # 条件1：最近十个交易日累计涨幅20%以上，
    # 条件2：10个交易日前的四十五个交易日内最高点最低的落差在20%以内
    def ruleTwo(self, df: DataFrame):
        if (len(df) <= 10) :
            return "不符合"
        build_list = list(df['涨跌幅（%）'])[0:10][::1]
        if (len(df) > 55):
            end = 55
        else:
            end = len(df)
        # 五日涨跌幅度
        sum_build = sum(build_list)
        close_list = list(df['收盘价'])[10:end][::1]
        max_num = max(close_list)
        min_num = min(close_list)
        sort = (max_num - min_num) / max_num
        if (sum_build >= 0.2 and sort <= 0.2):
            return "符合"
        else:
            return "不符合"

    # 规则三：（找联创，得润这类回调机会）
    # 条件1：当前价格离8个交易日的前五个交易日内最高价20%以上，
    # 条件2：8个交易日前的三十个交易日内最低价到最高价涨幅40%-80%内的
    def ruleThree(self, df: DataFrame):
        if (len(df) <= 14) :
            return "不符合"
        min8_num = min((df['收盘价'])[0:8][::1])
        max8_num = min((df['收盘价'])[9:14][::1])
        sort8_num = (max8_num - min8_num)/max8_num
        if (len(df) > 38):
            end = 38
        else:
            end = len(df)
        close_list = list(df['收盘价'])[8:end][::1]
        max_num = max(close_list)
        min_num = min(close_list)
        sort = (max_num - min_num) / max_num
        if (sort8_num >= 0.2 and sort >= 0.4 and sort <= 0.8):
            return "符合"
        else:
            return "不符合"


    # 条件1: 20个交易日内涨幅40%，
    # 条件2：当前价格处于5日均价和10日均价内的 or 当前价格处于10日均价和20日均价内的
    def ruleFour(self, df: DataFrame):
        if (len(df) <= 20) :
            return "不符合"
        sort20_num = sum((df['涨跌幅（%）'])[0:20][::1])
        avg5 = (df['5日均价'])[0]
        avg10 = (df['10日均价'])[0]
        avg20 = (df['20日均价'])[0]
        closed_price = (df['收盘价'])[0]
        if (sort20_num >= 40 and ((closed_price >= avg10 and closed_price <= avg5) or (closed_price >= avg20 and closed_price <= avg10))):
            return "符合"
        else:
            return "不符合"

    def ruleFive(self, df: DataFrame):
        if (len(df) <= 5):
            return "不符合"
        build_list = list(df['收盘价'])[0:5][::1]
        if (len(df) > 50):
            end = 50
        else:
            end = len(df)
        # 五日涨跌幅度
        sum_build = (max(build_list) - min(build_list))/ max(build_list)
        close_list = list(df['收盘价'])[5:end][::1]
        max_num = max(close_list)
        min_num = min(close_list)
        sort = (max_num - min_num) / max_num
        if (sum_build >= 0.03 and sum_build <= 0.15 and sort <= 0.15 and build_list[0] > build_list[1]):
            return "符合"
        else:
            return "不符合"