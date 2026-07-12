# 💰 Wealthora – Smart Personal Finance & Expense Intelligence Platform

<p align="center">
<img width="1917" height="910" alt="image" src="https://github.com/user-attachments/assets/0b3e0f11-5185-4044-b991-08ac8e915886" />

</p>

<p align="center">

![Django](https://img.shields.io/badge/Django-5.x-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-red?style=for-the-badge)

</p>

---

## 📖 Overview

**Wealthora** is a full-stack **Personal Finance Management System** built using **Django** and **MySQL**.

The application helps users manage their finances by tracking income, expenses, monthly budgets, savings goals, subscriptions, investments, and financial insights through an interactive analytics dashboard.

The goal of Wealthora is to provide a clean, intelligent, and user-friendly platform that helps users understand where their money goes and make better financial decisions.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Secure Login & Logout
- Profile Management
- Change Password
- Session-based Authentication

---

## 💵 Income Management

- Add Income
- Edit Income
- Delete Income
- Monthly Filtering
- Category Management
- Transaction History

---

## 💸 Expense Management

- Add Expenses
- Update Expenses
- Delete Expenses
- Expense Categories
- Search & Filter
- Monthly Tracking

---

## 📊 Smart Dashboard

Interactive dashboard showing:

- Total Income
- Total Expenses
- Monthly Surplus
- Highest Spending Category
- Budget Usage
- Savings Goal Progress
- Active Subscription Summary

Charts include:

- Income vs Expense (Bar Chart)
- Expense Category Distribution (Doughnut Chart)
- Monthly Spending Trend
- Dynamic Month & Year Filters

---

## 🎯 Budget Management

Create monthly budgets for categories.

Features include:

- Budget Progress Bars
- Live Spending Tracking
- 80% Warning
- 100% Limit Alert
- Budget Exceeded Indicator

---

## 🏦 Savings Goals

Manage financial goals with:

- Target Amount
- Current Savings
- Progress Bar
- Add Funds
- Remaining Amount
- Estimated Monthly Savings Required

---

## 🔄 Subscription Tracker

Track recurring payments including:

- Netflix
- Spotify
- Prime
- Insurance
- Gym Membership
- Custom Subscriptions

Supports:

- Weekly
- Monthly
- Quarterly
- Yearly

Automatically calculates:

- Next Payment Date
- Monthly Cost
- Annual Cost

---

## 📈 Investment Tracker 

Coming Soon

Features Planned:

- Investment Portfolio
- Profit & Loss
- Asset Allocation
- Returns Analysis

---

## 🧠 Financial Insights 

Coming Soon

Automatic insights such as:

- Highest Spending Category
- Budget Warnings
- Spending Trends
- Savings Suggestions
- Financial Health Score

---

## 📄 Reports & Analytics 

Coming Soon

- Monthly Reports
- CSV Export
- PDF Export
- Expense Analysis
- Income Reports

---

# 🛠 Tech Stack

| Technology | Used For |
|------------|----------|
| Python | Backend |
| Django | Web Framework |
| MySQL | Database |
| HTML5 | Frontend |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Client-side Functionality |
| Chart.js | Data Visualization |

---

# 📂 Project Structure

```
wealthora/
│
├── accounts/
├── dashboard/
├── income/
├── expenses/
├── budgets/
├── savings/
├── subscriptions/
├── investments/
├── insights/
├── reports/
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

# 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/wealthora.git

cd wealthora
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment

Create a `.env` file.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=wealthora

DB_USER=root

DB_PASSWORD=yourpassword

DB_HOST=localhost

DB_PORT=3306
```

---

### Apply Migrations

```bash
python manage.py migrate
```

---

### Create Superuser

```bash
python manage.py createsuperuser
```

---

### Run Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000
```

---

# 📷 Screenshots

## Dashboard

> Add your dashboard screenshot here

```
<img width="1913" height="907" alt="image" src="https://github.com/user-attachments/assets/bf3334d9-8b36-47f5-9ca4-eb3a09056c35" />

```

## Income

```
<img width="1914" height="904" alt="image" src="https://github.com/user-attachments/assets/954efd16-c9b6-4e8c-a1e5-a9e7e9310e9b" />

```
# 🎯 Future Enhancements

- AI Spending Prediction
- OCR Receipt Scanner
- Email Expense Reports
- Bank Statement Import
- Dark Mode
- Multi-Currency Support
- Mobile Responsive UI
- Notifications & Reminders

---

# 👩‍💻 Author

**Keerthana K R**

Python Full Stack Developer

Portfolio Project built using Django.

If you like this project, consider giving it a ⭐ on GitHub!
