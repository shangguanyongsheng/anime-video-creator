# 阿里云 通义万象 对接方案

## 1. 服务概述

**阿里云通义万象**是国内最成熟的 AI 视频生成服务，网络稳定，价格便宜。

| 属性 | 值 |
|------|-----|
| 官网 | https://tongyi.aliyun.com |
| API 文档 | https://help.aliyun.com/document_detail/... |
| 定价 | 按量计费，约 ¥0.1/秒 |
| 最大时长 | 10 秒 |
| 分辨率 | 1080p |
| 动漫风格 | ⭐⭐⭐ |

## 2. API 接入

### 2.1 开通服务

1. 登录阿里云控制台
2. 开通「通义万象」服务
3. 创建 AccessKey

### 2.2 安装 SDK

```bash
pip install alibabacloud-tea-openapi
pip install alibabacloud-videogen20240601
```

### 2.3 基础调用示例

```python
from alibabacloud_videogen20240601.client import Client
from alibabacloud_videogen20240601 import models as models
from alibabacloud_tea_openapi import models as open_api_models

# 创建客户端
config = open_api_models.Config(
    access_key_id=os.getenv("ALIBABA_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_ACCESS_KEY_SECRET"),
)
config.endpoint = "videogen.cn-shanghai.aliyuncs.com"
client = Client(config)

# 文生视频
request = models.SubmitTextToVideoProTaskRequest(
    prompt="动漫风格的少女在樱花树下跳舞",
    style="anime",
    duration=5,
    resolution="1080p"
)

response = client.submit_text_to_video_pro_task(request)
task_id = response.body.data.task_id

# 查询结果
import time
while True:
    result = client.get_task_result(task_id)
    if result.body.data.status == "SUCCESS":
        video_url = result.body.data.video_url
        break
    time.sleep(5)
```

## 3. Python 封装

```python
# video_generator/alibaba.py
from alibabacloud_videogen20240601.client import Client
from alibabacloud_videogen20240601 import models as models
from alibabacloud_tea_openapi import models as open_api_models
import os

class AlibabaGenerator(VideoGenerator):
    def __init__(self, access_key_id: str, access_key_secret: str):
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
        )
        config.endpoint = "videogen.cn-shanghai.aliyuncs.com"
        self.client = Client(config)
        self.cost_per_second = 0.1  # 约 ¥0.1/秒
    
    def generate(
        self, 
        prompt: str, 
        duration: int = 5,
        style: str = "anime",
        reference_image: Optional[str] = None
    ) -> VideoGenerationResult:
        request = models.SubmitTextToVideoProTaskRequest(
            prompt=self._optimize_prompt(prompt, style),
            duration=duration,
            resolution="1080p"
        )
        
        response = self.client.submit_text_to_video_pro_task(request)
        task_id = response.body.data.task_id
        
        video_url = self._wait_for_completion(task_id)
        
        return VideoGenerationResult(
            video_url=video_url,
            duration=duration,
            resolution="1080p",
            cost=duration * self.cost_per_second
        )
    
    def _optimize_prompt(self, prompt: str, style: str) -> str:
        # 阿里云对中文提示词支持更好
        style_map = {
            "anime": "日系动漫风格",
            "realistic": "写实风格",
            "cartoon": "卡通风格"
        }
        modifier = style_map.get(style, "")
        return f"{prompt}，{modifier}"
```

## 4. 优势与适用场景

### 优势
- ✅ 国内网络稳定，无需代理
- ✅ 中文提示词支持好
- ✅ 价格便宜
- ✅ 与阿里云生态打通（OSS、CDN）

### 适用场景
- 国内项目首选
- 成本敏感项目
- 中文内容创作
- 快速原型验证

## 5. 注意事项

1. **动漫风格有限**：不如 Runway 精细
2. **时长限制**：单次最长 10 秒
3. **需要企业认证**：部分功能需要