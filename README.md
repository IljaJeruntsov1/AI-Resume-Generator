# AI-Resume-Generator
[Eng]
An application with a graphical interface that helps to create basic but fast professional resumes in PDF format. The user fills in the fields, and the AI ​​supplements or clarifies the description, following strictly specified rules.

Installation
Before use, install the necessary dependencies:
pip install reportlab PyQt5 openai

Launch
Launch is performed via python main.py
After launch, a window will open in which you can fill out the form.

Sample output
The program creates the Output/generated_resume.pdf file (as specified in the config). It will contain a strictly formatted resume that meets the specified rules.

License
This project is provided "as is", without any warranties. Use and modify at your own discretion.

Basic modifications to change the font and specify the path to the final file can be made through the config.py file.

Writing Rules
For each text block that requires a specific format, a standardized example of formatting is provided. It serves as an example of the correct text structure for this block.

What is not important:
- Spaces at the beginning and end of lines.
- Enters after ";"
- You can skip blocks not marked with "*"

Use examples:
- Profile:
Responsible, creative, detail-oriented, analytical, communicative, self-motivated
— or —
I am a motivated and adaptable developer with strong problem-solving skills and attention to detail.
- Employment History:
ABC Tech, 2021–2024, I developed and maintained scalable backend systems in Python;
DataSys, 2019–2021, I worked on internal tools as a junior developer;
- Education:
Tallinn University of Technology, 2015–2019, I earned a Bachelor’s degree in Computer Science;
Open University, 2020–2021, I studied data analysis and machine learning;
- Internships:
NetGroup, Summer 2018, I assisted in frontend development and UI testing;
Telia, Summer 2017, I supported the IT team with hardware setup and software updates;
- Courses:
Machine Learning Specialization, 2023;
Web Development Bootcamp, 2022;
- Skills:
Python, 5;
JavaScript, 4;
SQL, 5;
Git, 5;
Docker, 4;
- Languages:
English, B2;
Estonian, C1;
Russian, Native;
- Hobbies:
Reading science fiction, running, traveling

[Rus]
Приложение с графическим интерфейсом, помогающее создовать базовые но быстрые профессиональные резюме в формат PDF. Пользователь заполняет поля, а ИИ дополняет или уточняет описание, следуя строго заданным правилам.

Установка
Перед использованием установите необходимые зависимости:
pip install reportlab PyQt5 openai

Запуск
Запуск осуществляется через python main.py
После запуска откроется окно, в котором можно заполнить форму.

Пример вывода
Программа создает файл Output/generated_resume.pdf (как указано в конфиге). Он будет содержать строго отформатированное резюме, соответствующее заданным правилам.

Лицензия
Данный проект предоставляется «как есть», без каких-либо гарантий. Используйте и изменяйте по своему усмотрению.

Базовые доработки по изменению шрифта и указанию пути к конечному файлу можно сделать через файл config.py.

Правила написания
Для каждого текстового блока, требующего определенного формата, приводится стандартизированный пример форматирования. Он служит примером правильной структуры текста для этого блока.

Что не важно:
- Пробелы в начале и конце строк.
- Энтеры после ";"
- Можно пропускать блоки не помеченные "*"

Примеры использования:
- Profile (Профиль):
Ответственный, креативный, ориентированный на детали, аналитический, коммуникабельный, самомотивированный
— или —
Я мотивированный и легко адаптирующийся разработчик с сильными навыками решения проблем и вниманием к деталям.
- Employment History (История трудоустройства):
ABC Tech, 2021–2024, я разрабатывал и поддерживал масштабируемые бэкэнд-системы на Python;
DataSys, 2019–2021, я работал над внутренними инструментами в качестве младшего разработчика;
- Education (Образование):
Таллиннский технический университет, 2015–2019, я получил степень бакалавра в области компьютерных наук;
Открытый университет, 2020–2021, я изучал анализ данных и машинное обучение;
- Internships (Стажировки):
NetGroup, лето 2018, я помогал в разработке фронтенда и тестировании пользовательского интерфейса;
Telia, лето 2017 г., я поддерживал ИТ-команду с настройкой оборудования и обновлениями программного обеспечения;
- Courses (Курсы):
Специализация по машинному обучению, 2023 г.;
Учебный лагерь по веб-разработке, 2022 г.;
- Skills (Навыки):
Python, 5;
JavaScript, 4;
SQL, 5;
Git, 5;
Docker, 4;
- Languages (Языки):
Английский, B2;
Эстонский, C1;
Русский, родной;
- Hobbies (Увлечения):
Чтение научной фантастики, бег, путешествия
