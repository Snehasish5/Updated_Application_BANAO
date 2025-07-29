from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Blog, User
import os

blog_bp = Blueprint('blog', __name__, template_folder='templates')

CATEGORIES = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']

@blog_bp.route('/blog/create', methods=['GET', 'POST'])
@login_required
def blog_create():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        summary = request.form['summary']
        content = request.form['content']
        is_draft = 'is_draft' in request.form
        image = request.files['image']

        filename = secure_filename(image.filename)
        image.save(os.path.join('static/uploads', filename))

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
        return redirect(url_for('blog.blog_list_doctor'))

    return render_template('blog_create.html', categories=CATEGORIES)

@blog_bp.route('/doctor/blogs')
@login_required
def blog_list_doctor():
    blogs = Blog.query.filter_by(author_id=current_user.id).all()
    return render_template('blog_list_doctor.html', blogs=blogs)

@blog_bp.route('/patient/blogs')
@login_required
def blog_list_patient():
    categorized = {cat: [] for cat in CATEGORIES}
    all_blogs = Blog.query.filter_by(is_draft=False).all()
    for blog in all_blogs:
        if blog.category in categorized:
            categorized[blog.category].append(blog)
    return render_template('blog_list_patient.html', categories=categorized)
