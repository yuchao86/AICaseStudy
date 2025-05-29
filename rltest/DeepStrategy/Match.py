from ChatStrategy import Strategy


# 具体策略类之意图是否匹配
class Match(Strategy):
    def __init__(self, accepted=500, reduction="匹配"):
        self.accepted = accepted
        self.reduction = reduction
        #可以添加匹配需要使用的参数

    def get_dialog(self, conversation):
        if conversation is None:
            print("no conversation")
            return self.reduction
        else:
            #todo模型判断是否匹配用户
            return "不匹配"
