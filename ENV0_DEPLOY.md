# env0 部署说明

这个仓库现在提供两部分：

- `Dockerfile`：稳定运行应用并提供 HTTP 健康检查。
- `env0-helm/`：env0 的 Helm Template，可把容器部署到已连接到 env0 的 Kubernetes 集群。

## 前置条件

1. 把仓库推到 GitHub，并让 GitHub Actions 成功发布：
   `ghcr.io/<GitHub用户名>/python-xray-argo:latest`
2. 在 env0 中连接一个 Kubernetes 集群。
3. 创建 Helm Template，仓库指向本仓库，Helm Chart Path 填：`env0-helm`。

## env0 变量

在 Helm Template 的 Variables 中设置：

`ENV0_HELM_SET_image.repository=ghcr.io/<GitHub用户名>/python-xray-argo`

常用运行变量直接对应 `env0-helm/values.yaml` 的 `env` / `secretEnv`。

建议至少设置：

- `ARGO_DOMAIN` + `ARGO_AUTH`：使用 Cloudflare 固定 Tunnel。两项必须一起设置。
- 或两者留空：程序会使用 Cloudflare Quick Tunnel。
- `UUID`：建议改成你自己的 UUID。
- `NAME`：节点名称前缀。

`NEZHA_KEY`、`ARGO_AUTH`、`BOT_TOKEN` 等凭证请在 env0 标记为 Sensitive。env0 官方文档说明敏感变量会加密存储并在日志中脱敏。

## 默认服务

默认只创建一个 `LoadBalancer` TCP Service，端口 `3000`，用于访问：

`http://<LoadBalancer地址>/sub`

程序自己的 Xray/Cloudflared 端口留在 Pod 内部，其中 Cloudflared 主动向外连接，因此无需把 `8001` 暴露到 Kubernetes Service。

## 注意

如果开启 `REALITY_PORT`、`HY2_PORT` 或 `S5_PORT`，这些协议是“直接入站”模式，不能仅依赖默认的 3000 LoadBalancer。需要另外为这些端口建立 Kubernetes Service，并把 `PUBLIC_HOST` 设置为实际对外可访问的 IP/域名；当前 Helm 默认配置不启用这些直连端口。

## 本地检查

`python -m py_compile app.py`

`docker build -t python-xray-argo:test .`

如部署后要确认订阅：

`curl -fsS http://<LoadBalancer地址>/sub`
