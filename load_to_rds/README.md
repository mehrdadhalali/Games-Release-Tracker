# 🚀 Transform and Load

This folder contains scripts to **transform** the data gathered by the web-scrapers, **load** it into the RDS, and **notify** users subscribed to games releases, about any newly released games of their favourite genres.

---

## 🛠️ Prerequisites

Ensure that you have the following:
- **Docker** installed for containerisation.
- **AWS CLI** configured to interact with AWS services (ECR, Lambda, RDS, etc.)
- **Python** installed on your local machine. 
---

## 📂 Setup

1. Create a `.env` file with the following content:

```bash
DB_HOST=XXXXX
DB_PORT=XXXXX
DB_PASSWORD=XXXXX
DB_USER=XXXXX
DB_NAME=XXXXX
```


## 📄 Files Explained
