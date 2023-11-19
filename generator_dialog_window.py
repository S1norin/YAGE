import io, sys, sqlite3
from PyQt5 import uic
import random
from config import DB_FILENAME
from test_field import TestField
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QCheckBox

template_dialog_generator = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>150</width>
    <height>158</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>150</width>
    <height>158</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>150</width>
    <height>158</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QWidget" name="">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>20</y>
     <width>122</width>
     <height>127</height>
    </rect>
   </property>
   <layout class="QGridLayout" name="gridLayout_2">
    <item row="0" column="0">
     <widget class="QLabel" name="label">
      <property name="text">
       <string>Выберите задания</string>
      </property>
     </widget>
    </item>
    <item row="1" column="0">
     <layout class="QGridLayout" name="gridLayout">
      <item row="2" column="0">
       <widget class="QCheckBox" name="check11">
        <property name="text">
         <string>11-е</string>
        </property>
       </widget>
      </item>
      <item row="3" column="0">
       <widget class="QCheckBox" name="check12">
        <property name="text">
         <string>12-е</string>
        </property>
       </widget>
      </item>
      <item row="1" column="0">
       <widget class="QCheckBox" name="check10">
        <property name="text">
         <string>10-е</string>
        </property>
       </widget>
      </item>
      <item row="1" column="1">
       <widget class="QSpinBox" name="spinBox10"/>
      </item>
      <item row="0" column="1">
       <widget class="QSpinBox" name="spinBox9"/>
      </item>
      <item row="3" column="1">
       <widget class="QSpinBox" name="spinBox12"/>
      </item>
      <item row="2" column="1">
       <widget class="QSpinBox" name="spinBox11"/>
      </item>
      <item row="0" column="0">
       <widget class="QCheckBox" name="check9">
        <property name="text">
         <string>9-е</string>
        </property>
       </widget>
      </item>
     </layout>
    </item>
    <item row="2" column="0">
     <widget class="QSplitter" name="splitter">
      <property name="orientation">
       <enum>Qt::Horizontal</enum>
      </property>
      <widget class="QPushButton" name="generateButton">
       <property name="text">
        <string>Сгенерировать</string>
       </property>
      </widget>
      <widget class="QPushButton" name="cancelButton">
       <property name="text">
        <string>Да ну его</string>
       </property>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

"""


class GeneratorDialogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template_dialog_generator)
        uic.loadUi(f, self)
        self.check_numbers = {self.check9: 9,
                              self.check10: 10,
                              self.check11: 11,
                              self.check12: 12,
                              }
        for i in range(9, 13):
            exec(f"self.check{i}.stateChanged.connect(self.enable_task)")
            exec(f"self.spinBox{i}.setEnabled(False)")

        self.generateButton.clicked.connect(self.generate)
        self.cancelButton.clicked.connect(self.cancel)

    def enable_task(self):
        if self.sender().checkState():
            exec(f"self.spinBox{self.check_numbers[self.sender()]}.setEnabled(True)")
        else:
            exec(f"self.spinBox{self.check_numbers[self.sender()]}.setEnabled(False)")

    def cancel(self):
        self.hide()

    def generate(self):
        self.quantity = []
        checks = [self.check9, self.check10, self.check11, self.check12]
        spins = [self.spinBox9, self.spinBox10, self.spinBox11, self.spinBox12]
        self.all_tasks = []
        for i in range(4):
            if checks[i].isEnabled():
                self.quantity.append(spins[i].value())
            else:
                self.quantity.append(0)
        if self.quantity == [0, 0, 0, 0]:
            self.cancel()
        else:
            for number, quantity_of_tasks in enumerate(self.quantity):
                # Вытаскиваем допустимые для текущего задания буквы
                current_task = number + 9
                connection = sqlite3.connect(DB_FILENAME)
                cursor = connection.cursor()
                available_letters = cursor.execute("""SELECT DISTINCT missed_letter FROM words WHERE task = ?""",
                                                   (current_task,)).fetchall()
                connection.close()
                # Генерируем непосредственно задания
                for task in range(quantity_of_tasks):
                    # Определяем колличество правильных ответов и список, в который будут заносится слова для каждого из заданий
                    all_task_list = []
                    quantity_of_correct_answers = random.randint(1, 4)
                    quantity_of_wrong_answers = 5 - quantity_of_correct_answers

                    # Генерим строки с правильными ответами
                    for i in range(quantity_of_correct_answers):
                        current_letter = random.choice(available_letters)

                        while True:
                            connection = sqlite3.connect(DB_FILENAME)
                            cursor = connection.cursor()
                            result = cursor.execute(
                                """SELECT id, word, missed_letter FROM words WHERE task = ? AND missed_letter = ?""",
                                (current_task, *current_letter)).fetchall()
                            connection.close()
                            # Обработка, на случай если трёх слов с такой буквой не найдётся
                            try:
                                current_correct_task = random.sample(result, 3)
                                break
                            except ValueError:
                                current_letter = random.choice(available_letters)

                        all_task_list.append(current_correct_task)

                    # Генерим строки с неправильным ответом
                    for i in range(quantity_of_wrong_answers):
                        # Вытаскиваем три буквы до тех пор, пока все из них не будут разными
                        while True:
                            current_letter = [i[0] for i in list(random.choices(available_letters, k=3))]
                            if current_letter[0] != current_letter[1] != current_letter[2]:
                                break
                        # Вытаскиваем слова до тех пор, пока мы не сможем вытащить оттуда три случайных слова
                        while True:
                            connection = sqlite3.connect(DB_FILENAME)
                            cursor = connection.cursor()
                            result = cursor.execute(
                                f"""SELECT id, word, missed_letter FROM words WHERE missed_letter IN {tuple(current_letter)}""").fetchall()
                            connection.close()
                            try:
                                current_wrong_task = random.sample(result, 3)
                                if current_wrong_task[0][2] == current_wrong_task[1][2] == current_wrong_task[2][2]:
                                    pass
                                else:
                                    break
                            except ValueError:
                                current_letter = random.choice(available_letters)
                        all_task_list.append(current_wrong_task)
                    # Перемешиваем порядок строк для задания
                    random.shuffle(all_task_list)
                    # Первое значение - задание, к которому относятся строки, второе - непосредсвенно сами строки
                    self.all_tasks.append([current_task, all_task_list])

        self.correct_answers = [[] for _ in range(len(self.all_tasks))]
        for number_of_task, entire_task in enumerate(self.all_tasks):
            for rows in entire_task[1:]:
                for number_of_row, row in enumerate(rows):
                    if row[0][2] == row[1][2] == row[2][2]:
                        self.correct_answers[number_of_task].append(number_of_row + 1)
        self.test = TestField(self.all_tasks, self.correct_answers)
        self.test.show()
        self.hide()
