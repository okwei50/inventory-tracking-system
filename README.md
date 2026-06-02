# Inventory Management System — Production AWS Platform

A production-grade, cloud-native inventory management system built from scratch on AWS, combining full-stack engineering, DevOps, and AI decision-making.

**Live Demo:** https://d3knwbrcu1kxhj.cloudfront.net
**Portfolio:** https://kwekuquaye.com
**GitHub:** https://github.com/okwei50/inventory-tracking-system

---

## Architecture

- **Backend:** Python/Flask, Node.js, REST APIs
- **Database:** PostgreSQL (AWS RDS)
- **Frontend:** React + CloudFront CDN
- **AI Layer:** Claude API (Anthropic) + LangChain
- **Infrastructure:** AWS Lambda, EC2, RDS, S3, CloudFront, API Gateway, DynamoDB, ECR, SES
- **DevOps:** Terraform, Docker, Kubernetes, CI/CD (CodePipeline + CodeBuild)
- **Observability:** Prometheus, Grafana, CloudWatch, Jaeger

---

## Roadmap

### ✅ Phase 1 — Backend (Lambda + RDS + API Gateway)
Fully serverless REST API handling real-time inventory CRUD, supplier management, purchase order automation, and sales recording.

### ✅ Phase 2 — Frontend (S3 + CloudFront + WAF)
React frontend with CDN delivery, HTTPS, and WAF protection. Deployed to S3 + CloudFront.

### ✅ Phase 3 — Terraform (IaC)
Entire infrastructure rebuilt as code — every AWS resource version controlled and reproducible.

### ✅ Phase 4 — Docker (Containerization)
All microservices containerized and pushed to AWS ECR private registry.

### ✅ Phase 5 — CI/CD (CodePipeline + CodeBuild)
Automated deployment pipeline — push to GitHub, pipeline builds and deploys automatically.

### ✅ Phase 6 — Microservices (4 Independent Services)
Split into 4 independently deployable services:
- Inventory API
- Purchase Orders
- Demand Forecasting
- Safety Stock Calculator

### ✅ Phase 7 — Portfolio Site (kwekuquaye.com)
Live portfolio on S3 + CloudFront + Route 53 with working contact form via Lambda + SES.

### ✅ Phase 8 — Darius AI Control Tower
AI assistant built on Claude API (Anthropic) with:
- DynamoDB session memory
- Intent detection
- Parallel data fetching across all 4 microservices
- Lambda + API Gateway + CloudFront delivery

### ✅ Phase 9 — Kubernetes (Minikube + ECR)
Full stack deployed into Kubernetes:
- 2 API replicas for high availability
- PostgreSQL pod for persistent storage
- ECR pull secret for private image authentication
- NodePort service exposing the API
- Full CRUD working end to end

### ⬜ Phase 10 — Service Mesh (Istio)
- mTLS encryption between all services
- Traffic management and canary deployments
- Circuit breakers and retries
- Distributed tracing integration

### ⬜ Phase 11 — Full Observability (Prometheus + Grafana + CloudWatch + Jaeger)
- Prometheus metrics scraping across all pods
- Grafana dashboards for visualization
- CloudWatch for AWS infrastructure monitoring
- Jaeger for distributed request tracing

### ⬜ Phase 12 — LangChain Decision Engine
Autonomous AI decision layer replacing basic intent detection with:
- Multi-step reasoning chains
- Tool calling across all 4 microservices
- Long-term decision memory
- RAG on historical inventory and PO data
- Autonomous workflow triggers

---

## Tech Stack

| Layer | Technology |
|---|---|
| Languages | Python, Node.js, TypeScript, JavaScript |
| Backend | Flask, Express.js, REST APIs |
| Database | PostgreSQL, AWS RDS, DynamoDB |
| Frontend | React, S3, CloudFront |
| AI | Claude API (Anthropic), LangChain |
| AWS | Lambda, EC2, RDS, S3, CloudFront, API Gateway, DynamoDB, ECR, SES, CodePipeline, CodeBuild |
| DevOps | Terraform, Docker, Kubernetes, CI/CD |
| Observability | Prometheus, Grafana, CloudWatch, Jaeger |

---

Built by Kweku Quaye — 9+ years supply chain & procurement, self-taught cloud & backend engineer.
