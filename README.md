# E-Commerce Flask App

A simple and scalable e-commerce web application built using **Flask**, supporting user authentication, product listings, cart functionality, order management, and an **admin dashboard** for managing users, products, and orders.

---

##  Features

### User Side

- **User Authentication**
  - Register / Login / Logout
  - Update password and profile

- **Product Catalog**
  - Browse products
  - Add to cart
  - Search products

- **Cart & Orders**
  - View cart and remove items
  - Place order (dummy checkout)
  - View order history with order status updates

- **Contact & About Pages**
  - Contact form for customer queries
  - Basic about-us section

---

### Admin Dashboard

(Admin access is restricted to backend only — not accessible via frontend for security.)

- **View Registered Users**
  - Admin can see all users who signed up

- **Manage Products**
  - Add new products with details like:
    - Product name
    - MRP & Discounted Price
    - Discount Percentage
    - Image Upload
    - Stock Quantity
  - **View All Products**
    - See the list of all uploaded products
    - **Edit product details**
    - **Delete any product**

- **View All Orders**
  - See all orders placed by users
  - Update order status to:
    - `Pending`
    - `Dispatched`
    - `Out for Delivery`
    - `Delivered`

---

## Technologies Used

- Python (Flask Framework)
- Jinja2 (templating)
- SQLite (database)
- HTML5, Bootstrap 5

