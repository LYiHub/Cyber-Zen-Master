import os

from llm_client import LLMClient

SELF_EXPRESSION_PATH = "prompt/self_expression.txt"
GOLDEN_SENTENCE_PATH = "prompt/golden_sentence.txt"

class ExpressAgent:
    def __init__(self):
        """初始化辩论Agent"""
        self.llm = LLMClient()
        self.STAGE1_DIR = "output/stage1"
        self.STAGE2_DIR = "output/stage2"
        self.OUTPUT_DIR = "output/stage3"
    
    def load_from_file(self, filename, dir):
        """从文件加载内容"""
        filepath = os.path.join(dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
        
    def save_to_file(self, content, filename):
        """保存内容到文件"""
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def load_self_expression_prompt(self, full_topic, opposite_opinion, argument, golden_sentence):
        """加载自我表达prompt模板"""
        with open(SELF_EXPRESSION_PATH, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        formatted_prompt = prompt_template.format(
            full_topic=full_topic,
            opposite_opinion=opposite_opinion,
            argument=argument,
            golden_sentence=golden_sentence
        )
        return formatted_prompt
    
    def load_golden_sentence_prompt(self, full_topic, opposite_opinion, critique, significance):
        """加载金句prompt模板"""
        with open(GOLDEN_SENTENCE_PATH, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        formatted_prompt = prompt_template.format(
            full_topic=full_topic,
            opposite_opinion=opposite_opinion,
            critique=critique,
            significance=significance
        )
        return formatted_prompt

    def build_self_expression(self, full_topic):
        """生成自我表达"""
        opposite_opinion = self.load_from_file("opposite_opinion.txt", self.STAGE1_DIR)
        argument = self.load_from_file("argument.txt", self.STAGE2_DIR)
        golden_sentence = self.load_from_file("golden_sentence.txt", self.OUTPUT_DIR)

        self_expression_prompt = self.load_self_expression_prompt(full_topic, opposite_opinion, argument, golden_sentence)
        messages = [
            {"role": "user", "content": self_expression_prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.5)
        response = '\n'.join(line.strip() for line in response.splitlines() if line.strip())
        self.save_to_file(response, "self_expression.txt")
        return response

    
    def build_golden_sentence(self, full_topic):
        """生成金句"""
        opposite_opinion = self.load_from_file("opposite_opinion.txt", self.STAGE1_DIR)
        critique = self.load_from_file("critique.txt", self.STAGE1_DIR)
        significance = self.load_from_file("significance.txt", self.STAGE1_DIR)
        
        golden_sentence_prompt = self.load_golden_sentence_prompt(full_topic, opposite_opinion, critique, significance)
        messages = [
            {"role": "user", "content": golden_sentence_prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        response = '\n'.join(line.strip() for line in response.splitlines() if line.strip())
        self.save_to_file(response, "golden_sentence.txt")
        return response