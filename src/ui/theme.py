"""
Theme styles for AudioTrans AI
现代化浅色主题 (Windows 11 风格)
"""

# 主色调
PRIMARY_COLOR = "#0078D4"  # Windows蓝
PRIMARY_HOVER = "#106EBE"
PRIMARY_PRESSED = "#005A9E"
BG_WHITE = "#FFFFFF"
BG_LIGHT_GRAY = "#F3F3F3"
BG_MEDIUM_GRAY = "#E5E5E5"
BG_DARK_GRAY = "#F9F9F9"
TEXT_PRIMARY = "#1A1A1A"
TEXT_SECONDARY = "#666666"
TEXT_TERTIARY = "#999999"
BORDER_COLOR = "#D1D1D1"
SUCCESS_COLOR = "#107C10"
ERROR_COLOR = "#D13438"
WARNING_COLOR = "#FFB900"

# 完整QSS样式表
MAIN_STYLE = f"""
/* 全局样式 */
QMainWindow {{
    background-color: {BG_WHITE};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 13px;
}}

QWidget {{
    background-color: {BG_WHITE};
    color: {TEXT_PRIMARY};
}}

QLabel {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    padding: 3px;
}}

QGroupBox {{
    background-color: {BG_LIGHT_GRAY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    margin-top: 12px;
    padding: 12px;
    font-weight: 600;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {PRIMARY_COLOR};
    font-weight: 600;
}}

/* 按钮样式 */
QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
    min-height: 28px;
}}

QPushButton:hover {{
    background-color: {PRIMARY_HOVER};
}}

QPushButton:pressed {{
    background-color: {PRIMARY_PRESSED};
}}

QPushButton:disabled {{
    background-color: {BG_MEDIUM_GRAY};
    color: {TEXT_TERTIARY};
}}

QPushButton[secondary="true"] {{
    background-color: {BG_MEDIUM_GRAY};
    color: {TEXT_PRIMARY};
}}

QPushButton[secondary="true"]:hover {{
    background-color: {BORDER_COLOR};
}}

/* 输入框 */
QLineEdit {{
    background-color: {BG_WHITE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 4px;
    padding: 8px 12px;
    selection-background-color: {PRIMARY_COLOR};
}}

QLineEdit:focus {{
    border: 2px solid {PRIMARY_COLOR};
}}

QLineEdit:disabled {{
    background-color: {BG_LIGHT_GRAY};
    color: {TEXT_TERTIARY};
}}

/* 下拉框 */
QComboBox {{
    background-color: {BG_WHITE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 4px;
    padding: 8px 12px;
}}

QComboBox:hover {{
    border: 1px solid {PRIMARY_COLOR};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {TEXT_SECONDARY};
    margin-right: 8px;
}}

QComboBox QAbstractItemView {{
    background-color: {BG_WHITE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    selection-background-color: {PRIMARY_COLOR};
    outline: none;
    padding: 4px;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px;
    border-radius: 2px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {BG_LIGHT_GRAY};
}}

/* 单选按钮 */
QRadioButton {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    spacing: 10px;
    padding: 6px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid {BORDER_COLOR};
    background-color: {BG_WHITE};
}}

QRadioButton::indicator:hover {{
    border-color: {PRIMARY_COLOR};
}}

QRadioButton::indicator:checked {{
    border: 2px solid {PRIMARY_COLOR};
    background-color: {PRIMARY_COLOR};
}}

/* 复选框 */
QCheckBox {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    spacing: 8px;
    padding: 4px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 2px solid {BORDER_COLOR};
    background-color: {BG_WHITE};
}}

QCheckBox::indicator:hover {{
    border-color: {PRIMARY_COLOR};
}}

QCheckBox::indicator:checked {{
    border-color: {PRIMARY_COLOR};
    background-color: {PRIMARY_COLOR};
}}

/* 进度条 */
QProgressBar {{
    background-color: {BG_MEDIUM_GRAY};
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}}

QProgressBar::chunk {{
    background-color: {PRIMARY_COLOR};
    border-radius: 4px;
}}

/* 文本编辑框 */
QTextEdit {{
    background-color: {BG_WHITE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 4px;
    padding: 8px;
    selection-background-color: {PRIMARY_COLOR};
}}

/* 表格 */
QTableWidget {{
    background-color: {BG_WHITE};
    alternate-background-color: {BG_LIGHT_GRAY};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 4px;
    gridline-color: {BG_MEDIUM_GRAY};
}}

QTableWidget::item {{
    padding: 6px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: {PRIMARY_COLOR};
    color: white;
}}

QHeaderView::section {{
    background-color: {BG_LIGHT_GRAY};
    color: {TEXT_PRIMARY};
    padding: 8px 12px;
    border: none;
    border-bottom: 2px solid {PRIMARY_COLOR};
    font-weight: 600;
}}

/* 堆叠窗口 */
QStackedWidget {{
    background-color: {BG_LIGHT_GRAY};
    border-radius: 8px;
    padding: 20px;
}}

/* 状态栏 */
QStatusBar {{
    background-color: {BG_LIGHT_GRAY};
    color: {TEXT_SECONDARY};
    padding: 6px 12px;
    border-top: 1px solid {BORDER_COLOR};
}}

QStatusBar QLabel {{
    color: {TEXT_SECONDARY};
}}

/* 导航按钮 */
QPushButton#navButton {{
    background-color: {BG_MEDIUM_GRAY};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#navButton:hover {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border-color: {PRIMARY_COLOR};
}}

QPushButton#navButton:disabled {{
    background-color: {BG_LIGHT_GRAY};
    color: {TEXT_TERTIARY};
    border-color: transparent;
}}

/* 步骤标题 */
QLabel#stepTitle {{
    font-size: 16px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    padding: 12px;
    background-color: transparent;
}}

/* 滚动条 */
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background-color: {BG_MEDIUM_GRAY};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {BORDER_COLOR};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: transparent;
    height: 10px;
    border: none;
}}

QScrollBar::handle:horizontal {{
    background-color: {BG_MEDIUM_GRAY};
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {BORDER_COLOR};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* 消息框 */
QMessageBox {{
    background-color: {BG_WHITE};
}}

QMessageBox QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
}}

/* 工具提示 */
QToolTip {{
    background-color: {BG_DARK_GRAY};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    padding: 4px 8px;
    border-radius: 4px;
}}
"""

# 步骤指示器样式 - 浅色
STEP_INDICATOR_LIGHT = f"""
QLabel#stepIndicator {{
    font-size: 20px;
    font-weight: bold;
    color: {PRIMARY_COLOR};
    padding: 15px;
    background-color: {BG_LIGHT_GRAY};
    border-radius: 10px;
}}
"""

# 步骤按钮样式 - 浅色主题
STEP_BUTTON_STYLE = """
    QLabel {
        background-color: #E5E5E5;
        border-radius: 14px;
        color: #666666;
        font-weight: 600;
        font-size: 12px;
    }
"""

STEP_CURRENT_STYLE = """
    QLabel {
        background-color: #0078D4;
        border-radius: 14px;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 12px;
    }
"""

STEP_DONE_STYLE = """
    QLabel {
        background-color: #107C10;
        border-radius: 14px;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 12px;
    }
"""