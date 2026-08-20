import os, sys, graphing_util, logger

os.environ["QT_API"] = "PySide6"

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QApplication,
    QFileDialog,
    QLabel,
)
from PySide6.QtCore import Qt

from pathlib import Path

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

compareGraphs = False
selections = 0x3F  # Clutch, Gas. Gear. Pitch, Suspension, Wheel Speed, RPM

curr_pass = None
prev_pass = None
gloMainLabel = None
gloPrevLabel = None

Path("output_logs").mkdir(exist_ok=True)


def reset_paths():
    global curr_pass, prev_pass
    curr_pass = None
    prev_pass = None

    # Define the target directory
    directory_path = Path("output_logs")

    # 1. Get all items, filter for files only
    files = [f for f in directory_path.iterdir() if f.is_file()]

    # 2. Sort files by modification time in descending order (newest first)
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    # 3. Safely pick the second newest file
    if len(files) >= 2:
        curr_pass = files[0]
        prev_pass = files[1]
        print(f"Current file: {curr_pass.name}")
        print(f"Full path: {curr_pass}")
        print(f"Second newest file: {prev_pass.name}")
        print(f"Full path: {prev_pass}")
    elif len(files) == 1:
        print("The directory contains only one file.")
        curr_pass = files[0]
        print(f"Current file: {curr_pass.name}")
        print(f"Full path: {curr_pass}")
    else:
        print("The directory is empty.")


