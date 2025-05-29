import re
import random
from typing import List, Dict, Tuple
import jieba.posseg as pseg


class EnhancedDialogEnhancer:
    def __init__(self, config: Dict = None):
        # 初始化词库和配置
        self._load_default_resources()
        if(config is None):
            self.config = config
        else:
            self.config = self._get_default_config()

        # 初始化分词模型
        self._init_nlp()

        # 状态跟踪
        self.dialog_history = []
        self.user_profile = {}

    def _load_default_resources(self):
        """加载多维度填充词库"""
        self.vocab = {
            # 犹豫填充词（按情感强度分类）
            'hesitation': {
                'low': ['嗯', '呃', '那个'],
                'medium': ['这个嘛', '怎么说呢', '其实呢'],
                'high': ['让我仔细想想啊', '这个问题需要仔细考虑一下']
            },

            # 确认性短语
            'confirmation': [
                '您说这样合适吗？', '不知道我这样解释清楚吗？',
                '您看这样处理可以吗？', '您觉得这个方案怎么样？'
            ],

            # 自然修正短语
            'correction': {
                'time': ['稍等纠正一下', '准确时间应该是', '我可能记错了应该是'],
                'quantity': ['大约', '左右', '上下'],
                'general': ['或者说', '更准确地说', '换种说法就是']
            },

            # 情感语气词
            'emotion': {
                'positive': ['太好了', '非常棒的是', '令人高兴的是'],
                'negative': ['遗憾的是', '不过需要注意的是', '可能不太理想的是']
            },

            # 专业场景填充
            'professional': {
                'finance': ['根据风控要求', '按照合规流程', '根据最新的监管规定'],
                'tech': ['从技术实现角度', '系统逻辑层面', '底层架构设计上']
            }
        }

    def _get_default_config(self) -> Dict:
        """获取默认处理配置"""
        return {
            'fill_prob': 0.35,  # 填充词触发概率
            'correction_prob': 0.2,  # 自我修正概率
            'context_window': 3,  # 上下文记忆轮数
            'max_fillers': 2,  # 单句最大填充词数
            'style': 'neutral',  # 默认对话风格
            'industry': 'finance'  # 行业领域
        }

    def _init_nlp(self):
        """初始化简单的NLP处理工具"""
        self.pos_tags = {'需要': 'v', '费用': 'n'}  # 简化的词性标注示例
        # 实际应用时应使用完整分词工具

    def _dynamic_hesitation(self, sentence: str) -> str:
        """动态插入符合场景的填充词"""
        if random.random() > self.config['fill_prob']:
            return sentence

        # 分析句子结构
        clauses = re.split(r'[，。；]', sentence)
        if not clauses:
            return sentence

        # 选择插入位置
        insert_pos = random.randint(0, min(2, len(clauses) - 1))
        intensity = self._get_hesitation_intensity(sentence)

        # 获取行业相关填充词
        industry_phrases = self.vocab['professional'].get(self.config['industry'], [])
        fillers = self.vocab['hesitation'][intensity] + industry_phrases

        selected_filler = random.choice(fillers)
        clauses.insert(insert_pos, selected_filler)

        return '，'.join([c for c in clauses if c])

    def _get_hesitation_intensity(self, sentence: str) -> str:
        """根据句子复杂度决定填充词强度"""
        length = len(sentence)
        if length > 50:
            return 'high'
        elif length > 25:
            return 'medium'
        return 'low'

    def _context_aware_correction(self, sentence: str) -> str:
        """上下文感知的自我修正"""
        if random.random() > self.config['correction_prob']:
            return sentence

        # 检测需要修正的内容类型
        correction_type = self._detect_correction_type(sentence)
        correction_phrases = self.vocab['correction'].get(correction_type, self.vocab['correction']['general'])

        # 生成修正格式
        correction_format = random.choice([
            f"{random.choice(correction_phrases)}...",
            "（{}）".format(random.choice(correction_phrases)),
            "——{}——".format(random.choice(correction_phrases))
        ])

        return f"{sentence}{correction_format}"

    def _detect_correction_type(self, sentence: str) -> str:
        """检测需要修正的内容类型"""
        if re.search(r'\d+[年月日]', sentence):
            return 'time'
        if re.search(r'\d+[个件项]', sentence):
            return 'quantity'
        return 'general'

    def _add_emotional_phrase(self, sentence: str) -> str:
        """添加情感语气词"""
        emotion = self._detect_sentence_emotion(sentence)
        phrase = random.choice(self.vocab['emotion'][emotion])

        insert_pos = random.choice(['prefix', 'suffix'])
        if insert_pos == 'prefix':
            return f"{phrase}，{sentence}"
        else:
            return f"{sentence}，{phrase}"

    def _detect_sentence_emotion(self, sentence: str) -> str:
        """简单情感分析（实际应用应使用模型）"""
        positive_words = ['成功', '顺利', '恭喜']
        negative_words = ['抱歉', '问题', '故障']

        if any(w in sentence for w in positive_words):
            return 'positive'
        if any(w in sentence for w in negative_words):
            return 'negative'
        return 'positive'  # 默认偏向积极

    def _add_professional_phrase(self, sentence: str) -> str:
        """添加行业相关短语"""
        industry_phrases = self.vocab['professional'].get(self.config['industry'], [])
        if industry_phrases and random.random() < 0.4:
            return f"{random.choice(industry_phrases)}，{sentence}"
        return sentence

    def enhance_sentence(self, raw_sentence: str) -> str:
        """全流程自然化处理"""
        processing_pipeline = [
            self._add_professional_phrase,
            self._dynamic_hesitation,
            self._context_aware_correction,
            self._add_emotional_phrase
        ]

        processed = raw_sentence
        for func in processing_pipeline:
            processed = func(processed)
            # 防止过度处理
            if len(processed) > 1.5 * len(raw_sentence):
                break

        # 最后处理确认性短语
        if random.random() < 0.3:
            processed += "，" + random.choice(self.vocab['confirmation'])

        return self._clean_overprocessing(processed)

    def _clean_overprocessing(self, sentence: str) -> str:
        """清理过度处理的情况"""
        # 移除连续重复的逗号
        sentence = re.sub(r'，+', '，', sentence)
        # 限制填充词数量
        clauses = sentence.split('，')
        if len(clauses) > self.config['max_fillers'] + 3:
            return '，'.join(clauses[:self.config['max_fillers'] + 3])
        return sentence

    def update_context(self, user_input: str, system_response: str):
        """更新对话上下文"""
        self.dialog_history.append((user_input, system_response))
        # 保留最近的对话历史
        if len(self.dialog_history) > self.config['context_window']:
            self.dialog_history.pop(0)

    def set_industry(self, industry: str):
        """设置行业领域"""
        self.config['industry'] = industry
        # 预加载行业特定词库
        if industry == 'finance':
            self.vocab['professional']['finance'] += ['根据公司规定', '按照公司要求']

    def load_user_profile(self, profile: Dict):
        """加载用户画像"""
        self.user_profile = profile
        # 根据用户特征调整填充策略
        if profile.get('age', 30) > 50:
            self.config['fill_prob'] = 0.4  # 年长用户更多解释


