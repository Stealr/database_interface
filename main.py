import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()
        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedeule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database='timetable_db', user='postgres', password='2003', host='localhost',
                                     port='5432')
        self.cursor = self.conn.cursor()

    def _create_shedeule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")
        self.monday_gbox = QGroupBox("Monday")
        self.update_shedule_button = QPushButton("Update")

        # оси внутри группы
        self.svbox = QVBoxLayout()  # главная вертикальная ось
        self.shbox1 = QHBoxLayout()  # горизонтальные оси, входящие в вертикальную ось
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.monday_gbox)
        self.shbox2.addWidget(self.update_shedule_button)
        self.shedule_tab.setLayout(self.svbox)

        self._create_monday_table()
        self.update_shedule_button.clicked.connect(self._update_shedule)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(5)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "Teacher", "Room numb", ""])
        self._update_monday_table()
        self.mvbox = QVBoxLayout()  # ещё одна ось для qtablewitget
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Monday'")
        records = list(self.cursor.fetchall())
        print(records)
        self.monday_table.setRowCount(len(records) + 1)
        records.reverse()
        for i, r in enumerate(records):
            r = list(r)
            print(r)
            joinButton = QPushButton("Join")
            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[2])))  # предмет
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[4])))  # время начала
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[4])))  # преподователь
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))  # номер аудитории
            self.monday_table.setCellWidget(i, 4, joinButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, 'Monday'))
        self.monday_table.resizeRowsToContents()

    def _change_day_from_table(self, rowNum, day):
        row = list()
        time = ['09:30', '11:20', '13:10', '15:25', '17:15']
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            print(row, row[0], row[1])
            self.cursor.execute(
                "UPDATE timetable SET subject={subject}, start_time={time}, room_numb={room} WHERE start_time={start_time}".format(
                    subject=row[0], time=row[1], room=row[3], start_time=time[rowNum]))
            print(11)
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_shedule(self):
        self._update_monday_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
