
# Items Inventory Management API

A FastAPI-based backend system for managing inventory items, user registration, and shop profiles. It supports JWT authentication and provides RESTful endpoints for managing users, shops, and items.

## Features

- ✅ JWT-based Authentication (Users & Shops)
- 🛒 CRUD operations for Shops and their Items
- 👥 User registration, update, deletion, and login
- 🧾 SQLite support with SQLModel
- 📦 Dependency Injection with FastAPI’s Depends
- 🔐 Password hashing using Passlib
- 🧪 Easily testable with Pytest

## Installation

```bash
git clone https://github.com/yourusername/dezra.git
cd dezra
python -m venv venv
source venv/bin/activate  # if on Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root with the following content:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./test.db
```

## Running the App

```bash
fastapi dev app/main.py
```

## Project Structure

```
app/
├── core/
│   └── security.py          # Password hashing, JWT utilities
├── models/
│   ├── user.py              # User models (User, UserCreate, UserRead)
│   ├── shop.py              # Shop models
│   └── item.py              # Item models
├── routers/
│   ├── auth.py              # Login and token
│   ├── user.py              # User endpoints
│   ├── shop.py              # Shop endpoints
│   └── item.py              # Item endpoints
├── database.py              # Session generator
└── main.py                  # FastAPI app instance
```

## Sample Dummy Data

### Create a Shop

```json
{
  "name": "Tropical Fruits",
  "email": "tropical@example.com",
  "description": "Exotic fruits from the tropics",
  "image": "https://example.com/image.jpg",
  "address": "123 Mango Lane",
  "state": "Lagos",
  "city": "Ikeja",
  "country": "Nigeria",
  "password": "secret123"
}
```

### Create an Item

```json
{
  "name": "Fresh Mango",
  "description": "Sweet and juicy mangoes from the farm",
  "image": "https://example.com/mango.jpg",
  "expiry_date": "2025-06-15"
}
```

### Create a User

```json
{
  "email": "user@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "password": "strongpassword"
}
```

## Testing

```bash
pytest
```

## License

MIT License
