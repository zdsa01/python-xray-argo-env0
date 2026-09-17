# env0 部署

此版本不依赖 GHCR 镜像。Helm Chart 内已经包含 `app.py` 和 `requirements.txt`，Pod 启动时使用公开的 `python:3.12-slim`，安装运行依赖后直接启动应用。

这样 env0 部署时不再需要 GitHub Actions、私有镜像凭据或 Container Registry。

## env0 Template

创建 **Helm Template**，VCS 使用 GitHub，Chart Path：

`env0-helm`

env0 会执行 Helm Diff 和 Helm Upgrade；env0 的 `ENV0_HELM_SET_<name>` 变量会传给 Helm 的 `--set`。

## 必填/推荐变量

推荐至少设置：

`ENV0_HELM_SET_env.UUID=<UUID>`

`ENV0_HELM_SET_env.NAME=env0-xray`

固定 Cloudflare Tunnel：

`ENV0_HELM_SET_env.ARGO_DOMAIN=<域名>`

`ENV0_HELM_SET_secretEnv.ARGO_AUTH=<Tunnel Token>`

将 `ARGO_AUTH` 在 env0 中设置为 Sensitive。

也可以把 `ARGO_DOMAIN` / `ARGO_AUTH` 留空，应用尝试使用 Cloudflare Quick Tunnel。

## Kubernetes 要求

Chart 默认创建 `ClusterIP` Service，不要求云厂商提供 `LoadBalancer`。

Pod 需要能够访问公网 HTTPS，至少包括：

- `pypi.org`：安装 Python 依赖
- Cloudflare API / Tunnel 网络
- Xray / Cloudflared 二进制下载源

如果集群不能访问公网，应用无法完成初始化。

## 访问订阅

Service：`3000`。

应用路径：`/{SUB_PATH}`，默认就是 `/sub`。

如果使用固定 Cloudflare Tunnel，Tunnel 把 `ARGO_PORT=8001` 转到 Pod 内 Xray。

如果需要从 Kubernetes Ingress 暴露订阅 HTTP：

`ENV0_HELM_SET_ingress.enabled=true`

同时设置 Ingress host/class。

## 探针

`/healthz` 仅表示 Python HTTP 进程正常。

`/readyz` 只有成功生成节点订阅后才返回 200。

如果 Xray/Cloudflared 下载失败、Cloudflare Tunnel 建立失败或最终没有生成可用节点，启动流程会返回失败并让 Kubernetes 重启 Pod，而不是假装部署成功。

## env0 日志排错

`ImagePullBackOff`：本版本默认是 `python:3.12-slim`，检查 Kubernetes 节点是否能访问 Docker Hub。

`Readiness probe failed`：执行 `kubectl logs <pod>`，重点检查 pip、Cloudflare 和二进制下载错误。

`CrashLoopBackOff`：执行 `kubectl logs <pod> --previous` 获取上一次启动失败原因。
