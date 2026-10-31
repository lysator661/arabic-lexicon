# Arabic Lexicon — 构建 / 安装 / 打包
PREFIX   ?= /usr
BINDIR   ?= $(PREFIX)/bin
PKGDIR   ?= $(PREFIX)/lib/python3/dist-packages
APPDIR   ?= $(PREFIX)/share/applications
ICODIR   ?= $(PREFIX)/share/icons/hicolor/scalable/apps
DESTDIR  ?=

PYTHON   ?= python3
PKG      ?= arabic_lexicon

.PHONY: all install uninstall clean deb buildpackage test icons

all:
	@echo "项目已就绪。可用目标："
	@echo "  make install        以 PREFIX 安装到本机（默认 /usr/local）"
	@echo "  make install DESTDIR=/tmp/root   打包式安装（staged）"
	@echo "  make deb            构建 .deb 包（需要 debhelper）"
	@echo "  make clean          清理构建产物"
	@echo "  make test           语法检查 + 冒烟测试"

# 安装：Python 模块 + 启动器 + 桌面项 + 图标
install: icons
	install -d "$(DESTDIR)$(BINDIR)" "$(DESTDIR)$(PKGDIR)" \
	          "$(DESTDIR)$(APPDIR)" "$(DESTDIR)$(ICODIR)"
	cp -r "$(PKG)" "$(DESTDIR)$(PKGDIR)/$(PKG)"
	# 去掉 __pycache__，避免打包进 deb
	find "$(DESTDIR)$(PKGDIR)/$(PKG)" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	install -m 755 bin/arabic-lexicon "$(DESTDIR)$(BINDIR)/arabic-lexicon"
	install -m 644 araby.desktop "$(DESTDIR)$(APPDIR)/araby.desktop"
	install -m 644 araby.svg "$(DESTDIR)$(ICODIR)/araby.svg"
	@echo "Installed to $(DESTDIR)$(PREFIX)"

# 卸载
uninstall:
	rm -f  "$(DESTDIR)$(BINDIR)/arabic-lexicon"
	rm -rf "$(DESTDIR)$(PKGDIR)/$(PKG)"
	rm -f  "$(DESTDIR)$(APPDIR)/araby.desktop"
	rm -f  "$(DESTDIR)$(ICODIR)/araby.svg"
	@echo "Uninstalled."

# 更新图标缓存（安装后让桌面立即看到新图标）
icons:
	@if command -v gtk-update-icon-cache >/dev/null 2>&1; then \
		gtk-update-icon-cache -q -t -f "$(DESTDIR)$(PREFIX)/share/icons/hicolor" 2>/dev/null || true; \
	fi

# 语法检查 + 冒烟测试（不启动 GUI）
test:
	$(PYTHON) -m compileall -q "$(PKG)"
	$(PYTHON) -c "import json; d=json.load(open('$(PKG)/data.json')); print('词条数:', len(d))"
	@echo "语法与数据校验通过。"

# 清理
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -f  *.deb *.buildinfo *.changes
	rm -rf debian/.debhelper debian/arabic-lexicon debian/files
	@echo "已清理构建产物。"

# 构建 deb 包（优先 debuild，退回到 dpkg-buildpackage）
deb buildpackage:
	@if command -v debuild >/dev/null 2>&1; then \
		debuild -us -uc -b; \
	elif command -v dpkg-buildpackage >/dev/null 2>&1; then \
		dpkg-buildpackage -us -uc -b; \
	else \
		echo "错误：未找到 debhelper/debuild/dpkg-buildpackage。请先运行："; \
		echo "  sudo apt install -y build-essential devscripts debhelper-compat dh-python"; \
		exit 1; \
	fi
