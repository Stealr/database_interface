import psycopg2, sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox)


# Установить размеры окна.
# Обновлять таблицы после изменения данных
# Добавить вкладку с предметами +
# Чётная, нечётная неделя
# попробовать добавить окно с предложением добавления новой пары в базу данных
# добавить сортировку по времени +
# Исправить ввод пустых строчек +-
# Изменять первую букву на большую.
# Увеличить размер клеток в таблице пар

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
        self._create_subject_tab()
        self._create_teacher_tab()
        # self._create_odd_shedeule_tab()

    # Присоединение к бд \/
    def _connect_to_db(self):
        self.conn = psycopg2.connect(database='timetable_db', user='postgres', password='2003', host='localhost',
                                     port='5432')
        self.cursor = self.conn.cursor()

    # Создание вкладки(расписания), групп и кнопки \/
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

        self._create_shedule_table()

        self.update_shedule_button.clicked.connect(self._update_shedule)

    # def _create_odd_shedeule_tab(self):
    #     self.sheduleodd_tab = QWidget()
    #     self.tabs.addTab(self.sheduleodd_tab, "Shedule_odd")
    #     self.monday_gbox = QGroupBox("Monday")
    #     self.tuesday_gbox = QGroupBox("Tuesday")
    #     self.wednesday_gbox = QGroupBox("Wednesday")
    #     self.thursday_gbox = QGroupBox("Thursday")
    #     self.friday_gbox = QGroupBox("Friday")
    #     self.saturday_gbox = QGroupBox("Saturday")
    #     self.update_sheduleodd_button = QPushButton("Update")
    #
    #     # оси внутри группы
    #     self.svbox = QVBoxLayout()  # главная вертикальная ось
    #     self.shbox1 = QHBoxLayout()  # горизонтальные оси, входящие в вертикальную ось
    #     self.shbox2 = QHBoxLayout()
    #     self.shbox3 = QHBoxLayout()
    #     self.shbox4 = QHBoxLayout()
    #     self.svbox.addLayout(self.shbox1)
    #     self.svbox.addLayout(self.shbox2)
    #     self.svbox.addLayout(self.shbox3)
    #     self.svbox.addLayout(self.shbox4)
    #     self.shbox1.addWidget(self.monday_gbox)
    #     self.shbox1.addWidget(self.thursday_gbox)
    #     self.shbox2.addWidget(self.tuesday_gbox)
    #     self.shbox2.addWidget(self.friday_gbox)
    #     self.shbox3.addWidget(self.wednesday_gbox)
    #     self.shbox3.addWidget(self.saturday_gbox)
    #     self.shbox4.addWidget(self.update_sheduleodd_button)
    #     self.sheduleodd_tab.setLayout(self.svbox)

    # Создание вкладки(преподователи), групп и кнопки \/
    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")
        self.teacher_gbox = QGroupBox("Teachers/Subjects")
        self.update_teachers_button = QPushButton("Update")

        self.tvbox = QVBoxLayout()
        self.thbox = QHBoxLayout()
        self.tvbox.addLayout(self.thbox)
        self.tvbox.addWidget(self.teacher_gbox)
        self.tvbox.addWidget(self.update_teachers_button)
        self.teacher_tab.setLayout(self.tvbox)

        self._create_teacher_table()
        self.update_teachers_button.clicked.connect(self._update_teacher_table)

    # Создание вкладки(пары), групп и кнопки \/
    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")
        self.subject_gbox = QGroupBox("Subjects")
        self.update_subject_button = QPushButton("Update")

        self.subvbox = QVBoxLayout()
        self.subhbox = QHBoxLayout()
        self.subvbox.addLayout(self.subhbox)
        self.subvbox.addWidget(self.subject_gbox)
        self.subvbox.addWidget(self.update_subject_button)
        self.subject_tab.setLayout(self.subvbox)

        self._create_subject_table()
        self.update_subject_button.clicked.connect(self._update_subject_table)

    # Создание таблицы для вкладки(преподователи) \/
    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teacher_table.setColumnCount(4)
        self.teacher_table.setHorizontalHeaderLabels(["Full_name", "Subject", "", ""])
        self._update_teacher_table()
        self.teachervbox = QVBoxLayout()
        self.teachervbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.teachervbox)

    # Создание таблицы для вкладки(пары) \/
    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(["Subjects", "", ""])
        self._update_subject_table()
        self.subjectvbox = QVBoxLayout()
        self.subjectvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.subjectvbox)

    # Создание таблиц для вкладки(расписание) \/
    def _create_shedule_table(self):
        for i in range(6):
            setattr(self, self.days[i].lower() + '_table', QTableWidget())
            self.day_table = getattr(self, self.days[i].lower() + '_table')
            self.day_gbox = getattr(self, self.days[i].lower() + '_gbox')
            self.day_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.day_table.setColumnCount(6)
            self.day_table.setHorizontalHeaderLabels(["Subject", "Time", "Teacher", "Room numb", "", ''])
            self._update_table(self.days[i])
            self.mvbox = QVBoxLayout()  # ещё одна ось для qtablewitget
            self.mvbox.addWidget(self.day_table)
            self.day_gbox.setLayout(self.mvbox)

    # Формирование таблицы с расписанием \/
    def _update_table(self, day):
        self.cursor.execute("SELECT * FROM timetable WHERE day='{day}'".format(day=day))
        records = list(self.cursor.fetchall())
        records.sort(key=lambda i: i[4])
        self.day_table = getattr(self, day.lower() + '_table')
        self.day_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            try:
                self.cursor.execute("SELECT * FROM teacher WHERE subject='{sub}'".format(sub=r[2]))
                teacher = list(self.cursor.fetchall())
                self.day_table.setItem(i, 2, QTableWidgetItem(str(teacher[0][1])))  # преподователь
            except:
                self.day_table.setItem(i, 2, QTableWidgetItem(''))

            joinButton = QPushButton("Join")
            deleteButton = QPushButton('Delete')
            self.day_table.setItem(i, 0, QTableWidgetItem(str(r[2])))  # предмет
            self.day_table.setItem(i, 1, QTableWidgetItem(str(r[4])))  # время начала
            self.day_table.setItem(i, 3, QTableWidgetItem(str(r[3])))  # номер аудитории
            self.day_table.setCellWidget(i, 4, joinButton)
            self.day_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_table(num, day, id))
            deleteButton.clicked.connect(lambda ch, id=r[0]: self._delete_from_table('...', id, day, 'shedeule'))
        addButton = QPushButton("Add")
        self.day_table.setCellWidget(len(records), 4, addButton)
        addButton.clicked.connect(lambda: self._add_to_table(records, day))
        self.day_table.resizeRowsToContents()

    # Формирование таблицы с преподователями \/
    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM teacher")
        records = self.cursor.fetchall()
        self.teacher_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton('Delete')
            self.teacher_table.setItem(i, 0, QTableWidgetItem(str(r[1])))  # full name
            self.teacher_table.setItem(i, 1, QTableWidgetItem(str(r[2])))  # subject
            self.teacher_table.setCellWidget(i, 2, joinButton)
            self.teacher_table.setCellWidget(i, 3, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_teacher_table(num, id))
            deleteButton.clicked.connect(lambda ch, id=r[0]: self._delete_from_table('...', id, '...', 'teacher'))
        add_teacher_button = QPushButton("Add")
        self.teacher_table.setCellWidget(len(records), 2, add_teacher_button)
        add_teacher_button.clicked.connect(lambda: self._add_to_teacher_table(records))
        self.teacher_table.resizeRowsToContents()

    # Формирование таблицы с парами \/
    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subject")
        records = self.cursor.fetchall()
        self.subject_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton('Delete')
            self.subject_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 1, joinButton)
            self.subject_table.setCellWidget(i, 2, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_subject_table(num, id))
            deleteButton.clicked.connect(lambda ch, id=r[0], subject=r[1]: self._delete_from_table(subject, id, '...', 'subject'))
        add_subject_button = QPushButton("Add")
        self.subject_table.setCellWidget(len(records), 1, add_subject_button)
        add_subject_button.clicked.connect(lambda: self._add_to_subject_table(records))
        self.subject_table.resizeRowsToContents()

    # Изменение отдельных строчек во вкладке расписание(кнопка join) \/
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
            self.cursor.execute("ROLLBACK")
            self.conn.commit()

    # Изменение отдельных строчек во вкладке преподователи(кнопка join) \/
    def _change_day_from_teacher_table(self, rowNum, id):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(
                "UPDATE teacher SET full_name='{full_name}', subject='{subject}' WHERE id='{id}'".format(
                    subject=row[1], full_name=row[0], id=id))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
            self.cursor.execute("ROLLBACK")
            self.conn.commit()

    #
    def _change_day_from_subject_table(self, rowNum, id):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            print(row[0], id)
            self.cursor.execute(
                "UPDATE subject SET name='{subject}' WHERE id='{id}'".format(subject=row[0], id=id))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Такой пары нет в базе данных.")
            self.cursor.execute("ROLLBACK")
            self.conn.commit()

    # Удаление отдельных строчек(кнопка delete) \/
    def _delete_from_table(self, subject, id, day, table):
        if table == 'shedeule':
            try:
                self.day_table = getattr(self, day.lower() + '_table')
                self.cursor.execute("DELETE FROM timetable WHERE id='{id}'".format(id=id))
                self.conn.commit()
                self.day_table.clear()
                self._update_table(day)
            except:
                QMessageBox.about(self, "Error", "Erorr delete")
                self.cursor.execute("ROLLBACK")
                self.conn.commit()
        elif table == 'teacher':
            try:
                self.cursor.execute("DELETE FROM teacher WHERE id='{id}'".format(id=id))
                self.conn.commit()
                self.teacher_table.clear()
                self._update_teacher_table()
            except:
                QMessageBox.about(self, "Error", "Erorr delete")
                self.cursor.execute("ROLLBACK")
                self.conn.commit()
        elif table == 'subject':
            try:
                self.cursor.execute("DELETE FROM teacher WHERE subject='{sub}'".format(sub=subject))
                self.cursor.execute("DELETE FROM timetable WHERE subject='{sub}'".format(sub=subject))
                self.cursor.execute("DELETE FROM subject WHERE name='{name}'".format(name=subject))
                # self.conn.commit()
                self.subject_table.clear()
                self._update_subject_table()
            except:
                QMessageBox.about(self, "Error", "Erorr delete")
                self.cursor.execute("ROLLBACK")
                self.conn.commit()

    # Добавление строчек во вкладке расписание(кнопка add) \/
    def _add_to_table(self, rec, day):
        try:
            self.day_table = getattr(self, day.lower() + '_table')
            subject = str(self.day_table.item(len(rec), 0).text())
            time = str(self.day_table.item(len(rec), 1).text())
            room_numb = str(self.day_table.item(len(rec),
                                                3).text())  # Здесь ошибка(если ввести предмет, время, а аудиторию и учителя оставить пустыми, то вот тут возникает ошибка)
            print(subject, time, room_numb)
            self.cursor.execute(
                "INSERT INTO timetable(day, subject, room_numb, start_time)VALUES('{day}', '{subject}', '{room_numb}', '{time}')".format(
                    subject=subject, room_numb=room_numb, time=time, day=day))
            self.conn.commit()
            self._update_table(day)
        except:
            QMessageBox.about(self, "Error", "Такого предмета не существует в базе данных")
            self.cursor.execute("ROLLBACK")
            self.conn.commit()

    # Добавление строчек во вкладке преподователи(кнопка add) \/
    def _add_to_teacher_table(self, rec):
        try:
            full_name = str(self.teacher_table.item(len(rec), 0).text())
            subject = str(self.teacher_table.item(len(rec), 1).text())
            self.cursor.execute(
                "INSERT INTO teacher(full_name, subject)VALUES('{name}', '{sub}')".format(name=full_name, sub=subject))
            self.conn.commit()
            self._update_teacher_table()
        except:
            QMessageBox.about(self, "Error", "Такого предмета не существует в базе данных")
            self.cursor.execute("ROLLBACK")
            self.conn.commit()

    def _add_to_subject_table(self, rec):
        try:
            subject = str(self.subject_table.item(len(rec), 0).text())
            self.cursor.execute("INSERT INTO subject(name)VALUES('{sub}')".format(sub=subject))
            self.conn.commit()
            self._update_subject_table()
        except:
            QMessageBox.about(self, "Error", "Error")
            self.cursor.execute("ROLLBACK")
            self.conn.commit()

    def _update_shedule(self):
        for i in self.days:
            self._update_table(i)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())