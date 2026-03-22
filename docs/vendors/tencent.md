# 腾讯混元 对接方案

## 1. 服务概述

**腾讯混元**是腾讯的大模型服务，包含视频生成能力。

| 属性 | 值 |
|------|-----|
| 官网 | https://cloud.tencent.com/product/hunyuan |
| API 文档 | https://cloud.tencent.com/document/... |
| 定价 | 待定（内测阶段） |
| 最大时长 | 10 秒 |
| 分辨率 | 1080p |
| 动漫风格 | ⭐⭐⭐ |

## 2. API 接入

### 2.1 开通服务

1. 登录腾讯云控制台
2. 申请「混元视频」内测资格
3. 获取 API 密钥

### 2.2 安装 SDK

```bash
pip install tencentcloud-sdk-python
```

### 2.3 基础调用示例

```python
from tencentcloud.common import credential
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

# 初始化客户端
cred = credential.Credential(
    os.getenv("TENCENT_SECRET_ID"),
    os.getenv("TENCENT_SECRET_KEY")
)
client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou")

# 视频生成
req = models.SubmitTextToVideoTaskRequest()
req.Prompt = "动漫少女在樱花树下跳舞"
req.Style = "anime"
req.Duration = 5

response = client.SubmitTextToVideoTask(req)
task_id = response.TaskId
```

## 3. 腾讯生态优势

### 3.1 微信小程序发布
```python
# 生成后发布到微信视频号
wechat_service.publish_video(
    video_url=video_url,
    title="动漫少女跳舞",
    account_id="your_account_id"
)
```

### 3.2 游戏素材生成
- 游戏角色动画
- 游戏特效
- 游戏宣传视频

## 4. 适用场景

- 微信生态内容创作
- 游戏行业
- 腾讯云用户

## 5. 注意事项

1. **仍在内测**：API 开放程度有限
2. **需要申请**：通过腾讯云控制台申请
3. **适合腾讯生态**：与微信、游戏深度绑定