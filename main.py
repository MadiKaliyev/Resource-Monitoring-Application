import tkinter as tk
from ui import ResourceCheckUI
from logic import ResourceCheckLogic
from database import Database

def main():
    root = tk.Tk()
    root.title("Отслеживание ресурсов")
    root.geometry("600x500")
    root.resizable(False, False)

    db = Database("resources.db")
    logic = ResourceCheckLogic(db)
    app = ResourceCheckUI(root, logic)

    root.mainloop()

if __name__ == "__main__":
    main()
