from ChatStrategy import Strategy

# 具体策略类之对客户说话进行呼应
class Feedback(Strategy):
    def __init__(self, discount=0.85):
        self.discount = discount

    def get_dialog(self, cash):
        return cash * self.discount
