# Splitwise Clone

## Overview
A web application for tracking and splitting expenses among friends and groups.

## Features
- User Registration and Authentication
- Create and Manage Groups
- Add Expenses
- View Group Expenses
- Track Personal Balances

## Tech Stack
- Backend: Flask
- Database: SQLAlchemy (SQLite)
- Frontend: Bootstrap
- Authentication: Flask-Login

## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/splitwise-clone.git
cd splitwise-clone
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
flask db upgrade
```

5. Run the application
```bash
flask run
```

## Environment Variables
Create a `.env` file with the following:
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///splitwise.db
FLASK_APP=app.py
FLASK_ENV=development
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
