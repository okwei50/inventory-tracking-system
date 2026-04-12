# 📦 AWS Supply Chain Control Tower

A production-grade, AI-powered supply chain management platform built entirely on AWS from scratch. Built in phases, each project independently deployable and designed to integrate into a unified **Supply Chain Control Tower**.

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
| **Safety Stock API** | https://ityntliklc.execute-api.ca-central-1.amazonaws.com/SafetyStock |

> **Note:** API requires `x-api-key` header for authentication

---

## 🗺️ Project Roadmap

| Phase | Project | Status | Description |
|-------|---------|--------|-------------|
| 1 | Inventory Tracking System | ✅ Complete | Real-time inventory management with full CRUD |
| 2 | Demand Forecasting System | ✅ Complete | AI-powered demand predictions + stockout alerts |
| 3 | Safety Stock Optimizer | ✅ Complete | Optimal buffer stock calculation per item |
| 4 | PO Auto Generator | 🔵 Next | Automated purchase order generation |
| Final | AI Control Tower | 🔮 Vision | Unified AI dashboard with AWS Bedrock |

---

## 🏗️ Architecture

```
Internet
    ↓
CloudFront (HTTPS + CDN + WAF)
    ↓
S3 (Static Dashboard — 3 tabs)
    ↓
API Gateway (HTTP API — Lambda Authorizer)
    ↓
┌─────────────────────────────────────────────────┐
│ Inventory Lambda │ Forecast Lambda │ SafetyStock │
│ (CRUD)          │ (predictions)   │ Lambda      │
└─────────────────────────────────────────────────┘
    ↓
RDS PostgreSQL (Private Subnet)
├── inventory
├── inventory_transactions
├── forecasts
├── safety_stock
├── suppliers
└── purchase_orders
```

### AWS Services Used

| Service | Purpose |
|---------|---------|
| **Lambda** | 4 functions — inventory, forecast, safetystock, authorizer |
| **RDS PostgreSQL** | Primary database (private subnet) |
| **API Gateway** | REST API with Lambda authorizer |
| **S3** | Dashboard hosting + Terraform state |
| **CloudFront** | CDN + HTTPS + WAF |
| **ECR** | Docker container registry (4 images) |
| **CodePipeline** | CI/CD orchestration |
| **CodeBuild** | Docker build + automated deployment |
| **VPC** | Public + private subnets across 2 AZs |
| **NAT Gateway** | Outbound internet for private resources |
| **IAM** | Roles and permissions |
| **Secrets Manager** | Secure credential storage |

---

## ✨ Features

### Project 1 — Inventory Tracking ✅
- Full CRUD — Add, view, edit, delete inventory items
- Rich fields — SKU, category, reorder point, lead time
- Real-time dashboard — Stock charts, value distribution, metrics
- Low stock alerts — Automatic warnings based on reorder points
- Transaction tracking — Every stock movement recorded automatically

### Project 2 — Demand Forecasting ✅
- Stockout predictions — Days until each item runs out
- Demand forecasting — 30, 60, 90 day projections
- Confidence scoring — Based on transaction history volume
- Reorder recommendations — Automatic reorder alerts
- Trend detection — Increasing, decreasing, or stable demand

### Project 3 — Safety Stock Optimizer ✅
- Optimal buffer stock — Calculated using demand variability + lead time
- Service level selector — 90%, 95%, or 99% fill rate
- Auto-update reorder points — Safety stock feeds back into inventory
- Statistical formula — Z-score × σ(demand) × √(lead_time)
- Confidence scoring — Based on transaction data volume

---

## 📊 Dashboard

Three tabs powered by live AWS data:

**Tab 1 — Inventory:**
- Stock levels bar chart + value doughnut chart
- Metric cards (products, units, value, alerts)
- Full inventory table with Edit and Delete buttons
- Add new item form

**Tab 2 — Demand Forecasting:**
- Stockout prediction cards (Critical/Warning/OK)
- Days until stockout per item
- 30 and 60 day demand forecasts
- Confidence percentage per forecast
- Run Forecast button

**Tab 3 — Safety Stock:**
- Safety stock per item (units buffer)
- Optimized reorder points
- Lead time per item
- Service level selector (90/95/99%)
- Calculate Now button

---

## 🗂️ Project Structure

```
inventory-tracking-system/
├── lambda_function.py           # Inventory Lambda (CRUD v4)
├── forecast_function.py         # Forecast Lambda
├── safety_stock_function.py     # Safety Stock Lambda
├── authorizer_function.py       # API Key authorizer
├── Dockerfile                   # Inventory container
├── Dockerfile.forecast          # Forecast container
├── Dockerfile.safetystock       # Safety Stock container
├── Dockerfile.authorizer        # Authorizer container
├── buildspec.yml                # CI/CD config
├── index.html                   # Dashboard (3 tabs)
├── inventory-terraform/         # Terraform IaC
└── README.md
```

---

## 📡 API Reference

**Base URL:** `https://ityntliklc.execute-api.ca-central-1.amazonaws.com`
**Required Header:** `x-api-key: <your-api-key>`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/Inventory` | Get all inventory items |
| POST | `/Inventory` | Add new item |
| PUT | `/Inventory/{id}` | Update item |
| DELETE | `/Inventory/{id}` | Delete item |
| GET | `/Forecasts` | Get demand forecasts |
| POST | `/Forecasts` | Run forecast analysis |
| GET | `/SafetyStock` | Get safety stock data |
| POST | `/SafetyStock` | Calculate safety stock |

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

CREATE TABLE safety_stock (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventory(id),
    optimal_quantity INTEGER, calculated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL,
    email VARCHAR(255), phone VARCHAR(50),
    lead_time_days INTEGER DEFAULT 7, created_at TIMESTAMP DEFAULT NOW()
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

## 🔒 Security

- ✅ Lambda authorizer — every API request requires valid key
- ✅ RDS in private subnet — never publicly accessible
- ✅ Security groups chained — least privilege
- ✅ CloudFront WAF — vulnerability protection
- ✅ HTTPS enforced everywhere
- ✅ Password rotation — regular credential updates
- ✅ No credentials in code

---

## 🧩 Key Challenges Solved

| Challenge | Solution |
|-----------|---------|
| RDS in wrong VPC | Snapshot → restore into correct VPC |
| psycopg2 Mac vs Linux | Build with `--platform manylinux2014_x86_64` |
| Docker platform mismatch | `--platform linux/amd64 --provenance=false` |
| Lambda Zip → Image | New function with `--package-type Image` |
| CI/CD async update | `aws lambda wait function-updated` |
| Wrong CloudFront | `aws cloudfront list-distributions` to verify |
| Open API | Lambda authorizer + API key |
| Exposed credentials | Password rotation policy |

---

## 🔮 What's Next

### Project 4 — PO Auto Generator 🔵
- AWS Step Functions orchestration
- Read from safety_stock + suppliers tables
- Auto-generate purchase orders
- Send via AWS SES email to suppliers
- Update purchase_orders table

### Final — AI Supply Chain Control Tower 🔮
- AWS Bedrock (Claude AI) — conversational interface
- Unified dashboard — all 4 systems
- EventBridge — events flow between projects
- AI recommendations — predictive reordering

---

## 👤 Author

Built by **Kweku** — Cloud Infrastructure Developer specializing in AI-powered supply chain systems on AWS.

🔗 GitHub: [@okwei50](https://github.com/okwei50)
🌐 Live: [https://d3knwbrcu1kxhj.cloudfront.net](https://d3knwbrcu1kxhj.cloudfront.net)
