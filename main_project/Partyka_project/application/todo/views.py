from flask import render_template, redirect, url_for, flash
from application import db
from .models import Todo
from .forms import TodoForm
from . import todo_blueprint

@todo_blueprint.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()
    todo_list = Todo.query.all()
    return render_template("todo.html", form=form, todo_list=todo_list)

@todo_blueprint.route('/add', methods=["POST"])
def add():
    form = TodoForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully', 'success')
    else:
        flash('Invalid input. Please try again.', 'danger')

    return redirect(url_for("todo.todo"))

@todo_blueprint.route('/update/<int:todo_id>')
def update(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    flash('Todo updated successfully', 'success')
    return redirect(url_for('todo.todo'))

@todo_blueprint.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')
    return redirect(url_for('todo.todo'))