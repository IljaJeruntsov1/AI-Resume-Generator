from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QLabel, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap
from openai import OpenAI
from pdf_generator import draw_resume, parse_resume
from config import output_pdf_path

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Profile Generator")
        self.resize(800, 850)
        self.setStyleSheet("background-color: rgb(61, 61, 61);")
        self.image_path = None
        self.parsed_resume = ""
        self.output_pdf_path = output_pdf_path

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        font = QtGui.QFont("Constantia", 10, QtGui.QFont.Bold)

        self.labels = {}
        self.text_edits = {}

        # Упрощённые поля с необходимыми
        fields = {
            "First Name*": (150, 20),
            "Last Name*": (150, 80),
            "Job Title*": (350, 20),
            "Email*": (350, 80),
            "Phone*": (550, 20),
            "Address*": (550, 80),
            "Profile* (1 sentence or 5-6 adjectives.)": (20, 200),
            "Employment History (Name, Dates, Few words; ...)": (20, 280),
            "Education (Name, Dates, Few words; ...)": (20, 360),
            "Internships (Name, Dates, Few words; ...)": (20, 440),
            "Skills (Skill, Range 1-5; ...)": (400, 200),
            "Languages (Language, Range 1-5 or A1-C2; ...)": (400, 280),
            "Courses (Name, Dates; ...)": (400, 360),
            "Hobbies (1-3 your hobbies)": (400, 440)
        }

        # Отдельный словарь размеров
        field_sizes = {
            # Обычные поля
            "default": (170, 30),
            # Многострочные поля
            "Profile* (1 sentence or 5-6 adjectives.)": (350, 50),
            "Employment History (Name, Dates, Few words; ...)": (350, 50),
            "Education (Name, Dates, Few words; ...)": (350, 50),
            "Internships (Name, Dates, Few words; ...)": (350, 50),
            "Courses (Name, Dates; ...)": (350, 50),
            "Skills (Skill, Range 1-5; ...)": (350, 50),
            "Languages (Language, Range 1-5 or A1-C2; ...)": (350, 50),
            "Hobbies (1-3 your hobbies)": (350, 50),
        }

        # Создание label'ов
        for name, (x, y) in fields.items():
            self.create_label(name, x, y, font)

        # Создание QTextEdit'ов с размерами из словаря
        for name, (x, y) in fields.items():
            width, height = field_sizes.get(name, field_sizes["default"])
            edit = QTextEdit(self.centralwidget)
            edit.setGeometry(x, y + 20, width, height)
            edit.setStyleSheet("color: white;")
            self.text_edits[name] = edit

        self.image_label = QLabel(self.centralwidget)
        self.image_label.setGeometry(20, 20, 120, 120)
        self.image_label.setStyleSheet("background-color: rgb(80, 80, 80); border: 1px solid white;")
        self.image_label.setScaledContents(True)

        self.add_button("Загрузить фото", 20, 150, self.load_image, "rgb(70, 130, 180)")
        self.add_button("Сгенерировать", 660, 740, self.generate_profile_text, "rgb(70, 130, 180)")
        self.add_button("Создать PDF", 660, 800, self.draw_resume_UI, "rgb(168, 70, 71)")

        self.result_box = QTextEdit(self.centralwidget)
        self.result_box.setGeometry(20, 530, 620, 300)
        self.result_box.setStyleSheet("background-color: white; color: black;")
        self.result_box.setReadOnly(True)

    def draw_resume_UI(self):
        draw_resume(self.parsed_resume, self.output_pdf_path, self.image_path)

    def create_label(self, text, x, y, font):
        label = QLabel(text, self.centralwidget)
        label.setGeometry(x, y, 300, 20)
        label.setFont(font)
        label.setStyleSheet("color: white;")
        self.labels[text] = label

    def add_button(self, text, x, y, callback, color):
        btn = QPushButton(text, self.centralwidget)
        btn.setGeometry(x, y, 120, 30)
        btn.setStyleSheet(f"background-color: {color}; color: white;")
        btn.clicked.connect(callback)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_label.setPixmap(QPixmap(file_name))
            self.image_path = file_name

    def generate_profile_text(self):
        api_key = "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"
        client = OpenAI(api_key=api_key)

        data = {k: self.text_edits[k].toPlainText().strip() for k in self.text_edits}

        # Формируем prompt для ИИ — просим раскрыть краткие записи в полноформатный резюме-стиль
        prompt = f"""
You are a professional resume writing assistant.

Using the data below, write a detailed professional CV with the following sections and structure (no extra empty lines):

[Name]
{data.get('First Name*', '')}
{data.get('Last Name*', '')}

[Title]
{data.get('Job Title*', '')}

[Contact]
{data.get('Email*', '')}
{data.get('Phone*', '')}
{data.get('Address*', '')}

[Profile]
Expand the following short description into a concise paragraph with 3-4 sentences:
{data.get('Profile* (1 sentence or 5-6 adjectives.)', '')}

[Employment History]
For each work entry separated by semicolon (;), format as:
Company Name, Dates, Few words describing role.
Expand each entry to 2-3 sentences describing responsibilities and accomplishments. Short and to the point.
Entries: {data.get('Employment History (Name, Dates, Few words; ...)', '')}

[Education]
For each education entry separated by semicolon (;), format as:
Institution Name, Dates, Few words about study.
Expand each entry to 1-2 sentences describing what you learned. Short and to the point.
Entries: {data.get('Education (Name, Dates, Few words; ...)', '')}

[Internships]
For each internship entry separated by semicolon (;), format as:
Company Name, Dates, Few words describing role.
Expand each entry to 1-2 sentences describing what you did. Short and to the point.
Entries: {data.get('Internships (Name, Dates, Few words; ...)', '')}

[Skills]
List skills and proficiency ratings as Skill | n/5 like 5/5 or 3/5. Instead of ";" go to the next line.
Entries: {data.get('Skills (Skill, Range 1-5; ...)', '')}

[Languages]
List languages and their proficiency ratings in the Language | rating form. Instead of ";" go to the next line.
Entries: {data.get('Languages (Language, Range 1-5 or A1-C2; ...)', '')}

[Courses]
For each course entry separated by semicolon (;), format as:
Course Name, Dates. Write as Course | date. Instead of ";" go to the next line.
Entries: {data.get('Courses (Name, Dates; ...)', '')}

[Hobbies]
Expand the following short description into a concise paragraph with 1-3 sentences:
{data.get('Hobbies (1-3 your hobbies)', '')}

Note: 
IN NO EVENT SHOULD THE TOTAL WORD NUMBER FOR Employment History + Education + Internships EXCEED 200.
There should be no more than 3 lines per 1 institution name in Employment History, Education and Internships. 1 line NAME 2 DATES 3 DESCRIPTION AND NOTHING MORE.
YOU MUST FOLLOW ALL THE RULES, REGARDLESS OF THE LANGUAGE YOU WRITE IN.
Format the text in the language in which the data was entered, do not change the language of the paragraphs “[]” BUT CONTINUE WRITING THEM. 
DON'T FORGET TO WRITE THE TITLE OF THE PARAGRAPHS (WHAT'S IN []) IF THERE IS INFORMATION ABOUT THEM.
If there is data for a section, always write its name in square brackets exactly as shown, then write the content. Do not skip or delete section names if the previous condition is met.
You are writing a resume. Write in the first person, always "I". 
Write briefly, no more than 40 words, 20-25 on average. 
Wherever there is a name and date, put enters after the name and date instead of ",". 
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a resume writing assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1200
            )
            result = response.choices[0].message.content.strip()
            self.parsed_resume = parse_resume(result)
            self.result_box.setPlainText(result)
        except Exception as e:
            self.result_box.setPlainText(f"❌ Error:\n{e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())