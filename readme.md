# Secant Minimization Web App

This project is a web application for finding the minimum of a function using the Secant method. It includes a **FastAPI** backend and a **React** frontend.

## Features
- Enter a mathematical function and range
- Compute the minimum using the Secant method
- Visualize the function and its derivative

## Installation and Setup

### 1. Clone the Repository
```sh
git clone https://github.com/adarsh40parihar/secant-minimization.git
cd secant-minimization
```

---

## Backend (FastAPI)

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r backend/requirements.txt
```

### 4. Run the FastAPI Server
```sh
cd backend
uvicorn main:app --reload
```

The API will be running at: `http://127.0.0.1:8000`

To check if the server is working, open a browser or use Postman to visit:
```
http://127.0.0.1:8000/
```

---

## Frontend (React)

### 5. Install Node.js Dependencies
```sh
cd frontend
npm install
```

### 6. Start the React App
```sh
npm run dev
```

The frontend will be available at:
```
http://localhost:5173
```

---

## Usage
1. Open the frontend in your browser.
2. Enter the function, range, and tolerance.
3. Click "Minimize" to compute the minimum.
4. View the results and function graph.

```


