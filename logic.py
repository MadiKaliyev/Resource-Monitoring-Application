import psutil
import time
from datetime import datetime

class ResourceCheckLogic:
    def __init__(self, db):
        self.db = db
        self.recording = False
        self.start_time = None

    def get_current_data(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "cpu": cpu,
            "ram_percent": ram.percent,
            "ram_free": ram.available / (1024 ** 3),
            "ram_total": ram.total / (1024 ** 3),
            "disk_percent": disk.percent,
            "disk_free": disk.free / (1024 ** 3),
            "disk_total": disk.total / (1024 ** 3),
        }

    def start_recording(self):
        self.recording = True
        self.start_time = time.time()
        return self.start_time

    def stop_recording(self):
        self.recording = False

    def get_elapsed_time(self, start_time):
        return int(time.time() - start_time)

    def record_data(self, ui):
        while self.recording:
            data = self.get_current_data()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.insert_record((
                timestamp,
                data["cpu"],
                data["ram_percent"],
                data["ram_free"],
                data["ram_total"],
                data["disk_percent"],
                data["disk_free"],
                data["disk_total"],
            ))
            time.sleep(1)

    def get_history(self):
        return self.db.get_history()
