**Health Blog & Dashboard Web Application**:


A Flask-based multi-role web application for doctors and patients to manage health profiles, write and read health-related blog posts, and maintain user-specific dashboards.



**Features**
User Roles: Supports Doctors and Patients with role-based access.

Authentication: Secure login/signup with password hashing.



**Doctor Dashboard**:

Create, edit, and publish blog posts.

Upload images for blogs.

Manage blog visibility (draft/published).



**Patient Dashboard**:

View profile details.

Browse published blog posts by category.

Read blog post details.



**Blog Management**:

Categorized blogs (Mental Health, Heart Disease, Covid19, Immunization).

Blog summaries truncated for listing.

Blog detail pages with full content and images.


**File Uploads**:

Profile pictures and blog images stored in static/uploads.

Responsive UI with HTML templates and CSS styling.

Role-based access control to secure sensitive pages and actions.

Flask-Migrate support for database migrations.



**Tech Stack**:

*Backend*: Python 3, Flask, Flask-Login, Flask-Migrate, SQLAlchemy


*Database*: MySQL (using mysql+pymysql)


*Frontend*: HTML, CSS, Jinja2 templates


*File Handling*: Werkzeug for secure file uploads


*Password Security*: Werkzeug security utilities



**Setup & Installation**:

*Clone the repository*

git clone https://github.com/yourusername/health-blog-dashboard.git
cd health-blog-dashboard


*Create & activate a virtual environment*:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows


*Install dependencies*:

pip install -r requirements.txt


*Configure MySQL database*:

Create a MySQL database, e.g., health_db.

Update app.config['SQLALCHEMY_DATABASE_URI'] in app.py with your MySQL username, password, host, and database name.


*Run database migrations*:


flask db init
flask db migrate -m "Initial migration"
flask db upgrade


*Create upload folder*

mkdir -p static/uploads


*Run the Flask application*:

python app.py

*Open browser and visit http://127.0.0.1:5000*



**Usage**

Signup as Doctor or Patient.

Doctors can create blog posts, upload images, save drafts, and toggle publish status.

Patients can view and browse only published blogs, organized by categories.

Users can view detailed blog posts with full content.

Profile pictures and blog images are uploaded and displayed from the server.



**Folder Structure**

health-blog-dashboard/
│
|
├── app.py   
|
├── migrations/    
|
├── static/
|
│   ├── css/ 
|
|        ├── style.css
|
|   ├──js/
|
|        ├── script.js
|
│   └── uploads/                               # store the uploaded photos   
|
├── templates/
|
│   ├── index.html
|
│   ├── login.html
|
│   ├── signup.html
|
│   ├── dashboard.html
|
|   ├── doctor_dashboard.html
|
|   ├── patient_dashboard.html
|
│   ├── blog_create.html
|
│   ├── blog_list_doctor.html
|
│   ├── blog_list_patient.html
|
│   └── blog_detail.html
|
└── README.md



**Important Notes**:


Only doctors can create and manage blogs.

Blogs in draft mode are visible only to the author doctor.

Published blogs are visible to all patients.

Profile pictures default to default.jpg if none uploaded.

Secure your SECRET_KEY for production environments.

Ensure proper permissions for the upload folder.
