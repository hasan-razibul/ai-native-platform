# AI-Native Internal Developer Platform

## 1. Overview

This project is a production-inspired **Internal Developer Platform (IDP)**
built to give developers a self-service way to deploy applications, provision
infrastructure, use the platform's observability stack, and get help with
operational issues.

The platform follows a **GitOps-based architecture** and uses Kubernetes as
the application runtime.

The primary goals are:

- Self-service application creation
- Standardized deployment workflows
- Infrastructure provisioning
- GitOps-based delivery
- Built-in observability
- Security and policy enforcement
- AI-assisted platform operations
- AI-assisted incident troubleshooting

The idea is to build something that resembles a platform an engineering team
could actually use, rather than just deploying a collection of DevOps tools.

---

## 2. Design Principles

### 2.1 Developer Self-Service

A developer should be able to create and operate a service without needing
the platform team to handle routine infrastructure work manually.

The platform should provide standardized **golden paths** for common
workloads, for example:

- Python APIs
- Go APIs
- Background workers
- Scheduled jobs
- Services requiring PostgreSQL
- Services requiring Redis
- Services requiring object storage

---

### 2.2 GitOps

Kubernetes desired state should live in Git and be continuously reconciled
by Argo CD.

Deployments should normally go through GitOps instead of direct imperative
commands such as:

```bash
kubectl apply -f deployment.yaml
```

Instead, the desired workflow is:

```text
Git Repository
      |
      v
   Argo CD
      |
      v
 Kubernetes
```

This provides:

- Auditable changes
- Version-controlled configuration
- Automatic drift detection
- Automatic reconciliation
- Easy rollback
- Clear ownership of desired state

---

### 2.3 Secure by Default

Applications should get the basic security and operational defaults
without every team having to configure them from scratch.

Developers should not have to remember every requirement for:

- Resource limits
- Security contexts
- Health probes
- Network policies
- Approved container registries
- Required metadata
- Image security
- Observability

These requirements should be enforced through policy rather than relying on
every developer to remember them.

---

### 2.4 Platform APIs Over Direct Infrastructure Access

Developers and AI agents should interact with platform capabilities through
well-defined APIs rather than directly accessing Kubernetes or cloud
infrastructure.

For example,

```text
Developer
    |
    v
Platform API
    |
    v
Terraform / Kubernetes / Git
```

The platform API provides the boundary between developers and the
underlying infrastructure.

---

### 2.5 AI With Guardrails

AI-generated actions should first be turned into structured intents and
validated before anything is executed.

The AI agent must not have unrestricted access to:

- Kubernetes
- AWS
- Terraform
- Production databases
- Secrets

The intended flow is:

```text
Natural Language
      |
      v
     LLM
      |
      v
Structured Intent
      |
      v
Policy Validation
      |
      v
Platform API
      |
      v
Controlled Action
```

---

### 2.6 Observable by Default

Applications created through the platform should automatically get:

- Metrics
- Logs
- Traces
- Health checks
- Dashboards
- Alerting integration

Developers should not need to manually configure the complete observability
stack for every new service.

---

## 3. High-Level Architecture

The platform is split into a few main layers.

```text
                              Developer
                                  |
                                  v
                       +----------------------+
                       |      Backstage       |
                       |   Developer Portal   |
                       +----------+-----------+
                                  |
                                  v
                       +----------------------+
                       | Platform API / AI    |
                       |       Agent          |
                       +----------+-----------+
                                  |
                    +-------------+-------------+
                    |             |             |
                    v             v             v
                 GitHub       Terraform      Policies
                    |             |             |
                    |             v             |
                    |            AWS           |
                    |                           |
                    +-------------+-------------+
                                  |
                                  v
                         GitOps Repository
                                  |
                                  v
                       +----------------------+
                       |       Argo CD        |
                       |   GitOps Controller  |
                       +----------+-----------+
                                  |
                                  v
                       +----------------------+
                       |    Kubernetes / EKS  |
                       +----------+-----------+
                                  |
                 +----------------+----------------+
                 |                |                |
                 v                v                v
               APIs            Workers          Databases
                 |
                 v
        +----------------------+
        |   OpenTelemetry      |
        +----------+-----------+
                   |
          +--------+--------+
          |        |        |
          v        v        v
     Prometheus   Loki     Tempo
          |        |        |
          +--------+--------+
                   |
                   v
                Grafana
                   |
                   v
             AI SRE Agent
```

---

## 4. Platform Components

