import sqlite3
import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QScrollArea, QMainWindow, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt




# --------------------მთავარი ფანჯარა ----------------------------- #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ქალაქობანა")
        self.setGeometry(100, 100, 966, 989)
        self.db_manager = DatabaseManager()
        central_widget = QWidget(self)

        background_image_path = "BEB644D2-DCB3-4CE5-9C54-233616085AFF.jpeg"

        central_widget.setStyleSheet(f"""
                    QWidget {{
                        background-image: url('{background_image_path}');
                        background-repeat: no-repeat;
                        background-position: center;
                        background-size: cover;
                    }}
                """)


        self.setStyleSheet("""
                     #Button {
                               background-color: #4CAF50;
                               color: white;
                               padding: 12px 25px;
                               border: none;
                               border-radius: 8px;
                               font-size: 15px;
                               font-weight: bold;
                               margin-top: 20px;
                           }

                """)

        self.setCentralWidget(central_widget)

        self.rules_button = QPushButton("თამაშის წესები", self)
        self.rules_button.setObjectName("Button")
        self.rules_button.setGeometry(350, 550, 300, 70)
        self.rules_button.clicked.connect(self.open_rules)

        self.cheat_button = QPushButton("შპარგალკა", self)
        self.cheat_button.setObjectName("Button")
        self.cheat_button.setGeometry(350, 450, 300, 70)
        self.cheat_button.clicked.connect(self.open_cheat)

        self.db_manage_button = QPushButton("შპარგალკის შეცვლა", self)
        self.db_manage_button.setObjectName("Button")
        self.db_manage_button.setGeometry(350, 650, 300, 70)
        self.db_manage_button.clicked.connect(self.open_db_management)

    def open_rules(self):
        self.rules_window = RulesWindow(self)
        self.rules_window.show()
        self.hide()

    def open_cheat(self):
        self.cheat_window = CheatInputWindow(self.db_manager, parent_window=self)
        self.cheat_window.show()
        self.hide()

    def open_db_management(self):
        self.db_management_window = DatabaseManagementWindow(self.db_manager, parent_window=self)
        self.db_management_window.show()
        self.hide()


# ----------------------------- წესების ფანჯარა ----------------------------- #
class RulesWindow(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("თამაშის წესები")
        self.setGeometry(100, 100, 966, 966)

        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #34495e;
            }
            QTextEdit {
                background-color: white;
                padding: 10px;
                border-radius: 12px;
                border: 1px solid #bdc3c7;
                color: black;
                font-size: 20px;
            }
            #backButton {
               background-color: #4CAF50; /* Green */
               color: white;
               padding: 12px 25px;
               border: none;
               border-radius: 8px;
               font-size: 15px;
               font-weight: bold;
               margin-top: 20px;
            }
            #backButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout(self)

        rules_text = (
            "ქალაქობანა — თამაშის წესები\n\n"
            "ქალაქობანა სიტყვების თამაშია, რომელსაც ხშირად თამაშობენ ზეპირად ან წერილობით, "
            "ორი ან რამდენიმე მოთამაშის მონაწილეობით. თამაშის მიზანია, მოთამაშემ შეძლოს რაც შეიძლება მეტი სწორი სიტყვა თქვას "
            "ან დაწეროს ერთმანეთის მიყოლებით ლოგიკურად, რომლებიც დაიწყება ერთი და იმავე თავდაპირველად მოცემულ ასო-ბგერაზე.\n\n"

            "სათამაშო საგნები (თუ წერით თამაშობთ):\n"
            "- ფურცელი და კალამი თითოეული მოთამაშისთვის\n"
            "ან\n"
            "- უბრალოდ კარგი მეხსიერება ზეპირი თამაშისთვის\n\n"

            "მოთამაშეთა რაოდენობა:\n"
            "- მინიმუმ 2 მოთამაშე\n"
            "- მაქსიმუმი — არ არის შეზღუდული\n\n"

            "დამატებითი წესები:\n"
            "- სიტყვა უნდა იყოს რეალური და ცნობადი.\n"
            "- გამოგონილი ან არარსებული ქალაქის გამოყენება თამაშში არ შეიძლება.\n\n"

            "დროის ლიმიტი:\n"
            "- როცა დაამთავრებს ამ სიტყვების ჩამოწერას ერთი მოთამაშე მაინც, თამაშის დრო იწურება.\n\n"

            "ქულების დათვლა (თუ წერით თამაშობთ):\n"
            "- თითოეული სწორი სიტყვა = 1 ქულა\n"
            "- დამატებითი ქულა შეიძლება მიენიჭოს იშვიათი ან ნაკლებად ცნობილი ქალაქისთვის\n"
        )

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("QLabel")
        self.text_edit.setText(rules_text)
        self.text_edit.setReadOnly(True)

        self.back_button = QPushButton("უკან დაბრუნება")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.go_back)

        layout.addWidget(self.text_edit)
        layout.addWidget(self.back_button)

    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

