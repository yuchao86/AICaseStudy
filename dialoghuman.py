import random
import re
from typing import List, Tuple


class SelfCorrectionGenerator:
    def __init__(self):
        # 预定义的中断触发词及修正模板
        self.correction_patterns = [
            (r"\b(大概|可能|或许)\b", 0.3, self._generate_hesitation_correction),
            (r"\b(首先|其一)\b", 0.2, self._generate_ordering_correction),
            (r"\d{4}年", 0.4, self._generate_date_correction)
        ]

        # 自然停顿短语库
        self.hesitation_phrases = [
            "等等", "稍等", "啊", "嗯", "对了",
            "话说回来", "准确地说", "严格来说"
        ]

    def _insert_hesitation(self, sentence: str) -> str:
        """在句子中插入自然停顿"""
        clauses = re.split(r'[,，。]', sentence)
        if len(clauses) > 1 and random.random() < 0.4:
            insert_pos = random.randint(0, len(clauses) - 1)
            clauses.insert(insert_pos, random.choice(self.hesitation_phrases))
            return '，'.join([c for c in clauses if c])
        return sentence

    def _generate_hesitation_correction(self, match: re.Match) -> str:
        """生成犹豫型修正"""
        original = match.group()
        corrections = {
            "大概": ["准确来说", "实际上"],
            "可能": ["后来确认应该是", "经过核实其实是"],
            "或许": ["严格来说应该是", "更准确的说法是"]
        }
        return f"{original}{random.choice(['', '…'])}…{random.choice(corrections.get(original, ['']))}"

    def _generate_ordering_correction(self, match: re.Match) -> str:
        """生成顺序型修正"""
        order_phrases = [
            "其实应该先说...",
            "等等，顺序可能需要调整一下",
            "啊，这里可能倒置了，正确的顺序应该是..."
        ]
        return f"{match.group()}…（{random.choice(order_phrases)}）"

    def _generate_date_correction(self, match: re.Match) -> str:
        """生成时间修正"""
        year = match.group()
        return f"{year}年左右…（具体时间可能需要再确认，可能是{int(year[:-1])+random.randint(1, 2)}年）"

    def _dynamic_correction(self, sentence: str) -> str:
        """动态应用修正规则"""
        for pattern, prob, func in self.correction_patterns:
            if random.random() < prob and re.search(pattern, sentence):
                return re.sub(pattern, func, sentence, count=1)
        return sentence

    def add_natural_corrections(self, original_response: str) -> str:
        """添加自然修正的三阶段处理"""
        # 第一阶段：句子级中断插入
        modified = self._insert_hesitation(original_response)

        # 第二阶段：动态规则修正
        modified = self._dynamic_correction(modified)

        # 第三阶段：添加口语化修正标记
        if random.random() < 0.25:
            correction_formats = [
                " → 应该说...",
                " —— 修正一下...",
                "，或者说...",
                "（更准确地说...）"
            ]
            modified += random.choice(correction_formats)

        return modified

    def add_verbal_fillers(self, text: str) -> str:
        fillers = ['呃', '嗯', '这个', '那个']
        positions = [m.start() for m in re.finditer(r'[，。]', text)]
        if positions:
            pos = random.choice(positions)
            return text[:pos] + random.choice(fillers) + text[pos:]
        return text

    #上下文感知修正
    def context_aware_correction(self, dialog_history: List[str], current_response: str) -> str:
        if "时间" in dialog_history[-1]:
            return self._generate_date_correction(current_response)
        if "步骤" in current_response:
            return self._generate_ordering_correction(current_response)
        return current_response

# 示例使用
if __name__ == "__main__":
    generator = SelfCorrectionGenerator()

    sample_responses = [
        "这个事件发生在1999年互联网泡沫时期",
        "可能需要三种步骤：首先下载软件，然后安装配置",
        "大概需要三天时间完成"
    ]

    for resp in sample_responses:
        print("原始回答:", resp)
        corrected = generator.add_natural_corrections(resp)
        print("修正后:", corrected)
        print("-" * 50)