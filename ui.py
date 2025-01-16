import tkinter as tk
from tkinter import ttk
from threading import Thread

class ResourceCheckUI:
    def __init__(self, root, logic):
        self.logic = logic
        self.root = root
        self.recording = False
        self.start_time = None

        self.setup_ui()

    def setup_ui(self):
        self.level_loading = ttk.Label(self.root, text="УРОВЕНЬ ЗАГРУЖЕННОСТИ", font=("Arial", 14))
        self.level_loading.pack(pady=10)

        self.cpu_label = ttk.Label(self.root, text="ЦП: --%", font=("Arial", 14))
        self.cpu_label.pack(pady=10)

        self.ozu_label = ttk.Label(self.root, text="ОЗУ: --% (Свободно: -- ГБ / Всего: -- ГБ)", font=("Arial", 14))
        self.ozu_label.pack(pady=10)

        self.pzu_label = ttk.Label(self.root, text="ПЗУ: --% (Свободно: -- ГБ / Всего: -- ГБ)", font=("Arial", 14))
        self.pzu_label.pack(pady=10)

        self.start_button = ttk.Button(self.root, text="Начать запись", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Остановить запись", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.history_button = ttk.Button(self.root, text="Просмотреть историю", command=self.show_history)
        self.history_button.pack(pady=10)

        self.timer_label = ttk.Label(self.root, text="Время записи: 0 сек", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        self.update_data()

    def update_data(self):
        data = self.logic.get_current_data()
        self.cpu_label.config(text=f"ЦП: {data['cpu']}%")
        self.ozu_label.config(
            text=f"ОЗУ: {data['ram_percent']}% (Свободно: {data['ram_free']:.2f} ГБ / Всего: {data['ram_total']:.2f} ГБ)"
        )
        self.pzu_label.config(
            text=f"ПЗУ: {data['disk_percent']}% (Свободно: {data['disk_free']:.2f} ГБ / Всего: {data['disk_total']:.2f} ГБ)"
        )
        self.root.after(1000, self.update_data)

    def start_recording(self):
        self.recording = True
        self.start_time = self.logic.start_recording()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()
        Thread(target=self.logic.record_data, args=(self,)).start()

    def stop_recording(self):
        self.recording = False
        self.logic.stop_recording()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.timer_label.config(text="Время записи: 0 сек")

    def update_timer(self):
        if self.recording