| Component | Purpose |
|-----------|---------|
| Backstage | Developer portal and self-service interface |
| Platform API | Backend API exposing platform capabilities |
| AI Agent | Natural-language interface and operational assistant |
| GitHub | Source code and configuration management |
| GitHub Actions | Continuous integration and automation |
| Terraform | Cloud infrastructure provisioning |
| Kubernetes | Application runtime |
| Helm | Kubernetes application packaging |
| Argo CD | GitOps continuous delivery |
| Kyverno | Kubernetes policy enforcement |
| Vault | Secret management |
| OpenTelemetry | Telemetry collection and instrumentation |
| Prometheus | Metrics collection |
| Loki | Log aggregation |
| Tempo | Distributed tracing |
| Grafana | Observability dashboards |
| AWS EKS | Production Kubernetes runtime |
| Karpenter | Kubernetes node autoscaling |
| HPA / KEDA | Application and workload autoscaling |
| Amazon ECR | Container image registry |

---

## 5. Application Lifecycle

The platform is intended to cover the application lifecycle from service
creation through deployment and day-to-day operations.

The intended developer workflow is:

1. Open Backstage.
2. Select **Create Service**.
3. Select the application type.
4. Select required capabilities.
5. Platform generates a standardized repository.
6. CI pipeline validates the application.
7. Security checks are performed.
8. Container image is built.
9. Container image is pushed to the registry.
10. GitOps configuration is generated or updated.
11. Argo CD detects the desired state.
12. Kubernetes deploys the application.
13. Policies validate the workload.
14. Observability is automatically configured.
15. Backstage displays service ownership and operational information.

The idea is to turn:

```text
"Create a new service"
```

into a standardized production-ready workflow.

---

## 6. AI Platform Workflow

The AI agent provides a natural-language interface to platform capabilities.

For example, a developer could ask:

> Create a Python API called payments-api with PostgreSQL, Redis,
> autoscaling and internal networking.

The AI should **not** turn this request directly into arbitrary shell commands.

Instead, the workflow should be:

```text
Natural Language Request
          |
          v
        LLM
          |
          v
   Structured Intent
          |
          v
   Policy Validation
          |
      +---+---+
      |       |
    Reject   Approve
              |
              v
        Platform API
              |
       +------+------+------+
       |      |      |      |
       v      v      v      v
     GitHub Terraform K8s  GitOps
```

For example, the natural-language request could be converted into:

```json
{
  "action": "create_service",
  "name": "payments-api",
  "runtime": "python",
  "database": "postgresql",
  "cache": "redis",
  "autoscaling": true,
  "exposure": "internal"
}
```

The platform then checks the request against predefined policies.

Only approved capabilities can be executed by the platform.

---

## 7. AI Incident Troubleshooting

The platform will eventually include an AI SRE agent that can help investigate
application incidents.

The agent can use operational context from:

- Kubernetes
- Argo CD
- Prometheus
- Loki
- Git
- Helm
- Deployment history
- Application metadata

For example, a developer could ask:

> Why is payments-api unhealthy?

The AI agent should correlate:

- Pod status
- Kubernetes events
- Restart counts
- OOMKilled events
- CPU usage
- Memory usage
- Application logs
- Recent deployments
- Git changes
- Helm configuration
- Argo CD synchronization status

The result should be a structured diagnosis.

Example:

```text
Diagnosis:
payments-api is experiencing OOMKilled events.

Evidence:
- 4 container restarts
- Memory usage reached 94%
- Container memory limit is 256Mi
- Previous deployment used a 512Mi limit
- Configuration changed 8 minutes ago
- Argo CD successfully deployed the new configuration

Confidence:
91%

Recommended action:
Rollback to the previous GitOps revision.

Risk:
LOW
```

The AI should recommend an action before changing anything.

Actions that could cause a significant or destructive change should require
explicit human approval.

---

## 8. Security Model

Security is based on **least privilege, policy enforcement and controlled
automation**.

The platform will use:

- Kubernetes RBAC
- AWS IAM
- HashiCorp Vault
- Kyverno
- NetworkPolicies
- Container image scanning
- SBOM generation
- Image signing
- GitHub branch protection
- GitOps
- Audit logging

### 8.1 AI Security

AI agents will not receive unrestricted `cluster-admin` access.

Instead:

```text
AI Agent
    |
    v
Structured Intent
    |
    v
Policy Engine
    |
    v
Platform API
    |
    v
Approved Operation
```

This provides a controlled boundary between AI reasoning and infrastructure
execution.

---

## 9. Kubernetes Policy

Kyverno will enforce platform-wide requirements.

Example policies may require:

- CPU and memory requests
- CPU and memory limits
- Non-root containers
- Security context
- Readiness probes
- Liveness probes
- Required labels
- Required ownership metadata
- Approved image registries
- NetworkPolicies
- Standard observability configuration

