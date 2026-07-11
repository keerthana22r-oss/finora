<<<<<<< HEAD
still we are in a phase 5 of our project 
project is in work will update soon
this is current status of the project
<img width="1898" height="907" alt="image" src="https://github.com/user-attachments/assets/6b5fe50e-bcfc-438c-a938-0e7d05256ce4" />

=======
# Wealthora — Smart Personal Finance & Expense Intelligence Platform
>>>>>>> d78966b (phases7)

Wealthora is a full-stack personal finance management web application built with Django and MySQL. It helps users track income, expenses, monthly budgets, savings goals, and recurring subscriptions through an interactive dashboard with live charts and spending insights.

> 🚧 **Project Status: In active development.** Phases 1–6 are complete and functional. See the roadmap below for what's built and what's coming next.

## Tech Stack

- **Backend:** Python, Django
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts:** Chart.js
- **Auth:** Django's built-in authentication system
- **Icons:** Bootstrap Icons

## Features Built So Far

- ✅ **Authentication** — registration, login, logout, profile management, password change
- ✅ **Income & Expense Tracking** — full CRUD, category-based organization, date/category filters, combined transaction history
- ✅ **Interactive Dashboard** — month/year filtering, income vs. expense charts, category breakdown doughnut chart, monthly spending trend line, live summary cards
- ✅ **Budget Management** — per-category monthly budgets with live spend tracking and an 80%/100%/exceeded warning system
- ✅ **Savings Goals** — goal tracking with progress bars, "Add Funds" flow, and automatic monthly-savings-required calculations
- ✅ **Subscription Tracker** — recurring payment tracking across weekly/monthly/quarterly/yearly cycles, dynamically-calculated next payment dates, monthly/annual cost totals

## Coming Next

- ⏳ Investment Tracker (manual entries, gain/loss calculations)
- ⏳ Rule-based Financial Insights Engine
- ⏳ Reports & Analytics with CSV/PDF export
- ⏳ Final security review, UI polish, and deployment prep

## Getting Started

```bash
# Clone the repository
git clone <your-repo-url>
cd wealthora

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (create a .env file)
# See .env.example for required variables

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

## Screenshots

*(To be added as the project nears completion)*

## Author

Built by Keerthana K R as a full-stack Django portfolio project.