# 使用示例
if __name__ == "__main__":
    enhancer = EnhancedDialogEnhancer(
        {
            'fill_prob': 0.35,  # 填充词触发概率
            'correction_prob': 0.3,  # 自我修正概率
            'context_window': 3,  # 上下文记忆轮数
            'max_fillers': 2,  # 单句最大填充词数
            'style': 'neutral',  # 默认对话风格
            'industry': 'finance'  # 行业领域
        }
    )

    samples = [
        "转账手续费是千分之二",
        "您的贷款申请已审批通过",
        "需要您提供最近三个月的银行流水",
        "需要先登录系统然后点击设置按钮进行系统设置"
    ]

    for text in samples:
        print("原始:", text)
        enhanced = enhancer.enhance_sentence(text)
        print("增强后:", enhanced)
        print("---")

# 自然化改写规则数据库（JSON格式）
natural_rules = {
    # 句式转换规则
    "sentence_structure": [
        {
            "formal": "请您提供身份证号码",
            "natural": [
                "麻烦您报一下身份证号呗～",
                "方不方便把身份证号码跟我说一下呀？",
                "您给报个身份证号码好吗？就现在系统需要登记一下"
            ]
        },
        {
            "formal": "正在为您查询，请稍后",
            "natural": [
                "稍等哈，我这儿正帮您查着呢～",
                "您等我几秒钟，马上帮您查到",
                "正在系统里搜，马上就好，别挂电话哦"
            ]
        }
    ],

    # 情感增强规则
    "emotional_enhancement": [
        {
            "neutral": "操作已完成",
            "natural": [
                "太好啦！您刚那个操作已经顺利搞定啦～",
                "恭喜您！这一步已经成功完成咯",
                "搞定了！系统显示操作完全没问题"
            ]
        },
        {
            "neutral": "验证失败",
            "natural": [
                "哎呀，这边显示验证没通过呢，咱们再试试别的办法？",
                "验证没成功，可能是哪里出错了，您看要不要再检查一下？",
                "有点小问题，系统说验证不匹配，咱们换个方式试试？"
            ]
        }
    ],

    # 专业领域适配规则
    "professional_adaptation": {
        "finance": [
            {
                "formal": "年利率为4.35%",
                "natural": [
                    "您这笔贷款的年息是4分35，这个利率现在算是挺划算的啦",
                    "系统显示年化利率4.35%，比市面上大多数产品都低呢",
                    "给您批下来的利率是4.35%，也就是一万块一年利息435元"
                ]
            }
        ],
        "tech": [
            {
                "formal": "需要重启服务器",
                "natural": [
                    "咱们得给服务器重新启动下，就像手机卡了要重启一样",
                    "现在这个情况得重启服务，大概需要两分钟时间",
                    "可能需要强制重启下后台服务，您看现在方便操作吗？"
                ]
            }
        ]
    },

    # 场景应对规则
    "scenario_response": {
        "urgent": [
            {
                "formal": "请保持冷静",
                "natural": [
                    "您先别着急，咱们一起想办法解决！",
                    "我完全理解您现在的心情，咱们一步步来处理",
                    "深呼吸，慢慢说，我在这儿帮您一起处理"
                ]
            }
        ],
        "transfer": [
            {
                "formal": "正在为您转接人工客服",
                "natural": [
                    "马上给您转真人客服，稍等别挂机哦～",
                    "这就帮您转接专业客服，请稍等几秒钟",
                    "您的情况需要专家处理，现在就转接过去"
                ]
            }
        ]
    },

    # 自然修正规则
    "natural_correction": [
        {
            "template": "(原句)...或者更准确地说...(修正内容)",
            "examples": [
                "需要3个工作日——准确来说是3到5个工作日",
                "费用是200元左右，严格来说要看具体使用情况",
                "周一下午能到，可能得周二上午，最近物流有点慢"
            ]
        }
    ],

    # 口语填充规则
    "verbal_fillers": {
        "prefix": ["那个", "嗯", "啊"],
        "infix": [
            "这么说吧",
            "您知道吗",
            "简单来说",
            "好比说"
        ],
        "suffix": [
            "您看这样行吗？",
            "这样清楚吗？",
            "不知道我说明白没有"
        ]
    },

    # 数字表达规则
    "number_expressions": [
        {
            "formal": "7天",
            "natural": ["一周", "七天时间", "个把星期"]
        },
        {
            "formal": "500元",
            "natural": ["五百块", "五张红的", "半千块钱"]
        }
    ],

    # 时间表达规则
    "time_expressions": [
        {
            "formal": "10:30",
            "natural": ["十点半", "上午十点半", "十点三十分整"]
        },
        {
            "formal": "3个工作日内",
            "natural": ["三天左右", "三个工作日差不多", "大概三天时间"]
        }
    ]
}

# 使用示例
print(natural_rules["sentence_structure"][0]["natural"][0])
# 输出：麻烦您报一下身份证号呗～

print(natural_rules["professional_adaptation"]["finance"][0]["natural"][1])
# 输出：系统显示年化利率4.35%，比市面上大多数产品都低呢