import sys
from PySide6 import QtWidgets, QtCore
from mode_dialog import Ui_ModeChooseDialog

class ModeChooseDialog(QtWidgets.QDialog, Ui_ModeChooseDialog):
    csv_chosen = QtCore.Signal()
    sql_chosen = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_choose_csv.clicked.connect(self.on_csv_button_clicked)
        self.button_choose_sql.clicked.connect(self.on_sql_button_clicked)

    def on_csv_button_clicked(self):
        print("CSV button clicked")
        self.csv_chosen.emit()
        self.close()

    def on_sql_button_clicked(self):
        print("SQL button clicked")
        self.sql_chosen.emit()
        self.close()


class MainApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.dialog = ModeChooseDialog()
        self.dialog.csv_chosen.connect(self.handle_csv_chosen)
        self.dialog.sql_chosen.connect(self.handle_sql_chosen)

    def handle_csv_chosen(self):
        print("CSV mode chosen")
        # Add your logic here

    def handle_sql_chosen(self):
        print("SQL mode chosen")
        # Add your logic here

    def run(self):
        self.dialog.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MainApp()
    app.run()
