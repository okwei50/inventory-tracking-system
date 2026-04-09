# 📦 AWS Inventory Tracking System

A production-grade cloud inventory management system built entirely on AWS from scratch. This is **Project 1** of a planned **AI-powered Supply Chain Control Tower** that will integrate demand forecasting, safety stock optimization, and automated purchase order generation.

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://docker.com)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)](https://terraform.io)
[![CI/CD](https://img.shields.io/badge/CI/CD-CodePipeline-green?logo=amazon-aws)](https://aws.amazon.com/codepipeline)

---

## 🌐 Live Demo

| Resource | URL |
|----------|-----|
| **Dashboard** | https://d3knwbrcu1kxhj.cloudfront.net |
| **API Endpoint** | https://ityntliklc.execute-api.ca-central-1.amazonaws.com/Inventory |

---

## 🏗️ Architecture

```
Internet
    ↓
CloudFront (HTTPS + CDN + WAF)
    ↓
S3 (Static Dashboard Hosting)
    ↓
API Gateway (HTTP API — GET/POST /Inventory)
    ↓
Lambda Function (Python 3.11 — Docker Container)
    ↓
RDS PostgreSQL (Private Subnet)

All inside a custom VPC with:
✅ Public & private subnets across 2 availability zones
✅ NAT Gateway for outbound access from private subnets
✅ Security group chaining (Public → Lambda → RDS)
✅ No public database exposure
```

### AWS Services Used

| Service | Purpose |
|---------|---------|
| **Lambda** | Backend API (Python 3.11, Docker container) |
| **RDS PostgreSQL** | Primary database (private subnet) |
| **API Gateway** | REST API endpoint with CORS |
| **S3** | Dashboard hosting + Terraform state storage |
| **CloudFront** | CDN + HTTPS + WAF protection |
| **ECR** | Docker container registry |
| **CodePipeline** | CI/CD orchestration |
| **CodeBuild** | Docker build + automated deployment |
| **VPC** | Network isolation and security |
| **NAT Gateway** | Outbound internet for private resources |
| **IAM** | Roles and permissions |

---

## 🚀 Features

- **Real-time inventory dashboard** with charts and metrics
- **REST API** supporting GET and POST operations
- **Low stock alerts** with configurable reorder points
- **Full inventory fields** — SKU, category, lead time, reorder point
- **HTTPS everywhere** via CloudFront
- **WAF protection** against common web vulnerabilities
- **Infrastructure as Code** — entire stack deployable with one command
- **Containerized** Lambda function via Docker + ECR
- **Automated CI/CD** — push to GitHub → auto deploy to AWS

---

## 📊 Dashboard Preview

The dashboard includes:
- 📈 **Stock levels bar chart** per product
- 🍩 **Value distribution doughnut chart**
- 🔢 **Metric cards** — total products, units, value, alerts
- ⚠️ **Low stock warning banner** with pulsing indicator
- 📋 **Full inventory table** with status badges
- ➕ **Add new item form** with all fields

---

## 🗂️ Project Structure

```
inventory-tracking-system/
├── lambda_function.py          # Lambda handler (Python 3.11)
├── Dockerfile                  # Container definition
├── buildspec.yml               # CodeBuild CI/CD config
├── index.html                  # Dashboard frontend
├── inventory-terraform/        # Terraform IaC
│   ├── main.tf                 # Provider + S3 backend
│   ├── variables.tf            # Input variables
│   ├── outputs.tf              # Output values
│   ├── modules.tf              # Module declarations
│   └── modules/
│       ├── vpc/                # VPC, subnets, NAT, security groups
│       ├── rds/                # RDS instance + subnet group
│       ├── lambda/             # Lambda function + IAM roles
│       ├── apigateway/         # HTTP API + routes + CORS
│       ├── s3/                 # S3 bucket + website config
│       └── cloudfront/         # CloudFront distribution
└── README.md
```

---

## 🛠️ Tech Stack

**Backend**
- Python 3.11
- psycopg2-binary (PostgreSQL driver)
- AWS Lambda (serverless)
- AWS API Gateway (HTTP API)

**Database**
- PostgreSQL 16.6 on AWS RDS
- Private subnet — not publicly accessible

**Frontend**
- Vanilla HTML/CSS/JavaScript
- Chart.js for visualizations
- DM Sans + DM Mono fonts

**Infrastructure**
- Terraform 1.5.7
- Docker (linux/amd64)
- AWS ECR

**CI/CD**
- GitHub (source control)
- AWS CodePipeline (orchestration)
- AWS CodeBuild (build + deploy)

---

## 📡 API Reference

**Base URL:** `https://ityntliklc.execute-api.ca-central-1.amazonaws.com`

### GET /Inventory
Returns all inventory items.

**Response:**
```json
{
  "version": "v3",
  "items": [
    {
      "id": 1,
      "name": "Laptop",
      "quantity": 3,
      "price": 999.99,
      "sku": "LAP-001",
      "reorder_point": 5,
      "lead_time_days": 7,
      "category": "Electronics"
    }
  ]
}
```

### POST /Inventory
Add a new inventory item.

**Request Body:**
```json
{
  "name": "Laptop",
  "quantity": 10,
  "price": 999.99,
  "sku": "LAP-001",
  "category": "Electronics",
  "reorder_point": 5,
  "lead_time_days": 7
}
```

**Response:**
```json
"Item added successfully"
```

---

## 🗄️ Database Schema

```sql
-- Core inventory table
CREATE TABLE inventory (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    quantity        INTEGER NOT NULL,
    price           DECIMAL(10,2) NOT NULL,
    sku             VARCHAR(100),
    reorder_point   INTEGER DEFAULT 5,
    lead_time_days  INTEGER DEFAULT 7,
    supplier_id     INTEGER,
    last_updated    TIMESTAMP DEFAULT NOW(),
    category        VARCHAR(100)
);

-- Suppliers (for PO auto generator)
CREATE TABLE suppliers (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    email           VARCHAR(255),
    phone           VARCHAR(50),
    lead_time_days  INTEGER DEFAULT 7,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Transaction history (feeds demand forecasting ML)
CREATE TABLE inventory_transactions (
    id              SERIAL PRIMARY KEY,
    inventory_id    INTEGER REFERENCES inventory(id),
    transaction_type VARCHAR(50),
    quantity        INTEGER,
    timestamp       TIMESTAMP DEFAULT NOW(),
    notes           TEXT
);

-- Demand forecasts (Project 2)
CREATE TABLE forecasts (
    id              SERIAL PRIMARY KEY,
    inventory_id    INTEGER REFERENCES inventory(id),
    forecast_date   DATE,
    predicted_demand INTEGER,
    confidence_score DECIMAL(5,2),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Safety stock (Project 3)
CREATE TABLE safety_stock (
    id              SERIAL PRIMARY KEY,
    inventory_id    INTEGER REFERENCES inventory(id),
    optimal_quantity INTEGER,
    calculated_at   TIMESTAMP DEFAULT NOW()
);

-- Purchase orders (Project 4)
CREATE TABLE purchase_orders (
    id              SERIAL PRIMARY KEY,
    inventory_id    INTEGER REFERENCES inventory(id),
    supplier_id     INTEGER REFERENCES suppliers(id),
    quantity        INTEGER,
    status          VARCHAR(50) DEFAULT 'pending',
    created_at      TIMESTAMP DEFAULT NOW(),
    expected_delivery DATE,
    notes           TEXT
);
```

---

## ⚙️ Infrastructure Deployment

### Prerequisites
- AWS CLI configured (`aws configure`)
- Terraform 1.5.7+
- Docker Desktop

### Deploy with Terraform

```bash
# Clone the repository
git clone https://github.com/okwei50/inventory-tracking-system.git
cd inventory-tracking-system/inventory-terraform

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy everything
terraform apply
```

### CI/CD Pipeline

Every `git push` to `main` automatically:
1. Triggers AWS CodePipeline
2. CodeBuild pulls latest code from GitHub
3. Builds Docker image (`linux/amd64`)
4. Pushes image to ECR
5. Updates Lambda function
6. Uploads dashboard to S3
7. Invalidates CloudFront cache

---

## 🔒 Security

- ✅ RDS in private subnet — never publicly accessible
- ✅ Lambda in private subnet with NAT Gateway
- ✅ Security groups chained — least privilege access
- ✅ CloudFront WAF — protection against common vulnerabilities
- ✅ HTTPS enforced — HTTP redirects to HTTPS
- ✅ No credentials in code — environment variables only

---

## 🧩 Key Challenges Solved

| Challenge | Solution |
|-----------|---------|
| RDS in wrong VPC | Snapshot → restore into correct VPC |
| psycopg2 Mac vs Linux | Build with `--platform manylinux2014_x86_64` |
| RDS requires 2 AZs | Created subnets in ca-central-1a and ca-central-1b |
| Docker platform mismatch | `--platform linux/amd64 --provenance=false` |
| Lambda Zip → Image conversion | Created new function with `--package-type Image` |
| CI/CD async Lambda update | Added `aws lambda wait function-updated` to buildspec |
| Wrong CloudFront distribution | Used `aws cloudfront list-distributions` to verify |

---

## 🗺️ Roadmap — Supply Chain Control Tower

This is **Project 1** of 4. The goal is to integrate all projects into one AI-powered platform.

```
Project 1: Inventory Tracking    ✅ Complete
Project 2: Demand Forecasting    🔵 Next — AWS SageMaker + time series ML
Project 3: Safety Stock Optimizer 🟡 Planned — optimal buffer stock calculation
Project 4: PO Auto Generator     🟡 Planned — AWS Step Functions + SES emails
AI Control Tower: Integration    🔮 Final — AWS Bedrock (Claude AI) unified dashboard
```

### How Projects Connect

```
inventory_transactions → SageMaker ML → forecasts table
forecasts + inventory  → Safety stock optimizer → safety_stock table
safety_stock + suppliers → PO generator → purchase_orders table + SES email
All tables → AI Control Tower → unified dashboard + recommendations
```

---

## 📝 License

This project is for educational and portfolio purposes.

---

## 👤 Author

Built by **Kweku** — cloud infrastructure enthusiast building a production-grade supply chain management platform on AWS.

🔗 GitHub: [@okwei50](https://github.com/okwei50)
