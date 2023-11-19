import io, sys, sqlite3
from generator_dialog_window import GeneratorDialogWindow
from config import TASK_NUMBERS, null_fill
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QLineEdit, QMessageBox, QAction, \
    QCheckBox

template_main_window = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>243</width>
    <height>278</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>243</width>
    <height>278</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>243</width>
    <height>278</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>YAGE</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLineEdit" name="searchField">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>241</width>
      <height>20</height>
     </rect>
    </property>
   </widget>
   <widget class="QSplitter" name="splitter_2">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>0</width>
      <height>0</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Vertical</enum>
    </property>
   </widget>
   <widget class="QSplitter" name="splitter_3">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>0</width>
      <height>0</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Vertical</enum>
    </property>
   </widget>
   <widget class="QWidget" name="layoutWidget">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>2</width>
      <height>2</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout"/>
   </widget>
   <widget class="QSplitter" name="splitter">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>20</y>
      <width>241</width>
      <height>221</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Vertical</enum>
    </property>
    <widget class="QTabWidget" name="tabWidget">
     <property name="currentIndex">
      <number>0</number>
     </property>
     <widget class="QWidget" name="wordTab">
      <attribute name="title">
       <string>Слова</string>
      </attribute>
      <widget class="QListWidget" name="wordList">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>241</width>
         <height>211</height>
        </rect>
       </property>
      </widget>
     </widget>
     <widget class="QWidget" name="mistakeTab">
      <attribute name="title">
       <string>Ошибки</string>
      </attribute>
      <widget class="QListWidget" name="mistakeList">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>241</width>
         <height>201</height>
        </rect>
       </property>
      </widget>
     </widget>
    </widget>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>243</width>
     <height>18</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuRun_generator">
    <property name="title">
     <string>Run generator</string>
    </property>
   </widget>
   <widget class="QMenu" name="menuAdd">
    <property name="title">
     <string>Add</string>
    </property>
    <addaction name="actionAdd_words"/>
    <addaction name="actionMistake_type"/>
   </widget>
   <addaction name="menuRun_generator"/>
   <addaction name="menuAdd"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <action name="actionAdd_words">
   <property name="text">
    <string>Add word</string>
   </property>
  </action>
  <action name="actionMistake_type">
   <property name="text">
    <string>Mistake type</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>

"""
template_word_window = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>250</width>
    <height>160</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>250</width>
    <height>130</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>250</width>
    <height>160</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QLabel" name="wordLabel">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>7</y>
     <width>241</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Слово с двумя точками вместо пропущенной буквы</string>
   </property>
  </widget>
  <widget class="QLabel" name="letterLabel">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>43</y>
     <width>191</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Пропущенная буква</string>
   </property>
  </widget>
  <widget class="QLabel" name="ruleLabel">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>79</y>
     <width>191</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Правило</string>
   </property>
  </widget>
  <widget class="QComboBox" name="ruleBox">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>92</y>
     <width>231</width>
     <height>16</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="wordEdit">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>20</y>
     <width>231</width>
     <height>16</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="letterEdit">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>56</y>
     <width>97</width>
     <height>16</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="warning">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>110</y>
     <width>221</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Заполните правильно первое и второе поле</string>
   </property>
  </widget>
  <widget class="QSplitter" name="splitter">
   <property name="geometry">
    <rect>
     <x>70</x>
     <y>130</y>
     <width>171</width>
     <height>20</height>
    </rect>
   </property>
   <property name="orientation">
    <enum>Qt::Horizontal</enum>
   </property>
   <widget class="QPushButton" name="saveButton">
    <property name="text">
     <string>Спасти и сохранить</string>
    </property>
   </widget>
   <widget class="QPushButton" name="cancelButton">
    <property name="text">
     <string>Отмена</string>
    </property>
   </widget>
  </widget>
  <widget class="QComboBox" name="taskBox">
   <property name="geometry">
    <rect>
     <x>120</x>
     <y>56</y>
     <width>121</width>
     <height>16</height>
    </rect>
   </property>
   <property name="minimumContentsLength">
    <number>0</number>
   </property>
  </widget>
  <widget class="QLabel" name="taskLabel">
   <property name="geometry">
    <rect>
     <x>122</x>
     <y>43</y>
     <width>121</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Задание</string>
   </property>
  </widget>
  <widget class="QPushButton" name="deleteButton">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>130</y>
     <width>56</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Удалить</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

"""

