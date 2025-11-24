# Library Management System

A comprehensive library management system built with FastAPI and PostgreSQL,
providing a robust API for managing books, users, and borrowing operations.

## Features

- **User Management**
  - User registration and authentication (JWT)
  - Role-based access control (Admin, Employee, User,Author)
  - User profile management

- **Book Management**
  - Add, update, and remove books
  - Search and filter books
  - Track book availability

- **Borrowing System**
  - Borrow and return books 
  - Track due dates
  - View borrowing history
  - Overdue book notifications

- **Admin Dashboard**
  - Manage users and their roles
  - View system statistics
  - Manage book inventory

## Tech Stack

- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+
- pip (Python package manager)

