START_PAGE_START_BUTTON_STYLESHEET = """
            QPushButton {
                background-color: #DD403A; /* Vermilion */
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            
            QPushButton:hover {
                background-color: #B62E29; /* Darker Green */
            }
            
            QPushButton:pressed {
                background-color: #8F1F1A; /* Dark Green */
            }   
        """

START_PAGE_LABEL_TITLE = "color: white;"

HOME_PAGE_LABEL_FRAMEWORK = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_COMBOBOX_FRAMEWORK = """
            QComboBox {
                padding: 8px 16px;
                border: 1px solid #DD403A; /* Vermilion */
                border-radius: 4px;
                background-color: #FFFFFF; /* White */
                color: #333333; /* Dark Gray */
            }

            QComboBox::drop-down {
                width: 16px;
            }

            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }

            QComboBox::down-arrow:on {
                image: url(down_arrow_hover.png);
            }
        """

HOME_PAGE_LABEL_ALGORITHM = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_COMBOBOX_ALGORITHM = """
            QComboBox {
                padding: 8px 16px;
                border: 1px solid #DD403A; /* Vermilion */
                border-radius: 4px;
                background-color: #FFFFFF; /* White */
                color: #333333; /* Dark Gray */
            }
            QComboBox::drop-down {
                width: 16px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
            QComboBox::down-arrow:on {
                image: url(down_arrow_hover.png);
            }
        """

HOME_PAGE_LABEL_CHOOSE_FILE = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_BUTTON_CHOOSE_FILE = """
            QPushButton {
                background-color: #DD403A; /* Vermilion */
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #B62E29; /* Darker Green */
                color: white;
            }
            QPushButton:pressed {
                background-color: #8F1F1A; /* Dark Green */
                color: white;
            }
        """

HOME_PAGE_LABEL_OPERATION = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_COMBOBOX_OPERATION = """
            QComboBox {
                padding: 8px 16px;
                border: 1px solid #DD403A; /* Green */
                border-radius: 4px;
                background-color: #FFFFFF; /* White */
                color: #333333; /* Dark Gray */
            }
            QComboBox::drop-down {
                width: 16px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
            QComboBox::down-arrow:on {
                image: url(down_arrow_hover.png);
            }
        """

HOME_PAGE_LABEL_KEY = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_COMBOBOX_KEY = """
            QComboBox {
                padding: 8px 16px;
                border: 1px solid #DD403A; /* Green */
                border-radius: 4px;
                background-color: #FFFFFF; /* White */
                color: #333333; /* Dark Gray */
            }
            QComboBox::drop-down {
                width: 16px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
            QComboBox::down-arrow:on {
                image: url(down_arrow_hover.png);
            }
        """

HOME_PAGE_BUTTON_GENERATE_KEYS = """
            QPushButton {
                background-color: #DD403A; /* Vermilion */
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #B62E29; /* Darker Green */
                color: white;
            }
            QPushButton:pressed {
                background-color: #8F1F1A; /* Dark Green */
                color: white;
            }
        """

HOME_PAGE_LABEL_SHOW_FIRST_KEY = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_LABEL_SHOW_SECOND_KEY = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_BUTTON_LOG_PERFORMANCE = """
            QPushButton {
                background-color: #DD403A; /* Vermilion */
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #B62E29; /* Darker Green */
                color: white;
            }
            QPushButton:pressed {
                background-color: #8F1F1A; /* Dark Green */
                color: white;
            }
        """

HOME_PAGE_LABEL_TIME = """
            QLabel {
                color: #333333; /* Dark Gray */
                font-size: 16px;
            }
        """

HOME_PAGE_TAB_WIDGET = """
                    QTabWidget::pane {
                        border: none;
                        background-color: #FFFFFF; /* White */
                    }
                    QTabBar::tab {
                        background-color: #DD403A; /* Vermilion */
                        color: white;
                        padding: 8px 16px;
                        border-top-left-radius: 4px;
                        border-top-right-radius: 4px;
                    }
                    QTabBar::tab:selected {
                        background-color: #B62E29; /* Darker Vermilion */
                    }
                """

HOME_PAGE_PERFORMANCE_TABLE_WIDGET = """
                    QTableWidget {
                        background-color: #FFFFFF; /* White */
                        color: #333333; /* Dark Gray */
                        border: 1px solid #DD403A; /* Green */
                        border-radius: 4px;
                    }
                    QTableWidget::item {
                        padding: 8px 16px;
                        border-bottom: 1px solid #DD403A; /* Green */
                    }
                    QTableWidget::item:selected {
                        background-color: #B62E29; /* Darker Green */
                        color: white;
                    }
                """

ABOUT_TAB_INFO_TEXT = """
                <p style='font-size: 14px; color: #333333;'>
                <b>CryptoKey Manager</b> is a simple application designed to manage cryptographic keys.
                It provides functionality to select a cryptographic framework, algorithm, and operation,
                and allows users to generate keys, perform encryption and decryption operations, and
                calculate performance metrics.
                </p>
                <p style='font-size: 12px; color: #666666;'>
                This application frontend is developed using PySide2, a Python binding for the Qt framework.
                </p>
                <p style='font-size: 12px; color: #666666;'>
                <b>Author Interface:</b> Florin Nistor<br>
                <b>Author Framework SSL + Performance Calculation:</b> Radu-Iulian Chirca<br>
                <b>Author Framework Crypto + Database:</b> Mihnea Bejinaru<br>
                <b>Author Framework PyCryptoDome + Key Generation:</b> Robert Ciocan<br>
                <b>Version:</b> 1.0
                </p>
            """