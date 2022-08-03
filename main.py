import sys, os, json, style_sheet
from PyQt5.QtWidgets import (QApplication, QWidget, QCheckBox, QLineEdit, QPushButton, QLabel, QHBoxLayout,
                             QVBoxLayout, QFrame, QInputDialog, QScrollArea, QGridLayout, QMessageBox)
from PyQt5.QtCore import QSize, Qt, QDate, QTime, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont, QPalette

class TaskWidget(QWidget):

    clicked_signal = pyqtSignal()
    state_signal = pyqtSignal(bool)

    def __init__(self, task_data):
        super(TaskWidget, self).__init__()
        self.task_data = task_data

        self.setMaximumHeight(100);
        self.initializeUI()

    def initializeUI(self):

        # create the main container
        self.main_container = QWidget()
        self.main_container.setObjectName("main_container")
        # set the tool tip for widget
        self.setToolTip(self.task_data["text"])

        self.updateUserData()
        self.setObjectName("main_widget")
        # set the widget basic properties
        # create the check box for set the state of the task
        self.state_box = QCheckBox()
        self.state_box.setCheckState(self.task_data["state"])
        self.state_box.stateChanged.connect(self.changeState)

        # create the task label
        self.task_label = QLabel(self.task_data["text"])
        self.task_label.setWordWrap(True)
        self.task_label.setFont(QFont("Helvetica [Cronyx]", 12))

        # create the drop down button
        self.drop_down_button = QPushButton(">")
        self.drop_down_button.pressed.connect(self.show)

        # create the date and time label
        self.generate_date_time_label = QLabel(f"Generate on {self.task_data['init_date']} \n at the {self.task_data['init_time']}")
        self.generate_date_time_label.setVisible(False)
        self.generate_date_time_label.setFont(QFont("Helvetica", 10))
        self.generate_date_time_label.setStyleSheet("color : rgb(100, 100, 100)")

        if ("end_date" in self.task_data.keys() and "end_time" in self.task_data.keys()):
            self.ended_date_time_label = QLabel(f"Task completed on {self.task_data['end_date']} \n at {self.task_data['end_time']}")
        else:
            self.ended_date_time_label = QLabel("Task Not Complete")

        self.ended_date_time_label.setVisible(False)
        self.ended_date_time_label.setFont(QFont("Helvetica", 10))
        self.ended_date_time_label.setStyleSheet("color : rgb(200, 100, 100)")

        # create the hide button
        self.hide_labels = QPushButton("<")
        self.hide_labels.pressed.connect(self.hide)
        self.hide_labels.setVisible(False)

        # pack the item for widget using layout
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.state_box)
        h_box1.addWidget(self.task_label, stretch=2)
        h_box1.addWidget(self.drop_down_button)

        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.generate_date_time_label)
        h_box2.addWidget(self.ended_date_time_label)
        h_box2.addWidget(self.hide_labels)

        # create the main layout for widget
        v_box = QVBoxLayout()
        v_box.addLayout(h_box1)
        v_box.addSpacing(10)
        v_box.addLayout(h_box2)

        self.main_container.setLayout(v_box)
        other_v_box = QVBoxLayout()
        other_v_box.addWidget(self.main_container)

        self.setLayout(other_v_box)

    def mousePressEvent(self, event):

        self.clicked_signal.emit()

    def updateUserData(self):

        # load the json file user data
        user_data = []
        with open("db/user_data.json", "r") as file:
            user_data = json.load(file)

        isExist = False
        for item in user_data:
            if item["text"] == self.task_data["text"]:
                isExist = True
                break
        if not isExist:
            user_data.append(self.task_data)

        # write the new json file
        with open("db/user_data.json", "w") as file:
            json.dump(user_data, file, indent=4)

    def setLabelText(self, text):

        self.task_label.setText(text)

    def show(self):

        # show the date and tim elabels
        self.generate_date_time_label.setVisible(True)
        self.ended_date_time_label.setVisible(True)
        self.hide_labels.setVisible(True)

        self.drop_down_button.setVisible(False)
        # create the an animation
        self.animation  = QPropertyAnimation(self, b"minimumHeight")
        self.animation.setStartValue(self.height())
        self.animation.setEndValue(150)
        self.animation.setCurrentTime(1000)
        self.animation.start()

        self.setMinimumHeight(150)
        self.setMaximumHeight(150)

    def hide(self):

        self.generate_date_time_label.setVisible(False)
        self.ended_date_time_label.setVisible(False)
        self.hide_labels.setVisible(False)

        self.drop_down_button.setVisible(True)
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)

    def changeState(self, boolValue : bool):

        # changed the check box state
        self.state_box.setCheckState(boolValue)
        self.state_signal.emit(boolValue)

        user_data = []
        # changed the user data
        with open("db/user_data.json", "r") as file:
            user_data = json.load(file)

        for item in user_data:
            if item["text"] == self.task_data["text"]:
                item["state"] = boolValue
                if boolValue:
                    item["end_date"] = QDate.currentDate().toString()
                    item["end_time"] = QTime.currentTime().toString()

                    self.ended_date_time_label.setText(f"Task completed on {item['end_date']} at {item['end_time']}")
                break

        # write to the json file again
        with open("db/user_data.json", "w") as file:
            json.dump(user_data, file, indent=4)

    def setClickedState(self):

        self.setStyleSheet("""
                            QWidget#main_container {border : none;
                                                    border-radius : 5px;
                                                    background-color : rgb(0, 0, 200)}""")

    def setUnClickedState(self):

        self.setStyleSheet("""
                            QWidget#main_container {background : none}""")

    def mouseDoubleClickEvent(self, event):

        # change the task widget text
        # first get the changed text for the widget
        text , ok = QInputDialog.getText(self, "Changes Text", "Enter the your changes text below : ")

        if ok:
            # change the task widget text and change the user data
            user_data = []
            with open("db/user_data.json", "r") as file:
                user_data = json.load(file)

            for part in user_data:
                if part["text"] == self.task_data["text"]:
                    part["text"] = text
                    self.task_data["text"] = text
                    break

            # save the changes
            with open("db/user_data.json", "w") as file:
                json.dump(user_data, file, indent=4)
            # change the label text
            self.setLabelText(text)

