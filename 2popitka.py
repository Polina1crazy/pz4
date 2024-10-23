import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTextEdit, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QColor, QPalette


class FileScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.scan_button = QPushButton("Сканировать папку")
        self.scan_button.clicked.connect(self.scan_folder)
        self.file_list = QTextEdit()
        self.file_list.setReadOnly(True)

        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.file_list)
        self.setLayout(self.layout)

    def scan_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            files = os.listdir(folder)
            self.file_list.setPlainText("\n".join(files))


class TextFileEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.open_button = QPushButton("Открыть файл")
        self.save_button = QPushButton("Сохранить файл")

        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.text_edit.setPlainText(file.read())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())


class DataSaver(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.data_elements = {}

        for i in range(5):
            line_edit = QLineEdit()
            self.data_elements[f'Element {i + 1}'] = line_edit
            self.form_layout.addRow(QLabel(f'Элемент {i + 1}:'), line_edit)

        self.save_button = QPushButton("Сохранить данные")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить данные")
        if file_name:
            with open(file_name, 'a', encoding='utf-8') as file:
                for key, line_edit in self.data_elements.items():
                    file.write(f"{key}: {line_edit.text()}\n")


class ListReader(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.result_label = QLabel("Результаты:")
        self.load_button = QPushButton("Загрузить файл")

        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                count = len(lines)
                if count > 0:
                    self.result_label.setText(f"Количество элементов: {count}\n" +
                                              "\n".join(
                                                  [f"Поле {i + 1}: {line.strip()}" for i, line in enumerate(lines)]))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение на PyQt")
        self.setGeometry(100, 100, 800, 600)

        # Установка цвета фона
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#dda0dd"))
        self.setPalette(palette)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        self.tabs.addTab(FileScanner(), "Сканер файлов")
        self.tabs.addTab(TextFileEditor(), "Редактор текста")
        self.tabs.addTab(DataSaver(), "Сохранение данных")
        self.tabs.addTab(ListReader(), "Чтение списка")

        self.layout.addWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
