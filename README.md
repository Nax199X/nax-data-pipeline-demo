# 🧠 AWS Data Cleaning Pipeline (S3 → Lambda → S3)

This project demonstrates a **serverless ETL data-cleaning pipeline** built on AWS.  
When a CSV file is uploaded to your S3 bucket, an AWS Lambda function automatically runs to **clean or transform the data**, then saves the cleaned version to another folder — all without managing any servers.

---

## 🔍 Goal

Build an automated pipeline using:
- **Amazon S3** → Data storage (input and output)
- **AWS Lambda** → Data processing (ETL logic)
- **AWS CloudWatch** → Monitoring & logging

---

## 🧩 How It Works

┌──────────────────────┐
│   Your Local Laptop  │
│  (Upload CSV file)   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     S3 Bucket        │
│  incoming/ (raw)     │  ← raw data uploaded here
│  processed/ (clean)  │  ← Lambda saves output here
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   AWS Lambda         │
│  • Triggered by S3   │
│  • Reads raw CSV     │
│  • Cleans & rewrites │
│  • Saves to /processed│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  CloudWatch Logs     │
│  • View logs/errors  │
│  • Monitor pipeline  │
└──────────────────────┘
   
