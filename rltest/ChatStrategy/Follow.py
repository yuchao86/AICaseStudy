from ChatStrategy import Strategy

# 具体策略类之是否跟随客户话题
class Follow(Strategy):
    def __init__(self, cash_accepted=300, reduction=50):
        self.cash_accepted = cash_accepted
        self.reduction = reduction

    def get_dialog(self, cash):
        if cash >= self.cash_accepted:
            return cash - self.reduction
        else:
            print("您不满足该条件")
            return cash
