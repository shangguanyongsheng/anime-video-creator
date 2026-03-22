"""
动漫短视频生成命令行工具

使用方法：
    python -m src.cli generate --prompt "动漫少女跳舞" --duration 5
    python -m src.cli anime --scene "樱花树下" --subject "动漫少女" --action "跳舞"
    python -m src.cli download --url "xxx" --output "video.mp4"
"""
import argparse
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_generator import WanxVideoGenerator
from video_generator.wanx_generator import VideoStyle, VideoResolution


def cmd_generate(args):
    """生成视频"""
    generator = WanxVideoGenerator()
    
    # 解析风格
    style_map = {
        "anime": VideoStyle.ANIME,
        "realistic": VideoStyle.REALISTIC,
        "cartoon": VideoStyle.CARTOON,
        "3d": VideoStyle.THREE_D
    }
    style = style_map.get(args.style, VideoStyle.ANIME)
    
    # 解析分辨率
    resolution_map = {
        "720p": VideoResolution.HD_720P,
        "1080p": VideoResolution.FHD_1080P,
        "2k": VideoResolution.QHD_2K
    }
    resolution = resolution_map.get(args.resolution, VideoResolution.FHD_1080P)
    
    print(f"🎬 正在生成视频...")
    print(f"   提示词: {args.prompt}")
    print(f"   时长: {args.duration}秒")
    print(f"   风格: {args.style}")
    
    result = generator.generate(
        prompt=args.prompt,
        duration=args.duration,
        style=style,
        resolution=resolution,
        reference_image=args.reference
    )
    
    print(f"\n✅ 视频生成成功!")
    print(f"   URL: {result.video_url}")
    print(f"   费用: ¥{result.cost:.2f}")
    
    if args.output:
        generator.download_video(result.video_url, args.output)
        print(f"   已保存: {args.output}")


def cmd_anime(args):
    """快捷生成动漫视频"""
    generator = WanxVideoGenerator()
    
    print(f"🎬 正在生成动漫视频...")
    print(f"   主体: {args.subject}")
    print(f"   场景: {args.scene}")
    print(f"   动作: {args.action}")
    
    result = generator.generate_anime(
        scene=args.scene,
        subject=args.subject,
        action=args.action,
        duration=args.duration
    )
    
    print(f"\n✅ 视频生成成功!")
    print(f"   URL: {result.video_url}")
    print(f"   费用: ¥{result.cost:.2f}")
    
    if args.output:
        generator.download_video(result.video_url, args.output)


def cmd_download(args):
    """下载视频"""
    generator = WanxVideoGenerator()
    generator.download_video(args.url, args.output)


def main():
    parser = argparse.ArgumentParser(
        description="动漫短视频生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # generate 命令
    gen_parser = subparsers.add_parser("generate", help="生成视频")
    gen_parser.add_argument("--prompt", "-p", required=True, help="视频描述提示词")
    gen_parser.add_argument("--duration", "-d", type=int, default=5, help="视频时长（秒）")
    gen_parser.add_argument("--style", "-s", default="anime", 
                           choices=["anime", "realistic", "cartoon", "3d"],
                           help="视频风格")
    gen_parser.add_argument("--resolution", "-r", default="1080p",
                           choices=["720p", "1080p", "2k"],
                           help="视频分辨率")
    gen_parser.add_argument("--reference", "-ref", help="参考图片 URL")
    gen_parser.add_argument("--output", "-o", help="输出文件路径")
    gen_parser.set_defaults(func=cmd_generate)
    
    # anime 命令（快捷）
    anime_parser = subparsers.add_parser("anime", help="快捷生成动漫视频")
    anime_parser.add_argument("--scene", default="樱花树下", help="场景")
    anime_parser.add_argument("--subject", default="动漫少女", help="主体")
    anime_parser.add_argument("--action", default="优雅地跳舞", help="动作")
    anime_parser.add_argument("--duration", "-d", type=int, default=5, help="时长")
    anime_parser.add_argument("--output", "-o", help="输出文件路径")
    anime_parser.set_defaults(func=cmd_anime)
    
    # download 命令
    dl_parser = subparsers.add_parser("download", help="下载视频")
    dl_parser.add_argument("--url", "-u", required=True, help="视频 URL")
    dl_parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    dl_parser.set_defaults(func=cmd_download)
    
    args = parser.parse_args()
    
    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()