reset_paths()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Controls Initialization
        mainFileLabel = QLabel("Pass 1: " + str(curr_pass.name if curr_pass else "No file selected"))  # type: ignore
        mainFileLabel.setAlignment(Qt.AlignCenter)  # type: ignore
        compareFileLabel = QLabel("Pass 2: " + str(prev_pass.name if prev_pass else "No comparison file selected"))  # type: ignore
        compareFileLabel.setAlignment(Qt.AlignCenter)  # type: ignore

        global gloMainLabel, gloPrevLabel
        gloMainLabel = mainFileLabel
        gloPrevLabel = compareFileLabel

        mainSelectButton = QPushButton("Select Main File")
        mainSelectButton.clicked.connect(
            lambda: self.select_file("Main")
        )
        compareSelectButton = QPushButton("Select Comparison File")
        compareSelectButton.clicked.connect(
            lambda: self.select_file("Comparison")
        )

        comparisonCheckbox = QCheckBox("Comparison Mode")
        comparisonCheckbox.stateChanged.connect(self.toggle_comparison)

        graphButton = QPushButton("Graph Data")
        graphButton.clicked.connect(self.graph_data)

        logButton = QPushButton("Log Data")
        logButton.clicked.connect(self.log_data)
        logButton.setMinimumHeight(100)

        deleteButton = QPushButton("Delete Last Pass")
        deleteButton.clicked.connect(self.delete_last_pass)
        deleteButton.setStyleSheet("background-color: red; color: white")
        #  Overall layout holding the graph and the controls
        topLayout = QHBoxLayout()

        #  Layout for the control widgets
        controlLayout = QVBoxLayout()

        #  Checkboxes for current graph shown
        self.list_widget = QListWidget()
        self.list_widget.setMaximumWidth(220)
        self.list_widget.setMinimumWidth(220)
        items = [
            "RPM",
            "Wheel Speed",
            "Suspension Position",
            "Pitch",
            "Gear",
            "Gas Pedal",
            "Clutch Pedal",
        ]
        for item_text in items:
            item = QListWidgetItem(item_text)
            item.setCheckState(Qt.Unchecked if item_text == "Clutch Pedal" else Qt.Checked)  # type: ignore
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # type: ignore
            self.list_widget.addItem(item)

        self.list_widget.itemChanged.connect(self.update_selection)
        controlLayout.addWidget(self.list_widget)

        controlLayout.addWidget(mainFileLabel)
        controlLayout.addWidget(mainSelectButton)
        controlLayout.addWidget(compareFileLabel)
        controlLayout.addWidget(compareSelectButton)

        controlLayout.addWidget(comparisonCheckbox)
        controlLayout.addWidget(graphButton)
        controlLayout.addWidget(logButton)
        controlLayout.addWidget(deleteButton)

        #  Graph Initialization

        self.canvas = FigureCanvasQTAgg(
            graphing_util.graph_single_data(
                graphing_util.read_csv_data(curr_pass), selections
            )
            if curr_pass
            else Figure(facecolor='black')
        )
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.graphLayout = QVBoxLayout()
        self.graphLayout.addWidget(self.toolbar)
        self.graphLayout.addWidget(self.canvas)

        topLayout.addLayout(controlLayout)
        topLayout.addLayout(self.graphLayout)

        # Create a placeholder widget to hold our toolbar, canvas, and controls.
        widget = QWidget()
        widget.setLayout(topLayout)
        self.setCentralWidget(widget)

        self.showMaximized()

    def toggle_comparison(self, state):
        global compareGraphs
        compareGraphs = not compareGraphs
        print(f"Comparison mode toggled: {compareGraphs}")

    def update_selection(self):
        global selections
        selections = 0x00
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:  # type: ignore
                selections |= 1 << i
        print(f"Selections updated: {selections:07b}")
        updated_fig = (
            graphing_util.graph_comparison_data(
                graphing_util.read_csv_data(curr_pass),
                graphing_util.read_csv_data(prev_pass),
                selections,
            )
            if compareGraphs and prev_pass != None
            else graphing_util.graph_single_data(
                graphing_util.read_csv_data(curr_pass), selections
            )
        )
        self.regraph(updated_fig)

    def regraph(self, figure):
        self.graphLayout.removeWidget(self.toolbar)
        self.graphLayout.removeWidget(self.canvas)
        self.toolbar.deleteLater()
        self.canvas.deleteLater()

        self.fig = figure
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.graphLayout.addWidget(self.toolbar)
        self.graphLayout.addWidget(self.canvas)
        self.canvas.draw_idle()

    def graph_data(self):
        updated_fig = (
            graphing_util.graph_comparison_data(
                graphing_util.read_csv_data(curr_pass),
                graphing_util.read_csv_data(prev_pass),
                selections,
            )
            if compareGraphs and prev_pass != None
            else graphing_util.graph_single_data(
                graphing_util.read_csv_data(curr_pass), selections
            )
        )
        self.regraph(updated_fig)

    def select_file(self, button):
        global curr_pass, prev_pass
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("CSV Files (*.csv)")
        dialog.setDirectory("output_logs")
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            if button == "Main":
                # Handle the selected main file path
                print(f"Main file selected: {file_path}")
                curr_pass = Path(file_path)
            elif button == "Comparison":
                # Handle the selected comparison file path
                print(f"Comparison file selected: {file_path}")
                prev_pass = Path(file_path)
            self.update_labels()

    def log_data(self):
        global curr_pass, prev_pass
        prev_pass = curr_pass if curr_pass else None
        curr_pass = Path(logger.log_pass())

        self.graph_data()
        self.update_labels()

    def update_labels(self):
        global gloMainLabel, gloPrevLabel
        if gloMainLabel:
            gloMainLabel.setText("Pass 1: " + str(curr_pass.name) if curr_pass else "No file selected")  # type: ignore
        if gloPrevLabel:
            gloPrevLabel.setText("Pass 2: " + str(prev_pass.name) if prev_pass else "No file selected")  # type: ignore

    def delete_last_pass(self):
        global curr_pass, prev_pass
        if curr_pass:
            curr_pass.unlink() #type: ignore
            curr_pass = None
        reset_paths()
        self.update_labels()
        self.graph_data()

app = QApplication(sys.argv)
window = MainWindow()

screens = QApplication.screens()

targetScreen = screens[1] if len(screens) > 1 else screens[0]

screen_geo = targetScreen.availableGeometry()

window.move(screen_geo.topLeft())

window.setWindowTitle("BeamNG.Drive Drag Racing Data Logger")

window.show()

sys.exit(app.exec())
