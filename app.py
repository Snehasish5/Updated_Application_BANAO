from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/health_app'  # Update with cloud URI if deploying

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Init Mongo
mongo = PyMongo(app)
db = mongo.db

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Static categories
CATEGORIES = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']

# Custom User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.role = user_data['role']
        self.data = user_data

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({'_id': ObjectId(user_id)})
    return User(user_data) if user_data else None

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.form
        username = data.get('username').strip()
        email = data.get('email').strip()
        password = data.get('password')
        confirm = data.get('confirm_password')
        if password != confirm:
            flash('Passwords do not match!')
            return render_template('signup.html')

        if db.users.find_one({'username': username}):
            flash('Username already exists!')
            return render_template('signup.html')

        profile_pic = request.files.get('profile_pic')
        filename = 'default.jpg'
        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'role': data.get('role'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'profile_pic': filename,
            'address_line': data.get('line1'),
            'city': data.get('city'),
            'state': data.get('state'),
            'pincode': data.get('pincode')
        }
        db.users.insert_one(user)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = db.users.find_one({'username': username})

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user.data
    return render_template('dashboard.html', user=user)

@app.route('/blog_create', methods=['GET', 'POST'])
@login_required
def blog_create():
    if current_user.role.lower() != 'doctor':
        flash('Only doctors can post blogs!')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.form
        image_file = request.files.get('image')
        filename = 'default_blog.jpg'
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        blog = {
            'title': data.get('title'),
            'image': filename,
            'category': data.get('category'),
            'summary': data.get('summary'),
            'content': data.get('content'),
            'is_draft': 'is_draft' in data,
            'author_id': ObjectId(current_user.get_id()),
            'created_at': datetime.utcnow()
        }
        db.blogs.insert_one(blog)
        flash('Blog created')
        return redirect(url_for('blog_list_doctor'))

    return render_template('blog_create.html', categories=CATEGORIES)

@app.route('/doctor/blogs')
@login_required
def blog_list_doctor():
    if current_user.role.lower() != 'doctor':
        flash('Access denied!')
        return redirect(url_for('dashboard'))
    blogs = list(db.blogs.find({'author_id': ObjectId(current_user.get_id())}).sort('created_at', -1))
    return render_template('blog_list_doctor.html', blogs=blogs)

@app.route('/patient/blogs')
@login_required
def blog_list_patient():
    if current_user.role.lower() != 'patient':
        flash('Access denied!')
        return redirect(url_for('dashboard'))

    categorized = {cat: [] for cat in CATEGORIES}
    blogs = db.blogs.find({'is_draft': False}).sort('created_at', -1)
    for blog in blogs:
        if blog['category'] in categorized:
            blog['summary'] = ' '.join(blog['summary'].split()[:15]) + '...' if len(blog['summary'].split()) > 15 else blog['summary']
            categorized[blog['category']].append(blog)

    return render_template('blog_list_patient.html', categorized_blogs=categorized)

@app.route('/blog/<blog_id>')
@login_required
def blog_detail(blog_id):
    blog = db.blogs.find_one({'_id': ObjectId(blog_id)})
    if not blog or (blog.get('is_draft') and blog['author_id'] != ObjectId(current_user.get_id())):
        flash('Blog not found or access denied')
        return redirect(url_for('dashboard'))
    return render_template('blog_detail.html', blog=blog)

if __name__ == '__main__':
    app.run(debug=True)
