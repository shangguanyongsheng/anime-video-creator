"""
完整的视频生成 Pipeline

一键生成：原始视频 → 配音 → 字幕 → 成品
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.video_generator import WanxVideoGenerator
from src.video_generator.wanx_generator import VideoStyle
from src.post_processor import VoiceGenerator, SubtitleGenerator, VideoComposer
from src.post_processor.voice_generator import VoiceType


class VideoPipeline:
    """
    视频生成 Pipeline
    
    使用方法：
        pipeline = VideoPipeline(api_key="your-key")
        result = pipeline.generate_anime_video(
            prompt="动漫少女在樱花树下跳舞",
            narration="在樱花树下，一位少女正在优雅地跳舞。",
            output_path="output/final.mp4"
        )
    """
    
    def __init__(self, api_key: str):
        """
        初始化 Pipeline
        
        Args:
            api_key: 万相 API Key
        """
        self.video_gen = WanxVideoGenerator(api_key=api_key)
        self.voice_gen = VoiceGenerator()
        self.composer = VideoComposer()
    
    def generate_anime_video(
        self,
        prompt: str,
        narration: str,
        output_path: str = "output/anime_video.mp4",
        duration: int = 5,
        voice: VoiceType = VoiceType.ZH_FEMALE_GENTLE
    ):
        """
        一键生成完整动漫视频
        
        Args:
            prompt: 视频提示词
            narration: 解说文本
            output_path: 输出路径
            duration: 视频时长
            voice: 配音声音类型
        
        Returns:
            dict: 包含所有生成结果的字典
        """
        results = {
            "success": False,
            "video_url": "",
            "voice_path": "",
            "subtitle_path": "",
            "final_path": "",
            "error": ""
        }
        
        try:
            # Step 1: 生成视频
            print("🎬 Step 1/4: 生成视频...")
            video_result = self.video_gen.generate(
                prompt=prompt,
                duration=duration,
                style=VideoStyle.ANIME
            )
            
            if not video_result.video_url:
                results["error"] = "视频生成失败"
                return results
            
            results["video_url"] = video_result.video_url
            print(f"   ✅ 视频URL: {video_result.video_url[:50]}...")
            
            # 下载视频
            base_path = output_path.replace(".mp4", "")
            raw_video_path = f"{base_path}_raw.mp4"
            self.video_gen.download_video(video_result.video_url, raw_video_path)
            print(f"   ✅ 已下载: {raw_video_path}")
            
            # Step 2: 生成配音
            print("🎙️ Step 2/4: 生成配音...")
            voice_path = f"{base_path}_voice.mp3"
            voice_result = self.voice_gen.generate(
                text=narration,
                output_path=voice_path,
                voice=voice,
                rate="-10%"
            )
            
            if not voice_result.success:
                results["error"] = f"配音生成失败: {voice_result.error}"
                return results
            
            results["voice_path"] = voice_path
            print(f"   ✅ 配音: {voice_path}")
            
            # Step 3: 生成字幕
            print("📝 Step 3/4: 生成字幕...")
            subtitle_path = f"{base_path}.srt"
            subtitle_gen = SubtitleGenerator()
            subtitle_gen.auto_generate(
                text=narration,
                total_duration=duration
            )
            subtitle_gen.save(subtitle_path)
            results["subtitle_path"] = subtitle_path
            print(f"   ✅ 字幕: {subtitle_path}")
            
            # Step 4: 合成视频
            print("🎥 Step 4/4: 合成视频...")
            compose_result = self.composer.compose(
                video_path=raw_video_path,
                audio_path=voice_path,
                subtitle_path=subtitle_path,
                output_path=output_path
            )
            
            if not compose_result.success:
                results["error"] = f"视频合成失败: {compose_result.error}"
                return results
            
            results["final_path"] = output_path
            results["success"] = True
            print(f"   ✅ 成品: {output_path}")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            return results


# ==================== 命令行入口 ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="一键生成动漫视频")
    parser.add_argument("--prompt", "-p", required=True, help="视频提示词")
    parser.add_argument("--narration", "-n", required=True, help="解说文本")
    parser.add_argument("--output", "-o", default="output/anime_video.mp4", help="输出路径")
    parser.add_argument("--duration", "-d", type=int, default=5, help="视频时长")
    parser.add_argument("--api-key", help="万相 API Key（或设置 DASHSCOPE_API_KEY）")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 请提供 API Key")
        return
    
    pipeline = VideoPipeline(api_key=api_key)
    
    result = pipeline.generate_anime_video(
        prompt=args.prompt,
        narration=args.narration,
        output_path=args.output,
        duration=args.duration
    )
    
    if result["success"]:
        print(f"\n🎉 视频生成成功!")
        print(f"   成品: {result['final_path']}")
    else:
        print(f"\n❌ 失败: {result['error']}")


if __name__ == "__main__":
    main()