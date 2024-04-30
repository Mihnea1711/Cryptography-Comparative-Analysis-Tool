import os

from PySide2.QtWidgets import QFileDialog


def on_comboboxFramework_changed(self):
    selected_item = self.comboboxFramework.currentText()
    selected_index = self.comboboxFramework.currentIndex()

    if selected_item:
        self.handle_framework_selection(selected_item, selected_index)
    else:
        self.clear_framework_related_components()


def on_comboboxAlgorithm_changed(self):
    selected_item = self.comboboxAlgorithm.currentText()
    selected_index = self.comboboxAlgorithm.currentIndex()

    if selected_item:
        self.handle_algorithm_selection(selected_item, selected_index)
    else:
        self.clear_algorithm_related_components()


def open_file_dialog(self):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(self, "Select File", os.getcwd(), "All Files (*);;Text Files (*.txt)", options=options)

    if file_path:
        self.handle_file_selection(file_path)
    else:
        self.clear_file_related_components()


def on_comboboxOperation_changed(self):
    selected_item = self.comboboxOperation.currentText()

    if selected_item:
        self.handle_operation_selection(selected_item)
    else:
        self.clear_operation_related_components()


def on_comboboxKey_changed(self):
    selected_item = self.comboboxKey.currentText()

    if selected_item:
        self.handle_key_selection(selected_item)
    else:
        self.clear_key_related_components()


def on_generate_keys_clicked(self):
    if self.picked_algorithm:
        try:
            self.generate_keys_for_algorithm()
        except Exception as e:
            self.handle_key_generation_error(e)
    else:
        self.show_error_message("Please select an algorithm first.")


def on_log_performance_clicked(self):
    if self.validate_performance_logging():
        try:
            self.log_performance_metrics()
        except Exception as e:
            self.handle_performance_logging_error(e)
