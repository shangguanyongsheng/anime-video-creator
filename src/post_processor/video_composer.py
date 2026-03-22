"""
视频合成器

合并视频、配音、字幕
"""
import os
import subprocess
from typing import Optional
from dataclasses import dataclass


@dataclass
class CompositionResult:
    """合成结果"""
    success: bool
    output_path: str = ""
    error: str = ""


class VideoComposer:
    """
    视频合成器

    使用方法：
        composer = VideoComposer()
        result = composer.compose(
            video_path="input/video.mp4",
            audio_path="input/voice.mp3",
            subtitle_path="input/subtitle.srt",
            output_path="output/final.mp4"
        )
    """

    def __init__(self):
        """初始化合成器"""
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """检查 FFmpeg 是否可用"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg 未安装。请安装：\n"
                "  Ubuntu/Debian: sudo apt install ffmpeg\n"
                "  macOS: brew install ffmpeg"
            )

    def compose(
        self,
        video_path: str,
        audio_path: Optional[str] = None,
        subtitle_path: Optional[str] = None,
        output_path: str = "output/composed.mp4",
        subtitle_style: str = "Fontname=Noto Sans CJK SC,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2"
    ) -> CompositionResult:
        """
        合成视频

        Args:
            video_path: 视频文件路径
            audio_path: 配音文件路径（可选）
            subtitle_path: 字幕文件路径（可选）
            output_path: 输出路径
            subtitle_style: 字幕样式

        Returns:
            CompositionResult: 合成结果
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

            # 构建 FFmpeg 命令
            cmd = ["ffmpeg", "-y"]  # -y 覆盖已存在文件

            # 输入视频
            cmd.extend(["-i", video_path])

            # 输入配音
            if audio_path:
                cmd.extend(["-i", audio_path])

            # 构建输出
            if subtitle_path and audio_path:
                # 有字幕和配音
                cmd.extend([
                    "-vf", f"subtitles={subtitle_path}",
                    "-map", "0:v",
                    "-map", "1:a",
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-shortest",
                    output_path
                ])
            elif subtitle_path:
                # 只有字幕
                cmd.extend([
                    "-vf", f"subtitles={subtitle_path}",
                    "-c:v", "libx264",
                    "-c:a", "copy",
                    output_path
                ])
            elif audio_path:
                # 只有配音
                cmd.extend([
                    "-map", "0:v",
                    "-map", "1:a",
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-shortest",
                    output_path
                ])
            else:
                # 无需处理
                return CompositionResult(
                    success=False,
                    error="请提供配音或字幕文件"
                )

            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return CompositionResult(
                    success=False,
                    error=f"FFmpeg 错误: {result.stderr[:500]}"
                )

            return CompositionResult(
                success=True,
                output_path=output_path
            )

        except Exception as e:
            return CompositionResult(
                success=False,
                error=str(e)
            )

    def create_final_video(
        self,
        video_path: str,
        narration_text: str,
        output_path: str,
        voice_type = None
    ) -> CompositionResult:
        """
        一键创建完整视频（配音+字幕）

        Args:
            video_path: 原始视频路径
            narration_text: 解说文本
            output_path: 输出路径
            voice_type: 声音类型

        Returns:
            CompositionResult: 合成结果
        """
        from .voice_generator import VoiceGenerator, VoiceType
        from .subtitle_generator import SubtitleGenerator

        base_path = output_path.replace(".mp4", "")

        # 获取视频时长
        duration = self._get_video_duration(video_path)

        # 生成配音
        voice_gen = VoiceGenerator()
        voice_result = voice_gen.generate(
            text=narration_text,
            output_path=f"{base_path}_voice.mp3",
            voice=voice_type or VoiceType.ZH_FEMALE_GENTLE
        )

        if not voice_result.success:
            return CompositionResult(
                success=False,
                error=f"配音生成失败: {voice_result.error}"
            )

        # 生成字幕
        subtitle_gen = SubtitleGenerator()
        subtitle_gen.auto_generate(
            text=narration_text,
            total_duration=duration
        )
        subtitle_path = f"{base_path}.srt"
        subtitle_gen.save(subtitle_path)

        # 合成视频
        return self.compose(
            video_path=video_path,
            audio_path=voice_result.audio_path,
            subtitle_path=subtitle_path,
            output_path=output_path
        )

    def _get_video_duration(self, video_path: str) -> float:
        """获取视频时长"""
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    video_path
                ],
                capture_output=True,
                text=True
            )
            return float(result.stdout.strip())
        except:
            return 5.0  # 默认 5 秒


# ==================== 使用示例 ====================

if __name__ == "__main__":
    composer = VideoComposer()

    # 一键创建完整视频
    result = composer.create_final_video(
        video_path="output/test_video.mp4",
        narration_text="在樱花树下，一位少女正在优雅地跳舞。",
        output_path="output/final_video.mp4"
    )

    if result.success:
        print(f"✅ 视频已合成: {result.output_path}")
    else:
        print(f"❌ 合成失败: {result.error}")