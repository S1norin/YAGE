import io, sys, sqlite3
from PyQt5 import uic
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QCheckBox, QLabel, QMessageBox

template_test_window = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>402</width>
    <height>271</height>
   </rect>
  </property>
  <property name="sizePolicy">
   <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
    <horstretch>0</horstretch>
    <verstretch>0</verstretch>
   </sizepolicy>
  </property>
  <property name="minimumSize">
   <size>
    <width>402</width>
    <height>271</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>402</width>
    <height>271</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QSplitter" name="splitter">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>30</y>
      <width>321</width>
      <height>131</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Vertical</enum>
    </property>
    <widget class="QLabel" name="words_1">
     <property name="text">
      <string>Words words 1</string>
     </property>
    </widget>
    <widget class="QLabel" name="words_2">
     <property name="text">
      <string>Words words 2</string>
     </property>
    </widget>
    <widget class="QLabel" name="words_3">
     <property name="text">
      <string>Words words 3</string>
     </property>
    </widget>
    <widget class="QLabel" name="words_4">
     <property name="text">
      <string>Words words 4</string>
     </property>
    </widget>
    <widget class="QLabel" name="words_5">
     <property name="text">
      <string>Words words 5</string>
     </property>
    </widget>
   </widget>
   <widget class="QSplitter" name="splitter_2">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>170</y>
      <width>351</width>
      <height>16</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Horizontal</enum>
    </property>
    <widget class="QCheckBox" name="check_1">
     <property name="text">
      <string>Первое</string>
     </property>
    </widget>
    <widget class="QCheckBox" name="check_2">
     <property name="text">
      <string>Второе</string>
     </property>
    </widget>
    <widget class="QCheckBox" name="check_3">
     <property name="text">
      <string>Третье</string>
     </property>
    </widget>
    <widget class="QCheckBox" name="check_4">
     <property name="text">
      <string>Четвёртое</string>
     </property>
    </widget>
    <widget class="QCheckBox" name="check_5">
     <property name="text">
      <string>Пятое</string>
     </property>
    </widget>
   </widget>
   <widget class="QSplitter" name="splitter_3">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>210</y>
      <width>341</width>
      <height>21</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Horizontal</enum>
    </property>
    <widget class="QPushButton" name="Finish">
     <property name="minimumSize">
      <size>
       <width>112</width>
       <height>21</height>
      </size>
     </property>
     <property name="maximumSize">
      <size>
       <width>112</width>
       <height>21</height>
      </size>
     </property>
     <property name="text">
      <string>Я закончил</string>
     </property>
    </widget>
    <widget class="QPushButton" name="prevButton">
     <property name="text">
      <string>Предыдущее</string>
     </property>
    </widget>
    <widget class="QPushButton" name="nextButton">
     <property name="text">
      <string>Следующее</string>
     </property>
    </widget>
   </widget>
   <widget class="QLabel" name="taskText">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>341</width>
      <height>20</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>7</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Выберите строку (строки), в которых все пропущенные буквы одинаковые</string>
    </property>
   </widget>
   <widget class="QLabel" name="choiceNumber">
    <property name="geometry">
     <rect>
      <x>350</x>
      <y>10</y>
      <width>35</width>
      <height>20</height>
     </rect>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>402</width>
     <height>18</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>


"""


class TestField(QMainWindow):
    def __init__(self, tasks, correct_answers):
        super().__init__()
        f = io.StringIO(template_test_window)
        uic.loadUi(f, self)
        self.choice = 0
        self.tasks = tasks
        self.answers = [[] for _ in range(len(self.tasks))]
        self.correct_answers = correct_answers
        self.nextButton.clicked.connect(self.choice_up)
        self.prevButton.clicked.connect(self.choice_down)
        self.Finish.clicked.connect(self.finish)
        self.check_numbers = {self.check_1: 1,
                              self.check_2: 2,
                              self.check_3: 3,
                              self.check_4: 4,
                              self.check_5: 5
                              }
        self.numbers_check = {1: self.check_1,
                              2: self.check_2,
                              3: self.check_3,
                              4: self.check_4,
                              5: self.check_5
                              }
        for i in range(1, 6):
            exec(f"self.check_{i}.clicked.connect(self.change_answer)")
        self.update_screen()

    # Кнопка "я закончил" заканчивает
    def finish(self):
        now = datetime.now()
        now = now.strftime("%d-%m-%Y %H-%M-%S")
        with open(f"Test Result - {now}.txt", "w", encoding="utf-8") as file:
            for index, tasks in enumerate(self.tasks):
                print(f"№{index + 1}", file=file)
                for task in tasks[1:]:
                    for row_number, row in enumerate(task):
                        to_write = ", ".join([value[1].replace("..", value[2]) for value in row])
                        print(f"{row_number + 1}) {to_write}", file=file)
                if set(self.correct_answers[index]) == set(self.answers[index]):
                    print(f"\t-Верно, выбранные ответы - {self.answers[index]}", file=file)
                else:
                    print(
                        f"\t-Неверно, выбранные ответы - {self.answers[index]}, правильные - {self.correct_answers[index]}",
                        file=file)
                print("\n", file=file)
        msgBox = QMessageBox()
        msgBox.setText(f"Результат в файле 'Test Result - {now}.txt'")
        msgBox.exec()
        self.hide()

    # Обновление списка выбранных ответов
    def change_answer(self):
        if self.sender().checkState():
            self.answers[self.choice].append(self.check_numbers[self.sender()])
            self.answers[self.choice].sort()
        else:
            self.answers[self.choice].remove(self.check_numbers[self.sender()])

    # Функции, отвечающие за смену задания в окне
    def choice_up(self):
        if self.choice + 1 < len(self.tasks):
            self.choice += 1
        self.update_screen()

    def choice_down(self):
        if self.choice - 1 > -1:
            self.choice -= 1
        self.update_screen()

    # Обновления экрана с заданиями
    def update_screen(self):
        to_add = []
        try:
            self.current_task = self.tasks[self.choice]
            self.choiceNumber.setText(f"№ {self.choice + 1}")  # Установка номера задания сверху
            # Переключаем при перелистывании все ответы на невыбранные
            for reset_to_false in self.check_numbers:
                reset_to_false.setChecked(False)
            # Переключаем при перелистывании до этого выбранные ответы на выбранные
            for load_answers in self.answers[self.choice]:
                self.numbers_check[load_answers].setChecked(True)
            # Загрузка текста заданий
            for number, entire_task in enumerate(self.current_task[1:6]):
                for row in entire_task:
                    to_add.append((", ".join([entry[1] for entry in row])))
                for i in range(5):
                    exec(f"self.words_{i + 1}.setText(str({i + 1}) +') ' + to_add[{i}])")
        except IndexError:
            msg = QMessageBox()
            msg.setText("Нельзя созадть ноль заданий")
            msg.exec()
            quit()


