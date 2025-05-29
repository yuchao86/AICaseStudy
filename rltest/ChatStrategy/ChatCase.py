from ChatContext import Accept
from Feedback import Feedback
from Follow import Follow
from Match import Match

if __name__ == '__main__':
    command = ''
    while command != 'exit':
        cashes = eval(input("原价: "))
        types = {'85折': Accept(Feedback()),
                 '满300减50': Accept(Follow()),
                 '满500减100': Accept(Match()),}
        model = input("选择折扣方式: 85折、满300减50、满500减100: ")
        if model in types:
            money = types[model]
            print("需要支付: ", money.get_result(cashes))
        else:
            print("不存在的折扣方式")
        command = input("按下回车键继续或输入exit退出：")