import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Настройки
HISTORY_FILE = "tasks.json"
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Посмотреть обучающее видео", "type": "учёба"},
    {"text": "Разобрать почту", "type": "работа"},
    {"text": "Погулять на свежем воздухе", "type": "отдых"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Генератор случайных задач")
        self.root.geometry("550x650")
        self.root.resizable(True, True)

        # Загрузка данных
        self.tasks = self.load_tasks()

        # Фильтр по типу
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5, fill=tk.X)
        tk.Label(filter_frame, text="Фильтр по типу:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="все")
        filter_options = ["все"] + sorted(set(task["type"] for task in self.tasks))
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly", width=12)
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        self.filter_var.trace_add("write", self.update_history_list)

        # Кнопка генерации
        tk.Button(root, text="✨ Сгенерировать задачу", bg="#4CAF50", fg="white", font=("Arial", 11), command=self.generate_task).pack(pady=10, fill=tk.X)

        # Поле текущей задачи
        self.current_task_label = tk.Label(root, text="Задача появится здесь", font=('Arial', 12, 'bold'), wraplength=500, fg="darkblue")
        self.current_task_label.pack(pady=10)

        # История задач
        history_frame = tk.Frame(root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        tk.Label(history_frame, text="История задач:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
        self.history_listbox = tk.Listbox(history_frame, height=10, font=("Arial", 10))
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)

        # Блок добавления новой задачи
        add_frame = tk.Frame(root)
        add_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(add_frame, text="Задача:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.task_entry = tk.Entry(add_frame, width=25, font=("Arial", 10))
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.new_type_var = tk.StringVar(value="работа")
        self.type_combo = ttk.Combobox(add_frame, textvariable=self.new_type_var, values=["учёба", "работа", "спорт", "отдых"], state="readonly", width=8)
        self.type_combo.pack(side=tk.LEFT, padx=5)

        tk.Button(add_frame, text="➕ Добавить", command=self.add_new_task, bg="#2196F3", fg="white").pack(side=tk.LEFT)

        # Кнопка очистки истории
        tk.Button(root, text="🗑 Очистить историю", command=self.clear_history, fg="white", bg="#f44336").pack(pady=5)

        # Инициализация истории
        self.update_history_list()

    def load_tasks(self):
        """Загрузка задач из JSON или возврат дефолтных."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return data
            except (json.JSONDecodeError, IOError):
                pass
        # Если файл повреждён или пуст — возвращаем дефолт
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_TASKS, f, ensure_ascii=False, indent=2)
        return DEFAULT_TASKS.copy()

    def save_tasks(self):
        """Сохранение задач в JSON."""
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def update_history_list(self, *args):
        """Обновление списка истории с фильтром."""
        self.history_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()
        for task in reversed(self.tasks):
            if filter_type == "все" or task["type"] == filter_type:
                self.history_listbox.insert(tk.END, f"{task['text']} ({task['type']})")

    def generate_task(self):
        """Генерация случайной задачи."""
        if not self.tasks:
            messagebox.showwarning("Предупреждение", "Список задач пуст!")
            return
        selected_task = random.choice(self.tasks)
        self.current_task_label.config(
            text=f"📌 {selected_task['text']}\n🏷 {selected_task['type'].capitalize()}",
            bg="#e8f5e8",
            relief="solid",
            padx=10,
            pady=5
        )

    def add_new_task(self):
        """Добавление новой задачи."""
        task_text = self.task_entry.get().strip()
        task_type = self.new_type_var.get()

        if not task_text:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return

        # Проверим, нет ли уже такой задачи
        if any(t["text"] == task_text and t["type"] == task_type for t in self.tasks):
            messagebox.showinfo("Уже есть", "Такая задача уже существует!")
            return

        new_task = {"text": task_text, "type": task_type}
        self.tasks.insert(0, new_task)  # В начало — как самая свежая
        self.save_tasks()
        self.update_history_list()
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Готово", f"Задача '{task_text}' добавлена!")

    def clear_history(self):
        """Очистка истории."""
        if messagebox.askyesno("Подтвердить", "Очистить всю историю задач?"):
            self.tasks = DEFAULT_TASKS.copy()  # Или оставить пустым — как хочешь
            self.save_tasks()
            self.update_history_list()
            self.current_task_label.config(text="История очищена", bg="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
