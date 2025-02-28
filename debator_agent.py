import os

from llm_client import LLMClient

CONSTRUCTION_PATH = "prompt/construction_agent.txt"

class DebatorAgent:
    def __init__(self):
        """初始化辩论Agent"""
        self.llm = LLMClient()
        self.winner = None
        self.STAGE1_DIR = "output/stage1"
        self.OUTPUT_DIR = "output/stage2"
    
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

    def load_construct_prompt(self, full_topic, opposite_opinion, critique, significance):
        """加载观点prompt模板"""
        with open(CONSTRUCTION_PATH, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        formatted_prompt = prompt_template.format(
            full_topic=full_topic,
            opposite_opinion=opposite_opinion,
            critique=critique,
            significance=significance
        )
        return formatted_prompt

    def generate_argument(self, full_topic):
        """生成观点"""
        opposite_opinion = self.load_from_file("opposite_opinion.txt", self.STAGE1_DIR)
        critique = self.load_from_file("critique.txt", self.STAGE1_DIR)
        significance = self.load_from_file("significance.txt", self.STAGE1_DIR)

        construction_prompt = self.load_construct_prompt(full_topic, opposite_opinion, critique, significance)
        messages = [
            {"role": "user", "content": construction_prompt},
        ]
        
        response = self.llm.chat(messages, temperature=0.5)
            
        self.save_to_file(response, "argument.txt")
        return response