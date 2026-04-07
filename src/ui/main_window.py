"""
Main Window - Application main window with step wizard
主窗口 - 应用主窗口，包含步骤向导
"""
import os
import sys
import traceback
from pathlib import Path

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QStackedWidget, QProgressBar,
                             QTextEdit, QMessageBox, QFileDialog, QLineEdit,
                             QRadioButton, QButtonGroup, QGroupBox, QTableWidget,
                             QTableWidgetItem, QComboBox, QInputDialog, QHeaderView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from utils.config_manager import ConfigManager
from utils.file_utils import FileUtils
from core.whisper_transcriber import WhisperTranscriber
from core.translator import Translator


class MainWindow(QMainWindow):
    """Main application window with 12-step wizard"""

    def __init__(self, whisper_model=None):
        super().__init__()
        self.config = ConfigManager()
        self.whisper = whisper_model  # Use pre-loaded model
        self.translator = None
        self.current_step = 1
        self.total_steps = 12

        # Step data storage
        self.source_dir = ""
        self.output_dir = ""
        self.audio_files = []
        self.filtered_files = []
        self.new_filenames = []
        self.is_loading_model = False

        self._init_ui()
        self._init_models()

    def _init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("AudioTrans AI - 音转译 AI")
        self.setGeometry(100, 100, 900, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Step indicator
        self.step_label = QLabel(f"步骤 1/12: 选择目录")
        self.step_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.step_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.step_label)

        # Step content area
        self.step_stack = QStackedWidget()
        layout.addWidget(self.step_stack)

        # Create all step pages
        self._create_step_pages()

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("上一步")
        self.prev_btn.clicked.connect(self._prev_step)
        self.next_btn = QPushButton("下一步")
        self.next_btn.clicked.connect(self._next_step)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)

        # Status bar
        self.statusBar().showMessage("就绪")

        self._update_navigation()

    def _init_models(self):
        """Initialize ML models (lazy load)"""
        pass

    def _create_step_pages(self):
        """Create all 12 step pages"""
        self.step1_widget = self._create_step1()
        self.step2_widget = self._create_step2()
        self.step3_widget = self._create_step3()
        self.step4_widget = self._create_step4()
        self.step5_widget = self._create_step5()
        self.step6_widget = self._create_step6()
        self.step7_widget = self._create_step7()
        self.step8_widget = self._create_step8()
        self.step9_widget = self._create_step9()
        self.step10_widget = self._create_step10()
        self.step11_widget = self._create_step11()
        self.step12_widget = self._create_step12()

        self.step_stack.addWidget(self.step1_widget)
        self.step_stack.addWidget(self.step2_widget)
        self.step_stack.addWidget(self.step3_widget)
        self.step_stack.addWidget(self.step4_widget)
        self.step_stack.addWidget(self.step5_widget)
        self.step_stack.addWidget(self.step6_widget)
        self.step_stack.addWidget(self.step7_widget)
        self.step_stack.addWidget(self.step8_widget)
        self.step_stack.addWidget(self.step9_widget)
        self.step_stack.addWidget(self.step10_widget)
        self.step_stack.addWidget(self.step11_widget)
        self.step_stack.addWidget(self.step12_widget)

    # ==================== Step 1: Select Directories ====================
    def _create_step1(self) -> QWidget:
        """Step 1: Select source and output directories"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("请选择源音频目录和输出目录"))

        # Source directory
        src_group = QGroupBox("源音频目录 (MP3文件)")
        src_layout = QHBoxLayout(src_group)
        self.src_path_edit = QLineEdit()
        self.src_path_edit.setPlaceholderText("选择包含MP3文件的目录...")
        self.src_path_edit.setReadOnly(True)
        src_btn = QPushButton("浏览")
        src_btn.clicked.connect(self._browse_source_dir)
        src_layout.addWidget(self.src_path_edit)
        src_layout.addWidget(src_btn)
        layout.addWidget(src_group)

        # Output directory
        out_group = QGroupBox("输出目录")
        out_layout = QHBoxLayout(out_group)
        self.out_path_edit = QLineEdit()
        self.out_path_edit.setPlaceholderText("选择输出目录...")
        self.out_path_edit.setReadOnly(True)
        out_btn = QPushButton("浏览")
        out_btn.clicked.connect(self._browse_output_dir)
        out_layout.addWidget(self.out_path_edit)
        out_layout.addWidget(out_btn)
        layout.addWidget(out_group)

        self.step1_warning = QLabel("")
        self.step1_warning.setStyleSheet("color: red;")
        layout.addWidget(self.step1_warning)

        layout.addStretch()
        return widget

    def _browse_source_dir(self):
        """Browse for source directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择源音频目录")
        if dir_path:
            self.source_dir = dir_path
            self.src_path_edit.setText(dir_path)
            self._validate_step1()

    def _browse_output_dir(self):
        """Browse for output directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_dir = dir_path
            self.out_path_edit.setText(dir_path)
            self._validate_step1()

    def _validate_step1(self):
        """Validate step 1 selections"""
        self.step1_warning.setText("")

        if not self.source_dir or not self.output_dir:
            return

        # Validate directories
        valid, error = FileUtils.validate_directory(self.source_dir)
        if not valid:
            self.step1_warning.setText(f"源目录错误: {error}")
            return

        valid, error = FileUtils.validate_directory(self.output_dir)
        if not valid:
            self.step1_warning.setText(f"输出目录错误: {error}")
            return

        # Check for MP3 files (recursive)
        self.audio_files = FileUtils.get_audio_files(self.source_dir, recursive=True)
        if not self.audio_files:
            self.step1_warning.setText("未找到MP3文件，请重新选择源目录")
            return

        self.step1_warning.setText(f"找到 {len(self.audio_files)} 个MP3文件")
        self.config.set("source_dir", self.source_dir)
        self.config.set("output_dir", self.output_dir)

    # ==================== Step 2: File Matching Rules ====================
    def _create_step2(self) -> QWidget:
        """Step 2: Set filename matching rules"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("设置文件名匹配规则，筛选目标音频"))

        # Match rule selection
        self.match_rule_group = QButtonGroup(widget)
        keyword_radio = QRadioButton("关键词匹配 (多个关键词用逗号分隔)")
        prefix_radio = QRadioButton("前缀匹配")
        suffix_radio = QRadioButton("后缀匹配")

        self.match_rule_group.addButton(keyword_radio, 0)
        self.match_rule_group.addButton(prefix_radio, 1)
        self.match_rule_group.addButton(suffix_radio, 2)
        keyword_radio.setChecked(True)

        layout.addWidget(keyword_radio)
        layout.addWidget(prefix_radio)
        layout.addWidget(suffix_radio)

        # Match value input
        self.match_value_edit = QLineEdit()
        self.match_value_edit.setPlaceholderText("输入匹配关键词、前缀或后缀...")
        layout.addWidget(QLabel("匹配值:"))
        layout.addWidget(self.match_value_edit)

        # Preview button
        self.preview_match_btn = QPushButton("预览匹配文件")
        self.preview_match_btn.clicked.connect(self._preview_matches)
        layout.addWidget(self.preview_match_btn)

        # Match result table
        self.match_table = QTableWidget()
        self.match_table.setColumnCount(3)
        self.match_table.setHorizontalHeaderLabels(["文件名", "原路径", "大小"])
        self.match_table.setMaximumHeight(200)
        # Set column widths - filename wider
        self.match_table.horizontalHeader().setStretchLastSection(False)
        self.match_table.setColumnWidth(0, 250)  # 文件名
        self.match_table.setColumnWidth(1, 350)  # 原路径
        self.match_table.setColumnWidth(2, 80)   # 大小
        self.match_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.match_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.match_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        layout.addWidget(self.match_table)

        self.step2_warning = QLabel("")
        self.step2_warning.setStyleSheet("color: red;")
        layout.addWidget(self.step2_warning)

        return widget

    def _preview_matches(self):
        """Preview matched files"""
        rule_map = {0: "keyword", 1: "prefix", 2: "suffix"}
        rule = rule_map[self.match_rule_group.checkedId()]
        value = self.match_value_edit.text().strip()

        self.filtered_files = FileUtils.filter_files_by_rule(self.audio_files, rule, value)

        if not self.filtered_files:
            self.step2_warning.setText("无符合规则的MP3文件，请调整匹配规则")
            self.match_table.setRowCount(0)
            return

        self.step2_warning.setText(f"匹配到 {len(self.filtered_files)} 个文件")

        # Populate table
        self.match_table.setRowCount(len(self.filtered_files))
        for i, file_path in enumerate(self.filtered_files):
            filename = FileUtils.get_file_size(file_path)
            size_kb = f"{filename / 1024:.1f} KB"
            self.match_table.setItem(i, 0, QTableWidgetItem(Path(file_path).name))
            self.match_table.setItem(i, 1, QTableWidgetItem(file_path))
            self.match_table.setItem(i, 2, QTableWidgetItem(size_kb))

        # Save config
        self.config.set("match_rule", rule)
        self.config.set("match_value", value)

    # ==================== Step 3: New Filename Rules ====================
    def _create_step3(self) -> QWidget:
        """Step 3: Set new filename rules"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("设置新文件名规则"))

        # Prefix input
        layout.addWidget(QLabel("文件名前缀:"))
        self.new_prefix_edit = QLineEdit()
        self.new_prefix_edit.setPlaceholderText("输入新文件名前缀 (不可包含特殊字符)...")
        layout.addWidget(self.new_prefix_edit)

        # Filename rule
        self.filename_rule_group = QButtonGroup(widget)
        preserve_radio = QRadioButton("保留原核心名")
        prefix_seq_radio = QRadioButton("前缀+序号")
        seq_radio = QRadioButton("仅序号命名")
        self.filename_rule_group.addButton(preserve_radio, 0)
        self.filename_rule_group.addButton(prefix_seq_radio, 1)
        self.filename_rule_group.addButton(seq_radio, 2)
        preserve_radio.setChecked(True)
        layout.addWidget(preserve_radio)
        layout.addWidget(prefix_seq_radio)
        layout.addWidget(seq_radio)

        # Sequence digits
        layout.addWidget(QLabel("序号位数:"))
        self.seq_digits_combo = QComboBox()
        self.seq_digits_combo.addItems(["2位", "3位"])
        self.seq_digits_combo.setCurrentIndex(1)  # Default 3
        layout.addWidget(self.seq_digits_combo)

        # Preview button
        self.preview_new_names_btn = QPushButton("预览新文件名")
        self.preview_new_names_btn.clicked.connect(self._preview_new_names)
        layout.addWidget(self.preview_new_names_btn)

        # Preview table
        self.new_names_table = QTableWidget()
        self.new_names_table.setColumnCount(2)
        self.new_names_table.setHorizontalHeaderLabels(["原文件名", "新文件名"])
        self.new_names_table.setMaximumHeight(200)
        self.new_names_table.setColumnWidth(0, 250)
        self.new_names_table.setColumnWidth(1, 250)
        layout.addWidget(self.new_names_table)

        self.step3_warning = QLabel("")
        self.step3_warning.setStyleSheet("color: red;")
        layout.addWidget(self.step3_warning)

        return widget

    def _preview_new_names(self):
        """Preview new filenames"""
        prefix = self.new_prefix_edit.text().strip()
        rule_id = self.filename_rule_group.checkedId()
        rule = {0: "preserve", 1: "prefix_seq", 2: "sequential"}[rule_id]
        digits = int(self.seq_digits_combo.currentText().replace("位", ""))

        # Check prefix validity
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(c in prefix for c in invalid_chars):
            self.step3_warning.setText("前缀不可包含特殊字符: / \\ : * ? \" < > |")
            return

        self.step3_warning.setText("")

        # Generate new names
        self.new_filenames = []
        for i, file_path in enumerate(self.filtered_files):
            new_name = FileUtils.generate_new_filename(
                Path(file_path).name, rule, prefix, i + 1, digits
            )
            self.new_filenames.append(new_name)

        # Populate table (show first 5)
        self.new_names_table.setRowCount(min(5, len(self.new_filenames)))
        for i in range(min(5, len(self.filtered_files))):
            self.new_names_table.setItem(i, 0, QTableWidgetItem(Path(self.filtered_files[i]).name))
            self.new_names_table.setItem(i, 1, QTableWidgetItem(self.new_filenames[i]))

        # Save config
        self.config.set("filename_rule", rule)
        self.config.set("filename_prefix", prefix)
        self.config.set("seq_digits", digits)

    # ==================== Step 4: Organize Files ====================
    def _create_step4(self) -> QWidget:
        """Step 4: Copy/move files to output"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("整理生成新的目录和文件"))

        # Operation mode
        self.organize_mode_group = QButtonGroup(widget)
        copy_radio = QRadioButton("复制 (源文件保留)")
        move_radio = QRadioButton("移动 (源文件移动)")
        self.organize_mode_group.addButton(copy_radio, 0)
        self.organize_mode_group.addButton(move_radio, 1)
        copy_radio.setChecked(True)
        layout.addWidget(copy_radio)
        layout.addWidget(move_radio)

        # Organize button
        self.organize_btn = QPushButton("开始整理")
        self.organize_btn.clicked.connect(self._organize_files)
        layout.addWidget(self.organize_btn)

        # Progress
        self.organize_progress = QProgressBar()
        layout.addWidget(self.organize_progress)

        # Status
        self.organize_status = QLabel("等待整理...")
        layout.addWidget(self.organize_status)

        return widget

    def _organize_files(self):
        """Execute file organization"""
        mode = "copy" if self.organize_mode_group.checkedId() == 0 else "move"

        self.organize_progress.setMaximum(len(self.filtered_files))
        self.organize_progress.setValue(0)

        success, failed = FileUtils.organize_files(
            self.filtered_files,
            self.output_dir,
            self.new_filenames,
            mode
        )

        self.organize_progress.setValue(len(self.filtered_files))
        self.organize_status.setText(f"整理完成: 成功 {success} 个, 失败 {failed} 个")

        self.config.set("organize_mode", mode)

    # ==================== Step 5: Confirm Structure ====================
    def _create_step5(self) -> QWidget:
        """Step 5: Confirm directory structure"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("请检查目录结构是否合适"))

        # Buttons
        self.open_output_btn = QPushButton("打开输出目录")
        self.open_output_btn.clicked.connect(self._open_output_directory)
        layout.addWidget(self.open_output_btn)

        self.redo_organize_btn = QPushButton("重新整理")
        self.redo_organize_btn.clicked.connect(lambda: self._go_to_step(3))
        layout.addWidget(self.redo_organize_btn)

        layout.addWidget(QLabel("确认无误后，点击下一步继续"))

        return widget

    def _open_output_directory(self):
        """Open output directory"""
        FileUtils.open_directory(self.output_dir)
        self.next_btn.setEnabled(True)

    # ==================== Step 6: Generate First Subtitle ====================
    def _create_step6(self) -> QWidget:
        """Step 6: Generate first subtitle for testing"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("生成第一个音频的字幕文件 (测试用)"))

        # Model selection
        layout.addWidget(QLabel("模型选择:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["Whisper base"])
        layout.addWidget(self.model_combo)

        # Generate button
        self.gen_first_subtitle_btn = QPushButton("生成第一个字幕")
        self.gen_first_subtitle_btn.clicked.connect(self._generate_first_subtitle)
        layout.addWidget(self.gen_first_subtitle_btn)

        # Progress
        self.gen_progress = QProgressBar()
        layout.addWidget(self.gen_progress)

        # Status
        self.gen_status = QLabel("等待生成...")
        layout.addWidget(self.gen_status)

        return widget

    def _generate_first_subtitle(self):
        """Generate subtitle for first audio file"""
        # Get first file from output directory
        output_files = FileUtils.get_audio_files(self.output_dir)
        if not output_files:
            self.gen_status.setText("错误: 输出目录无音频文件")
            return

        first_file = sorted(output_files)[0]
        audio_name = Path(first_file).stem
        lrc_path = os.path.join(self.output_dir, f"{audio_name}.lrc")

        # Model should already be loaded from main.py
        if not self.whisper:
            self.gen_status.setText("模型未加载，请重启程序")
            return

        # Do transcription with QTimer to keep UI responsive
        self._do_transcribe(first_file, lrc_path)

    def _do_transcribe(self, audio_file, lrc_path):
        """Do the actual transcription"""
        if not self.whisper:
            return

        self.gen_first_subtitle_btn.setEnabled(False)
        self.gen_status.setText(f"正在生成字幕: {Path(audio_file).stem}.lrc...")

        def transcribe():
            try:
                # Process events to keep UI responsive
                QApplication.processEvents()

                ok, result = self.whisper.transcribe_to_lrc(audio_file, lrc_path)

                # Process events again after transcription
                QApplication.processEvents()

                if ok:
                    self.gen_status.setText(f"字幕生成完成: {result}")
                else:
                    self.gen_status.setText(f"字幕生成失败: {result}")
            except Exception as e:
                self.gen_status.setText(f"转写失败: {e}")
            finally:
                self.gen_first_subtitle_btn.setEnabled(True)

        QTimer.singleShot(100, transcribe)

    # ==================== Step 7: Review First Subtitle ====================
    def _create_step7(self) -> QWidget:
        """Step 7: Review first subtitle"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("请查看生成的字幕文件，校验转写效果"))

        self.open_subtitle_btn = QPushButton("打开字幕文件")
        self.open_subtitle_btn.clicked.connect(self._open_first_subtitle)
        layout.addWidget(self.open_subtitle_btn)

        return widget

    def _open_first_subtitle(self):
        """Open first subtitle file"""
        output_files = FileUtils.get_audio_files(self.output_dir)
        if output_files:
            first_file = sorted(output_files)[0]
            audio_name = Path(first_file).stem
            lrc_path = os.path.join(self.output_dir, f"{audio_name}.lrc")
            if os.path.exists(lrc_path):
                FileUtils.open_file(lrc_path)

    # ==================== Step 8: Batch Subtitles ====================
    def _create_step8(self) -> QWidget:
        """Step 8: Batch generate subtitles"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("批量生成所有音频的字幕"))

        self.batch_subtitle_btn = QPushButton("批量生成字幕")
        self.batch_subtitle_btn.clicked.connect(self._batch_generate_subtitles)
        layout.addWidget(self.batch_subtitle_btn)

        # Control buttons
        ctrl_layout = QHBoxLayout()
        self.pause_btn = QPushButton("暂停")
        self.pause_btn.setEnabled(False)
        self.continue_btn = QPushButton("继续")
        self.continue_btn.setEnabled(False)
        self.terminate_btn = QPushButton("终止")
        self.terminate_btn.setEnabled(False)
        ctrl_layout.addWidget(self.pause_btn)
        ctrl_layout.addWidget(self.continue_btn)
        ctrl_layout.addWidget(self.terminate_btn)
        layout.addLayout(ctrl_layout)

        # Progress
        self.batch_subtitle_progress = QProgressBar()
        layout.addWidget(self.batch_subtitle_progress)

        # Log
        self.batch_subtitle_log = QTextEdit()
        self.batch_subtitle_log.setReadOnly(True)
        self.batch_subtitle_log.setMaximumHeight(200)
        layout.addWidget(QLabel("处理日志:"))
        layout.addWidget(self.batch_subtitle_log)

        # Status
        self.batch_subtitle_status = QLabel("")
        layout.addWidget(self.batch_subtitle_status)

        self.is_paused = False
        self.is_terminated = False

        return widget

    def _batch_generate_subtitles(self):
        """Generate subtitles for all audio files"""
        # Model should already be loaded
        if not self.whisper:
            self.batch_subtitle_status.setText("模型未加载，请重启程序")
            return

        self._do_batch_transcribe()

    def _do_batch_transcribe(self):
        """Do the actual batch transcription"""
        audio_files = FileUtils.get_audio_files(self.output_dir)
        if not audio_files:
            self.batch_subtitle_status.setText("输出目录无音频文件")
            return

        self.batch_subtitle_progress.setMaximum(len(audio_files))
        self.batch_subtitle_progress.setValue(0)
        self.batch_subtitle_log.clear()

        self.pause_btn.setEnabled(True)
        self.terminate_btn.setEnabled(True)
        self.batch_subtitle_btn.setEnabled(False)

        # Process files
        success = 0
        failed = 0

        def process_next(index=0):
            if index >= len(audio_files):
                self.batch_subtitle_status.setText(f"完成: 成功 {success}, 失败 {failed}")
                self.pause_btn.setEnabled(False)
                self.terminate_btn.setEnabled(False)
                self.batch_subtitle_btn.setEnabled(True)
                return

            # Process events to keep UI responsive
            QApplication.processEvents()

            audio_file = audio_files[index]
            self.batch_subtitle_progress.setValue(index + 1)
            self.batch_subtitle_log.append(f"正在处理: {Path(audio_file).name}")

            audio_name = Path(audio_file).stem
            lrc_path = os.path.join(self.output_dir, f"{audio_name}.lrc")

            # Skip if already exists
            if os.path.exists(lrc_path):
                success += 1
            else:
                try:
                    ok, result = self.whisper.transcribe_to_lrc(audio_file, lrc_path)
                    if ok:
                        success += 1
                        self.batch_subtitle_log.append(f"处理成功: {audio_name}.lrc")
                    else:
                        failed += 1
                        self.batch_subtitle_log.append(f"处理失败: {audio_name}")
                except Exception as e:
                    failed += 1
                    self.batch_subtitle_log.append(f"错误: {e}")

            # Process events again
            QApplication.processEvents()

            # Process next file
            QTimer.singleShot(10, lambda i=index+1: process_next(i))

        process_next(0)

    # ==================== Step 9: Translate First Subtitle ====================
    def _create_step9(self) -> QWidget:
        """Step 9: Translate first subtitle"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("翻译第一个字幕"))

        # Translation mode
        self.translate_mode_group = QButtonGroup(widget)
        local_radio = QRadioButton("本地翻译 (CSANMT)")
        ai_radio = QRadioButton("AI翻译 (DeepSeek)")
        self.translate_mode_group.addButton(local_radio, 0)
        self.translate_mode_group.addButton(ai_radio, 1)
        local_radio.setChecked(True)
        layout.addWidget(local_radio)
        layout.addWidget(ai_radio)

        # API Key input
        layout.addWidget(QLabel("DeepSeek API Key:"))
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_key_edit.setPlaceholderText("输入API Key...")
        layout.addWidget(self.api_key_edit)

        # Translate button
        self.translate_first_btn = QPushButton("翻译第一个字幕")
        self.translate_first_btn.clicked.connect(self._translate_first)
        layout.addWidget(self.translate_first_btn)

        # Status
        self.translate_first_status = QLabel("")
        layout.addWidget(self.translate_first_status)

        return widget

    def _translate_first(self):
        """Translate first subtitle"""
        mode = "local" if self.translate_mode_group.checkedId() == 0 else "ai"

        if mode == "ai":
            api_key = self.api_key_edit.text().strip()
            if not api_key:
                self.translate_first_status.setText("请先配置DeepSeek AI翻译API Key")
                return

        # Initialize translator
        self.translator = Translator(mode)
        if mode == "ai":
            self.translator.set_api_key(self.api_key_edit.text().strip())

        # Get first LRC file
        lrc_files = list(Path(self.output_dir).glob("*.lrc"))
        if not lrc_files:
            self.translate_first_status.setText("字幕文件未生成，请先生成字幕")
            return

        first_lrc = str(sorted(lrc_files)[0])
        self.translate_first_status.setText("正在翻译...")

        def translate():
            try:
                ok, result = self.translator.translate_lrc(first_lrc)
                if ok:
                    self.translate_first_status.setText(f"翻译完成: {result}")
                else:
                    self.translate_first_status.setText(f"翻译失败: {result}")
            except Exception as e:
                self.translate_first_status.setText(f"翻译失败: {e}")

        QTimer.singleShot(100, translate)

        self.config.set("translate_mode", mode)

    # ==================== Step 10: Review Translation ====================
    def _create_step10(self) -> QWidget:
        """Step 10: Review first translation"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("请查看翻译效果"))

        self.open_translation_btn = QPushButton("打开翻译文件")
        self.open_translation_btn.clicked.connect(self._open_first_translation)
        layout.addWidget(self.open_translation_btn)

        self.retranslate_btn = QPushButton("重新翻译")
        self.retranslate_btn.clicked.connect(lambda: self._go_to_step(9))
        layout.addWidget(self.retranslate_btn)

        return widget

    def _open_first_translation(self):
        """Open first translation file"""
        translation_files = list(Path(self.output_dir).glob("*中文翻译.txt"))
        if translation_files:
            FileUtils.open_file(str(translation_files[0]))

    # ==================== Step 11: Batch Translation ====================
    def _create_step11(self) -> QWidget:
        """Step 11: Batch translate all subtitles"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("批量翻译所有字幕"))

        self.batch_translate_btn = QPushButton("批量翻译")
        self.batch_translate_btn.clicked.connect(self._batch_translate)
        layout.addWidget(self.batch_translate_btn)

        # Progress
        self.batch_translate_progress = QProgressBar()
        layout.addWidget(self.batch_translate_progress)

        # Log
        self.batch_translate_log = QTextEdit()
        self.batch_translate_log.setReadOnly(True)
        self.batch_translate_log.setMaximumHeight(200)
        layout.addWidget(QLabel("处理日志:"))
        layout.addWidget(self.batch_translate_log)

        # Status
        self.batch_translate_status = QLabel("")
        layout.addWidget(self.batch_translate_status)

        return widget

    def _batch_translate(self):
        """Batch translate all subtitles"""
        lrc_files = list(Path(self.output_dir).glob("*.lrc"))
        if not lrc_files:
            self.batch_translate_status.setText("无字幕文件可翻译")
            return

        self.batch_translate_progress.setMaximum(len(lrc_files))
        self.batch_translate_progress.setValue(0)
        self.batch_translate_log.clear()

        def translate_next(index=0):
            if index >= len(lrc_files):
                self.batch_translate_status.setText("批量翻译完成")
                return

            # Process events to keep UI responsive
            QApplication.processEvents()

            lrc_file = lrc_files[index]
            self.batch_translate_progress.setValue(index + 1)
            self.batch_translate_log.append(f"正在翻译: {lrc_file.name}")

            try:
                ok, result = self.translator.translate_lrc(str(lrc_file))
                if ok:
                    self.batch_translate_log.append(f"翻译成功: {Path(result).name}")
                else:
                    self.batch_translate_log.append(f"翻译失败")
            except Exception as e:
                self.batch_translate_log.append(f"错误: {e}")

            # Process events again
            QApplication.processEvents()

            QTimer.singleShot(10, lambda i=index+1: translate_next(i))

        translate_next(0)

    # ==================== Step 12: Complete ====================
    def _create_step12(self) -> QWidget:
        """Step 12: Completion"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("处理完成！"))

        # Summary
        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

        self.open_final_btn = QPushButton("打开输出目录")
        self.open_final_btn.clicked.connect(lambda: FileUtils.open_directory(self.output_dir))
        layout.addWidget(self.open_final_btn)

        self.restart_btn = QPushButton("重新开始")
        self.restart_btn.clicked.connect(self._restart)
        layout.addWidget(self.restart_btn)

        return widget

    def _restart(self):
        """Restart the entire workflow"""
        self.config.reset()
        self.current_step = 1
        self.step_stack.setCurrentIndex(0)
        self._update_navigation()

    # ==================== Navigation ====================
    def _next_step(self):
        """Go to next step"""
        if self.current_step < self.total_steps:
            self.current_step += 1
            self.step_stack.setCurrentIndex(self.current_step - 1)
            self._update_navigation()

    def _prev_step(self):
        """Go to previous step"""
        if self.current_step > 1:
            self.current_step -= 1
            self.step_stack.setCurrentIndex(self.current_step - 1)
            self._update_navigation()

    def _go_to_step(self, step: int):
        """Jump to specific step"""
        self.current_step = step
        self.step_stack.setCurrentIndex(step - 1)
        self._update_navigation()

    def _update_navigation(self):
        """Update navigation buttons and step label"""
        self.step_label.setText(f"步骤 {self.current_step}/{self.total_steps}: {self._get_step_name()}")
        self.prev_btn.setEnabled(self.current_step > 1)
        self.next_btn.setText("完成" if self.current_step == self.total_steps else "下一步")

    def _get_step_name(self) -> str:
        """Get step name"""
        names = {
            1: "选择目录",
            2: "设置匹配规则",
            3: "设置新文件名",
            4: "整理文件",
            5: "确认目录结构",
            6: "生成第一个字幕",
            7: "查看字幕效果",
            8: "批量生成字幕",
            9: "翻译第一个字幕",
            10: "查看翻译效果",
            11: "批量翻译",
            12: "完成"
        }
        return names.get(self.current_step, "")