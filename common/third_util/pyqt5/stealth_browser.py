import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


class StealthBrowser(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

        # 无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 窗口初始位置和大小
        screen_geometry = QApplication.desktop().availableGeometry()
        self.setGeometry(
            screen_geometry.width() - 600,  # 右侧
            screen_geometry.height() - 400,  # 底部
            580,  # 宽度
            350,  # 高度
        )
        # 初始化透明度
        self.opacity = 0.9
        # 初始化窗口
        self.init_ui()

        # 窗口拖动相关变量
        self.dragging = False
        self.drag_position = QPoint()

        # 隐藏控制面板
        self.controls_visible = False

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
        # 创建控制按钮
        self.create_control_buttons()

        # 浏览器视图

        self.browser.setUrl(QUrl("https://www.google.com"))

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
        """导航到输入的URL"""
        url = self.url_bar.text().strip()
        if url:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        """更新地址栏显示当前URL"""
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def change_opacity(self, value):
        """改变窗口透明度"""
        self.opacity = value / 100
        self.setWindowOpacity(self.opacity)

    def hide_window(self):
        """隐藏窗口"""
        self.hide()
        # 5秒后自动显示（可选）
        # QTimer.singleShot(5000, self.show)

    # 鼠标事件处理 - 实现窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
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
            if self.windowFlags() & Qt.WindowStaysOnTopHint:
                self.setWindowFlags(Qt.FramelessWindowHint)
            else:
                self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.show()

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

        menu.addSeparator()

        quit_action = menu.addAction("退出")
        quit_action.triggered.connect(self.close)

        menu.exec_(event.globalPos())

    def toggle_controls(self):
        """切换控制面板显示"""
        if self.controls_visible:
            self.control_panel.hide()
            self.controls_visible = False
        else:
            self.control_panel.show()
            self.controls_visible = True

    def exec(self):
        self.app.setStyle("Fusion")
        self.show()
        sys.exit(self.app.exec_())
