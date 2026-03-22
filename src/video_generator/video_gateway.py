"""
多厂商视频生成网关

统一接口，支持多厂商切换：
- 阿里云通义万象（主力）
- Runway（备选）
- 火山引擎（备选）
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class VendorType(Enum):
    """厂商类型"""
    ALIBABA_WANX = "alibaba_wanx"     # 阿里云通义万象
    RUNWAY = "runway"                  # Runway
    VOLCENGINE = "volcengine"          # 火山引擎
    OPENAI_SORA = "openai_sora"        # OpenAI Sora


@dataclass
class VideoConfig:
    """视频生成配置"""
    prompt: str
    duration: int = 5
    style: str = "anime"
    resolution: str = "1080p"
    reference_image: Optional[str] = None


@dataclass
class VideoResult:
    """视频生成结果"""
    success: bool
    video_url: str = ""
    cost: float = 0.0
    vendor: str = ""
    error: str = ""
    task_id: str = ""


class VideoGeneratorBase(ABC):
    """视频生成器基类"""
    
    @abstractmethod
    def generate(self, config: VideoConfig) -> VideoResult:
        """生成视频"""
        pass
    
    @abstractmethod
    def query_task(self, task_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        pass


class VideoGateway:
    """
    多厂商视频生成网关
    
    使用方法：
        gateway = VideoGateway()
        gateway.add_vendor(VendorType.ALIBABA_WANX, api_key="xxx")
        
        result = gateway.generate(
            prompt="动漫少女跳舞",
            duration=5,
            preferred_vendor=VendorType.ALIBABA_WANX
        )
    """
    
    def __init__(self):
        self._vendors: Dict[VendorType, VideoGeneratorBase] = {}
        self._fallback_order = [
            VendorType.ALIBABA_WANX,
            VendorType.RUNWAY,
            VendorType.VOLCENGINE
        ]
    
    def add_vendor(
        self, 
        vendor_type: VendorType, 
        api_key: str,
        **kwargs
    ):
        """
        添加厂商
        
        Args:
            vendor_type: 厂商类型
            api_key: API Key
            **kwargs: 其他配置
        """
        if vendor_type == VendorType.ALIBABA_WANX:
            from .wanx_generator import WanxVideoGenerator
            self._vendors[vendor_type] = WanxVideoGenerator(api_key=api_key)
        
        elif vendor_type == VendorType.RUNWAY:
            # TODO: 实现 Runway 生成器
            raise NotImplementedError("Runway 生成器待实现")
        
        elif vendor_type == VendorType.VOLCENGINE:
            # TODO: 实现火山引擎生成器
            raise NotImplementedError("火山引擎生成器待实现")
    
    def generate(
        self,
        prompt: str,
        duration: int = 5,
        style: str = "anime",
        preferred_vendor: Optional[VendorType] = None,
        auto_fallback: bool = True
    ) -> VideoResult:
        """
        生成视频
        
        Args:
            prompt: 视频描述
            duration: 时长（秒）
            style: 风格
            preferred_vendor: 首选厂商
            auto_fallback: 失败时是否自动切换厂商
        
        Returns:
            VideoResult: 生成结果
        """
        config = VideoConfig(
            prompt=prompt,
            duration=duration,
            style=style
        )
        
        # 确定厂商顺序
        vendors_to_try = []
        if preferred_vendor and preferred_vendor in self._vendors:
            vendors_to_try.append(preferred_vendor)
        
        if auto_fallback:
            for v in self._fallback_order:
                if v in self._vendors and v not in vendors_to_try:
                    vendors_to_try.append(v)
        
        if not vendors_to_try:
            return VideoResult(
                success=False,
                error="没有可用的视频生成厂商"
            )
        
        # 尝试生成
        last_error = ""
        for vendor_type in vendors_to_try:
            try:
                generator = self._vendors[vendor_type]
                result = generator.generate(config)
                
                if result.success:
                    result.vendor = vendor_type.value
                    return result
                
                last_error = result.error
                
            except Exception as e:
                last_error = str(e)
                print(f"⚠️ {vendor_type.value} 生成失败: {e}")
                continue
        
        return VideoResult(
            success=False,
            error=f"所有厂商都失败: {last_error}"
        )
    
    def list_vendors(self) -> list:
        """列出已配置的厂商"""
        return [v.value for v in self._vendors.keys()]


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化网关
    gateway = VideoGateway()
    
    # 配置厂商（按优先级）
    gateway.add_vendor(
        VendorType.ALIBABA_WANX, 
        api_key="your-dashscope-api-key"
    )
    
    # 生成视频
    result = gateway.generate(
        prompt="动漫少女在樱花树下跳舞",
        duration=5,
        style="anime",
        preferred_vendor=VendorType.ALIBABA_WANX
    )
    
    if result.success:
        print(f"✅ 视频已生成: {result.video_url}")
        print(f"💰 费用: ¥{result.cost:.2f}")
        print(f"🏭 厂商: {result.vendor}")
    else:
        print(f"❌ 生成失败: {result.error}")