# 🛒 Advanced E-Commerce Platform

A full-fledged e-commerce platform with user authentication, product management, shopping cart, wishlist, order processing, payments, and more.

## 🚀 Features Implemented Today:
### ✅ **User Authentication**
- Custom **User Model** with `user_type` (Superadmin, Admin, Customer)
- Fields: `username`, `email`, `phone`, `is_available`, `is_active`
- JWT-based authentication

### ✅ **Product Management**
- **Product Model** with `category`, `price`, `stock`, `is_available`
- Admin can **CRUD** products
- Search & filter support

### ✅ **Shopping Cart API**
- Add products to cart
- View cart items
- Update cart quantity
- Remove products from cart

### ✅ **Order Processing**
- Create an order from cart
- View order history
- Track order status

### ✅ **Payment Integration**
- **Stripe Payment** integration
- **PayPal Payment** integration
- Store payment details in DB
- Send order confirmation & payment receipt emails

### ✅ **Wishlist API**
- Add products to wishlist
- View wishlist
- Remove from wishlist

### ✅ **User Reviews & Ratings**
- Users can rate products (1-5 stars)
- Add, edit, delete reviews
- View all reviews for a product

### ✅ **Discount & Coupons**
- Admin can create coupons
- Users can apply promo codes at checkout
- Validate and expire coupons automatically

---

## ⚙️ **Setup & Installation**
### 1️⃣ Clone the Repository:
```bash
git clone https://github.com/Abidanik86/django-ecommerce.git
cd ecommerce-platform
