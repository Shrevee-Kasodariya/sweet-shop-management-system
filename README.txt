# Sweet Shop Management System

A simple, modern web application for managing a sweet shop inventory. Built with Python (Flask) for the backend and vanilla JavaScript/HTML/CSS for the frontend.

## Features
- Add, view, delete sweets
- Search and sort sweets by name, category, price, or quantity
- Purchase and restock sweets with inventory management
- Attractive, responsive UI for laptops
- Full test coverage for backend logic

## Getting Started

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd sweet_shop
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the backend server:
   ```sh
   python api.py
   ```
   The API will run at `http://127.0.0.1:5000`.
2. Open `frontend/index.html` in your browser (double-click or use `file:///` path).

### Running Tests
```sh
python -m unittest discover tests
```

## Project Structure
```
api.py                # Flask API
run.py                # CLI runner (optional)
app/
  sweet.py            # Sweet model
  sweetshop.py        # SweetShop logic
frontend/
  index.html          # Web UI
  app.js              # Frontend logic
  style.css           # Styles
requirements.txt      # Python dependencies
tests/
  test_sweetshop.py   # Unit tests
```

## Screenshots
_Add screenshots of your UI here_

## License
MIT

---
Made with ❤️ for sweet lovers!
