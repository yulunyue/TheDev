import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from common.util.export import File


os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"


class StealthBrowser(QMainWindow):
    CONFIG_PATH = "config/setting/qt.json"
    instance = None

    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        StealthBrowser.instance = self
        f = File(self.CONFIG_PATH)
        self.config_mtime = f.get_m_time() if f.exists() else 0

        self.config = self.load_config()
        self.opacity = self.config.get("opacity", 0.9)
        self.setWindowFlags(self.get_window_flags())
        self.init_geometry()
        self.init_ui()
        self.dragging = False
        self.drag_position = QPoint()
        self.controls_visible = False
        self.resizing = False
        self.resize_edge = None
        self.resize_margin = 8
        self.dev_tools_window = None
        self.watch_timer = QTimer()
        self.watch_timer.timeout.connect(self.check_config_change)
        self.watch_timer.start(1000)

    def load_config(self):
        f = File(self.CONFIG_PATH)
        if f.exists():
            return f.read_file()
        return {
            "x": None,
            "y": None,
            "width": 580,
            "height": 350,
            "url": "https://www.google.com",
            "opacity": 0.9,
            "frameless": True,
            "stay_on_top": True,
        }

    def get_window_flags(self):
        flags = Qt.Window
        if self.config.get("frameless", True):
            flags |= Qt.FramelessWindowHint
        if self.config.get("stay_on_top", True):
            flags |= Qt.WindowStaysOnTopHint
        return flags

    def save_config(self):
        File(self.CONFIG_PATH).write_file(self.config)

    def reload_config(self):
        self.config = self.load_config()
        opacity = self.config.get("opacity", 0.9)
        self.opacity = opacity
        self.setWindowOpacity(opacity)
        self.opacity_slider.setValue(int(opacity * 100))
        url = self.config.get("url", "https://www.google.com")
        self.browser.setUrl(QUrl(url))
        x = self.config.get("x")
        y = self.config.get("y")
        width = self.config.get("width", 580)
        height = self.config.get("height", 350)
        if x and y:
            self.setGeometry(x, y, width, height)
        self.setWindowFlags(self.get_window_flags())
        self.show()

    def check_config_change(self):
        f = File(self.CONFIG_PATH)
        if f.exists():
            m_time = f.get_m_time()
            if m_time != self.config_mtime:
                self.config_mtime = m_time
                self.reload_config()

    def init_geometry(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = self.config.get("x")
        y = self.config.get("y")
        width = self.config.get("width", 580)
        height = self.config.get("height", 350)
        if x is None:
            x = screen_geometry.width() - width - 20
        if y is None:
            y = screen_geometry.height() - height - 40
        self.setGeometry(x, y, width, height)

    def init_ui(self):
        """初始化用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 控制面板（默认隐藏）
        self.control_panel = QWidget()
        self.control_panel.setMaximumHeight(40)
        self.control_layout = QHBoxLayout(self.control_panel)
        self.control_layout.setContentsMargins(5, 5, 5, 5)
        self.browser = QWebEngineView()
        settings = self.browser.page().settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.create_control_buttons()
        url = self.config.get("url", "https://www.google.com")
        self.browser.setUrl(QUrl(url))

        # 添加到主布局
        main_layout.addWidget(self.control_panel)
        main_layout.addWidget(self.browser)

        # 初始隐藏控制面板
        self.control_panel.hide()

        # 设置窗口透明度
        self.setWindowOpacity(self.opacity)

        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QWidget {
                background-color: transparent;
            }
            QPushButton {
                background-color: rgba(44, 62, 80, 180);
                color: white;
                border: 1px solid #34495e;
                border-radius: 3px;
                padding: 3px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(52, 73, 94, 200);
                border: 1px solid #4a90e2;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid #34495e;
                border-radius: 3px;
                padding: 3px;
                font-size: 12px;
            }
            QSlider::groove:horizontal {
                height: 4px;
                background: rgba(255, 255, 255, 100);
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
        """)

        # 安装事件过滤器
        self.installEventFilter(self)

    def create_control_buttons(self):
        """创建控制按钮"""
        # 后退按钮
        back_btn = QPushButton("◀")
        back_btn.setFixedWidth(30)
        back_btn.clicked.connect(self.browser.back)
        self.control_layout.addWidget(back_btn)

        # 前进按钮
        forward_btn = QPushButton("▶")
        forward_btn.setFixedWidth(30)
        forward_btn.clicked.connect(self.browser.forward)
        self.control_layout.addWidget(forward_btn)

        # 刷新按钮
        reload_btn = QPushButton("↻")
        reload_btn.setFixedWidth(30)
        reload_btn.clicked.connect(self.browser.reload)
        self.control_layout.addWidget(reload_btn)

        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url_bar)
        self.control_layout.addWidget(self.url_bar)

        # 透明度滑块
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(20, 100)
        self.opacity_slider.setValue(int(self.opacity * 100))
        self.opacity_slider.setFixedWidth(80)
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        self.control_layout.addWidget(QLabel("透明度:"))
        self.control_layout.addWidget(self.opacity_slider)

        # 关闭按钮
        close_btn = QPushButton("×")
        close_btn.setFixedWidth(30)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(231, 76, 60, 180);
            }
            QPushButton:hover {
                background-color: rgba(192, 57, 43, 200);
            }
        """)
        self.control_layout.addWidget(close_btn)

        # 隐藏按钮
        hide_btn = QPushButton("_")
        hide_btn.setFixedWidth(30)
        hide_btn.clicked.connect(self.hide_window)
        self.control_layout.addWidget(hide_btn)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if url:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            self.browser.setUrl(QUrl(url))
            self.config["url"] = url
            self.save_config()

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
        self.config["url"] = q.toString()
        self.save_config()

    def change_opacity(self, value):
        self.opacity = value / 100
        self.setWindowOpacity(self.opacity)
        self.config["opacity"] = self.opacity
        self.save_config()

    def hide_window(self):
        self.hide()

    def get_edge(self, pos):
        geo = self.rect()
        x, y = pos.x(), pos.y()
        margin = self.resize_margin
        edge = 0
        if x <= margin:
            edge |= 1
        elif x >= geo.width() - margin:
            edge |= 2
        if y <= margin:
            edge |= 4
        elif y >= geo.height() - margin:
            edge |= 8
        return edge if edge else None

    def get_cursor_for_edge(self, edge):
        cursors = {
            1: Qt.SizeHorCursor,
            2: Qt.SizeHorCursor,
            4: Qt.SizeVerCursor,
            8: Qt.SizeVerCursor,
            5: Qt.SizeFDiagCursor,
            6: Qt.SizeBDiagCursor,
            9: Qt.SizeBDiagCursor,
            10: Qt.SizeFDiagCursor,
        }
        return cursors.get(edge, Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edge = self.get_edge(event.pos())
            if edge:
                self.resizing = True
                self.resize_edge = edge
                self.resize_start_pos = event.globalPos()
                self.resize_start_geo = self.geometry()
            else:
                self.dragging = True
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resizing and event.buttons() & Qt.LeftButton:
            delta = event.globalPos() - self.resize_start_pos
            geo = self.resize_start_geo
            x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()
            edge = self.resize_edge
            min_w, min_h = 200, 150
            if edge & 1:
                new_w = w - delta.x()
                if new_w >= min_w:
                    x += delta.x()
                    w = new_w
            if edge & 2:
                w = max(min_w, w + delta.x())
            if edge & 4:
                new_h = h - delta.y()
                if new_h >= min_h:
                    y += delta.y()
                    h = new_h
            if edge & 8:
                h = max(min_h, h + delta.y())
            self.setGeometry(x, y, w, h)
            event.accept()
        elif self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        else:
            edge = self.get_edge(event.pos())
            if edge:
                self.setCursor(self.get_cursor_for_edge(edge))
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.resizing = False
            self.resize_edge = None
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

    # 键盘快捷键
    def keyPressEvent(self, event):
        # Ctrl+W 关闭窗口
        if event.key() == Qt.Key_W and event.modifiers() == Qt.ControlModifier:
            self.close()

        # Ctrl+H 隐藏窗口
        elif event.key() == Qt.Key_H and event.modifiers() == Qt.ControlModifier:
            self.hide()

        # Ctrl+↑ 增加透明度
        elif event.key() == Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            new_value = min(100, self.opacity_slider.value() + 10)
            self.opacity_slider.setValue(new_value)

        # Ctrl+↓ 减少透明度
        elif event.key() == Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            new_value = max(20, self.opacity_slider.value() - 10)
            self.opacity_slider.setValue(new_value)

        # F2 切换控制面板
        elif event.key() == Qt.Key_F2:
            if self.controls_visible:
                self.control_panel.hide()
                self.controls_visible = False
            else:
                self.control_panel.show()
                self.controls_visible = True

        # ESC 退出程序
        elif event.key() == Qt.Key_Escape:
            self.close()

        # F11 切换窗口置顶
        elif event.key() == Qt.Key_F11:
            stay_on_top = self.config.get("stay_on_top", True)
            self.config["stay_on_top"] = not stay_on_top
            self.save_config()
            self.setWindowFlags(self.get_window_flags())
            self.show()

        # F12 打开调试工具
        elif event.key() == Qt.Key_F12:
            self.open_dev_tools()

    def open_dev_tools(self):
        if self.dev_tools_window is None:
            self.dev_tools_window = QMainWindow()
            self.dev_tools_window.setWindowTitle("DevTools")
            self.dev_tools_window.resize(800, 600)
            dev_view = QWebEngineView()
            self.dev_tools_window.setCentralWidget(dev_view)
            self.browser.page().setDevToolsPage(dev_view.page())
        self.dev_tools_window.show()

    # 双击切换控制面板
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.controls_visible:
                self.control_panel.hide()
                self.controls_visible = False
            else:
                self.control_panel.show()
                self.controls_visible = True
            event.accept()

    # 右键菜单
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # 添加菜单项
        back_action = menu.addAction("后退")
        back_action.triggered.connect(self.browser.back)

        forward_action = menu.addAction("前进")
        forward_action.triggered.connect(self.browser.forward)

        menu.addSeparator()

        reload_action = menu.addAction("刷新")
        reload_action.triggered.connect(self.browser.reload)

        menu.addSeparator()

        opacity_menu = menu.addMenu("透明度")
        for value in [20, 40, 60, 80, 100]:
            action = opacity_menu.addAction(f"{value}%")
            action.triggered.connect(
                lambda checked, v=value: self.opacity_slider.setValue(v)
            )

        menu.addSeparator()

        toggle_controls = menu.addAction("显示/隐藏控制栏")
        toggle_controls.triggered.connect(self.toggle_controls)

        toggle_stay_on_top = menu.addAction(
            "置顶" if not self.config.get("stay_on_top", True) else "取消置顶"
        )
        toggle_stay_on_top.triggered.connect(self.toggle_stay_on_top)

        toggle_frame = menu.addAction(
            "显示边框" if self.config.get("frameless", True) else "隐藏边框"
        )
        toggle_frame.triggered.connect(self.toggle_frame)

        menu.addSeparator()

        quit_action = menu.addAction("退出")
        quit_action.triggered.connect(self.close)

        menu.exec_(event.globalPos())

    def toggle_controls(self):
        if self.controls_visible:
            self.control_panel.hide()
            self.controls_visible = False
        else:
            self.control_panel.show()
            self.controls_visible = True

    def toggle_stay_on_top(self):
        stay_on_top = self.config.get("stay_on_top", True)
        self.config["stay_on_top"] = not stay_on_top
        self.save_config()
        self.setWindowFlags(self.get_window_flags())
        self.show()

    def toggle_frame(self):
        frameless = self.config.get("frameless", True)
        self.config["frameless"] = not frameless
        self.save_config()
        self.setWindowFlags(self.get_window_flags())
        self.show()

    def closeEvent(self, event):
        geo = self.geometry()
        self.config["x"] = geo.x()
        self.config["y"] = geo.y()
        self.config["width"] = geo.width()
        self.config["height"] = geo.height()
        self.save_config()
        event.accept()

    def exec(self):
        self.app.setStyle("Fusion")
        self.show()
        sys.exit(self.app.exec_())
