from ChatStrategy import Strategy

# 具体策略类之是否跟随客户话题
class Follow(Strategy):
    def __init__(self, accepted=300, reduction="好的"):
        self.accepted = accepted
        self.reduction = reduction
        #可以添加跟随需要使用的参数

    def get_dialog(self, conversation):
        if conversation is None:
            print("no conversation")
            return self.reduction
        else:
            #todo模型判断是否跟随用户
            return "你请说"
