import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QListWidgetItem,  # Eklendi
)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from qtawesome import icon

class ToDoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My To-Do List")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.task_input = QLineEdit(self)
        self.add_button = QPushButton(icon("fa.plus", color="blue"), "Add Task", self)
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; border: 1px solid #357f3a;")
        self.add_button.clicked.connect(self.add_task)

        self.tasks_list = QListWidget(self)
        self.tasks_list.setStyleSheet("border: 1px solid #ccc; background-color: #f7f7f7;")
        self.tasks_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_list.customContextMenuRequested.connect(self.show_context_menu)
        self.delete_button = QPushButton(icon("fa.trash", color="red"), "Delete Task", self)
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; border: 1px solid #d32f2f;")
        self.delete_button.clicked.connect(self.delete_task)

        self.layout.addWidget(self.task_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.tasks_list)
        self.layout.addWidget(self.delete_button)

        self.tasks = []
        self.load_tasks_from_database()

    def load_tasks_from_database(self):
        try:
            connection = sqlite3.connect('todo.db')
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS tasks (task TEXT)')
            cursor.execute('SELECT task FROM tasks')
            tasks = cursor.fetchall()
            for task in tasks:
                item = QListWidgetItem(task[0])
                item.setForeground(QColor(Qt.black))  # Set text color to black
                self.tasks_list.addItem(item)
                self.tasks.append(task[0])
            connection.close()
        except sqlite3.Error as e:
            print("SQLite error:", str(e))

    def save_task_to_database(self, task):
        try:
            connection = sqlite3.connect('todo.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            print("SQLite error:", str(e))

    def add_task(self):
        task = self.task_input.text()
        if task:
            self.save_task_to_database(task)
            self.tasks.append(task)
            item = QListWidgetItem(task)
            item.setForeground(QColor(Qt.black))  # Set text color to black
            self.tasks_list.addItem(item)
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a task.")

    def delete_task(self):
        selected_item = self.tasks_list.currentItem()
        if selected_item:
            task = selected_item.text()
            confirm = QMessageBox.question(self, "Confirm Delete", f"Delete task: {task}?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.tasks.remove(task)
                self.tasks_list.takeItem(self.tasks_list.row(selected_item))
                self.delete_task_from_database(task)

    def delete_task_from_database(self, task):
        try:
            connection = sqlite3.connect('todo.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM tasks WHERE task = ?', (task,))
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            print("SQLite error:", str(e))

    def show_context_menu(self, event):
        context_menu = self.tasks_list.contextMenuPolicy()
        delete_action = context_menu.addAction(icon("fa.trash", color="red"), "Delete Task")
        action = context_menu.exec_(self.tasks_list.mapToGlobal(event))
        if action == delete_action:
            self.delete_task()

def main(dark_mode=False):
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use the Fusion style for better appearance

    # Tema ayarlamaları
    if dark_mode:
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)

    todo_app = ToDoListApp()
    todo_app.show()
    exit_code = app.exec_()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
