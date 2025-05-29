from ChatStrategy import Strategy

# 具体策略类之对客户说话进行呼应
class Feedback(Strategy):
    def __init__(self, tempture=0.85):
        self.tempture = tempture
        #可以添加反馈需要使用的参数

    def get_dialog(self, conversation):
        #dialog = conversation.get_dialog()
        #todo模型判断是否输出呼应内容
        return "嗯"