class TaskCompleter(QWidget):
    def __init__(self):
        super(TaskCompleter, self).__init__()
        self.initializeUI()

    def initializeUI(self):

        user_data = []
        if not os.path.exists("db"):
        	os.makedirs("db/")

        if not (os.path.exists("db/user_data.json")):
            # create the new json file to store the user data
            with open("db/user_data.json", "w") as file:
                json.dump(user_data, file, indent=4)
        # create the program main lists
        self.taskWidget_list = []
        self.currentSelect_widget = None

        # set the title to window
        self.setWindowTitle("Task Completer version-1.0.0")
        self.setGeometry(250, 100, 550, 600)
        self.setUpWidgets()
        self.setStyleSheet(style_sheet.style_sheet)

        # show the window in the screen
        self.show()

    def setUpWidgets(self):

        # this is the setUp method for the main widgets
        # create the title label
        title_label = QLabel("Task Completer")
        title_label.setFont(QFont("Helvetica", 30))
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setObjectName("titleLabel")

        author_label  =QLabel("developed by Shavin Anjitha \n on 2021-06-10")
        author_label.setFont(QFont("verdana", 10))
        author_label.setStyleSheet("color : rgb(70, 70, 70)")

        # create the information tab
        self.information_tab = QWidget()
        # create the information tab
        self.createInformationTab()

        # create the button for add the task to the program
        self.addButton = QPushButton("+")
        self.addButton.setFont(QFont("Helvetica", 33))
        self.addButton.pressed.connect(self.createNewTask)
        self.addButton.setObjectName("addButton")

        self.removeButton = QPushButton("-")
        self.removeButton.setFont(QFont("Helvetica", 33))
        self.removeButton.setObjectName("removeButton")
        self.removeButton.pressed.connect(self.removeTask)

        # create the delete All button
        self.deleteAllButton = QPushButton("Delete All")
        self.deleteAllButton.setFont(QFont("Helvetica", 10))
        self.deleteAllButton.setObjectName("delete_all_button")
        self.deleteAllButton.pressed.connect(self.removeAll)

        # create the frame object for pack the task widgets
        self.taskFrame = QWidget()
        # self.taskFrame.setObjectName("main_widget")
        # create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setObjectName("main_widget")
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.taskFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # create the layout for set to the frame
        self.widget_lyt = QVBoxLayout()
        self.widget_lyt.setSpacing(0)
        self.taskFrame.setLayout(self.widget_lyt)

        # set up the frame widget
        self.setUpFrame()

        # create the layout for pack the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.removeButton)
        button_layout.addWidget(self.deleteAllButton)
        button_layout.addStretch()


        # create the v box for pack the all of widgets
        v_box = QVBoxLayout()
        v_box.addWidget(title_label)
        v_box.addWidget(author_label, alignment=Qt.AlignmentFlag.AlignRight)
        v_box.addWidget(self.information_tab)
        v_box.addWidget(scroll_area)
        v_box.addLayout(button_layout)

        self.setLayout(v_box)

    def createInformationTab(self):

        # calculate the number of tasks
        user_data = []
        with open("db/user_data.json", "r") as file:
            user_data = json.load(file)

        total_value = len(user_data)
        current_value = 0
        completed_value = 0

        for part in user_data:
            if part["state"]:
                completed_value += 1
        current_value = total_value - completed_value

        # create the layout for pack the labels
        title_list = []
        for text in ["Current Task", "Completed Task", "Total Task"]:
            # create new label
            new_label = QLabel(text)
            new_label.setFont(QFont('Helvetica [Cronyx]', 12))
            new_label.setStyleSheet("color : rgb(100, 100, 100)")
            title_list.append(new_label)

        # create the value Labels
        current_label = QLabel(str(current_value))
        completed_label = QLabel(str(completed_value))
        total_label = QLabel(str(total_value))

        self.value_label = [current_label, completed_label, total_label]
        for label in self.value_label:
            label.setFont(QFont("Helvetica [Cronyx]", 33))
            label.setStyleSheet("color : rgb(250, 0, 150)")

        # create the layout
        self.info_lyt = QGridLayout()
        self.info_lyt.setVerticalSpacing(5)

        for i, label in enumerate([*title_list, *self.value_label]):
            self.info_lyt.addWidget(label, i//3, i%3)
            self.info_lyt.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        self.information_tab.setLayout(self.info_lyt)

    def setUpFrame(self):

        # load the json file and create the TaskWidget using json data
        user_data = []
        with open("db/user_data.json", "r") as file:
            user_data = json.load(file)

        for item in user_data:
            # create the Task Widget and add to the layout
            new_task_widget = TaskWidget(item)
            new_task_widget.clicked_signal.connect(lambda e=new_task_widget : self.clickedWidget(e))
            new_task_widget.state_signal.connect(self.changeValue)
            # append to the list of widgets
            self.taskWidget_list.append(new_task_widget)
            # adf to the layout
            self.widget_lyt.insertWidget(0, new_task_widget)


    def createNewTask(self):

        # first ask the task tex from the user
        text, ok = QInputDialog.getText(self, "Add Task", "Enter Your Task below as the Plain text : ")

        if ok:
            # create the new task widget
            current_date, current_time = QDate.currentDate().toString() , QTime.currentTime().toString()
            new_widget = TaskWidget({"text" : text, "state" : False , "init_date" : current_date , "init_time" : current_time})
            new_widget.clicked_signal.connect(lambda e=new_widget : self.clickedWidget(e))
            new_widget.state_signal.connect(self.changeValue)
            # add to the widget list
            self.taskWidget_list.append(new_widget)
            # add to the layout
            self.widget_lyt.insertWidget(0, new_widget)

            # change the value labels text
            self.value_label[2].setText(str(int(self.value_label[2].text()) + 1))
            self.value_label[0].setText(str(int(self.value_label[0].text()) + 1))

    def removeTask(self):

        warning =  QMessageBox.warning(self, "Remove Task Warning", "do you want to remove this task?", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)

        if self.currentSelect_widget != None and warning == QMessageBox.StandardButton.Yes:

            # delete the task from the user_data
            user_data = []
            with open("db/user_data.json", "r") as file:
                user_data = json.load(file)

            new_user_data = []
            for part in user_data:
                if part["text"] != self.currentSelect_widget.task_data["text"]:
                    new_user_data.append(part)

            with open("db/user_data.json", "w") as file:
                json.dump(new_user_data, file, indent=4)

            # changed the value labels text
            self.value_label[2].setText(str(int(self.value_label[2].text()) - 1))
            if self.currentSelect_widget.task_data["state"]:
                self.value_label[1].setText(str(int(self.value_label[1].text()) - 1))
            else:
                self.value_label[0].setText(str(int(self.value_label[0].text()) - 1))

            # delete the selected task widget from the widget list
            self.taskWidget_list.remove(self.currentSelect_widget)
            self.currentSelect_widget.deleteLater()

            self.currentSelect_widget = None

    def clickedWidget(self, widget : TaskWidget):

        self.currentSelect_widget = widget

        for task_widget in self.taskWidget_list:
            # changes the widget style
            if task_widget == widget:
                task_widget.setClickedState()
            else:
                task_widget.setUnClickedState()

    def changeValue(self, bool):

        if bool:
            # change the label values
            self.value_label[0].setText(str(int(self.value_label[0].text()) - 1))
            self.value_label[1].setText(str(int(self.value_label[1].text()) + 1))
        else:
            # change the label values
            self.value_label[0].setText(str(int(self.value_label[0].text()) + 1))
            self.value_label[1].setText(str(int(self.value_label[1].text()) - 1))

    def removeAll(self):

        message = QMessageBox.warning(self, "Delete All Tasks Warning", "Are you sure want to delete all of tasks?", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        if message == QMessageBox.StandardButton.Yes:
            # delete the all widget of the window
            for widget in self.taskWidget_list:
                widget.deleteLater()
            self.currentSelect_widget = None
            self.taskWidget_list = []

            # set the user data as the empty data
            user_data = []
            with open("db/user_data.json", "w") as file:
                json.dump(user_data, file, indent=4)

            for label in self.value_label:
                label.setText(str(0))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Shadow, QColor(25, 25, 25))
    palette.setColor(QPalette.Window, QColor(10, 10, 10))
    palette.setColor(QPalette.WindowText, QColor("white"))
    palette.setColor(QPalette.Base, QColor(10, 10, 10))
    palette.setColor(QPalette.AlternateBase, QColor(10, 10, 10))
    palette.setColor(QPalette.ToolTipBase, QColor('white'))
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(43, 43, 43))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)

    palette.setColor(QPalette.Highlight, QColor(250, 70, 8))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)

    window = TaskCompleter()
    app.exec_()