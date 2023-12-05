from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .models import Post, Category, Tag
from .forms import PostForm, EditPostForm, CategoryForm, EditCategoryForm
from . import post_blueprint
from .utilities import save_picture
from application import db
from sqlalchemy import desc

@post_blueprint.route('/post/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    if form.validate_on_submit():
        category = Category.query.get(form.category.data)
        tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        title = form.title.data
        text = form.text.data
        type = form.type.data
        
        if form.image.data:
            image = save_picture(form.image.data)
        else:
            image = 'postdefault.jpg' 
            
        post = Post(title=title, text=text, image=image, type=type, category=category, tags=tags, user_id=current_user.id) 
        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for("post.create"))
                        
    return render_template("create_post.html", form=form)

@post_blueprint.route('/post', methods=['GET'])
def all_posts():
    page = request.args.get('page', 1, type=int)
    posts_per_page = 3

    posts = Post.query.filter_by(enabled=True).order_by(Post.created.desc()).paginate(page=page, per_page=posts_per_page)

    return render_template('all_posts.html', posts=posts)

@post_blueprint.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@post_blueprint.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = EditPostForm()
    
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    
    if form.validate_on_submit():
        if form.image.data:
            post.image = save_picture(form.image.data)
        else:
            post.image = 'postdefault.jpg'
        try:
            post.title = form.title.data
            post.text = form.text.data
            post.type = form.type.data
            post.enabled = bool(form.enabled.data)
            post.category = Category.query.get(form.category.data)
            post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        
            db.session.commit()
            flash('Post has been updated!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Failed to update! Error: {str(e)}", category="danger") 

        return redirect(url_for('post.view_post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
        form.type.data =  post.type
        form.enabled.data = post.enabled
        form.category.data = post.category_id
        form.tags.data = [tag.id for tag in post.tags]

    return render_template('edit_post.html', post=post, form=form)


@post_blueprint.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('post.all_posts'))




@post_blueprint.route('/categories', methods=['GET', 'POST'])
def categories():
    form = CategoryForm()
    
    if form.validate_on_submit():
        print(form.name.data)
        name = form.name.data
        new_category = Category(name=name)
        try:
            db.session.add(new_category)
            db.session.commit()
            flash('New category added successfully', 'success')
            return redirect(url_for("post.categories"))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            
    categories = Category.query.all()

    return render_template('categories.html', form=form, categories=categories)


@post_blueprint.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = EditCategoryForm()
    
    if form.validate_on_submit():
        try:
            category.name = form.name.data
            db.session.commit()
            flash('Category has been updated!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Failed to update! Error: {str(e)}", category="danger") 

        return redirect(url_for('post.categories'))

    elif request.method == 'GET':
        form.name.data = category.name

    return render_template('edit_category.html', category=category, form=form)

@post_blueprint.route('/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('post.categories'))
