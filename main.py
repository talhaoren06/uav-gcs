import sys
from tkinter import filedialog
import os
import psutil
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QTimer
from PyQt5.QtGui import QImage, QPixmap, QStandardItem, QStandardItemModel
from ultralytics import YOLO
import time
from interface import Ui_MainWindow
from collections import Counter


# ---------------------------------------------------------
#                      WORKER THREAD
# ---------------------------------------------------------
class UAVVisionThread(QThread):
    # Signals to communicate with the main GUI thread safely
    change_pixmap_signal = pyqtSignal(QImage)
    video_ended_signal = pyqtSignal()
    sitrep_signal = pyqtSignal(str)

    def __init__(self):
        """Initializes the worker thread, YOLO model, and necessary variables."""
        super().__init__()
        self._run_flag = True
        self.time = 0
        self.model = YOLO("models/best.pt")
        self.target_classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.show_labels = False
        self.show_conf = False
        self.last_sitrep_time = 0

        # Create intelligence captures directory if it does not exist
        if not os.path.isdir("intelligence_captures"):
            os.mkdir("intelligence_captures")
            print("intelligence_captures folder created")

    def run(self):
        """Main loop for video capture, YOLO inference, and telemetry reporting."""
        if self.current_source == 0:
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(self.current_source)

        while self._run_flag:
            success, frame = cap.read()
            if success:
                # Run YOLO object detection on the current frame
                results = self.model(frame, classes=self.target_classes, verbose=False)

                # Retrieve the current time for SITREP frequency control
                self.current_rep_time = time.time()

                # Generate and emit Situation Report (SITREP) every 2 seconds
                if self.current_rep_time - self.last_sitrep_time >= 2.0:
                    sitrep = results[0].boxes.cls.tolist()
                    if sitrep:
                        sitrep_counts = Counter(sitrep)
                        report_pieces = []
                        for class_id, count in sitrep_counts.items():
                            class_name = results[0].names[int(class_id)].upper()
                            report_pieces.append(f"{count} {class_name}")
                        sitrep_text = ", ".join(report_pieces)
                        current_time_str = time.strftime("%H:%M:%S")
                        report_text = f"[{current_time_str}] SITREP : {sitrep_text} on radar."
                        self.sitrep_signal.emit(report_text)
                    self.last_sitrep_time = self.current_rep_time

                # Draw bounding boxes and labels on the frame
                annotated_frame = results[0].plot(conf=self.show_conf, labels=self.show_labels, line_width=2,
                                                  boxes=True)

                # Calculate and display FPS on the top-left corner
                current_time = time.time()
                fps = 1 / (current_time - self.time)
                fps = str(int(fps))
                cv2.putText(annotated_frame, f"FPS: {fps}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2,
                            cv2.LINE_AA)

                # Convert the OpenCV BGR image to PyQt-compatible RGB image
                rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w

                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                scaled_image = convert_to_qt_format.scaled(1400, 1050, Qt.KeepAspectRatio)

                self.time = time.time()
                self.change_pixmap_signal.emit(scaled_image)
                time.sleep(0.03)  # Prevent thread from consuming 100% CPU to maintain system stability
            else:
                self.video_ended_signal.emit()
                break

        cap.release()

    def stop(self):
        """Gracefully stops the worker thread and releases resources."""
        self._run_flag = False
        self.wait()