# --------------------ბაზებზე მანიპულაცია---------------------
class DatabaseManager:
    def __init__(self, db_name='All_categories_data.sqlite'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

# CRUD ოპერაციების ფუნქციონალი

    def get_word_details(self, word):
        self.cursor.execute(
            f"SELECT word, category, start_letter FROM {"categorized_words"} WHERE word = ?",
            (word,)
        )
        # დავაბრუნოთ მოძებნილი სიტყვის tuple
        return self.cursor.fetchone()

    def update_word(self, old_word, new_word, new_category, new_start_letter):
        self.cursor.execute(
            f"UPDATE {"categorized_words"} SET word = ?, category = ?, start_letter = ? WHERE word = ? ",
            (new_word, new_category, new_start_letter, old_word)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0



    def delete_word(self, word):
            self.cursor.execute(
                f"DELETE FROM {"categorized_words"} WHERE word = ?",
                (word,)
            )
            self.conn.commit()
            return self.cursor.rowcount > 0

    def add_word(self, word, category, start_letter):
        self.cursor.execute(
            f"INSERT INTO {"categorized_words"} (word, category, start_letter) VALUES (?, ?, ?)",
            (word, category, start_letter)
        )
        self.conn.commit()
        return True


# ფუნქციონალი შპარგალკისთვის

    def get_all_categorized_words(self, letter):
            self.cursor.execute(
                f"SELECT word, category FROM {"categorized_words"} WHERE start_letter = ?",
                (letter,)
            )
            results = self.cursor.fetchall()

            categorized_words = {}


            for word, category in results:
                if category not in categorized_words:
                    categorized_words[category] = []
                categorized_words[category].append(word)

            return categorized_words

# ---------------------------- შპარგალკის ინპუტის ფანჯარა --------------------------- #
class CheatInputWindow(QWidget):
    def __init__(self, db_manager, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.db_manager = db_manager
        self.cheat_result_window = None

        self.setWindowTitle("შპარგალკა - ასოს შეყვანა და შედეგები")
        self.setGeometry(150, 150, 500, 500)


        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                }
            QLabel {
                font-size: 18px;
                color: #333;
                font-weight: bold;
                padding: 5px;
                }
            QLabel.result_category_title {
                font-size: 18px;
                font-weight: bold;
                color: #0056b3;
                margin-top: 10px;
                margin-bottom: 5px;
                }
            QLineEdit {
                padding: 10px;
                font-size: 20px;
                border: 2px solid #007bff;
                border-radius: 8px;
                background-color: white;
                color: black;
                }
            #searchButton {
                font-size: 20px;
                background-color: #007bff;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                border: none;
                }
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: white;
                margin-top: 15px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #ccc;
                min-height: 20px;
                border-radius: 5px;
            }
            #backButton {
               background-color: #4CAF50;
               color: white;
               padding: 12px 25px;
               border: none;
               border-radius: 8px;
               font-size: 15px;
               font-weight: bold;
               margin-top: 20px;
            }
        """)

        main_layout = QVBoxLayout(self)

        input_section_layout = QVBoxLayout()
        input_section_layout.setAlignment(Qt.AlignTop and Qt.AlignCenter)

        self.label = QLabel("შეიყვანე ასო:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Sylfaen", 18))
        input_section_layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setMaxLength(1)
        self.input.setPlaceholderText("მაგ: ა")
        self.input.setAlignment(Qt.AlignCenter)

        input_layout = QHBoxLayout()
        input_layout.addStretch(1)
        input_layout.addWidget(self.input)
        input_layout.addStretch(1)
        input_section_layout.addLayout(input_layout)

        self.button = QPushButton("ძებნა")
        self.button.setObjectName("searchButton")
        self.button.clicked.connect(self.open_cheat_results)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.button)
        button_layout.addStretch(1)
        input_section_layout.addLayout(button_layout)

        main_layout.addLayout(input_section_layout)

        self.back_to_main_button = QPushButton("მთავარ მენიუში დაბრუნება")
        self.back_to_main_button.setObjectName("backButton")
        self.back_to_main_button.clicked.connect(self.go_back_to_main)

        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch(1)
        back_button_layout.addWidget(self.back_to_main_button)
        back_button_layout.addStretch(1)
        main_layout.addLayout(back_button_layout)

    def open_cheat_results(self):
        letter = self.input.text()

        if not letter:
            QMessageBox.warning(self, "შეცდომა", "გთხოვთ, შეიყვანოთ ასო!")
            return

        if self.cheat_result_window and self.cheat_result_window.isVisible():
            self.cheat_result_window.close()

        self.cheat_result_window = CheatResultWindow(letter, self.db_manager, parent_window=self)
        self.cheat_result_window.show()
        self.hide()

    def go_back_to_main(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()


# --------------------------- შპარგალკის შედეგის ფანჯარა --------------------------- #
class CheatResultWindow(QWidget):
    def __init__(self, letter, database, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.database = database
        self.letter = letter.upper()

        self.setWindowTitle(f"შპარგალკა: {self.letter} ასოზე")
        self.setGeometry(200, 200, 550, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                color: #333;
                line-height: 1.5;
            }
            QLabel.category_title {
                font-size: 18px;
                font-weight: bold;
                color: #0056b3;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            #backButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            #backButton:hover {
                background-color: #45a049;
            }
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #ccc;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        main_layout = QVBoxLayout(self)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

# წამოვიღოთ კატეგორიების მიხედვით სიტყვები ბაზიდან
        all_words_by_category = self.database.get_all_categorized_words(self.letter)
        desired_category_order = [
            'ქვეყანა',
            'ქალაქი',
            'სოფელი',
            'სახელი',
            'გვარი',
            'ცხოველი',
            'მცენარე'
        ]

        # ვამზადებ ლექსიკონს თითოეულ ასო-ბგერაზე მოსულ სიტყვებზე კატეგორიების მიხედვით
        random_words_by_category = {}
        for category in desired_category_order:
            if category in all_words_by_category and all_words_by_category[category]:
                # ლისტიდან ერთ რენდომ სიტყვას ვირჩევთ
                random_words_by_category[category] = random.choice(all_words_by_category[category])
            else:
                random_words_by_category[category] = None


        for category in desired_category_order:
            word = random_words_by_category.get(category)

            category_label = QLabel(f"{category}:")
            category_label.setObjectName("QLabel.category_title")
            category_label.setFont(QFont("Sylfaen", 18, QFont.Bold))
            content_layout.addWidget(category_label)

            words_text = word if word else '—'  # თუ ამ ასოზე კატეგორიაში სიტყვა მოიძებნა გადმოსცემს ამ ცვლადს,თუ არ იძებნება "-"-ს ამოაგდებს

            words_label = QLabel(words_text)
            words_label.setFont(QFont("Sylfaen", 14))
            content_layout.addWidget(words_label)

            content_layout.addSpacing(15)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget) #ადგენს, თუ რომელი ვიჯეტი იქნება QScrollArea-ს შიგნით.
        main_layout.addWidget(scroll_area)

        self.back_button = QPushButton("უკან დაბრუნება")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.go_back)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.back_button)
        button_layout.addStretch(1)

        main_layout.addLayout(button_layout)

    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()


# ---------------------- შპარგალკის შეცვლის ფანჯარა ---------------------- #
class DatabaseManagementWindow(QWidget):
    def __init__(self, db_manager, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.db_manager = db_manager

        self.setWindowTitle("შპარგალკის შეცვლა")
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                }
            QLabel {
                font-size: 18px;
                color: #333;
                padding: 5px;
                }
            QLabel.result_category_title {
                font-size: 18px;
                font-weight: bold;
                color: #0056b3;
                margin-top: 10px;
                margin-bottom: 5px;
                }
            QLineEdit {
                padding: 10px;
                font-size: 20px;
                border: 2px solid #007bff;
                border-radius: 8px;
                background-color: white;
                color: black;
                }
            #searchButton {
                font-size: 20px;
                background-color: #007bff;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                border: none;
            }
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: white;
                margin-top: 15px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #ccc;
                min-height: 20px;
                border-radius: 5px;
            }
            #deleteButton {
                       background-color: #FF6961;
                       color: white;
                       padding: 12px 25px;
                       border: none;
                       border-radius: 8px;
                       font-size: 15px;
                       font-weight: bold;
                       margin-top: 20px;
            }
            #updateButton {
                       background-color: #FFC067;
                       color: white;
                       padding: 12px 25px;
                       border: none;
                       border-radius: 8px;
                       font-size: 15px;
                       font-weight: bold;
                       margin-top: 20px;
            }
            #backButton {
                       background-color: #4CAF50;
                       color: white;
                       padding: 12px 25px;
                       border: none;
                       border-radius: 8px;
                       font-size: 15px;
                       font-weight: bold;
                       margin-top: 20px;
            }
        """)
        main_layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("სიტყვის შეყვანა (მაგ: თბილისი)")
        self.search_button = QPushButton("მოძიება")
        self.search_button.setObjectName("searchButton")
        self.search_button.clicked.connect(self.search_word)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)

        self.result_label = QLabel("მოძიებული სიტყვის დეტალები:")
        main_layout.addWidget(self.result_label)

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("სიტყვა")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("კატეგორია (მაგ: ქალაქი)")
        self.start_letter_input = QLineEdit()
        self.start_letter_input.setPlaceholderText("დამწყები ასო (მაგ: თ)")

        main_layout.addWidget(self.word_input)
        main_layout.addWidget(self.category_input)
        main_layout.addWidget(self.start_letter_input)

        action_layout = QHBoxLayout()

        self.update_button = QPushButton("განახლება")
        self.update_button.setObjectName("updateButton")
        self.update_button.clicked.connect(self.update_word_entry)

        self.delete_button = QPushButton("წაშლა")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_word_entry)

        action_layout.addWidget(self.update_button)
        action_layout.addWidget(self.delete_button)
        main_layout.addLayout(action_layout)

        self.back_button = QPushButton("უკან დაბრუნება")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.go_back)
        main_layout.addWidget(self.back_button)

        self.current_word_to_manage = None
        self.reset_ui() # Reset UI state initially

    def set_fields_enabled(self, enabled):
        self.word_input.setEnabled(enabled)
        self.category_input.setEnabled(enabled)
        self.start_letter_input.setEnabled(enabled)
        self.update_button.setEnabled(enabled)

    def search_word(self):
        word = self.search_input.text()
        if not word:
            QMessageBox.warning(self, "შეცდომა", "გთხოვთ, შეიყვანოთ სიტყვა.")
            return

        details = self.db_manager.get_word_details(word)

        if details:
            self.current_word_to_manage = details[0]
            self.word_input.setText(details[0])
            self.category_input.setText(details[1])
            self.start_letter_input.setText(details[2])
            self.result_label.setText(f"{details[0]} მოიძებნა!")
            self.set_fields_enabled(True)
            self.update_button.setText("განახლება")
            self.delete_button.setEnabled(True)
        else:
            self.current_word_to_manage = None
            self.result_label.setText(f"სიტყვა '{word}' ვერ მოიძებნა. შეგიძლიათ დაამატოთ.")
            self.word_input.setText(word) # Pre-fill the word field
            self.category_input.clear()
            self.start_letter_input.clear()
            self.set_fields_enabled(True) # Enable fields for new input
            self.update_button.setText("დამატება") # Change button text
            self.delete_button.setEnabled(False) # Cannot delete a non-existent word


    def update_word_entry(self):
        is_update_mode = self.current_word_to_manage is not None

        new_word = self.word_input.text()
        new_category = self.category_input.text()
        new_start_letter = self.start_letter_input.text()

        if not new_word or not new_category or not new_start_letter:
            QMessageBox.warning(self, "შეცდომა", "ყველა ველი უნდა იყოს შევსებული.")
            return

        if len(new_start_letter) != 1:
            QMessageBox.warning(self, "შეცდომა", "დამწყები ასო უნდა იყოს ერთი სიმბოლო.")
            return

        success = False
        operation_name = ""

        if is_update_mode:
            old_word = self.current_word_to_manage
            success = self.db_manager.update_word(old_word, new_word, new_category, new_start_letter)
            operation_name = "განახლება"
        else:
            success = self.db_manager.add_word(new_word, new_category, new_start_letter)
            operation_name = "დამატება"

        if success:
            QMessageBox.information(self, "წარმატება", f"სიტყვა წარმატებით დაემატა!")
            self.reset_ui()
            self.search_input.clear()
        else:
            QMessageBox.critical(self, "შეცდომა", f"{operation_name} ვერ მოხერხდა.")

    def delete_word_entry(self):
        if not self.current_word_to_manage:
            QMessageBox.warning(self, "შეცდომა", "სიტყვა არ არის არჩეული წასაშლელად.")
            return

        word_to_delete = self.current_word_to_manage

        reply = QMessageBox.question(self, 'დადასტურება',
                                     f"დარწმუნებული ხართ, რომ გსურთ '{word_to_delete}' წაშლა?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            success = self.db_manager.delete_word(word_to_delete)

            if success:
                QMessageBox.information(self, "წარმატება", f"სიტყვა '{word_to_delete}' წარმატებით წაიშალა.")
                self.reset_ui()
            else:
                QMessageBox.critical(self, "შეცდომა", "წაშლა ვერ მოხერხდა.")

    def reset_ui(self):
        self.search_input.clear()
        self.word_input.clear()
        self.category_input.clear()
        self.start_letter_input.clear()
        self.current_word_to_manage = None
        self.set_fields_enabled(False)
        self.result_label.setText("მოძიებული სიტყვის დეტალები:")
        self.update_button.setText("განახლება")
        self.delete_button.setEnabled(False)


    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()


# ----------------------------- აპლიკაციის გაშვება ----------------------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
