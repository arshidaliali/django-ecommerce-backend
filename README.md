# Django E-commerce Backend

## Project Status
This project is currently under active development.  
It is not production-ready yet. Features are being built step by step.

---

## Overview
This is a backend system for an e-commerce application built using Django and Django REST Framework (DRF).

The goal of this project is to build a scalable, modular, and production-ready backend for an online store.

---

## Current Progress

### Completed
- Django project setup
- Git initialized and connected to GitHub
- Project structure created
- Apps created:
  - accounts
  - products
  - carts
  - orders
  - categories
- First commit pushed to GitHub

### In Progress
- User authentication system (JWT / session-based)
- Product APIs (CRUD operations)
- Cart functionality
- Order management system

###  Planned Features
- Payment gateway integration (Stripe or others)
- Advanced search & filtering
- Admin dashboard improvements
- API documentation (Swagger / DRF schema)

---

##  Project Structure

- accounts/      → User authentication & profiles  
- products/      → Product management  
- categories/    → Product categorization  
- carts/         → Shopping cart logic  
- orders/        → Order processing  
- config/        → Project settings  
- manage.py      → Django project entry point  

---

##  Tech Stack

- Python 🐍
- Django 🌐
- Django REST Framework ⚙️
- MYSQL (development database)

---

##  Setup Instructions

###  Clone Repository
```bash id="finalreadme2"
git clone https://github.com/arshidaliali/django-ecommerce-backend.git
cd django-ecommerce-backend




## Create Virtual Environment

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

## Install Dependencies

pip install -r requirements.txt


## Run Migrations
python manage.py migrate

## Start Server
python manage.py runserver
