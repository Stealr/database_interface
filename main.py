import psycopg2, sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox)

# Обновлять таблицы после изменения данных
# Добавить вкладку с преподователями и с предметами
# Чётная, нечётная неделя
# попробовать добавить окно с предложением добавления новой пары в базу данных

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()
        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        self._create_shedeule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database='timetable_db', user='postgres', password='2003', host='localhost',
                                     port='5432')
        self.cursor = self.conn.cursor()

    def _create_shedeule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")
        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.saturday_gbox = QGroupBox("Saturday")
        self.update_shedule_button = QPushButton("Update")

        # оси внутри группы
        self.svbox = QVBoxLayout()  # главная вертикальная ось
        self.shbox1 = QHBoxLayout()  # горизонтальные оси, входящие в вертикальную ось
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)
        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox2.addWidget(self.tuesday_gbox)
        self.shbox2.addWidget(self.friday_gbox)
        self.shbox3.addWidget(self.wednesday_gbox)
        self.shbox3.addWidget(self.saturday_gbox)
        self.shbox4.addWidget(self.update_shedule_button)
        self.shedule_tab.setLayout(self.svbox)

        self._create_table()
        self.update_shedule_button.clicked.connect(self._update_shedule)

    def _create_table(self):
        for i in range(6):
            setattr(self,  self.days[i].lower() + '_table', QTableWidget())
            self.day_table = getattr(self, self.days[i].lower() + '_table')
            self.day_gbox = getattr(self, self.days[i].lower() + '_gbox')
            self.day_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.day_table.setColumnCount(6)
            self.day_table.setHorizontalHeaderLabels(["Subject", "Time", "Teacher", "Room numb", "", ''])
            self._update_table(self.days[i])
            self.mvbox = QVBoxLayout()  # ещё одна ось для qtablewitget
            self.mvbox.addWidget(self.day_table)
            self.day_gbox.setLayout(self.mvbox)

    # def _create_tuesday_table(self):
    #     self.tuesday_table = QTableWidget()
    #     self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    #     self.tuesday_table.setColumnCount(6)
    #     self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Teacher", "Room numb", "", ''])
    #     self._update_table('Tuesday')
    #     self.mvbox = QVBoxLayout()  # ещё одна ось для qtablewitget
    #     self.mvbox.addWidget(self.tuesday_table)
    #     self.tuesday_gbox.setLayout(self.mvbox)

    def _update_table(self, day):
        self.cursor.execute("SELECT * FROM timetable WHERE day='{day}'".format(day=day))
        records = list(self.cursor.fetchall())
        self.day_table = getattr(self, day.lower() + '_table')
        self.day_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            self.cursor.execute("SELECT * FROM teacher WHERE subject='{sub}'".format(sub=r[2]))
            teacher = list(self.cursor.fetchall())
            joinButton = QPushButton("Join")
            deleteButton = QPushButton('Delete')
            self.day_table.setItem(i, 0, QTableWidgetItem(str(r[2])))  # предмет
            self.day_table.setItem(i, 1, QTableWidgetItem(str(r[4])))  # время начала
            self.day_table.setItem(i, 2, QTableWidgetItem(str(teacher[0][1])))  # преподователь
            self.day_table.setItem(i, 3, QTableWidgetItem(str(r[3])))  # номер аудитории
            self.day_table.setCellWidget(i, 4, joinButton)
            self.day_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_table(num, day, id))
            deleteButton.clicked.connect(lambda ch, id=r[0]: self._delete_from_table(id, day))

        addButton = QPushButton("Add")
        self.day_table.setCellWidget(len(records), 4, addButton)
        addButton.clicked.connect(lambda: self._add_to_table(records, day))
        self.day_table.resizeRowsToContents()

    def _change_day_from_table(self, rowNum, day, id):
        row = list()
        self.day_table = getattr(self, day.lower() + '_table')
        for i in range(self.day_table.columnCount()):
            try:
                row.append(self.day_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(
                "UPDATE timetable SET subject='{subject}', start_time='{time}', room_numb='{room}' WHERE id='{id}'".format(
                    subject=row[0], time=row[1], room=row[3], id=id))
            self.conn.commit()
            self.cursor.execute(
                "UPDATE teacher SET full_name='{name}' WHERE subject='{sub}'".format(name=row[2], sub=row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_from_table(self, id, day):  # добавить разные дни недели
        try:
            self.day_table = getattr(self, day.lower() + '_table')
            self.cursor.execute("DELETE FROM timetable WHERE id='{id}'".format(id=id))
            self.day_table.clear()
            self._update_table(day)
        except:
            QMessageBox.about(self, "Error", "Erorr delete")

    def _add_to_table(self, rec, day):  # добавить разные дни недели
        try:
            self.day_table = getattr(self, day.lower() + '_table')
            subject = str(self.day_table.item(len(rec), 0).text())
            time = str(self.day_table.item(len(rec), 1).text())
            # teacher = str(self.day_table.item(len(rec), 2).text())
            room_numb = str(self.day_table.item(len(rec), 3).text())
            self.cursor.execute(
                "INSERT INTO timetable(day, subject, room_numb, start_time)VALUES('{day}', '{subject}', '{room_numb}', '{time}')".format(
                    subject=subject, room_numb=room_numb, time=time, day=day))
            self.conn.commit()
            self._update_table(day)
        except:
            QMessageBox.about(self, "Error",
                              "Такого предмета не существует в базе данных")

    def _update_shedule(self):
        for i in self.days:
            self._update_table(i)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())