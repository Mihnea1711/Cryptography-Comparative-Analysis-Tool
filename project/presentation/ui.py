import os
from typing import Optional, List

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import *

from business.service.keygen import KeygenService
from business.service.performance import ApplicationService
from persistence.models.orms import Algorithm, Framework, PerformanceMetrics, KeyPair
from presentation.stylesheets import START_PAGE_LABEL_TITLE, ABOUT_TAB_INFO_TEXT, START_PAGE_START_BUTTON_STYLESHEET
from utils.constants import CryptoOperation, ALGORITHM_TYPE_SYMM, ALGORITHM_TYPE_ASYMM


####################################
#           Start Page UI          #
####################################
class StartPage(QWidget):
    def __init__(self, app_service: ApplicationService, key_gen_service: KeygenService):
        super().__init__()

        self.app_service = app_service
        self.key_gen_service = key_gen_service

        self.setWindowTitle("🔒 CryptoKey Manager 🔒")

        self.setFixedSize(400, 150)  # Adjust width and height as needed

        # Set logo
        app_icon = QIcon()
        app_icon.addFile("/static/logo.png")
        self.setWindowIcon(app_icon)

        # background color
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColor()
        color.setRed(62)
        color.setGreen(54)
        color.setBlue(63)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

        # Set background image
        self.background_label = QLabel(self)
        pixmap = QPixmap("/static/background.png")
        self.background_label.setPixmap(pixmap)
        self.background_label.setAlignment(Qt.AlignCenter)

        # Start button
        self.start_button = QPushButton("Start Encrypting/Decrypting")
        self.start_button.clicked.connect(self.go_to_home_page)
        self.start_button.setStyleSheet(START_PAGE_START_BUTTON_STYLESHEET)

        #Titlu
        labelTitle = QLabel("🔒 CryptoKey Manager 🔒")
        labelTitle.setAlignment(Qt.AlignCenter)  # Center the text
        title_font = QFont()  # Set font properties
        title_font.setBold(True)
        title_font.setPixelSize(30)
        title_font.setFamily("Arial")
        labelTitle.setFont(title_font)  # Apply the font to the label
        labelTitle.setStyleSheet(START_PAGE_LABEL_TITLE)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(labelTitle)
        layout.addWidget(self.background_label)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        self.home_page = None
    def go_to_home_page(self):
        self.hide()
        if self.home_page is None:
            self.home_page = HomePage(self.app_service, self.key_gen_service)
        self.home_page.show()