For example,

```text
Developer creates workload
          |
          v
       Kubernetes
          |
          v
       Kyverno
          |
      +---+---+
      |       |
    Reject   Allow
```

The goal is to make the secure path the easiest path.

---

## 10. Observability

Observability will be part of the platform instead of something each
application has to build from scratch.

The intended flow is:

```text
Applications
     |
     v
OpenTelemetry
     |
     +-------------------+
     |         |         |
     v         v         v
 Metrics     Logs     Traces
     |         |         |
     v         v         v
Prometheus   Loki      Tempo
     |         |         |
     +---------+---------+
               |
               v
            Grafana
```

A service created through the platform should eventually have:

- Application metrics
- Request latency
- Request rate
- Error rate
- Container CPU usage
- Container memory usage
- Logs
- Distributed traces
- Health status
- Deployment information
- Dashboard links

Backstage can then provide a central view of the service.

---

## 11. Infrastructure Provisioning

Terraform will be used primarily for cloud infrastructure.

The target AWS architecture includes:

```text
                         AWS
                          |
          +---------------+---------------+
          |                               |
          v                               v
         VPC                             ECR
          |
          v
         EKS
          |
    +-----+-----+
    |           |
    v           v
 Karpenter   Kubernetes
                |
        +-------+-------+
        |       |       |
        v       v       v
       API   Workers  Platform
                       Services
```

Infrastructure that may eventually be provisioned using Terraform includes:

- VPC
- Subnets
- EKS
- IAM
- ECR
- RDS
- S3
- ElastiCache
- CloudWatch integration
- Security groups
- KMS
- Route 53
- Load balancers

Terraform will provision infrastructure while Argo CD manages Kubernetes
application state.

---

## 12. Environments

The project will initially use a local Kubernetes environment for development.

The progression will be:

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

This keeps most of the early development work independent of AWS costs.

AWS infrastructure can be introduced once the core platform workflow is
working reliably on the local cluster.

---

## 13. Repository Structure

The repository is split into a few areas based on responsibility.

```text
ai-native-platform/
│
├── README.md
├── LICENSE
│
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── runbooks/
│   └── threat-model/
│
├── platform/
│   ├── backstage/
│   ├── platform-api/
│   └── ai-agent/
│
├── infrastructure/
│   ├── terraform/
│   └── kubernetes/
│
├── gitops/
│   ├── applications/
│   └── environments/
│
├── policies/
│   └── kyverno/
│
├── observability/
│   ├── otel/
│   ├── prometheus/
│   ├── loki/
│   ├── tempo/
│   └── grafana/
│
├── services/
│   └── examples/
│
└── .github/
    └── workflows/
```

### Directory Responsibilities

| Directory | Responsibility |
|-----------|----------------|
| `docs/` | Architecture, decisions, runbooks and security documentation |
| `platform/backstage/` | Backstage developer portal |
| `platform/platform-api/` | Platform backend API |
| `platform/ai-agent/` | AI platform and SRE agents |
| `infrastructure/terraform/` | AWS infrastructure |
| `infrastructure/kubernetes/` | Kubernetes platform components |
| `gitops/` | Application desired state |
| `policies/kyverno/` | Kubernetes security and governance policies |
| `observability/` | Monitoring, logging and tracing configuration |
| `services/examples/` | Example applications used to demonstrate the platform |
| `.github/workflows/` | CI and repository automation |

---

## 14. Initial Implementation Strategy

The platform will be built in small, working stages rather than all at once.

### Phase 1 - Kubernetes Foundation

Build the local platform environment.

Components:

- kind
- Kubernetes
- Helm
- Argo CD

Goal:

```text
Git
 |
 v
Argo CD
 |
 v
Kubernetes
 |
 v
Application
```

---

### Phase 2 - Golden Path

Add Backstage.

Build the first service template.

Goal:

```text
Developer
    |
    v
Backstage
    |
    v
Create Service
    |
    v
GitHub Repository
```

---

### Phase 3 - CI/CD

Introduce GitHub Actions.

Pipeline:

```text
Code
 |
 v
Tests
 |
 v
Lint
 |
 v
Security Scan
 |
 v
SBOM
 |
 v
Container Build
 |
 v
Container Registry
```

---

### Phase 4 - GitOps Application Lifecycle

Connect CI/CD with the GitOps repository and Argo CD.

Goal:

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    v
Container Registry
    |
    v
GitOps Repository
    |
    v
Argo CD
    |
    v