template_mistake_window = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>250</width>
    <height>90</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>250</width>
    <height>90</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>250</width>
    <height>160</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QLabel" name="mistakeLabel">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>7</y>
     <width>241</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Название ошибки</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="mistakeEdit">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>20</y>
     <width>231</width>
     <height>16</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="warning">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>38</y>
     <width>221</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Такая ошибка уже существует</string>
   </property>
  </widget>
  <widget class="QSplitter" name="splitter">
   <property name="geometry">
    <rect>
     <x>67</x>
     <y>58</y>
     <width>171</width>
     <height>20</height>
    </rect>
   </property>
   <property name="orientation">
    <enum>Qt::Horizontal</enum>
   </property>
   <widget class="QPushButton" name="saveButton">
    <property name="text">
     <string>Спасти и сохранить</string>
    </property>
   </widget>
   <widget class="QPushButton" name="cancelButton">
    <property name="text">
     <string>Отмена</string>
    </property>
   </widget>
  </widget>
  <widget class="QPushButton" name="deleteButton">
   <property name="geometry">
    <rect>
     <x>7</x>
     <y>58</y>
     <width>56</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Удалить</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
DB_FILENAME = "words_db.sqlite"


class EditMistakeWindow(QMainWindow):
    def __init__(self):
        # Инициализация интерфейса
        super().__init__()
        f = io.StringIO(template_mistake_window)
        uic.loadUi(f, self)
        self.warning.hide()  # Скрываем строчку, сообщающую об ошибке при сохранении
        self.deleteButton.clicked.connect(self.delete)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.cancel)

    def delete(self):
        connection = sqlite3.connect(DB_FILENAME)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM mistakes WHERE title = ?", (ex.mistake_title,))
        connection.commit()
        connection.close()
        ex.update_mistakeList()
        self.hide()

    def cancel(self):
        self.hide()

    def save(self):
        current_mistake_title = self.mistakeEdit.text()
        connection = sqlite3.connect(DB_FILENAME)
        cursor = connection.cursor()
        try:
            if ex.mistake_title != "":
                cursor.execute("UPDATE mistakes SET title = ? WHERE title = ?",
                               (current_mistake_title, ex.mistake_title))
            else:
                cursor.execute("INSERT INTO mistakes(title) VALUES(?)", (current_mistake_title,))
            connection.commit()
            connection.close()
        except sqlite3.IntegrityError:
            warning = QMessageBox()
            warning.setText("Такая ошибка уже существует")
            warning.exec()
        ex.update_mistakeList()
        self.hide()


