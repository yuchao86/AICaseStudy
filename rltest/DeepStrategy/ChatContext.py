from collections import namedtuple

Customer = namedtuple("Customer", "name sex age classname address time buy order fidelity")


class DialogItem:
    def __init__(self, item_id, last_id, context, state) -> None:
        self.itemId = item_id
        self.lastId = last_id
        self.context = context
        self.state = state

    def gen_prompt(self):
        #根据self.state状态获取不同的prompt
        return self.context


# 对话上下文管理类
class Conversation(object):
    def __init__(self, customer, item, strategy1):
        self.customer = customer
        self.dialogs = list(item)
        self.strategy = strategy1

    def get_result(self, conversation):
        item = self.dialogs.pop()
        print(item.gen_prompt())
        return self.strategy.get_dialog(conversation)
