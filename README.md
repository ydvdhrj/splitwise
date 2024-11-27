# Splitwise Expense Tracking App

A web application for tracking and splitting expenses among friends and groups.

## Features

- User Authentication (Register/Login)
- Create and Join Groups
- Add and Track Expenses
- Split Bills Among Group Members
- View Expense History
- Modern, Responsive UI

## Tech Stack

- Backend: Flask 2.3.3
- Database: PostgreSQL (Neon)
- ORM: SQLAlchemy 2.0.23
- Authentication: Flask-Login 0.6.3
- Frontend: Bootstrap 5, Custom CSS
- Deployment: Render.com

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd splitwise
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

4. Run the application:
```bash
python app.py
```

## Deployment

This application is configured for deployment on Render.com:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables:
     * SECRET_KEY
     * DATABASE_URL
     * FLASK_APP=app.py
     * FLASK_ENV=production

## Database

The application uses Neon PostgreSQL as the database. To set up:

1. Create a Neon account and database
2. Get your connection string
3. Add it to your environment variables as DATABASE_URL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
