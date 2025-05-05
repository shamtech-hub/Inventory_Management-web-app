# 🏪 Inventory Management Web Application

A lightweight, full-stack inventory management system built with **Flask** and **MySQL**, designed for small warehouses or retail shops to manage products, warehouse locations, and track inventory movements.

---

## 📦 Project Overview

This web application helps businesses keep track of inventory by allowing them to manage:
- Products
- Warehouse Locations
- Product Movements (transfers in/out/between locations)

It also generates real-time inventory reports showing the current quantity of each product at each location.

---

## 🛠️ Features

### CRUD Operations
- ✅ Add / Edit / View **Products**
- ✅ Add / Edit / View **Locations**
- ✅ Add / Edit / View **Product Movements**

### Product Movement Logic
- Move products *into* a warehouse (no `from_location`)
- Move products *out of* a warehouse (no `to_location`)
- Move products *between* locations

### Reports
- 📊 **Inventory Balance Report**  
  Displays a grid view of:
  - Product
  - Warehouse
  - Current Quantity

---

## 🗃️ Database Schema

### Tables:

#### Product
| Column      | Type    | Notes        |
|-------------|---------|--------------|
| product_id  | VARCHAR | Primary Key  |
| name        | VARCHAR |              |

#### Location
| Column       | Type    | Notes        |
|--------------|---------|--------------|
| location_id  | VARCHAR | Primary Key  |
| name         | VARCHAR |              |

#### ProductMovement
| Column        | Type    | Notes                              |
|---------------|---------|------------------------------------|
| movement_id   | VARCHAR | Primary Key                        |
| timestamp     | DATETIME| Automatically set at movement time |
| from_location | VARCHAR | Nullable (for incoming)            |
| to_location   | VARCHAR | Nullable (for outgoing)            |
| product_id    | VARCHAR | Foreign Key to Product             |
| qty           | INT     | Quantity moved                     |

---

## 💡 Use Cases Demonstrated

- ✅ Created 3–4 sample **Products** and **Locations**
- ✅ Performed 20+ product movements including:
  - Moving Product A to Location X
  - Moving Product B to Location X
  - Transferring Product A from Location X to Y
- ✅ Generated inventory balance report showing stock by product/location

---

## 📷 Screenshots (Optional)

_Add UI screenshots here if available (e.g., product list, movement form, balance report)_

---

## 🚀 Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, Bootstrap, AJAX (for dynamic updates)
- **Templating**: Jinja2
- **ORM (optional)**: SQLAlchemy

---

## 🔧 Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/inventory-management-flask.git
   cd inventory-management-flask

   Install Dependencies

2. **install dependencies**
   ```bash
    pip install -r requirements.txt
3. **Configure MySQL Database**

    -Create a database and import schema (SQL file provided in /db/schema.sql)

    -Update DB config in app.py or a separate config file

4. **Run the Flask App**
   ```bash
   flask run
5. Visit: http://localhost3000
