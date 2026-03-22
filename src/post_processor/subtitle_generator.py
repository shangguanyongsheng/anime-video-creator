"""
字幕生成器

生成 SRT 格式字幕文件
"""
import os
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class SubtitleLine:
    """字幕行"""
    index: int
    start_time: float  # 秒
    end_time: float    # 秒
    text: str


class SubtitleGenerator:
    """
    字幕生成器
    
    使用方法：
        generator = SubtitleGenerator()
        generator.add_line(0, 3, "在樱花树下")
        generator.add_line(3, 5, "少女正在跳舞")
        generator.save("output/subtitle.srt")
    """
    
    def __init__(self):
        """初始化字幕生成器"""
        self.lines: List[SubtitleLine] = []
    
    def add_line(
        self,
        start_time: float,
        end_time: float,
        text: str
    ):
        """
        添加一行字幕
        
        Args:
            start_time: 开始时间（秒）
            end_time: 结束时间（秒）
            text: 字幕文本
        """
        self.lines.append(SubtitleLine(
            index=len(self.lines) + 1,
            start_time=start_time,
            end_time=end_time,
            text=text
        ))
    
    def auto_generate(
        self,
        text: str,
        total_duration: float,
        max_chars_per_line: int = 20
    ):
        """
        自动根据文字生成字幕
        
        Args:
            text: 完整文本
            total_duration: 视频总时长（秒）
            max_chars_per_line: 每行最多字符数
        """
        # 按句子分割
        import re
        sentences = re.split(r'[，。！？；]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return
        
        # 计算每个句子的平均时长
        chars_per_second = len(text) / total_duration
        
        current_time = 0.0
        for sentence in sentences:
            # 计算这句的时长
            duration = len(sentence) / chars_per_second
            end_time = min(current_time + duration, total_duration)
            
            self.add_line(current_time, end_time, sentence)
            current_time = end_time
    
    def save(self, output_path: str):
        """
        保存为 SRT 文件
        
        Args:
            output_path: 输出路径
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in self.lines:
                f.write(f"{line.index}\n")
                f.write(f"{self._format_time(line.start_time)} --> {self._format_time(line.end_time)}\n")
                f.write(f"{line.text}\n")
                f.write("\n")
    
    def _format_time(self, seconds: float) -> str:
        """将秒数转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    @staticmethod
    def create_simple_subtitle(
        text: str,
        duration: float,
        output_path: str
    ):
        """
        快捷方法：创建简单字幕
        
        Args:
            text: 字幕文本
            duration: 视频时长
            output_path: 输出路径
        """
        generator = SubtitleGenerator()
        generator.add_line(0, duration, text)
        generator.save(output_path)


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 方式1：手动添加字幕
    generator = SubtitleGenerator()
    generator.add_line(0, 2, "在樱花树下")
    generator.add_line(2, 4, "一位少女正在跳舞")
    generator.add_line(4, 5, "优雅动人")
    generator.save("output/subtitle.srt")
    print("✅ 字幕已保存")
    
    # 方式2：自动生成
    generator2 = SubtitleGenerator()
    generator2.auto_generate(
        text="在樱花树下，一位少女正在优雅地跳舞。粉色的花瓣随风飘落。",
        total_duration=5
    )
    generator2.save("output/subtitle_auto.srt")
    print("✅ 自动字幕已保存")