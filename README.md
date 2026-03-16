Great — here is a **more professional GitHub README** that looks **much stronger to recruiters**. It includes badges, structure, architecture, and demo sections.

You can **copy-paste this directly into your `README.md`**.

---

# Business Insight AI 📊🤖

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-green)
![LangChain](https://img.shields.io/badge/AI-LangChain-orange)

An **AI-powered Sales Intelligence Dashboard** built with **Streamlit**, **SQL Server**, and a **LangChain-based conversational agent** that answers business questions using natural language.

The system enables sales teams and analysts to **monitor KPIs, explore trends, and query business data conversationally**.

To simulate a real production workflow, a **Global Superstore dataset (CSV)** was imported into a **local SQL Server database**, allowing the AI assistant to generate SQL queries and retrieve insights dynamically.

---

# 🚀 Features

### 🎯 KPI Dashboard

Displays core business metrics:

* **Number of Orders**
* **Total Sales Revenue**
* **Total Profit**
* **Average Order Value**

All metrics update dynamically based on user filters.

---

### 📈 Interactive Visualizations

The dashboard provides multiple analytics views:

• **Monthly Revenue Trend** — Line Chart
• **Monthly Sales by Category** — Stacked Bar Chart
• **Annual Category Distribution** — Treemap

Built using **Plotly for interactive analytics**.

---

### 🔎 Dynamic Filters

Users can explore the data using:

* **Year Filter**
* **Product Category Filter**

All charts and KPIs update automatically when filters change.

---

### 🤖 AI Assistant Manager

A **LangChain-powered conversational assistant** allows users to ask business questions directly.

The assistant automatically:

1️⃣ Interprets the user question
2️⃣ Generates a SQL query
3️⃣ Retrieves data from SQL Server
4️⃣ Returns a clear business insight

Example questions:

```
Which product category generated the highest sales?
```

```
Show the top 10 products by sales.
```

```
Which category generated the highest profit?
```

```
Which sub-category contributes the most revenue?
```

```
Which region generated the highest profit?
```

---

# 🧠 Tech Stack

### Backend & Data Processing

* Python
* Pandas
* PyODBC

### Dashboard & Visualization

* Streamlit
* Plotly

### Database

* Microsoft SQL Server (Local Instance)

### AI Layer

* LangChain
* OpenAI GPT Model
* Custom SQL Query Agent

---

# ⚙️ System Architecture

```
Global Superstore CSV Dataset
            ↓
      SQL Server Database
            ↓
      Python (pyodbc + pandas)
            ↓
      Streamlit Dashboard
            ↓
      LangChain AI Assistant
```

---

# 📊 Dataset

The project uses the **Global Superstore Dataset**, which contains:

• Sales transactions
• Product categories
• Regional performance
• Profit metrics
• Customer segments

This dataset enables realistic **business analytics workflows**.

---

# 🎯 Example Business Insights

The system can answer questions such as:

| Question                                   | Insight                         |
| ------------------------------------------ | ------------------------------- |
| Which category generates the most revenue? | Category-wise sales analysis    |
| Which products drive the highest profit?   | Product profitability insights  |
| Which region performs best?                | Regional performance comparison |
| What are the top-selling products?         | Product demand analysis         |


# 💡 Why This Project Is Interesting

Traditional dashboards require users to **write SQL queries manually**.

This project demonstrates how **AI can enable natural language querying of structured business data**, making analytics accessible to non-technical users.

It combines:

• Data visualization
• SQL databases
• Natural language interfaces
• AI-powered analytics

---

# 📌 Future Improvements

* Automatic chart generation from AI queries
* Natural language → SQL optimization
* Support for multiple datasets
* Cloud deployment

---

# 👨‍💻 Author

**Umang Sinha**
B.Tech Electronics and Communication Engineering
IIT ISM Dhanbad