class EditWordWindow(QMainWindow):
    def __init__(self):
        # Инициализация интерфейса
        super().__init__()
        f = io.StringIO(template_word_window)
        uic.loadUi(f, self)
        self.deleteButton.clicked.connect(self.delete)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.cancel)
        self.warning.hide()  # Скрываем строчку, сообщающую об ошибке при сохранении

        # Чтение всех правил
        connection = sqlite3.connect("words_db.sqlite")
        cursor = connection.cursor()
        rule = cursor.execute("SELECT title FROM rules").fetchall()
        connection.close()

        # Занесение правил в combobox
        self.ruleBox.addItem("")
        for i in rule:
            self.ruleBox.addItem(*i)

        # Занесение заданий в combobox
        self.taskBox.addItems(TASK_NUMBERS)

    def save(self):
        word_text, missed_letter, rule, task = self.wordEdit.text(), self.letterEdit.text(), self.ruleBox.currentIndex(), self.taskBox.currentIndex() + 8
        if ".." in word_text and len(
                word_text) >= 2 and missed_letter != "" and ex.old_word_text != "" and ex.old_missed_letter != "" and ex.old_missed_letter != "":

            connection = sqlite3.connect(DB_FILENAME)
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE words SET word = ?, missed_letter = ?, rule = ?, task = ? WHERE id = (SELECT id FROM words WHERE word = ? AND missed_letter = ? AND (rule = ? OR rule is NULL))""",
                (word_text, missed_letter, null_fill(rule), null_fill(task), ex.old_word_text, ex.old_missed_letter,
                 null_fill(ex.old_rule)))

            connection.commit()
            connection.close()
            self.warning.hide()
            ex.update_wordList()
            self.hide()
        elif ex.old_word_text == "" and ex.old_missed_letter == "" and ex.old_missed_letter == "" and \
                ".." in word_text and len(word_text) >= 2 and missed_letter != "":
            connection = sqlite3.connect(DB_FILENAME)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO words(word, missed_letter, rule, task) VALUES(?, ?, ?, ?)",
                           (word_text, missed_letter, null_fill(rule), null_fill(task)))
            connection.commit()
            connection.close()

            self.warning.hide()
            ex.update_wordList()
            self.hide()
        else:
            self.warning.show()

    def cancel(self):
        self.hide()

    def delete(self):
        word_text, missed_letter, rule, task = self.wordEdit.text(), self.letterEdit.text(), self.ruleBox.currentIndex(), self.taskBox.currentIndex() + 8
        connection = sqlite3.connect(DB_FILENAME)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM words WHERE word = ? AND missed_letter = ? AND rule = ? AND task = ?",
                       (word_text, missed_letter, null_fill(rule), null_fill(task)))
        connection.commit()
        connection.close()
        self.hide()
        ex.update_wordList()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template_main_window)
        uic.loadUi(f, self)
        # Обновление боковых панелий
        self.update_wordList()
        self.update_mistakeList()
        # Соединение виджетов с функциями
        self.searchField.textChanged.connect(self.update_wordList)
        self.searchField.textChanged.connect(self.update_mistakeList)
        self.wordList.itemDoubleClicked.connect(self.edit_word_entry)
        self.mistakeList.itemDoubleClicked.connect(self.edit_mistake_entry)
        self.actionAdd_words.triggered.connect(self.edit_word_entry)
        self.actionMistake_type.triggered.connect(self.edit_mistake_entry)
        self.menuRun_generator.aboutToShow.connect(self.run_generator)

    # Взаимодействия с ошибками
    def update_mistakeList(self):  # Обновление бокового списка со словами
        self.mistakeList.clear()
        connection = sqlite3.connect(DB_FILENAME)
        cursor = connection.cursor()
        if isinstance(self.sender(), QLineEdit):
            results = cursor.execute(
                f"SELECT title FROM mistakes WHERE title LIKE '%{self.sender().text()}%'").fetchall()
        else:
            results = cursor.execute("SELECT title FROM mistakes").fetchall()
        for i in results:
            self.mistakeList.addItem(*i)
        connection.close()

    def edit_mistake_entry(self, entry_text):
        self.addMistake = EditMistakeWindow()
        self.addMistake.show()

        if isinstance(self.sender(), QListWidget):
            self.mistake_title = entry_text.text()
        else:
            self.addMistake.deleteButton.hide()
            self.mistake_title = ""
        self.addMistake.mistakeEdit.setText(self.mistake_title)

    # Взаимодействия со словами
    def update_wordList(self):  # Обновление бокового списка со словами
        self.wordList.clear()
        connection = sqlite3.connect(DB_FILENAME)
        cursor = connection.cursor()
        if isinstance(self.sender(), QLineEdit):
            results = cursor.execute(
                f"SELECT word, task, missed_letter FROM words WHERE word IS NOT NULL AND word LIKE '%{self.sender().text().lower()}%'").fetchall()
        else:
            results = cursor.execute("SELECT word, task, missed_letter FROM words WHERE word IS NOT NULL").fetchall()
        results.sort(key=lambda x: (x[1], x[0]))
        for i in results:
            if i[1] == 8:
                task_output = "Не определено"
            else:
                task_output = i[1]
            self.wordList.addItem(f"{task_output} - {i[0]} - [{i[2]}]")
        connection.close()

    def edit_word_entry(self, entry_text):
        # Инициализация окна изменения слова
        self.addWindow = EditWordWindow()
        self.addWindow.show()

        if isinstance(self.sender(), QListWidget):
            # Определение значений выбранной ячейки
            task_number, word, missed_letter = entry_text.text().split(" - ")
            if task_number == "Не определено": task_number = "8"
            missed_letter = missed_letter[1:-1]
            # Чтение правила из БД
            connection = sqlite3.connect(DB_FILENAME)
            cursor = connection.cursor()
            rule = cursor.execute(
                "SELECT id FROM rules WHERE id = (SELECT rule FROM words WHERE word = ? AND task = ? AND missed_letter = ?)",
                (word, task_number, missed_letter)).fetchone()
            connection.close()
            # Установка комбобокса на нужное правило
            if rule is not None:
                self.addWindow.ruleBox.setCurrentIndex(int(*list(rule)))
            else:
                self.addWindow.ruleBox.setCurrentText("")
            # Подстановка значений в поля
            self.addWindow.wordEdit.setText(word)
            self.addWindow.letterEdit.setText(missed_letter)
            self.addWindow.taskBox.setCurrentText(task_number)
            self.old_word_text, self.old_missed_letter, self.old_rule = self.addWindow.wordEdit.text(), self.addWindow.letterEdit.text(), self.addWindow.ruleBox.currentIndex()
        else:
            self.addWindow.deleteButton.hide()
            task_number, word, missed_letter, self.old_word_text, self.old_missed_letter, self.old_rule = "", "", "", "", "", ""

    def run_generator(self):
        self.generatorDialog = GeneratorDialogWindow()
        self.generatorDialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
