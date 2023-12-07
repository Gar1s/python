from flask import url_for
from application import db
from application.todo.models import Todo
from .base import BaseTest

class TodoTest(BaseTest):
    def test_todo_create(self):
        '''Tests if a new todo item can be created successfully.'''
        data = {
            'title': 'Write flask tests',  
            'description': 'New description', 
        }
        with self.client:
            response = self.client.post(url_for('todo.add'), data=data, 
                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todo added successfully', response.data)
            
            todo = Todo.query.filter_by(title='Write flask tests').first()
            self.assertIsNotNone(todo)
            
    def test_get_all_todo(self):
        '''Tests if retrieving all todo items works correctly.'''
        todo1 = Todo(title='todo1', description='description1', complete=False)
        todo2 = Todo(title='todo2', description='description2', complete=False)
        db.session.add_all([todo1, todo2])
        
        response = self.client.get(url_for('todo.todo'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"{todo1.title}".encode(), response.data)
        self.assertEqual(Todo.query.count(), 2)
        
    def test_update_todo_complete(self):
        '''Tests if marking a todo as complete works correctly.'''
        todo1 = Todo(title='todo1', description='description1', complete=False)
        db.session.add(todo1)
        with self.client:
            response = self.client.get(url_for('todo.update',todo_id=1), follow_redirects=True)
            updated_todo = Todo.query.filter_by(id=1).first()
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todo updated successfully', response.data)
            self.assertTrue(updated_todo.complete)
            
    def test_delete_todo(self):
        '''Tests if deleting a todo item works correctly.'''
        todo1 = Todo(title="todo1", description="description1", complete=False)
        db.session.add(todo1)

        with self.client:
            response = self.client.get(url_for("todo.delete", todo_id=1), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Todo deleted successfully", response.data)

            deleted_todo = Todo.query.filter_by(id=1).first()
            self.assertIsNone(deleted_todo)