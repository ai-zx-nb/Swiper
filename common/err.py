'''程序错误码'''

OK = 0  # 正常


class LogicError(Exception):
    code = OK
    data = 'OK'

    def __init__(self, data=None):
        cls_name = self.__class__.__name__
        self.data = data or cls_name


def gen_logic_err(name, code):
    '''生成一个 LogicError 的子类 (LogicError 的工厂函数)'''
    err_cls = type(name, (LogicError,), {'code': code})
    return err_cls


VcodeSendErr = gen_logic_err('VcodeSendErr', 1000)      # 验证码发送失败
VcodeErr = gen_logic_err('VcodeErr', 1001)              # 验证码错误
LoginRequired = gen_logic_err('LoginRequired', 1002)    # 需要用户登陆
ProfileErr = gen_logic_err('ProfileErr', 1003)          # 用户资料表单数据错误
SidErr = gen_logic_err('SidErr', 1004)                  # SID 错误
StypeErr = gen_logic_err('StypeErr', 1005)              # 滑动类型错误
SwipeRepeatErr = gen_logic_err('SwipeRepeatErr', 1006)  # 重复滑动
RewindLimitErr = gen_logic_err('RewindLimitErr', 1007)  # 反悔次数达到限制
RewindTimeout = gen_logic_err('RewindTimeout', 1008)    # 反悔超时
NonSwipe = gen_logic_err('NonSwipe', 1009)              # 当前还没有滑动记录
