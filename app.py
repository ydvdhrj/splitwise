# python app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key-for-dev')

# Handle database URL for both local and production
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///splitwise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Initialize the app with extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    groups = db.relationship('Group', secondary='user_groups', back_populates='members')
    expenses = db.relationship('Expense', back_populates='paid_by')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    members = db.relationship('User', secondary='user_groups', back_populates='groups')
    expenses = db.relationship('Expense', back_populates='group')

user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    paid_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paid_by = db.relationship('User', back_populates='expenses')
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group', back_populates='expenses')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables within app context
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        group = Group(name=group_name)
        group.members.append(current_user)
        db.session.add(group)
        db.session.commit()
        flash('Group created successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('create_group.html')

@app.route('/add_expense/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_expense(group_id):
    group = Group.query.get_or_404(group_id)
    
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        
        expense = Expense(
            description=description,
            amount=amount,
            date=datetime.utcnow(),
            paid_by=current_user,
            group=group
        )
        
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('group_details', group_id=group_id))
    
    return render_template('add_expense.html', group=group)

@app.route('/group/<int:group_id>')
@login_required
def group_details(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user not in group.members:
        flash('You do not have access to this group.')
        return redirect(url_for('dashboard'))
    
    expenses = Expense.query.filter_by(group_id=group_id).order_by(Expense.date.desc()).all()
    return render_template('group_details.html', group=group, expenses=expenses)

@app.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    if request.method == 'POST':
        group_id = request.form.get('group_id')
        group = Group.query.get_or_404(group_id)
        
        if current_user in group.members:
            flash('You are already a member of this group.')
            return redirect(url_for('dashboard'))
        
        group.members.append(current_user)
        db.session.commit()
        flash(f'Successfully joined group: {group.name}')
        return redirect(url_for('group_details', group_id=group_id))
    
    # Get all groups that the user is not a member of
    subquery = db.session.query(user_groups.c.group_id).filter(user_groups.c.user_id == current_user.id)
    available_groups = Group.query.filter(~Group.id.in_(subquery)).all()
    
    return render_template('join_group.html', available_groups=available_groups)

if __name__ == '__main__':
    app.run(debug=True)
