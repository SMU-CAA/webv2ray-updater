# webv2ray-updater

在 WebVPN 中运行 V2Ray 代理，可配合 Clash Premium 内核 (TUN 模式) 实现类 VPN 功能，实现更便捷的校内资源访问权限

## 原理

在校内网运行 V2Ray 服务端接受请求，通过 WebVPN 作为出口

协议选择：VMess over WebSocket，因为 WebVPN 支持 WebSocket 转发

注意事项：验证码识别默认使用 CPU，如需使用 CUDA 加速，请参考 [cas-captcha-pytorch](https://github.com/SMU-CAA/cas-captcha-pytorch)

## 特性

- 自动登录 CAS 获取 Cookie，掉线重登
- 自动发送 Cookie 到 Cloudflare Workers，使用 [webv2ray-worker](https://github.com/SMU-CAA/webv2ray-worker) 实时更新 Clash 节点配置

## 使用

需要提前下载 [预训练验证码识别 JIT 模型](https://dl.lililili.net/directlink/2/files/2022/05/10/pre-trained_model_100k.jit.pt)

### Docker Compose

```yaml
version: "3"
services:
  updater:
    build:
      context: .
      dockerfile: ./Dockerfile
    environment:
      - SHMTU_CAS_USERNAME=202310000000
      - SHMTU_CAS_PASSWORD=foobar2023
      - V2RAY_PATH=/http-80/77726476706e69737468656265737421f4f34f8f747e61407a38495069562d
      - WEBV2RAY_UPDATE_TOKEN=a18cebca-1c92-4338-b6d2-26982f7e1f8c
    volumes:
      - /path/to/pre-trained_model_100k.jit.pt:/app/src/ai/model.jit.pt
    restart: always
```
