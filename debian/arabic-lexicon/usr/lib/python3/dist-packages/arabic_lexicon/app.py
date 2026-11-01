import tkinter as tk
from tkinter import ttk, messagebox
from arabic_lexicon.db import get_connection, init_db, get_all_entries, DEFAULT_DB_PATH

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("阿拉伯语词典")

        # 初始化数据库
        self.conn = get_connection()
        init_db(self.conn)

        # UI 布局
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 刷新按钮
        self.btn_refresh = ttk.Button(self.frame, text="刷新词库", command=self.refresh_list)
        self.btn_refresh.pack(side=tk.TOP, fill=tk.X, pady=5)

        # 列表框 (绑定 StringVar 实现动态更新)[2,3](@ref)
        self.list_var = tk.StringVar(value=[])
        self.listbox = tk.Listbox(
            self.frame,
            listvariable=self.list_var,
            font=("Noto Sans Arabic", 14),
            height=15
        )
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 详情标签
        self.detail_label = ttk.Label(self.frame, text="选择词条查看详情", wraplength=400)
        self.detail_label.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.listbox.bind("<<ListSelection>>", self.show_detail)
        self.refresh_list()

    def refresh_list(self):
        """从 SQLite 重新读取并刷新列表"""
        entries = get_all_entries(self.conn)
        self.entries_cache = entries
        # 格式化显示文本
        display_list = [f"{e['arabic']} - {e['meaning']}" for e in entries]
        self.list_var.set(display_list) # 动态更新 Listbox[4](@ref)

    def show_detail(self, event):
        sel = self.listbox.curselection()
        if not sel: return
        e = self.entries_cache[sel[0]]
        text = f"类型: {e['type']}\n含义: {e['meaning']}\n例句: {e['example_ar']}"
        self.detail_label.config(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
