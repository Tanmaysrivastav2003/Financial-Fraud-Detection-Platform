
# End-to-End Financial Fraud Detection Platform

## Project Overview

This project is a comprehensive, multi-stage platform designed to detect, analyze, and investigate financial fraud. It moves beyond simple prediction by providing a full suite of tools for different user personas within a financial institution: a real-time prediction app for analysts, high-level dashboards for managers, and advanced network analysis tools for investigators.

The platform is built around a series of synthetic datasets, generated to mimic real-world transaction patterns and fraudulent activities. It features a machine learning model with integrated explainability (XAI) to ensure that predictions are transparent and actionable.

---

## Architecture

The platform is built in distinct, modular stages, feeding data and intelligence forward to empower a suite of analytical tools tailored for different user personas.

| **Stage 1: Foundation (Data Generation)** | **Stage 2: Intelligence (Modeling & XAI)** | **Stage 3: Action & Insights (Deployment)** |
| :--- | :--- | :--- |
| **Code:**<br>`01_data_generation/`<br>• `transactiondataset-1.ipynb`<br>• `credit-debitdataset.ipynb`<br>• `phonenumber.ipynb` | **Code:**<br>`02_eda_and_modeling/`<br>• `final-model.ipynb` | **Track A: The Manager's View**<br>• **Tool:** `Tableau`<br>• **Input:** `data/*.csv`<br>• **Output:** Interactive BI Dashboard<br>• **Purpose:** High-level monitoring of trends & KPIs. |
| **⬇️** | **⬇️** | **Track B: The Analyst's Tool**<br>• **Tool:** `Streamlit`<br>• **Input:** `models/fraud_detection_artifacts.pkl`<br>• **Output:** Interactive Web App<br>• **Purpose:** Real-time prediction & explanation. |
| **Output:**<br>`data/`<br>• `TransactionDataset1.csv`<br>• `credit-debit dataset.csv`<br>• `synthetic_bank_data.csv`| **Output:**<br>`models/`<br>• `fraud_detection_artifacts.pkl` | **Track C: The Investigator's Edge**<br>• **Tool:** `Python (NetworkX)`<br>• **Input:** `data/synthetic_bank_data.csv`<br>• **Output:** Graph Visualization (`.png`)<br>• **Purpose:** Uncovering hidden networks & fraud rings. |

---

## How to Run This Project

### Prerequisites

*   Python 3.10+
*   An IDE like VS Code
*   (Optional) Tableau Public for dashboard visualization.
*   (Optional) Docker Desktop for running a dedicated graph database like Memgraph.

### Step 1: Clone the Repository & Set Up Environment

```bash
# Clone this repository to your local machine
git clone <YOUR_REPO_URL>
cd financial-fraud-detection-platform

# Create and activate a Python virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install all required Python packages
pip install -r requirements.txt
pip install -r 03_streamlit_app/requirements.txt
