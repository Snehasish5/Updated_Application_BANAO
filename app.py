from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:user@localhost/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    profile_pic = db.Column(db.String(100))
    address_line = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    
    # Relationship with blogs
    blogs = db.relationship('Blog', backref='author', lazy=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(100))
    category = db.Column(db.String(100))
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    is_draft = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Blog categories
CATEGORIES = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']

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
        try:
            # Get form data
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
            
            # Validate passwords match
            if password != confirm_password:
                flash('Passwords do not match!')
                return render_template('signup.html')
            
            # Check if username already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists!')
                return render_template('signup.html')
            
            # Handle profile picture upload
            profile_pic = request.files.get('profile_pic')
            filename = 'default.jpg'
            if profile_pic and profile_pic.filename:
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role=role,
                first_name=first_name,
                last_name=last_name,
                profile_pic=filename,
                address_line=address_line,
                city=city,
                state=state,
                pincode=pincode
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')
            return render_template('signup.html')
    
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
        
        user = User.query.filter_by(username=username).first()
        
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

# Blog Routes
@app.route('/blog_create', methods=['GET', 'POST'])
@login_required
def blog_create():
    if current_user.role.lower() != 'doctor':
        flash('Only doctors can create blog posts!')
        return redirect(url_for('dashboard'))

    CATEGORIES = ["Mental Health", "Heart Disease", "Covid19", "Immunization"]
    
    if request.method == 'POST':
        try:
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

            new_blog = Blog(
                title=title,
                image=filename,
                category=category,
                summary=summary,
                content=content,
                is_draft=is_draft,
                author_id=current_user.id
            )
            db.session.add(new_blog)
            db.session.commit()

            flash('Blog created successfully!')
            return redirect(url_for('blog_list_doctor'))
            
        except Exception as e:
            db.session.rollback()
            print("Error in blog_create:", str(e))
            flash(f'An error occurred: {str(e)}')

    return render_template('blog_create.html', categories=CATEGORIES, blog=None)

@app.route('/doctor/blogs')
@login_required
def blog_list_doctor():
    # Only doctors can view this page
    if current_user.role != 'Doctor':
        flash('Access denied!')
        return redirect(url_for('doctor_dashboard'))
    
    blogs = Blog.query.filter_by(author_id=current_user.id).order_by(Blog.created_at.desc()).all()
    return render_template('blog_list_doctor.html', blogs=blogs)

@app.route('/patient/blogs')
@login_required
def blog_list_patient():
    # Only patients can view this page
    if current_user.role != 'Patient':
        flash('Access denied!')
        return redirect(url_for('dashboard'))

    categorized = {cat: [] for cat in CATEGORIES}
    all_blogs = Blog.query.filter_by(is_draft=False).order_by(Blog.created_at.desc()).all()

    for blog in all_blogs:
        if blog.category in categorized:
            categorized[blog.category].append(blog)

    return render_template('blog_list_patient.html', categorized_blogs=categorized, any_func=any)


@app.route('/blog/<int:blog_id>')
@login_required
def blog_detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    
    # Check if user can view this blog
    if blog.is_draft and blog.author_id != current_user.id:
        flash('Blog not found!')
        return redirect(url_for('dashboard'))
    
    return render_template('blog_detail.html', blog=blog)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    print("Starting Flask application...")
    app.run(debug=True, host='127.0.0.1', port=5000)