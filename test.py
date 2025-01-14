import tkinter as tk
from tkinter import ttk
import psutil
import sqlite3
from datetime import datetime
import threading
import time

class ResourceCheck:
    def __init__(self, check):
        self.check = check
        self.check.title("Отслеживание ресурсов")
        self.check.geometry("600x500")
        self.check.resizable(False, False)

        self.level_loading = ttk.Label(check, text="УРОВЕНЬ ЗАГРУЖЕННОСТИ", font=("Arial", 14))
        self.level_loading.pack(pady=10)
        self.cpu_label = ttk.Label(check, text="ЦП: --%", font=("Arial", 14))
        self.cpu_label.pack(pady=10)

        self.ozu_label = ttk.Label(check, text="ОЗУ: --% (Свободно: -- ГБ / Всего: -- ГБ)", font=("Arial", 14))
        self.ozu_label.pack(pady=10)

        self.pzu_label = ttk.Label(check, text="ПЗУ: --% (Свободно: -- ГБ / Всего: -- ГБ)", font=("Arial", 14))
        self.pzu_label.pack(pady=10)

        self.start_button = ttk.Button(check, text="Начать запись", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(check, text="Остановить запись", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.history_button = ttk.Button(check, text="Просмотреть историю", command=self.show_history)
        self.history_button.pack(pady=10)

        self.recording = False
        self.start_time = None
        self.timer_label = ttk.Label(check, text="Время записи: 0 сек", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        self.setup_database()

        self.update_data()

    def setup_database(self):
        conn = sqlite3.connect("resources.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS records")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_usage REAL,
                ozu_usage REAL,
                ozu_free REAL,
                ozu_total REAL,
                pzu_usage REAL,
                pzu_free REAL,
                pzu_total REAL
            )
        """)
        conn.commit()
        conn.close()

    def update_data(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        ram_free = ram.available / (1024 ** 3)
        ram_total = ram.total / (1024 ** 3)
        
        disk_free = disk.free / (1024 ** 3)
        disk_total = disk.total / (1024 ** 3)

        self.cpu_label.config(text=f"ЦП: {cpu}%")
        self.ozu_label.config(text=f"ОЗУ: {ram.percent}% (Свободно: {ram_free:.2f} ГБ / Всего: {ram_total:.2f} ГБ)")
        self.pzu_label.config(text=f"ПЗУ: {disk.percent}% (Свободно: {disk_free:.2f} ГБ / Всего: {disk_total:.2f} ГБ)")

        self.check.after(1000, self.update_data)

    def start_recording(self):
        self.recording = True
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()

        self.record_thread = threading.Thread(target=self.record_data)
        self.record_thread.daemon = True
        self.record_thread.start()

    def stop_recording(self):
        self.recording = False
        self.start_time = None
        self.timer_label.config(text="Время записи: 0 сек")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.recording:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Время записи: {elapsed} сек")
            self.check.after(1000, self.update_timer)

    def record_data(self):
        conn = sqlite3.connect("resources.db")
        cursor = conn.cursor()

        while self.recording:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            ram_free = ram.available / (1024 ** 3)
            ram_total = ram.total / (1024 ** 3)
            
            disk_free = disk.free / (1024 ** 3)
            disk_total = disk.total / (1024 ** 3)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            INSERT INTO records (timestamp, cpu_usage, ozu_usage, ozu_free, ozu_total, pzu_usage, pzu_free, pzu_total) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, cpu, ram.percent, ram_free, ram_total, disk.percent, disk_free, disk_total))

            conn.commit()
            time.sleep(1)

        conn.close()

    def show_history(self):
        conn = sqlite3.connect("resources.db")
        cursor = conn.cursor()

        history_window = tk.Toplevel(self.check)
        history_window.title("История записей")
        history_window.geometry("800x400")

        tree = ttk.Treeview(history_window, columns=("timestamp", "cpu", "ram", "ram_free", "ram_total", "disk", "disk_free", "disk_total"), show="headings")
        tree.heading("timestamp", text="Время")
        tree.heading("cpu", text="ЦП")
        tree.heading("ram", text="ОЗУ (%)")
        tree.heading("ram_free", text="ОЗУ Свободно (ГБ)")
        tree.heading("ram_total", text="ОЗУ Всего (ГБ)")
        tree.heading("disk", text="ПЗУ (%)")
        tree.heading("disk_free", text="ПЗУ Свободно (ГБ)")
        tree.heading("disk_total", text="ПЗУ Всего (ГБ)")
        tree.pack(fill=tk.BOTH, expand=True)

        cursor.execute("SELECT timestamp, cpu_usage, ozu_usage, ozu_free, ozu_total, pzu_usage, pzu_free, pzu_total FROM records")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        conn.close()

check = tk.Tk()
app = ResourceCheck(check)
check.mainloop()
