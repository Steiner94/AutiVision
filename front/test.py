from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject


class InputValidator(QObject):
    validation_done = pyqtSignal(bool)

    def validate_input(self, input_data):
        # Validate the input data here
        is_valid = True
        if not input_data:
            is_valid = False
        # Emit a signal to indicate the validation result
        self.validation_done.emit(is_valid)


class MainForm(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Enter some text:")
        self.line_edit = QLineEdit()
        self.validate_button = QPushButton("Validate")
        self.validation_result_label = QLabel()

        # Create an instance of the input validator
        self.validator = InputValidator()
        # Connect the validation_done signal to a slot function
        self.validator.validation_done.connect(self.handle_validation_result)

        # Connect the validate button click event to a slot function
        self.validate_button.clicked.connect(self.validate_input)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.validate_button)
        layout.addWidget(self.validation_result_label)
        self.setLayout(layout)

    def validate_input(self):
        input_data = self.line_edit.text()
        # Start the input validation in a separate thread
        self.validator.moveToThread(self.validator_thread)
        self.validator.validation_done.connect(self.validator_thread.quit)
        self.validator_thread.started.connect(
            lambda: self.validator.validate_input(input_data))
        self.validator_thread.finished.connect(self.validator.deleteLater)
        self.validator_thread.start()

    def handle_validation_result(self, is_valid):
        if is_valid:
            self.validation_result_label.setText("Input is valid")
        else:
            self.validation_result_label.setText("Input is invalid")


if __name__ == '__main__':
    app = QApplication([])
    main_form = MainForm()
    main_form.show()
    app.exec_()
