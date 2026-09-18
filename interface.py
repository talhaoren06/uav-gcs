from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QGroupBox, QCheckBox, QComboBox, QProgressBar, QListWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # ---------------------------------------------------------
        #                     MAIN WINDOW SETUP
        # ---------------------------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        # Apply global hacker/military theme (Dark background, Lime green text)
        MainWindow.setStyleSheet("background-color: #121212; color: #00FF00;")

        central_widget = QWidget()
        MainWindow.setCentralWidget(central_widget)

        # Main layout splitting the screen into Left (Video) and Right (Controls)
        main_layout = QHBoxLayout(central_widget)

        # ---------------------------------------------------------
        #                     RIGHT PANEL DESIGN
        # ---------------------------------------------------------
        right_panel = QVBoxLayout()

        # --- APP TITLE ---
        self.app_title = QLabel("OVERWATCH TACTICAL GCS")  # Seçtiğin ismi buraya yaz
        self.app_title.setAlignment(Qt.AlignCenter)
        self.app_title.setStyleSheet("font-size: 22px; font-weight: bold; color: lime; margin-bottom: 15px; margin-top: 15px;")
        right_panel.addWidget(self.app_title)

        # --- 1. VISION SETTINGS BOX ---
        settings_box = QGroupBox("VISION SETTINGS")
        group_layout = QVBoxLayout()

        # Bounding Box Checkbox Layout
        lbl_layout = QHBoxLayout()
        self.lbl_chck_dscrp = QLabel("Bounding Box Labels:")
        self.lbl_chck_dscrp.setStyleSheet("padding: 10px; font-weight: bold;")
        self.lbl_chck_box = QCheckBox("Enable/Disable")
        lbl_layout.addWidget(self.lbl_chck_dscrp)
        lbl_layout.addWidget(self.lbl_chck_box)
        group_layout.addLayout(lbl_layout)

        # Confidence Scores Checkbox Layout
        cnf_layout = QHBoxLayout()
        self.conf_chck_descrb = QLabel("Confidence Scores:")
        self.conf_chck_descrb.setStyleSheet("padding: 10px; font-weight: bold;")
        self.conf_chck_box = QCheckBox("Enable/Disable")
        cnf_layout.addWidget(self.conf_chck_descrb)
        cnf_layout.addWidget(self.conf_chck_box)
        group_layout.addLayout(cnf_layout)

        # Class Filter ComboBox Layout
        class_fltr_layout = QHBoxLayout()
        self.class_fltr_dscrb = QLabel("Class Labels:")
        self.class_fltr_dscrb.setStyleSheet("padding: 10px; font-weight: bold;")
        self.combo_box = QComboBox()
        class_fltr_layout.addWidget(self.class_fltr_dscrb)
        class_fltr_layout.addWidget(self.combo_box)
        group_layout.addLayout(class_fltr_layout)

        settings_box.setLayout(group_layout)

        # --- 2. TELEMETRY SETTINGS BOX ---
        telemetry_box = QGroupBox("TELEMETRY SETTINGS")
        telemetry_layout = QVBoxLayout()

        # CPU Usage Bar
        cpu_layout = QHBoxLayout()
        self.cpu_lbl = QLabel("CPU:")
        self.cpu_lbl.setStyleSheet("padding: 10px; font-weight: bold;")
        self.cpu_progress = QProgressBar()
        cpu_layout.addWidget(self.cpu_lbl)
        cpu_layout.addWidget(self.cpu_progress)
        telemetry_layout.addLayout(cpu_layout)

        # RAM Usage Bar
        ram_layout = QHBoxLayout()
        self.ram_lbl = QLabel("RAM:")
        self.ram_lbl.setStyleSheet("padding: 10px; font-weight: bold;")
        self.ram_progress = QProgressBar()
        ram_layout.addWidget(self.ram_lbl)
        ram_layout.addWidget(self.ram_progress)
        telemetry_layout.addLayout(ram_layout)

        telemetry_box.setLayout(telemetry_layout)

        # --- 3. SITUATION REPORT BOX ---
        report_group = QGroupBox("SITUATION REPORT")
        report_group.setMinimumHeight(250)  # Ensure the box is large enough for multiple logs
        report_layout = QVBoxLayout()

        # Mission Log List Widget
        self.report_list = QListWidget()
        # Remove inner border and set colors for a seamless terminal look
        self.report_list.setStyleSheet("QListWidget { border: none; color: lime;}")
        self.report_list.setWordWrap(True)  # Prevent horizontal scrollbars

        report_layout.addWidget(self.report_list)
        report_group.setLayout(report_layout)

        # --- ASSEMBLE RIGHT PANEL ---
        right_panel.addWidget(settings_box)
        right_panel.addWidget(telemetry_box)
        right_panel.addWidget(report_group)
        # Add expanding spacer at the bottom to push all boxes to the top
        right_panel.addItem(QSpacerItem(20, 600, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # ---------------------------------------------------------
        #                     LEFT PANEL DESIGN
        # ---------------------------------------------------------
        left_panel = QVBoxLayout()

        # Main Video Display Label
        self.video_label = QLabel("NO SIGNAL")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: #000000; border: 2px solid #333333;")
        self.video_label.setMinimumSize(1400, 1050)
        left_panel.addWidget(self.video_label)

        # Control Buttons Layout (Bottom of the video)
        control_layout = QHBoxLayout()

        self.btn_source = QPushButton("Select the video file")
        self.btn_source.setStyleSheet("background-color: #7a6f11; padding: 10px; font-weight: bold;")

        self.source_label = QLabel("SOURCE: CAMERA")
        self.source_label.setAlignment(Qt.AlignCenter)
        self.source_label.setStyleSheet("padding: 10px; font-weight: bold;")

        self.btn_start = QPushButton("CONNECT FEED")
        self.btn_start.setStyleSheet("background-color: #1A361A; padding: 10px; font-weight: bold;")

        self.btn_stop = QPushButton("DISCONNECT")
        self.btn_stop.setStyleSheet("background-color: #361A1A; padding: 10px; font-weight: bold;")

        control_layout.addWidget(self.btn_source)
        control_layout.addWidget(self.source_label)
        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)

        left_panel.addLayout(control_layout)

        # --- ASSEMBLE MAIN LAYOUT ---
        main_layout.addLayout(left_panel)
        main_layout.addLayout(right_panel)

        # ---------------------------------------------------------
        #                     MENU & STATUS BAR
        # ---------------------------------------------------------
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """Sets the dynamic texts and window titles."""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UAV Tactical Ground Control Station"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
