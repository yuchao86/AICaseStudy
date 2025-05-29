
# 对话上下文管理类
class Accept(object):
    def __init__(self, cash_):
        self.cash_ = cash_

    def get_result(self, cash):
        return self.cash_.get_dialog(cash)
