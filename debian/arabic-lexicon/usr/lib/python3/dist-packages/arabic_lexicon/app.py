# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLineEdit, QLabel, QTextBrowser
)
from PyQt6.QtCore import Qt

# 词典数据路径：优先使用同目录下的 data.json（源码/开发模式），
# 其次使用 /usr/lib/python3/dist-packages 下的安装路径。
_HERE = Path(__file__).parent
DATA = _HERE / "data.json"
if not DATA.exists():
    DATA = Path("/usr/lib/python3/dist-packages/arabic_lexicon/data.json")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arabic Lexicon")
        self.resize(560, 460)

        # —— RTL 适配核心 ——
        # 1) 窗口整体布局方向设为从右到左
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)

        self.input = QLineEdit()
        self.input.setPlaceholderText("اكتب كلمة عربية…")  # 写阿拉伯词…
        self.input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.input.textChanged.connect(self.lookup)

        self.pos_label = QLabel()
        self.pos_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.meanings = QTextBrowser()
        self.meanings.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.meanings.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.examples = QTextBrowser()
        self.examples.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.examples.setAlignment(Qt.AlignmentFlag.AlignRight)

        lay.addWidget(QLabel("Arabic → English"))
        lay.addWidget(self.input)
        lay.addWidget(self.pos_label)
        lay.addWidget(QLabel("Meanings:"))
        lay.addWidget(self.meanings)
        lay.addWidget(QLabel("Examples:"))
        lay.addWidget(self.examples)

        self.data = json.loads(DATA.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------
    # 查询逻辑
    # ------------------------------------------------------------------
    def lookup(self):
        word = self.input.text().strip()
        entry = self.data.get(word)
        if not entry:
            self.pos_label.clear()
            self.meanings.clear()
            self.examples.clear()
            if word:
                self.meanings.setPlainText("No entry found.")
            return

        self.pos_label.setText(f"<b>POS:</b> {entry.get('pos', '')}")

        # meanings: 英文，保持 LTR
        self.meanings.setMarkdown("- " + "\n- ".join(entry.get("meanings", [])))

        # examples: 阿语用 dir=rtl，英文回译用 dir=ltr 包裹，双向文本不乱
        ex = ""
        for e in entry.get("examples", []):
            ex += (
                f"<p dir='rtl'>{e['ar']}"
                f"<br><span dir='ltr'>↳ {e['en']}</span></p>"
            )
        self.examples.setHtml(ex)


def main():
    # Wayland 优先，失败自动回退 X11；不在脚本/desktop 里写死后端。
    os.environ.setdefault("QT_QPA_PLATFORM", "wayland;xcb")
    app = QApplication([])
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    win = MainWindow()
    win.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
