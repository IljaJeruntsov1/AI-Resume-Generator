from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from config import font_normal, font_bold
import textwrap
import os

def draw_resume(parsed, output_path, photo_path=None):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    left_x = 20 * mm
    right_x = 80 * mm
    top_x = 80 * mm
    top_y = height - 20 * mm

    if photo_path and os.path.exists(photo_path):
        from PIL import Image
        # Обрезка изображения в соотношении 3:4 по центру
        with Image.open(photo_path) as im:
            width, height = im.size
            target_ratio = 3 / 4
            current_ratio = width / height

            if current_ratio > target_ratio:
                # Ширина слишком большая — обрезать по бокам
                new_width = int(height * target_ratio)
                offset = (width - new_width) // 2
                box = (offset, 0, offset + new_width, height)
            else:
                # Высота слишком большая — обрезать сверху и снизу
                new_height = int(width / target_ratio)
                offset = (height - new_height) // 2
                box = (0, offset, width, offset + new_height)

            cropped = im.crop(box)
            cropped_path = "_cropped_photo_temp.jpg"
            if cropped.mode == 'RGBA':
                cropped = cropped.convert('RGB')
            cropped.save(cropped_path, format='JPEG')

        image = ImageReader(cropped_path)
        c.drawImage(image, right_x - 165, top_y - 110, width=90, height=120)
        photo_block_start = top_y - 110
        top_x -= 165
    else:
        photo_block_start = top_y - 110
        top_x -= 265

    y2 = top_y - 10
    if "Name" in parsed:
        c.setFont(font_bold, 32)
        for line in parsed["Name"]:
            c.drawString(top_x + 100, y2, line)
            y2 -= 32
    y2 += 100

    if "Title" in parsed:
        c.setFont(font_bold, 24)
        for line in parsed["Title"]:
            for line in textwrap.wrap(line, width=18):
                c.drawString(top_x + 280, y2, line)
                y2 -= 24

    if "Contact" in parsed:
        c.setFont(font_normal, 10)
        for line in parsed["Contact"]:
            for line in textwrap.wrap(line, width=60):
                c.drawString(top_x + 280, y2, line)
                y2 -= 12

    if "Profile" in parsed:
        c.setFont(font_bold, 16)
        c.drawString(top_x + 100, y2, "Profile")
        y2 -= 14
        c.setFont(font_normal, 10)
        for line in parsed["Profile"]:
            for wrapped in textwrap.wrap(line, 80):
                c.drawString(top_x + 100, y2, wrapped)
                y2 -= 12

    y = photo_block_start

    y -= 25
    c.setStrokeColor(HexColor("#999999"))  # серый цвет
    c.setLineWidth(1)
    c.line(left_x, y, left_x + 180 * mm, y)

    left_content_end = y - 30
    right_content_end = y2 - 30

    # Нижняя граница для синхронного старта нижнего блока
    next_column_top = min(left_content_end, right_content_end)

    # 3. Левая колонка — Employment, Education, Internships
    content_y = next_column_top
    for section in ["Employment History", "Education", "Internships"]:
        if section in parsed:
            c.setFont(font_bold, 16)
            c.drawString(left_x, content_y, section)
            content_y -= 18
            lines_group = parsed[section]
            for i in range(0, len(lines_group), 4):
                for j in range(4):
                    if i + j < len(lines_group):
                        line = lines_group[i + j]
                        font_name = font_bold if j == 0 else font_normal
                        font_size = 12 if j == 0 else 10
                        width_size = 40 if j == 0 else 50
                        c.setFont(font_name, font_size)
                        for line in textwrap.wrap(line, width=width_size):
                            c.drawString(left_x + 10, content_y, line)
                            content_y -= 14
                content_y -= 7
            content_y -= 18

    # 4. Правая колонка — Skills, Languages, Hobbies, Courses
    block_y = next_column_top
    for section in ["Skills", "Languages", "Courses", "Hobbies"]:
        if section in parsed:
            c.setFont(font_bold, 16)
            c.drawString(right_x + 110, block_y, section)
            block_y -= 18
            c.setFont(font_normal, 10)
            for line in parsed[section]:
                for line in textwrap.wrap(line, width=45):
                    c.drawString(right_x + 120, block_y, line)
                    block_y -= 14
            block_y -= 12

    c.save()

    # Удаление временного файла, если был создан
    if photo_path and os.path.exists("_cropped_photo_temp.jpg"):
        os.remove("_cropped_photo_temp.jpg")

def parse_resume(text):
    sections = {}
    current = None
    temp_content = []

    for line in text.strip().splitlines():
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            # Добавляем раздел только если в temp_content есть не пустые строки
            if current and any(s for s in temp_content if s):
                sections[current] = temp_content
            current = line[1:-1]
            temp_content = []
        elif current:
            temp_content.append(line)

    # Для последнего раздела тоже проверяем наличие непустых строк
    if current and any(s for s in temp_content if s):
        sections[current] = temp_content

    return sections