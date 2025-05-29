
from ChatContext import Conversation, Customer, DialogItem
from Feedback import Feedback
from Follow import Follow
from Match import Match

if __name__ == '__main__':
    command = ''
    #Customer = namedtuple("Customer", "name sex age class address time buy order fidelity")
    myself = Customer("Yu Chao", "Y", 25, "三班", "北京海淀", 1500, 1, 101010, 123)
    dialog = [DialogItem(1, 0,"家长，你好，我能给你孩子提供一些学习上的帮助", 0.5),
              DialogItem(2,1,"我们是名师天团著名的老师，有丰富的教学经验",  1.5),
              DialogItem(3,2,"你看孩子什么时间有空", 2.5),
              DialogItem(4,3,"孩子目前的成绩怎么样？",  5.0)]

    while command != 'exit':
        items = eval(input("上一句话id: "))
        types = {'feed': Conversation(myself,dialog,Feedback()),
                 'follow': Conversation(myself,dialog,Follow()),
                 'match': Conversation(myself,dialog,Match()),}
        model = input("选择策略: feed、follow、match: ")
        if model in types:
            chat = types[model]
            print("输出结果: ", chat.get_result(items))
        else:
            print("不存在的策略")
        command = input("按下回车键继续或输入exit退出：")