# ---------------------------------------------------------
#                       MAIN APP
# ---------------------------------------------------------
class GCSApp(QMainWindow):
    def __init__(self):
        """Initializes the main GUI, UI components, styles, and signal connections."""
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Style definition for dynamic telemetry progress bars
        self.progress_bar_style = """
            QProgressBar {
                color: #FFFFFF;               /* Text color */
                border: 2px solid gray;       /* Border color */
                border-radius: 5px;           /* Rounded border edges */
                margin-left: 24px;
                margin-right: 24px;           
                text-align: center;           /* Center the X% indicator */
            }
            """

        # Target classes for VisDrone/YOLO model
        self.od_classes = ["PEDESTRIAN", "PEOPLE", "BICYCLE", "CAR", "VAN", "TRUCK", "TRICYCLE", "AWNING-TRICYCLE",
                           "BUS", "MOTOR"]

        # Set up a checkable model for the combobox to filter detection classes
        self.item_model = QStandardItemModel()
        for od_class in self.od_classes:
            item = QStandardItem(od_class)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.item_model.appendRow(item)

        self.ui.combo_box.setModel(self.item_model)
        self.ui.combo_box.view().viewport().installEventFilter(self)

        self.current_source = 0

        # Connect UI interactions to their respective functions
        self.item_model.itemChanged.connect(self.update_target_classes)
        self.ui.conf_chck_box.toggled.connect(self.toggle_conf)
        self.ui.lbl_chck_box.toggled.connect(self.toggle_labels)
        self.ui.btn_source.clicked.connect(self.select_source)
        self.ui.btn_start.clicked.connect(self.start_system)
        self.ui.btn_stop.clicked.connect(self.stop_system)

        # Initialize hardware telemetry monitoring timer (refreshes every 1 second)
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self.update_telemetry)
        self.telemetry_timer.start(1000)

    def start_system(self):
        """Starts the YOLO vision thread and initiates video processing."""
        self.ui.statusbar.showMessage("SYSTEM ONLINE - Establishing video feed...", 3000)

        self.vision_thread = UAVVisionThread()
        self.vision_thread.current_source = self.current_source

        # Connect worker signals to main GUI slots
        self.vision_thread.change_pixmap_signal.connect(self.update_image)
        self.vision_thread.video_ended_signal.connect(self.stop_system)
        self.vision_thread.sitrep_signal.connect(self.sitrep)

        self.vision_thread.start()

        self.ui.lbl_chck_box.setChecked(False)
        self.ui.conf_chck_box.setChecked(False)

    def stop_system(self):
        """Stops the YOLO vision thread and resets the video display area."""
        if hasattr(self, 'vision_thread'):
            self.vision_thread.stop()
            time.sleep(1)
            self.ui.video_label.clear()
            self.ui.video_label.setText("SYSTEM OFFLINE")
            self.ui.statusbar.showMessage("SYSTEM OFFLINE", 3000)
            self.ui.lbl_chck_box.setChecked(False)
            self.ui.conf_chck_box.setChecked(False)

    def select_source(self):
        """Opens a file dialog allowing the user to select a custom video source."""
        current_path = os.path.dirname(__file__)
        chosen_source = filedialog.askopenfilename(
            initialdir=current_path,
            title="Select Source",
            filetypes=[("Video Files", ".mp4")]
        )
        if chosen_source:
            self.current_source = chosen_source
            self.ui.source_label.setText(os.path.basename(chosen_source))
            self.ui.report_list.addItem(
                "[" + time.strftime("%H:%M:%S") + "] The source has changed: " + os.path.basename(chosen_source))

    def update_image(self, qt_image):
        """Updates the main video label with the latest processed frame from the thread."""
        self.ui.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def toggle_labels(self):
        """Toggles the visibility of class name labels on detected objects."""
        if hasattr(self, 'vision_thread') and self.vision_thread.isRunning():
            is_checked = self.ui.lbl_chck_box.isChecked()
            self.vision_thread.show_labels = is_checked

    def toggle_conf(self):
        """Toggles the visibility of confidence score labels on detected objects."""
        if hasattr(self, 'vision_thread') and self.vision_thread.isRunning():
            is_checked = self.ui.conf_chck_box.isChecked()
            self.vision_thread.show_conf = is_checked

    def eventFilter(self, obj, event):
        """Filters mouse click events to prevent the combobox dropdown from closing automatically."""
        if obj == self.ui.combo_box.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.ui.combo_box.view().indexAt(event.pos())
                if index.isValid():
                    item = self.item_model.itemFromIndex(index)
                    if item.checkState() == Qt.Checked:
                        item.setCheckState(Qt.Unchecked)
                    else:
                        item.setCheckState(Qt.Checked)
                    return True
        return super().eventFilter(obj, event)

    def update_target_classes(self):
        """Updates the list of active target classes based on user selection in the combobox."""
        selected_ids = []
        for i in range(self.item_model.rowCount()):
            item = self.item_model.item(i)
            if item.checkState() == Qt.Checked:
                selected_ids.append(i)

        if hasattr(self, 'vision_thread') and self.vision_thread.isRunning():
            self.vision_thread.target_classes = selected_ids

    def update_telemetry(self):
        """Reads hardware metrics (CPU/RAM) and updates progress bars dynamically based on load."""
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        # Change CPU bar color based on usage thresholds
        if cpu_usage > 90:
            self.ui.cpu_progress.setStyleSheet(
                self.progress_bar_style + "QProgressBar::chunk {background-color: red; }")
        elif cpu_usage > 80:
            self.ui.cpu_progress.setStyleSheet(
                self.progress_bar_style + "QProgressBar::chunk {background-color: #d1d100; }")
        else:
            self.ui.cpu_progress.setStyleSheet(
                self.progress_bar_style + "QProgressBar::chunk {background-color: green; }")

        # Change RAM bar color based on usage thresholds
        if ram_usage > 90:
            self.ui.ram_progress.setStyleSheet(
                self.progress_bar_style + "QProgressBar::chunk {background-color: red; }")
        elif ram_usage > 80:
            self.ui.ram_progress.setStyleSheet(
                self.progress_bar_style + "QProgressBar::chunk {background-color: #d1d100; }")
        else:
            self.ui.ram_progress.setStyleSheet(
                self.progress_bar_style + "QProgressBar::chunk {background-color: green; }")

        self.ui.cpu_progress.setValue(int(cpu_usage))
        self.ui.ram_progress.setValue(int(ram_usage))

    def sitrep(self, report_text):
        """Receives SITREP data from the vision thread and appends it to the mission log."""
        if hasattr(self, 'vision_thread') and self.vision_thread.isRunning():
            self.ui.report_list.addItem(report_text)
            self.ui.report_list.scrollToBottom()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GCSApp()
    window.showMaximized()
    sys.exit(app.exec_())