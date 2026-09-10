# Kubernetes Infrastructure

## Local Development Cluster

The platform uses a local Kubernetes cluster for development and testing.

The local cluster is currently implemented using [kind](https://kind.sigs.k8s.io/),
which runs Kubernetes nodes as Docker containers.

## Cluster Configuration

| Property | Value |
|---|---|
| Cluster name | `platform-dev` |
| Kubernetes version | `v1.34.0` |
| Provider | kind |
| Runtime | Docker |
| Nodes | 1 control-plane node |
| Environment | Local development |

## Current Architecture

```text
MacBook
   |
   v
 Docker
   |
   v
 kind
   |
   v
 Kubernetes
   |
   v
platform-dev-control-plane
```

## Verify the Cluster

Check the current Kubernetes context:

```bash
kubectl config current-context
```

Expected:

```text
kind-platform-dev
```

Check node health:

```bash
kubectl get nodes
```

Expected status:

```text
NAME                         STATUS   ROLES
platform-dev-control-plane   Ready    control-plane
```

Check all Kubernetes system workloads:

```bash
kubectl get pods -A
```

## Purpose

The local cluster provides a low-cost environment for developing and testing
the platform before deploying components to AWS EKS.

The initial platform components will be deployed to this cluster before
introducing AWS infrastructure.

## Future Evolution

The local environment will eventually be complemented by AWS environments:

```text
Local Development
       |
       v
      kind
       |
       v
AWS Development
       |
       v
      EKS
       |
       v
AWS Production
       |
       v
      EKS
```

The local environment is not intended to reproduce the complete production
infrastructure. Its purpose is to provide a fast and inexpensive development
environment for the platform.