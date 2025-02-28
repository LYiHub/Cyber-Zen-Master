import os

from llm_client import LLMClient

OPPOSITE_OPINION_PROMPT = "prompt/opposite_opinion_agent.txt"
CRITIQUE_PROMPT = "prompt/critique_agent.txt"
SIGNIFICANCE_PROMPT = "prompt/significance_agent.txt"


class AnalyzeAgent:
    def __init__(self):
        """初始化分析Agent"""
        self.llm = LLMClient()
        self.OUTPUT_DIR = "output/stage1"
    
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
    
    def opposite_opinion_association(self, full_topic):
        """对问题进行联想"""
        with open(OPPOSITE_OPINION_PROMPT, 'r', encoding='utf-8') as f:
            template = f.read()
        
        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": f"问题: {full_topic}"}
        ]
        
        response = self.llm.chat(messages, temperature=0.5)
            
        self.save_to_file(response, "opposite_opinion.txt")
        return response

    def analyze_critique(self):
        """对反面观点进行批判性分析"""
        with open(CRITIQUE_PROMPT, 'r', encoding='utf-8') as f:
            template = f.read()

        opposite_opinion = self.load_from_file("opposite_opinion.txt", self.OUTPUT_DIR)
            
        # 分析反方对正方的批判
        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": f"观点: {opposite_opinion}"}
        ]
        
        critique = self.llm.chat(messages, temperature=0.6)
        # 保存反方批判
        self.save_to_file(critique, "critique.txt")
        
        return critique

    def analyze_significance(self, full_topic):
        """分析正面观点的现实意义"""
        with open(SIGNIFICANCE_PROMPT, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # 分析正方现实意义
        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": f"观点: {full_topic}"}
        ]
        
        significance = self.llm.chat(messages, temperature=0.6)
        # 保存正方现实意义
        self.save_to_file(significance, "significance.txt")
        
        return significance