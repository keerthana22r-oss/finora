# 💰 Wealthora

### Smart Personal Finance Management Platform built with Django

<p align="center">
<img width="1917" height="910" alt="Wealthora Dashboard" src="https://github.com/user-attachments/assets/0b3e0f11-5185-4044-b991-08ac8e915886" />
</p>

<p align="center">

![Version](https://img.shields.io/badge/Version-v1.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-5.x-green?style=for-the-badge\&logo=django)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge\&logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge\&logo=bootstrap)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-red?style=for-the-badge)

</p>

---

# 📖 Overview

**Wealthora** is a full-stack **Personal Finance Management System** built with **Django**, **Python**, and **MySQL**.

It enables users to manage their finances efficiently by tracking income, expenses, budgets, savings goals, and recurring subscriptions while providing interactive dashboards and insightful financial analytics.

The project is designed to simulate a real-world finance application and demonstrates full-stack development, database design, authentication, analytics, and responsive UI development.

---

# 🚀 Project Status

**Current Version:** **v1.0**

**Status:** 🟢 Active Development

### ✅ Completed Modules

* Authentication
* Dashboard
* Income Management
* Expense Management
* Budget Management
* Savings Goals
* Subscription Tracker

### 🚧 Currently Working On

* Investment Tracker
* Financial Insights
* Reports & Export

---

# ✨ Features

## 🔐 Authentication

* User Registration
* Secure Login & Logout
* Change Password
* Profile Management
* Session-based Authentication

---

## 💵 Income Management

* Add Income
* Edit Income
* Delete Income
* Category Management
* Monthly Filtering
* Transaction History

---

## 💸 Expense Management

* Add Expenses
* Edit Expenses
* Delete Expenses
* Expense Categories
* Search & Filter
* Monthly Expense Tracking

---

## 📊 Smart Dashboard

Interactive dashboard displaying:

* Total Income
* Total Expenses
* Monthly Balance
* Highest Spending Category
* Budget Usage
* Savings Goal Progress
* Subscription Summary

### Charts

* Income vs Expense
* Expense Category Distribution
* Monthly Spending Trend
* Dynamic Month & Year Filtering

---

## 🎯 Budget Management

Create and monitor monthly budgets.

Features include:

* Category-wise Budgets
* Budget Progress Bars
* Live Spending Tracking
* 80% Warning Indicator
* Budget Limit Alerts
* Remaining Budget Calculation

---

## 🏦 Savings Goals

Track financial goals with:

* Target Amount
* Current Savings
* Remaining Amount
* Progress Tracking
* Add Funds
* Estimated Monthly Savings

---

## 🔄 Subscription Tracker

Manage recurring subscriptions such as:

* Netflix
* Spotify
* Amazon Prime
* Insurance
* Gym Membership
* Custom Services

Supports:

* Weekly
* Monthly
* Quarterly
* Yearly Plans

Automatically calculates:

* Next Payment Date
* Monthly Cost
* Annual Cost

---

# 🧠 Planned Features

The following modules are part of the upcoming roadmap.

## 📈 Investment Tracker

* Investment Portfolio
* Profit & Loss
* Asset Allocation
* Investment Performance

---

## 💡 Financial Insights

Automatic insights including:

* Spending Trends
* Budget Warnings
* Savings Suggestions
* Financial Health Score
* Highest Spending Category Detection

---

## 📄 Reports & Analytics

* Monthly Reports
* CSV Export
* PDF Export
* Expense Analysis
* Income Reports

---

## 🤖 Future AI Features

* AI Spending Prediction
* Smart Expense Categorization
* Personalized Saving Suggestions
* Expense Forecasting

---

# 🛠 Tech Stack

| Technology  | Purpose                   |
| ----------- | ------------------------- |
| Python      | Backend Development       |
| Django      | Web Framework             |
| MySQL       | Database                  |
| HTML5       | Frontend Structure        |
| CSS3        | Styling                   |
| Bootstrap 5 | Responsive UI             |
| JavaScript  | Client-side Functionality |
| Chart.js    | Data Visualization        |

---

# 🏗 Project Architecture

```text
User
   │
   ▼
Authentication
   │
   ▼
Dashboard
   │
   ├───────────────┐
   ▼               ▼
Income         Expenses
   │               │
   └──────┬────────┘
          ▼
      Budget Manager
          │
          ▼
    Savings Goals
          │
          ▼
 Subscription Tracker
          │
          ▼
     Analytics Engine
          │
          ▼
      MySQL Database
```

---

# 📂 Project Structure

```text
wealthora/
│
├── accounts/          # User authentication
├── dashboard/         # Dashboard & analytics
├── income/            # Income management
├── expenses/          # Expense management
├── budgets/           # Budget tracking
├── savings/           # Savings goals
├── subscriptions/     # Subscription tracker
├── investments/       # Planned module
├── insights/          # Planned module
├── reports/           # Planned module
│
├── templates/
├── static/
├── media/
├── screenshots/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🎓 Skills Demonstrated

* Django Authentication
* CRUD Operations
* Django ORM
* MySQL Database Design
* MVC Architecture
* Responsive Web Design
* Bootstrap UI
* Chart.js Integration
* Session Management
* Form Validation
* Git & GitHub Workflow

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/wealthora.git

cd wealthora
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Development Server

```bash
python manage.py runserver
```

Open your browser:

```text
http://127.0.0.1:8000/
```

---

# 📷 Screenshots

## Dashboard

<img width="1913" height="907" alt="Dashboard" src="https://github.com/user-attachments/assets/bf3334d9-8b36-47f5-9ca4-eb3a09056c35" />

---

## Income Management

<img width="1914" height="904" alt="Income" src="https://github.com/user-attachments/assets/954efd16-c9b6-4e8c-a1e5-a9e7e9310e9b" />

---

> More screenshots will be added as new modules are completed.

---

# 🛣 Development Roadmap

## ✅ Version 1.0

* Authentication
* Income Management
* Expense Management
* Dashboard
* Budget Management
* Savings Goals
* Subscription Tracker

---

## 🚧 Version 1.1

* Reports Module
* CSV Export
* PDF Export
* Improved Dashboard Analytics

---

## 📅 Version 1.2

* Investment Tracker
* Financial Insights
* Advanced Charts
* Search Improvements

---

## 🔮 Version 2.0

* AI Expense Prediction
* OCR Receipt Scanner
* Email Reports
* Bank Statement Import
* Multi-Currency Support
* Dark Mode
* Notification System

---

# 💡 Why Wealthora?

Many finance applications are either too complex for everyday users or lock advanced features behind paid subscriptions.

Wealthora was created as a practical full-stack application that focuses on simplicity, usability, and meaningful financial insights while demonstrating modern Django development practices.

---

# 🤝 Contributing

Contributions, suggestions, and feature requests are always welcome.

If you have ideas to improve Wealthora:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👩‍💻 Author

## **Keerthana K R**

**Aspiring Software Engineer | Python Full Stack Developer**

Passionate about building scalable web applications using Django, Python, and MySQL while continuously improving software engineering skills through real-world projects.

⭐ **If you found this project useful, consider giving it a Star on GitHub!**
