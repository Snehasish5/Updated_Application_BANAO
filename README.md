**Health Blog & Dashboard Web Application**:


A Flask-based multi-role web application for doctors and patients to manage health profiles, write and read health-related blog posts, and maintain user-specific dashboards.



**Features**:


1.*User Roles*: Supports Doctors and Patients with role-based access.



2.*Authentication*: Secure login/signup with password hashing.



3.*Doctor Dashboard*:


Create, edit, and publish blog posts.

Upload images for blogs.

Manage blog visibility (draft/published).



4.*Patient Dashboard*:


View profile details.

Browse published blog posts by category.

Read blog post details.



5.*Blog Management*:


Categorized blogs (Mental Health, Heart Disease, Covid19, Immunization).

Blog summaries truncated for listing.

Blog detail pages with full content and images.


6.*File Uploads*:

Profile pictures and blog images stored in static/uploads.

Responsive UI with HTML templates and CSS styling.

Role-based access control to secure sensitive pages and actions.

Flask-Migrate support for database migrations.



**Tech Stack**:


1.*Backend*: Python 3, Flask, Flask-Login, Flask-Migrate, SQLAlchemy


2.*Database*: MySQL (using mysql+pymysql)


3.*Frontend*: HTML, CSS, Jinja2 templates


4.*File Handling*: Werkzeug for secure file uploads


5.*Password Security*: Werkzeug security utilities



**Setup & Installation**:


1.*Clone the repository*

--git clone https://github.com/yourusername/health-blog-dashboard.git
--cd health-blog-dashboard


2.*Create & activate a virtual environment*:

--python -m venv venv
--source venv/bin/activate   # Linux/macOS
--venv\Scripts\activate      # Windows


3.*Install dependencies*:

--pip install flask


4.*Configure MySQL database*:

--Create a MySQL database, e.g., health_db.

--Update app.config['SQLALCHEMY_DATABASE_URI'] in app.py with your MySQL username, password, host, and database name.


5.*Run database migrations*:


--flask db init
--flask db migrate -m "Initial migration"
--flask db upgrade


6.*Create upload folder*

--mkdir -p static/uploads


7.*Run the Flask application*:

--python app.py

*--Open browser and visit http://127.0.0.1:5000*



**Usage**

Signup as Doctor or Patient.

Doctors can create blog posts, upload images, save drafts, and toggle publish status.

Patients can view and browse only published blogs, organized by categories.

Users can view detailed blog posts with full content.

Profile pictures and blog images are uploaded and displayed from the server.



**Folder Structure**

health-blog-dashboard/
│

├── app.py   

├── migrations/    

├── static/

│   ├── css/ 

|        ├── style.css

|   ├──js/

|        ├── script.js

│   └── uploads/                               # store the uploaded photos   

├── templates/

│   ├── index.html

│   ├── login.html

│   ├── signup.html

│   ├── dashboard.html

|   ├── doctor_dashboard.html

|   ├── patient_dashboard.html

│   ├── blog_create.html

│   ├── blog_list_doctor.html

│   ├── blog_list_patient.html

│   └── blog_detail.html

└── README.md



**Important Notes**:


Only doctors can create and manage blogs.

Blogs in draft mode are visible only to the author doctor.

Published blogs are visible to all patients.

Profile pictures default to default.jpg if none uploaded.

Secure your SECRET_KEY for production environments.

Ensure proper permissions for the upload folder.