####################################
#             Home Page            #
####################################
class HomePage(QWidget):
    def __init__(self, app_service: ApplicationService, key_gen_service: KeygenService):
        super().__init__()

        self.app_service = app_service
        self.key_gen_service = key_gen_service

        self.framework_list: Optional[List[Framework]] = None
        self.algorithm_list: Optional[List[Algorithm]] = None
        self.key_pair_list: Optional[List[KeyPair]] = None
        self.performance_list: Optional[List[PerformanceMetrics]] = None

        self.picked_framework: Optional[Framework] = None
        self.picked_algorithm: Optional[Algorithm] = None
        self.picked_file: Optional[str] = None
        self.picked_operation: Optional[str] = None

        self.temporary_key_pair: Optional[(bytes, bytes)] = None

        self.about_tab = QWidget()
        self.table_widget = QTableWidget()
        self.performance_tab = QWidget()
        self.home_tab = QWidget()

        self.setup_home_page_details()

        ####################################
        #       Create page components     #
        ####################################
        # combobox Framework
        self.labelFramework = QLabel("Select Framework")
        # self.labelFramework.setStyleSheet(HOME_PAGE_LABEL_FRAMEWORK)
        self.comboboxFramework = QComboBox()
        # self.comboboxFramework.setStyleSheet(HOME_PAGE_COMBOBOX_FRAMEWORK)

        # combobox Algorithm
        self.labelAlgorithm = QLabel("Select Algorithm")
        self.labelAlgorithm.setDisabled(True)
        # self.labelAlgorithm.setStyleSheet(HOME_PAGE_LABEL_ALGORITHM)
        self.comboboxAlgorithm = QComboBox()
        self.comboboxAlgorithm.setDisabled(True)
        # self.comboboxAlgorithm.setStyleSheet(HOME_PAGE_COMBOBOX_ALGORITHM)

        # Select file
        self.labelChooseFile = QLabel("")
        self.labelChooseFile.setDisabled(True)
        # self.labelChooseFile.setStyleSheet(HOME_PAGE_LABEL_CHOOSE_FILE)
        self.buttonChooseFile = QPushButton("Select File")
        self.buttonChooseFile.clicked.connect(self.open_file_dialog)
        self.buttonChooseFile.setDisabled(True)
        # self.buttonChooseFile.setStyleSheet(HOME_PAGE_BUTTON_CHOOSE_FILE)

        # Operation
        self.labelOperation = QLabel("Select Operation")
        self.labelOperation.setDisabled(True)
        # self.labelOperation.setStyleSheet(HOME_PAGE_LABEL_OPERATION)
        self.comboboxOperation = QComboBox()
        self.comboboxOperation.addItems(["", CryptoOperation.ENCRYPT.value, CryptoOperation.DECRYPT.value])
        self.comboboxOperation.setDisabled(True)
        # self.comboboxOperation.setStyleSheet(HOME_PAGE_COMBOBOX_OPERATION)

        # Key
        self.labelKey = QLabel("Select Key")
        self.labelKey.setDisabled(True)
        # self.labelKey.setStyleSheet(HOME_PAGE_LABEL_KEY)
        self.comboboxKey = QComboBox()
        self.comboboxKey.setMinimumWidth(300)  # Adjust the width as needed
        self.comboboxKey.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.comboboxKey.setDisabled(True)
        # self.comboboxKey.setStyleSheet(HOME_PAGE_COMBOBOX_KEY)

        # GenerateKey
        self.buttonGenerateKeys = QPushButton("Generate Key")
        self.buttonGenerateKeys.setDisabled(True)
        # self.buttonGenerateKeys.setStyleSheet(HOME_PAGE_BUTTON_GENERATE_KEYS)

        # Calculate performance
        self.buttonLogPerformance = QPushButton("Log Performance")
        self.buttonLogPerformance.setDisabled(True)
        # self.buttonLogPerformance.setStyleSheet(HOME_PAGE_BUTTON_LOG_PERFORMANCE)
        self.labelTime = QLabel("Time: ")
        self.labelTime.setDisabled(True)
        # self.labelTime.setStyleSheet(HOME_PAGE_LABEL_TIME)

        ####################################
        #              Menu                #
        ####################################
        self.setup_home_tab()
        self.setup_performance_tab()
        self.setup_about_tab()

        self.tab_widget = QTabWidget()
        # self.tab_widget.setStyleSheet(HOME_PAGE_TAB_WIDGET)
        self.tab_widget.addTab(self.home_tab, "Home")
        self.tab_widget.addTab(self.performance_tab, "Performance")
        self.tab_widget.addTab(self.about_tab, "About")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        # set page layout
        self.setLayout(layout)

        # set component callbacks
        self.setup_component_callbacks()

        self.setup_framework_list()

    @staticmethod
    def show_error_message(message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec_()

    @staticmethod
    def show_info_message(message):
        info_box = QMessageBox()
        info_box.setIcon(QMessageBox.Information)
        info_box.setWindowTitle("Information")
        info_box.setText(message)
        info_box.exec_()

    def setup_framework_list(self):
        # Clear the existing items in the combobox
        self.comboboxFramework.clear()

        # Add an empty option as the first item
        self.comboboxFramework.addItem("")

        # Fetch the frameworks from the database
        self.framework_list = self.app_service.get_available_frameworks()

        # Iterate over the framework list and add the framework names to the combobox
        for framework in self.framework_list:
            self.comboboxFramework.addItem(framework.framework_name)

    def setup_algorithm_list(self):
        # Clear the existing items in the combobox
        self.comboboxAlgorithm.clear()

        # Add an empty option as the first item
        self.comboboxAlgorithm.addItem("")

        # Fetch the frameworks from the database
        self.algorithm_list = self.app_service.get_available_algorithms()

        # Iterate over the framework list and add the framework names to the combobox
        for algorithm in self.algorithm_list:
            self.comboboxAlgorithm.addItem(algorithm.algorithm_name)

    def setup_key_list(self):
        if self.picked_algorithm is None:
            # Show an error message if no algorithm is selected
            self.show_error_message("Please select an algorithm first.")
            return
        try:
            self.key_pair_list = self.app_service.get_key_pairs_for_chosen_algorithm(self.picked_algorithm.algorithm_id)
            self.comboboxKey.clear()
            self.comboboxKey.addItem("")

            if not self.key_pair_list:
                # If there are no keys available for decryption, display a message
                self.show_error_message("No keys available for decryption. Please encrypt something first.")
                self.comboboxOperation.setCurrentIndex(0)
                return

            # Iterate over the key pair list and add each first key to the comboboxKey
            for key_pair in self.key_pair_list:
                first_key_hex = key_pair.first_key.key_value.hex()
                self.comboboxKey.addItem(first_key_hex)
        except Exception as e:
            # Show an error message if there's an exception while retrieving keys
            error_message = f"Error fetching keys: {str(e)}"
            self.show_error_message(error_message)
            self.comboboxOperation.setCurrentIndex(0)

    def setup_performance_list(self):
        self.performance_list = self.app_service.get_recorded_performances()

    def refresh_performance_table(self):
        # Clear the existing table content
        self.table_widget.clearContents()

        # Update the performance list
        self.setup_performance_list()

        # Populate performance table
        self.table_widget.setRowCount(len(self.performance_list))
        for i, performance in enumerate(self.performance_list):
            timestamp_item = QTableWidgetItem(str(performance.timestamp))
            filename_item = QTableWidgetItem(performance.file.file_name if performance.file else "")
            framework_item = QTableWidgetItem(str(performance.framework.framework_name) if performance.framework else "")
            algorithm_item = QTableWidgetItem(str(performance.algorithm.algorithm_name) if performance.algorithm else "")
            operation_item = QTableWidgetItem(performance.op_type)
            time_taken_item = QTableWidgetItem(str(performance.time))

            self.table_widget.setItem(i, 0, timestamp_item)
            self.table_widget.setItem(i, 1, filename_item)
            self.table_widget.setItem(i, 2, framework_item)
            self.table_widget.setItem(i, 3, algorithm_item)
            self.table_widget.setItem(i, 4, operation_item)
            self.table_widget.setItem(i, 5, time_taken_item)

    def clear_all_components(self):
        self.comboboxFramework.setCurrentIndex(0)

        self.labelAlgorithm.setDisabled(True)
        self.comboboxAlgorithm.setCurrentIndex(0)
        self.comboboxAlgorithm.setDisabled(True)

        self.labelChooseFile.setDisabled(True)
        self.buttonChooseFile.setText("Select File")
        self.buttonChooseFile.setDisabled(True)

        self.buttonGenerateKeys.setDisabled(True)

        self.labelOperation.setDisabled(True)
        self.comboboxOperation.setCurrentIndex(0)
        self.comboboxOperation.setDisabled(True)

        self.labelKey.setDisabled(True)
        self.comboboxKey.setCurrentIndex(0)
        self.comboboxKey.setDisabled(True)

        self.buttonLogPerformance.setText("Log Performance")
        self.buttonLogPerformance.setDisabled(True)
        self.labelTime.setDisabled(True)

        self.picked_framework = None
        self.picked_algorithm = None
        self.picked_file = None
        self.picked_operation = None

        self.algorithm_list = None
        self.key_pair_list = None

    def setup_component_callbacks(self):
        #####################################################
        #          Event related callback functions         #
        #####################################################
        self.comboboxFramework.activated.connect(self.on_comboboxFramework_changed)
        self.comboboxAlgorithm.activated.connect(self.on_comboboxAlgorithm_changed)
        self.comboboxOperation.activated.connect(self.on_comboboxOperation_changed)
        self.comboboxKey.activated.connect(self.on_comboboxKey_changed)

        # self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Connect buttonGenerateKeys to its callback method
        self.buttonGenerateKeys.clicked.connect(self.on_generate_keys_clicked)
        # Connect buttonLogPerformance to its callback method
        self.buttonLogPerformance.clicked.connect(self.on_log_performance_clicked)

    #####################################################
    #                 App Title/Icon                    #
    #####################################################
    def setup_home_page_details(self):
        self.setWindowTitle("🔒 CryptoKey Manager 🔒")

        # set fixed size so no resizing is available
        self.setFixedSize(1000, 290)  # Adjust width and height as needed

        # background color
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColor()
        color.setRed(62)
        color.setGreen(54)
        color.setBlue(63)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

        # set logo
        app_icon = QIcon()
        app_icon.addFile("/static/logo.png")
        self.setWindowIcon(app_icon)

    #####################################################
    #                    Home Tab                       #
    #####################################################
    def setup_home_tab(self):
        # layout framework
        layoutFramework = QHBoxLayout()
        layoutFramework.addWidget(self.labelFramework)
        layoutFramework.addWidget(self.comboboxFramework)
        layoutFramework.addStretch()

        # layout generate keys
        hboxGenerateKeys = QHBoxLayout()
        hboxGenerateKeys.addStretch()  # Add stretchable space to push the button to the right
        hboxGenerateKeys.addWidget(self.buttonGenerateKeys)  # Add the button to the layout

        # layout for the first row
        hboxFirstRow = QHBoxLayout()
        hboxFirstRow.addLayout(layoutFramework)  # Add the framework layout to the first row
        hboxFirstRow.addStretch()  # Add stretchable space between the framework and button
        hboxFirstRow.addLayout(hboxGenerateKeys)  # Add the generate keys layout to the first row

        # layout algorithm
        hboxAlgorithm = QHBoxLayout()
        hboxAlgorithm.addWidget(self.labelAlgorithm)
        hboxAlgorithm.addWidget(self.comboboxAlgorithm)
        hboxAlgorithm.addStretch()

        # layout file
        hboxFile = QHBoxLayout()
        hboxFile.addWidget(self.buttonChooseFile)
        hboxFile.addStretch()

        # layout operation including key combobox
        hboxOperation = QHBoxLayout()
        hboxOperation.addWidget(self.labelOperation)
        hboxOperation.addWidget(self.comboboxOperation)
        hboxOperation.addStretch()  # Add stretchable space to push widgets to the right
        hboxOperation.addWidget(self.labelKey)  # Add the label before the key combobox
        hboxOperation.addWidget(self.comboboxKey)  # Add the key combobox

        # layout get performance
        hboxLogPerformance = QHBoxLayout()
        hboxLogPerformance.addStretch()  # Add stretchable space to push widgets to the center
        hboxLogPerformance.addWidget(self.buttonLogPerformance)
        hboxLogPerformance.addSpacing(10)  # Add a little gap between the button and the label
        hboxLogPerformance.addWidget(self.labelTime)
        hboxLogPerformance.addStretch()  # Add stretchable space to push widgets to the center

        # layout full home page
        layoutHomePage = QVBoxLayout()
        layoutHomePage.addLayout(hboxFirstRow)  # Add the first row layout
        layoutHomePage.addLayout(hboxAlgorithm)
        layoutHomePage.addLayout(hboxFile)
        layoutHomePage.addLayout(hboxOperation)
        layoutHomePage.addLayout(hboxLogPerformance)

        # menu
        self.home_tab.setLayout(layoutHomePage)

    #####################################################
    #                Performance Tab                    #
    #####################################################
    def setup_performance_tab(self):
        # Create Table
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["Timestamp", "Filename", "Framework", "Algorithm", "Operation", "Time_taken(ms)"])
        # Set the resize mode for the last column to stretch
        self.table_widget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        # Retrieve performance data from the service
        self.setup_performance_list()

        # Populate performance table
        self.table_widget.setRowCount(len(self.performance_list))
        for i, performance in enumerate(self.performance_list):
            timestamp_item = QTableWidgetItem(str(performance.timestamp))
            filename_item = QTableWidgetItem(performance.file.file_name if performance.file else "")
            framework_item = QTableWidgetItem(str(performance.framework.framework_name) if performance.framework else "")
            algorithm_item = QTableWidgetItem(str(performance.algorithm.algorithm_name) if performance.algorithm else "")
            operation_item = QTableWidgetItem(performance.op_type)
            time_taken_item = QTableWidgetItem(str(performance.time))

            self.table_widget.setItem(i, 0, timestamp_item)
            self.table_widget.setItem(i, 1, filename_item)
            self.table_widget.setItem(i, 2, framework_item)
            self.table_widget.setItem(i, 3, algorithm_item)
            self.table_widget.setItem(i, 4, operation_item)
            self.table_widget.setItem(i, 5, time_taken_item)

        # Set fixed column widths
        self.table_widget.setColumnWidth(0, 200)  # Timestamp
        self.table_widget.setColumnWidth(1, 280)  # Filename
        self.table_widget.setColumnWidth(2, 125)  # Framework
        self.table_widget.setColumnWidth(3, 75)  # Algorithm
        self.table_widget.setColumnWidth(4, 120)  # Operation
        self.table_widget.setColumnWidth(5, 120)  # Time_taken

        # Set up the scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.table_widget)
        scroll_area.setWidgetResizable(True)

        # Calculate window width based on table width
        table_width = self.table_widget.horizontalHeader().length() + \
                      self.table_widget.verticalHeader().width() + \
                      scroll_area.verticalScrollBar().width()
        window_width = table_width - 60
        window_height = 60

        self.performance_tab.setMinimumSize(window_width, window_height)

        # Set up layout
        layout_performance = QVBoxLayout()
        layout_performance.addWidget(scroll_area)

        self.performance_tab.setLayout(layout_performance)

    #####################################################
    #                   About Tab                       #
    #####################################################
    def setup_about_tab(self):

        about_text_label = QLabel()
        about_text_label.setText(ABOUT_TAB_INFO_TEXT)
        about_text_label.setWordWrap(True)
        about_text_label.setAlignment(Qt.AlignCenter)

        # layout text
        layout_about = QVBoxLayout()
        layout_about.addWidget(about_text_label)

        self.about_tab.setLayout(layout_about)


    #####################################
    #              Callbacks            #
    #####################################
    def on_comboboxFramework_changed(self):
        selected_item = self.comboboxFramework.currentText()
        selected_index = self.comboboxFramework.currentIndex()
        if selected_item != "" and selected_item is not None and len(selected_item) > 0:
            self.comboboxAlgorithm.setDisabled(False)
            self.labelAlgorithm.setDisabled(False)

            # Retrieve the Framework object corresponding to the selected index
            if selected_index <= len(self.framework_list):
                self.picked_framework = self.framework_list[selected_index - 1]
                print(self.picked_framework)

            self.setup_algorithm_list()
        else:
            self.labelAlgorithm.setDisabled(True)
            self.comboboxAlgorithm.setCurrentIndex(0)
            self.comboboxAlgorithm.setDisabled(True)

            self.labelChooseFile.setDisabled(True)
            self.buttonChooseFile.setText("Select File")
            self.buttonChooseFile.setDisabled(True)

            self.buttonGenerateKeys.setDisabled(True)

            self.labelOperation.setDisabled(True)
            self.comboboxOperation.setCurrentIndex(0)
            self.comboboxOperation.setDisabled(True)

            self.labelKey.setDisabled(True)
            self.comboboxKey.setCurrentIndex(0)
            self.comboboxKey.setDisabled(True)

            self.buttonLogPerformance.setText("Log Performance")
            self.buttonLogPerformance.setDisabled(True)
            self.labelTime.setDisabled(True)

            self.picked_framework = None
            self.picked_algorithm = None
            self.picked_file = None
            self.picked_operation = None

            self.algorithm_list = None
            self.key_pair_list = None

    def on_comboboxAlgorithm_changed(self):
        selected_item = self.comboboxAlgorithm.currentText()
        selected_index = self.comboboxAlgorithm.currentIndex()
        if selected_item != "" and selected_item is not None and len(selected_item) > 0:
            self.labelChooseFile.setDisabled(False)
            self.buttonChooseFile.setDisabled(False)
            self.buttonGenerateKeys.setDisabled(False)

            # Retrieve the Framework object corresponding to the selected index
            if selected_index <= len(self.algorithm_list):
                self.picked_algorithm = self.algorithm_list[selected_index - 1]
                print(self.picked_algorithm)
        else:
            self.labelChooseFile.setDisabled(True)
            self.buttonChooseFile.setText("Select File")
            self.buttonChooseFile.setDisabled(True)

            self.buttonGenerateKeys.setDisabled(True)

            self.labelOperation.setDisabled(True)
            self.comboboxOperation.setCurrentIndex(0)
            self.comboboxOperation.setDisabled(True)

            self.labelKey.setDisabled(True)
            self.comboboxKey.setCurrentIndex(0)
            self.comboboxKey.setDisabled(True)

            self.buttonLogPerformance.setText("Log Performance")
            self.buttonLogPerformance.setDisabled(True)
            self.labelTime.setDisabled(True)

            self.picked_algorithm = None
            self.picked_file = None
            self.picked_operation = None

            self.algorithm_list = None
            self.key_pair_list = None

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", os.getcwd(), "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.buttonChooseFile.setText(os.path.basename(file_path).split('/')[-1])
            print("Selected File:", file_path)
            self.picked_file = file_path
            self.labelOperation.setDisabled(False)
            self.comboboxOperation.setDisabled(False)
        else:
            self.buttonChooseFile.setText("Select File")
            self.labelOperation.setDisabled(True)
            self.comboboxOperation.setCurrentIndex(0)
            self.comboboxOperation.setDisabled(True)

            self.labelKey.setDisabled(True)
            self.comboboxKey.setCurrentIndex(0)
            self.comboboxKey.setDisabled(True)

            self.buttonLogPerformance.setText("Log Performance")
            self.buttonLogPerformance.setDisabled(True)
            self.labelTime.setDisabled(True)

            self.picked_file = None
            self.picked_operation = None

            self.algorithm_list = None
            self.key_pair_list = None

    def on_comboboxOperation_changed(self):
        selected_item = self.comboboxOperation.currentText()
        self.comboboxKey.setCurrentIndex(0)
        if selected_item != "" and selected_item is not None and len(selected_item) > 0:
            self.labelKey.setDisabled(False)
            self.comboboxKey.setDisabled(False)
            self.picked_operation = selected_item
            if selected_item == CryptoOperation.ENCRYPT.value:
                if self.temporary_key_pair is None:
                    # Display a message prompting the user to generate an encryption key
                    message_box = QMessageBox()
                    message_box.setIcon(QMessageBox.Information)
                    message_box.setWindowTitle("Generate Encryption Key")
                    message_box.setText("Please click the 'Generate Key' button to generate an encryption key.")
                    message_box.exec_()
                else:
                    # Insert the second key of the pair into the combobox_key
                    second_key_bytes = self.temporary_key_pair[1]  # Assuming the second key is stored at index 1
                    second_key_hex = second_key_bytes.hex()  # Convert bytes to hexadecimal string
                    self.comboboxKey.clear()
                    self.comboboxKey.addItem("")  # Add the key to the combobox
                    # Add the hexadecimal string representation of the key to the combobox
                    self.comboboxKey.addItem(second_key_hex)  # Add the key to the combobox
                    # Find the index of the newly added item
                    index = self.comboboxKey.findText(second_key_hex)
                    if index != -1:
                        # Set the current index to the index of the newly added item
                        self.comboboxKey.setCurrentIndex(index)

                    self.labelTime.setDisabled(False)
                    self.buttonLogPerformance.setDisabled(False)
            elif selected_item == CryptoOperation.DECRYPT.value:
                self.setup_key_list()
        else:
            self.labelKey.setDisabled(True)
            self.comboboxKey.setCurrentIndex(0)
            self.comboboxKey.setDisabled(True)

            self.buttonLogPerformance.setText("Log Performance")
            self.buttonLogPerformance.setDisabled(True)
            self.labelTime.setDisabled(True)

            self.picked_operation = None

            self.algorithm_list = None
            self.key_pair_list = None

    def on_comboboxKey_changed(self):
        selected_item = self.comboboxKey.currentText()
        print(selected_item)
        if selected_item != "" and selected_item is not None and len(selected_item) > 0:
            self.labelTime.setDisabled(False)
            self.buttonLogPerformance.setDisabled(False)
        else:
            self.buttonLogPerformance.setText("Log Performance")
            self.buttonLogPerformance.setDisabled(True)
            self.labelTime.setDisabled(True)

            self.algorithm_list = None
            self.key_pair_list = None

    def on_generate_keys_clicked(self):
        if self.picked_algorithm is None:
            self.show_error_message("Please select an algorithm first.")
            return
        try:
            # Call the key generation service method
            self.temporary_key_pair = self.key_gen_service.generate_keys(self.picked_algorithm.algorithm_type)
            private_key = self.temporary_key_pair[0]
            public_key = self.temporary_key_pair[1]

            message = None
            if self.picked_algorithm.algorithm_type == ALGORITHM_TYPE_SYMM:
                message = f"Symmetric Key generated successfully:\n\n{private_key}"
            elif self.picked_algorithm.algorithm_type == ALGORITHM_TYPE_ASYMM:
                message = f"Asymmetric Keys generated successfully:\n\nPrivate Key:\n{private_key}\n\nPublic Key:\n{public_key}"
            self.show_info_message(message)

            # only if the user selected to encrypt
            if self.comboboxOperation.currentIndex() != 0 and self.comboboxOperation.currentText() == CryptoOperation.ENCRYPT.value:
                # Insert the second key of the pair into the combobox_key
                second_key_bytes = self.temporary_key_pair[1]  # Assuming the second key is stored at index 1
                second_key_hex = second_key_bytes.hex()  # Convert bytes to hexadecimal string
                self.comboboxKey.clear()
                self.comboboxKey.addItem("")  # Add the key to the combobox
                # Add the hexadecimal string representation of the key to the combobox
                self.comboboxKey.addItem(second_key_hex)  # Add the key to the combobox
                # Find the index of the newly added item
                index = self.comboboxKey.findText(second_key_hex)
                if index != -1:
                    # Set the current index to the index of the newly added item
                    self.comboboxKey.setCurrentIndex(index)
                self.labelTime.setDisabled(False)
                self.buttonLogPerformance.setDisabled(False)
        except Exception as e:
            error_message = f"Error generating keys: {str(e)}"
            self.show_error_message(error_message)

    def on_log_performance_clicked(self):
        if self.picked_framework is None:
            self.show_error_message("Please select an framework.")
            return

        if self.picked_algorithm is None:
            self.show_error_message("Please select an algorithm.")
            return

        if self.picked_file is None:
            self.show_error_message("Please select a file.")
            return

        if self.picked_operation is None:
            self.show_error_message("Please select an operation.")
            return

        if self.comboboxKey.currentText() is None:
            self.show_error_message("Please select a key.")
            return

        self.app_service.set_framework(self.picked_framework)
        self.app_service.set_algorithm(self.picked_algorithm)

        try:
            # Get the hexadecimal string from the comboboxKey
            picked_key_hex = self.comboboxKey.currentText()
            print(picked_key_hex)

            # Convert the hexadecimal string to bytes
            picked_key_bytes = bytes.fromhex(picked_key_hex)
            print(picked_key_bytes)
            # Call the performance logging service method with the key as bytes
            new_file_path, time_taken_ms = self.app_service.measure_algorithm_performance(
                self.picked_framework.framework_id,
                self.picked_algorithm.algorithm_id,
                self.picked_file,
                self.picked_operation,
                picked_key_bytes  # Pass the key as bytes
            )

            # Refresh performance table after inserting new data
            self.refresh_performance_table()

            # save the keys to db if encrypting
            if self.picked_operation == CryptoOperation.ENCRYPT.value and self.temporary_key_pair is not None:
                self.key_gen_service.save_key_pair_in_db(self.temporary_key_pair, self.picked_algorithm)

            # display time taken
            self.labelTime.setText(str(time_taken_ms) + " ms")

            # clear all components to start fresh
            self.clear_all_components()

            print("Performance metrics logged successfully. New file generated at " + new_file_path)
        except Exception as e:
            error_message = f"Error logging performance: {str(e)}"
            self.show_error_message(error_message)