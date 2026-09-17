# env0 deployment

This repository is packaged as a Helm chart at the repository root.

## env0 template

Create a **Helm** template using Git as the chart source.
Set **Chart Path** to:

    .

Do not set it to `env0-helm`.

Connect the Kubernetes cluster to env0, then create the environment.

## Required variables

Set these according to your deployment:

- `ENV0_HELM_SET_env.UUID` — a UUID used by the application.
- `ENV0_HELM_SET_env.NAME` — node name.
- `ENV0_HELM_SET_env.ARGO_DOMAIN` — optional Cloudflare Tunnel hostname.
- `ENV0_HELM_SET_secretEnv.ARGO_AUTH` — optional Cloudflare Tunnel token.

The default Kubernetes Service is `ClusterIP` so the chart does not require a cloud load balancer.

## Optional ingress

Enable with:

    ENV0_HELM_SET_ingress.enabled=true

Then configure the ingress controller/class and hostname in Helm values.

## Important

The application image defaults to the public `python:3.12-slim` image. The chart copies `files/app.py` and `files/requirements.txt` into a ConfigMap, so no GHCR image or registry secret is required.