Kubernetes
```

---

### Phase 5 - Infrastructure Provisioning

Introduce Terraform.

Developers should eventually be able to request infrastructure such as:

- PostgreSQL
- Redis
- S3
- Kafka
- AWS resources

Approved requests can then be translated into Terraform configuration and
applied through the normal infrastructure change process.

---

### Phase 6 - Security and Policy

Introduce:

- Kyverno
- Vault
- RBAC
- NetworkPolicies
- Trivy
- SBOM
- Cosign

Security should be part of the golden paths instead of another set of steps
developers have to remember.

---

### Phase 7 - Observability

Introduce:

- OpenTelemetry
- Prometheus
- Loki
- Tempo
- Grafana

Every application generated by the platform should receive the same basic
observability setup.

---

### Phase 8 - Platform API

Build a backend API that provides controlled platform capabilities.

For example,

```text
POST /services
POST /databases
POST /caches
POST /deployments
GET  /services/{name}
GET  /services/{name}/status
```

The API becomes the controlled interface between the developer portal and
the underlying automation.

---

### Phase 9 - AI Platform Assistant

Introduce an AI agent capable of understanding natural-language platform
requests.

Example:

```text
"Create a Go API called inventory-service
with PostgreSQL and autoscaling."
```

The AI converts this into a structured platform request.

---

### Phase 10 - AI SRE Agent

Introduce an AI agent capable of investigating operational problems.

Example:

```text
"Why is inventory-service failing?"
```

The agent correlates:

- Kubernetes
- Git
- Argo CD
- Metrics
- Logs
- Traces
- Deployment history

and produces a diagnosis and recommended action.

---

### Phase 11 - AWS Production Architecture

Move the platform from local Kubernetes to AWS EKS.

Introduce:

- VPC
- EKS
- IAM
- ECR
- RDS
- Karpenter
- AWS networking
- Load balancing
- Security controls
- Cost controls

By this point, the architecture should be close enough to a real production
platform that the design and operational trade-offs are meaningful.

---

## 15. Target Developer Experience

The intended end-to-end developer workflow is:

```text
Developer

"Create a Python payments API with PostgreSQL,
Redis, autoscaling and observability."

                    |
                    v

              Backstage
                    |
                    v
             Platform Agent
                    |
                    v
          Structured Platform Plan
                    |
                    v
             Policy Validation
                    |
                    v
              GitHub Repository
                    |
                    v
                CI Pipeline
                    |
                    v
              Container Image
                    |
                    v
               GitOps Commit
                    |
                    v
                 Argo CD
                    |
                    v
                  EKS
                    |
                    v
          Running Production Service
                    |
                    v
       Metrics / Logs / Traces
                    |
                    v
                 Grafana
                    |
                    v
               AI SRE Agent
```

The point of the project is to demonstrate a realistic **platform engineering
system**, not just a collection of isolated DevOps tools.

The project is intended to demonstrate practical experience with:

- Platform engineering
- Kubernetes
- AWS
- Infrastructure as Code
- GitOps
- CI/CD
- Developer self-service
- Security engineering
- Observability
- AI agents
- LLM integration
- Automated operations
- Infrastructure automation
- Production architecture
---

## 16. Practical Trade-offs

This architecture deliberately keeps a few boundaries clear.

### GitOps vs. Infrastructure Provisioning

Terraform is responsible for cloud infrastructure, while Argo CD manages
Kubernetes application state. Keeping those responsibilities separate makes it
easier to understand what changed and which system is responsible for applying
it.

The platform API may eventually trigger both workflows, but it should not
bypass them.

### AI Starts Read-Only

The first version of the AI SRE agent should focus on investigation and
recommendations. It can read metrics, logs, deployment history and Kubernetes
state, but it should not make production changes automatically.

Once the read-only workflow is reliable, selected actions can be introduced
behind explicit policies and approval.

### Local Development vs. AWS

kind is useful for developing the platform itself, but it cannot reproduce every
AWS-specific behavior. EKS, IAM, load balancing, networking and AWS-managed
services need to be tested separately once the core workflow is stable.

The goal is not to pretend that a local cluster is identical to production.
It is to keep the early feedback loop fast and inexpensive.

### Backstage Is Not the Control Plane

Backstage provides the developer-facing interface. It should not become the
place where infrastructure logic is implemented.

The platform API and the underlying automation remain responsible for the
actual platform operations. This keeps the developer portal replaceable and
makes the platform capabilities usable by other clients, including the AI
agent.

### Build the Smallest Useful Version First

The project contains several advanced components, but they do not all need to
exist on day one. A working path from Git to Kubernetes is more valuable than
having every component installed without a complete workflow.

The implementation should therefore prioritize a small end-to-end path first
and add capabilities as that path becomes reliable.
