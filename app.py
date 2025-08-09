from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

USERS_FILE = 'users.json'
BLOGS_FILE = 'blogs.json'
CATEGORIES = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']

# Helper functions to load/save JSON files
def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# User class compatible with Flask-Login, but data from JSON
class User(UserMixin):
    def __init__(self, data):
        self.id = str(data['id'])
        self.username = data['username']
        self.password = data['password']  # hashed
        self.role = data['role']
        self.email = data.get('email', '')
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.profile_pic = data.get('profile_pic', 'default.jpg')
        self.address_line = data.get('address_line', '')
        self.city = data.get('city', '')
        self.state = data.get('state', '')
        self.pincode = data.get('pincode', '')

    def get_dict(self):
        return {
            'id': int(self.id),
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_pic': self.profile_pic,
            'address_line': self.address_line,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode
        }

def find_user_by_username(username):
    users = load_json(USERS_FILE)
    for u in users:
        if u['username'] == username:
            return User(u)
    return None

def find_user_by_id(user_id):
    users = load_json(USERS_FILE)
    for u in users:
        if str(u['id']) == str(user_id):
            return User(u)
    return None

@login_manager.user_loader
def load_user(user_id):
    return find_user_by_id(user_id)

def get_next_user_id():
    users = load_json(USERS_FILE)
    if not users:
        return 1
    return max(u['id'] for u in users) + 1

def get_next_blog_id():
    blogs = load_json(BLOGS_FILE)
    if not blogs:
        return 1
    return max(b['id'] for b in blogs) + 1

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
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        address_line = request.form.get('line1', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        pincode = request.form.get('pincode', '').strip()

        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('signup.html')

        if find_user_by_username(username):
            flash('Username already exists!')
            return render_template('signup.html')

        profile_pic = request.files.get('profile_pic')
        filename = 'default.jpg'
        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        users = load_json(USERS_FILE)
        new_id = get_next_user_id()
        new_user_data = {
            'id': new_id,
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'role': role,
            'first_name': first_name,
            'last_name': last_name,
            'profile_pic': filename,
            'address_line': address_line,
            'city': city,
            'state': state,
            'pincode': pincode
        }
        users.append(new_user_data)
        save_json(USERS_FILE, users)

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            return render_template('login.html', error='Please enter both username and password')

        user = find_user_by_username(username)

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_data = {
        'role': current_user.role,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'username': current_user.username,
        'email': current_user.email,
        'profile_pic': current_user.profile_pic or 'default.jpg',
        'address': {
            'line1': current_user.address_line or '',
            'city': current_user.city or '',
            'state': current_user.state or '',
            'pincode': current_user.pincode or ''
        }
    }
    return render_template('dashboard.html', user=user_data)

@app.route('/blog_create', methods=['GET', 'POST'])
@login_required
def blog_create():
    if current_user.role.lower() != 'doctor':
        flash('Only doctors can create blog posts!')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '')
        summary = request.form.get('summary', '').strip()
        content = request.form.get('content', '').strip()
        is_draft = 'is_draft' in request.form
        image = request.files.get('image')

        filename = 'default_blog.jpg'
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        blogs = load_json(BLOGS_FILE)
        new_blog_id = get_next_blog_id()
        new_blog = {
            'id': new_blog_id,
            'title': title,
            'image': filename,
            'category': category,
            'summary': summary,
            'content': content,
            'is_draft': is_draft,
            'author_id': int(current_user.id),
            'created_at': datetime.now().isoformat()
        }
        blogs.append(new_blog)
        save_json(BLOGS_FILE, blogs)

        flash('Blog created successfully!')
        return redirect(url_for('blog_list_doctor'))

    return render_template('blog_create.html', categories=CATEGORIES, blog=None)

@app.route('/doctor/blogs')
@login_required
def blog_list_doctor():
    if current_user.role.lower() != 'doctor':
        flash('Access denied!')
        return redirect(url_for('dashboard'))

    blogs = load_json(BLOGS_FILE)
    user_blogs = [b for b in blogs if b['author_id'] == int(current_user.id)]
    user_blogs.sort(key=lambda b: b['created_at'], reverse=True)

    return render_template('blog_list_doctor.html', blogs=user_blogs)

@app.route('/patient/blogs')
@login_required
def blog_list_patient():
    if current_user.role.lower() != 'patient':
        flash('Access denied!')
        return redirect(url_for('dashboard'))

    blogs = load_json(BLOGS_FILE)
    categorized = {cat: [] for cat in CATEGORIES}
    for blog in blogs:
        if not blog.get('is_draft', False) and blog.get('category') in categorized:
            categorized[blog['category']].append(blog)

    # Sort blogs in each category by created_at descending
    for cat_blogs in categorized.values():
        cat_blogs.sort(key=lambda b: b['created_at'], reverse=True)

    return render_template('blog_list_patient.html', categorized_blogs=categorized, any_func=any)

@app.route('/blog/<int:blog_id>')
@login_required
def blog_detail(blog_id):
    blogs = load_json(BLOGS_FILE)
    blog = next((b for b in blogs if b['id'] == blog_id), None)
    if not blog:
        flash('Blog not found!')
        return redirect(url_for('dashboard'))

    # Only author can see draft blogs
    if blog.get('is_draft', False) and blog['author_id'] != int(current_user.id):
        flash('Blog not found!')
        return redirect(url_for('dashboard'))

    # Get author info
    author = find_user_by_id(blog['author_id'])
    return render_template('blog_detail.html', blog=blog, author=author)

if __name__ == '__main__':
    print("Starting Flask application with JSON storage...")
    app.run(debug=True, host='127.0.0.1', port=5000)
