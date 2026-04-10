# 📦 AWS Supply Chain Control Tower

A production-grade, AI-powered supply chain management platform built entirely on AWS from scratch. This project is being built in phases, with each project independently deployable and designed to integrate into a unified **Supply Chain Control Tower**.

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://docker.com)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)](https://terraform.io)
[![CI/CD](https://img.shields.io/badge/CI/CD-CodePipeline-green?logo=amazon-aws)](https://aws.amazon.com/codepipeline)
[![Security](https://img.shields.io/badge/Security-API%20Key%20Auth-red?logo=amazon-aws)](https://aws.amazon.com)

---

## 🌐 Live Demo

| Resource | URL |
|----------|-----|
| **Dashboard** | https://d3knwbrcu1kxhj.cloudfront.net |
| **Inventory API** | https://ityntliklc.execute-api.ca-central-1.amazonaws.com/Inventory |
| **Forecast API** | https://ityntliklc.execute-api.ca-central-1.amazonaws.com/Forecasts |

> **Note:** API requires `x-api-key` header for authentication

---

## 🗺️ Project Roadmap

| Phase | Project | Status | Description |
|-------|---------|--------|-------------|
| 1 | Inventory Tracking System | ✅ Complete | Real-time inventory management with full CRUD |
| 2 | Demand Forecasting System | ✅ Complete | AI-powered demand predictions + stockout alerts |
| 3 | Safety Stock Optimizer | 🔵 Next | Optimal buffer stock calculation |
| 4 | PO Auto Generator | 🟡 Planned | Automated purchase order generation |
| Final | AI Control Tower | 🔮 Vision | Unified AI dashboard with AWS Bedrock |

---

## 🏗️ Architecture

```
Internet
    ↓
CloudFront (HTTPS + CDN + WAF)
    ↓
S3 (Static Dashboard — Inventory + Forecasting tabs)
    ↓
API Gateway (HTTP API — authenticated with Lambda Authorizer)
    ↓
┌──────────────────────────────────────────┐
│  Inventory Lambda  │  Forecast Lambda     │
│  (CRUD operations) │  (demand predictions)│
└──────────────────────────────────────────┘
    ↓
RDS PostgreSQL (Private Subnet)
├── inventory table
├── inventory_transactions table
├── forecasts table
├── suppliers table
├── safety_stock table
└── purchase_orders table

Security:
✅ Lambda Authorizer — API key authentication
✅ WAF — Web Application Firewall
✅ Private subnets — RDS never publicly accessible
✅ Security group chaining
✅ HTTPS enforced everywhere
✅ Secrets Manager for credentials
```

### AWS Services Used

| Service | Purpose |
|---------|---------|
| **Lambda** | Inventory API + Forecast engine (Python 3.11, Docker) |
| **RDS PostgreSQL** | Primary database (private subnet) |
| **API Gateway** | REST API with Lambda authorizer |
| **S3** | Dashboard hosting + Terraform state |
| **CloudFront** | CDN + HTTPS + WAF |
| **ECR** | Docker container registry (3 images) |
| **CodePipeline** | CI/CD orchestration |
| **CodeBuild** | Docker build + automated deployment |
| **VPC** | Network isolation (public + private subnets, 2 AZs) |
| **NAT Gateway** | Outbound internet for private resources |
| **IAM** | Roles and permissions |
| **Secrets Manager** | Secure credential storage |

---

## ✨ Features

### Project 1 — Inventory Tracking
- **Full CRUD operations** — Add, view, edit, delete inventory items
- **Rich item fields** — SKU, category, reorder point, lead time
- **Real-time dashboard** — Stock charts, value distribution, metrics
- **Low stock alerts** — Automatic warnings based on reorder points
- **Transaction tracking** — Every stock movement recorded automatically

### Project 2 — Demand Forecasting
- **Stockout predictions** — Days until each item runs out
- **Demand forecasting** — 30, 60, 90 day projections
- **Confidence scoring** — Based on transaction history volume
- **Reorder recommendations** — Automatic reorder alerts
- **Trend detection** — Increasing, decreasing, or stable demand
- **One-click forecast** — Run new forecasts anytime from dashboard

---

## 📊 Dashboard

The live dashboard features two tabs:

**Inventory Tab:**
- Stock levels bar chart per product
- Value distribution doughnut chart
- Metric cards (total products, units, value, alerts)
- Full inventory table with Edit and Delete buttons
- Add new item form with all fields

**Demand Forecasting Tab:**
- Stockout prediction cards (Critical/Warning/OK)
- Days until stockout per item
- Daily demand estimates
- 30 and 60 day demand forecasts
- Confidence percentage per forecast
- Run Forecast button to trigger new analysis

---

## 🗂️ Project Structure

```
inventory-tracking-system/
├── lambda_function.py          # Inventory Lambda (CRUD v4)
├── forecast_function.py        # Forecast Lambda (demand predictions)
├── authorizer_function.py      # API Key authorizer Lambda
├── Dockerfile                  # Inventory Lambda container
├── Dockerfile.forecast         # Forecast Lambda container
├── Dockerfile.authorizer       # Authorizer Lambda container
├── buildspec.yml               # CodeBuild CI/CD config
├── index.html                  # Dashboard (Inventory + Forecasting tabs)
├── inventory-terraform/        # Terraform IaC
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules.tf
│   └── modules/
│       ├── vpc/
│       ├── rds/
│       ├── lambda/
│       ├── apigateway/
│       ├── s3/
│       └── cloudfront/
└── README.md
```

---

## 🛠️ Tech Stack

**Backend**
- Python 3.11
- psycopg2-binary (PostgreSQL driver)
- AWS Lambda (3 functions — inventory, forecast, authorizer)
- AWS API Gateway (HTTP API with Lambda authorizer)

**Database**
- PostgreSQL 16.6 on AWS RDS
- Private subnet — not publicly accessible
- 6 tables supporting all 4 projects

**Frontend**
- Vanilla HTML/CSS/JavaScript
- Chart.js for visualizations
- DM Sans + DM Mono fonts
- Two-tab layout (Inventory + Forecasting)

**Security**
- Lambda authorizer with API key
- WAF protection
- HTTPS enforced via CloudFront
- RDS in private subnet

**Infrastructure**
- Terraform 1.5.7
- Docker (linux/amd64)
- AWS ECR (3 repositories)

**CI/CD**
- GitHub (source control)
- AWS CodePipeline (orchestration)
- AWS CodeBuild (build + deploy)

---

## 📡 API Reference

**Base URL:** `https://ityntliklc.execute-api.ca-central-1.amazonaws.com`

**Required Header:** `x-api-key: <your-api-key>`

### Inventory Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/Inventory` | Get all inventory items |
| POST | `/Inventory` | Add new item |
| PUT | `/Inventory/{id}` | Update existing item |
| DELETE | `/Inventory/{id}` | Delete item |

### Forecast Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/Forecasts` | Get all forecasts |
| POST | `/Forecasts` | Run new forecast analysis |

---

## 🗄️ Database Schema

```sql
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL, price DECIMAL(10,2) NOT NULL,
    sku VARCHAR(100), reorder_point INTEGER DEFAULT 5,
    lead_time_days INTEGER DEFAULT 7, supplier_id INTEGER,
    last_updated TIMESTAMP DEFAULT NOW(), category VARCHAR(100)
);

CREATE TABLE inventory_transactions (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventory(id),
    transaction_type VARCHAR(50), quantity INTEGER,
    timestamp TIMESTAMP DEFAULT NOW(), notes TEXT
);

CREATE TABLE forecasts (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventory(id),
    forecast_date DATE, predicted_demand DECIMAL(10,2),
    confidence_score DECIMAL(5,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL,
    email VARCHAR(255), phone VARCHAR(50),
    lead_time_days INTEGER DEFAULT 7, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE safety_stock (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventory(id),
    optimal_quantity INTEGER, calculated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventory(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    quantity INTEGER, status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    expected_delivery DATE, notes TEXT
);
```

---

## ⚙️ Infrastructure Deployment

```bash
git clone https://github.com/okwei50/inventory-tracking-system.git
cd inventory-tracking-system/inventory-terraform
terraform init
terraform plan
terraform apply
```

---

## 🔒 Security

- ✅ Lambda authorizer — every API request requires valid key
- ✅ RDS in private subnet — never publicly accessible
- ✅ Lambda in private subnet with NAT Gateway
- ✅ Security groups chained — least privilege access
- ✅ CloudFront WAF — common vulnerability protection
- ✅ HTTPS enforced — HTTP redirects to HTTPS
- ✅ Secrets Manager — no credentials in code
- ✅ Password rotation — RDS password changed regularly

---

## 🧩 Key Challenges Solved

| Challenge | Solution |
|-----------|---------|
| RDS in wrong VPC | Snapshot → restore into correct VPC |
| psycopg2 Mac vs Linux | Build with `--platform manylinux2014_x86_64` |
| RDS requires 2 AZs | Created subnets in ca-central-1a and ca-central-1b |
| Docker platform mismatch | `--platform linux/amd64 --provenance=false` |
| Lambda Zip → Image conversion | Created new function with `--package-type Image` |
| CI/CD async Lambda update | Added `aws lambda wait function-updated` |
| Wrong CloudFront distribution | Used `aws cloudfront list-distributions` to verify |
| Open API security risk | Lambda authorizer with API key authentication |
| Exposed DB credentials | Password rotation + Secrets Manager |

---

## 🔮 What's Next

### Project 3 — Safety Stock Optimizer
- Read from `forecasts` and `inventory` tables
- Calculate optimal buffer stock using demand variability + lead time
- Update `safety_stock` table automatically
- EventBridge trigger when stock drops below reorder point

### Project 4 — Purchase Order Auto Generator
- AWS Step Functions orchestration
- Auto-generate purchase orders
- Send PO via AWS SES email to suppliers

### Final — AI Supply Chain Control Tower
- **AWS Bedrock (Claude AI)** — conversational interface
- **Unified dashboard** — all 4 systems in one view
- **EventBridge** — events flow between all projects
- **AI recommendations** — predictive reordering and alerts

---

## 👤 Author

Built by **Kweku** — Cloud Infrastructure Developer specializing in building AI-powered supply chain systems on AWS.

🔗 GitHub: [@okwei50](https://github.com/okwei50)
🌐 Live: [https://d3knwbrcu1kxhj.cloudfront.net](https://d3knwbrcu1kxhj.cloudfront.net)
