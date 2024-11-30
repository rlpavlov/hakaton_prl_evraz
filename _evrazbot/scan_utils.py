import os
import re

import os
import re
from fpdf import FPDF

import os
import re

# Функция uniP: возвращает подстроку, используя разделитель
def uniP(a_string, a_delimiter, a_start_pos, a_end_pos):
    parts = a_string.split(a_delimiter)
    return a_delimiter.join(parts[a_start_pos - 1:a_end_pos])

def is_camel_case(filepath: str) -> bool:
    """
    Проверяет, соответствует ли имя файла в указанном пути нотации CamelCase.

    :param filepath: Полное имя файла, включая путь.
    :return: True, если имя файла соответствует CamelCase, иначе False.
    """
    # Получение имени файла без пути и расширения
    filename = os.path.basename(filepath)  # Извлекаем имя файла с расширением
    name_without_extension = os.path.splitext(filename)[0]  # Удаляем расширение

    # Регулярное выражение для проверки CamelCase
    camel_case_pattern = r'^[A-Z][a-zA-Z0-9]*$'

    # Проверка соответствия имени шаблону
    return bool(re.match(camel_case_pattern, name_without_extension))


def is_snake_case(filepath: str) -> bool:
    """
    Проверяет, соответствует ли имя файла в указанном пути нотации snake_case.

    :param filepath: Полное имя файла, включая путь.
    :return: True, если имя файла соответствует snake_case, иначе False.
    """
    # Получение имени файла без пути и расширения
    filename = os.path.basename(filepath)  # Например: "your_file_name_123.py"
    name_without_extension = os.path.splitext(filename)[0]  # Например: "your_file_name_123"

    # Регулярное выражение для проверки snake_case
    snake_case_pattern = r'^[a-z0-9]+(_[a-z0-9]+)*$'

    # Возвращает True, если имя соответствует паттерну
    return bool(re.match(snake_case_pattern, name_without_extension))

def save_result_to_pdf_v1(filepath: str, output_pdf: str):
    """
    Проверяет имя файла на соответствие snake_case и сохраняет результат в PDF.

    :param filepath: Полный путь к файлу для проверки.
    :param output_pdf: Имя PDF файла для сохранения результата.
    """
    result = is_snake_case(filepath)
    filename = os.path.basename(filepath)

    # Создание PDF-документа
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Calibri", "", "calibri.ttf", uni=True)
    pdf.set_font("Calibri", size=12)
    

    # Запись результата в PDF
    pdf.cell(200, 10, txt="Проверка имени файла на соответствие snake_case", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Имя файла: {filename}", ln=True)
    pdf.cell(200, 10, txt=f"Результат: {'Соответствует' if result else 'Не соответствует'}", ln=True)

    # Сохранение PDF
    pdf.output(output_pdf)
    print(f"Результат сохранен в файл {output_pdf}")
    
from fpdf import FPDF

#results - массив массивов
#table_header - заголовок документа
#output_file - имя выходного файла
def save_results_to_pdf(results, table_header, output_file="output.pdf"):
    """
    Сохраняет массив results в PDF файл в виде таблицы.
    
    :param results: массив, содержащий элементы - массивы из 4 полей: [filepath, file, line, comment]
    :param table_header: строка, используемая как заголовок таблицы
    :param output_file: имя выходного PDF файла
    """
    #font_name="Arial"
    font_name="Сalibri"
    #font_name="Tahoma"
    #font_name="Times New Roman"
    
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    #pdf.set_font("Arial", size=12)
    pdf.add_font("Сalibri", "", "calibri.ttf", uni=True)
    pdf.set_font(font_name, size=12)

    # Добавляем заголовок таблицы
    #pdf.set_font("Arial", style="B", size=14)
    #pdf.set_font(font_name, style="B", size=14)
    pdf.set_font(font_name, size=12)
    pdf.cell(0, 10, table_header, ln=True, align="C")
    pdf.ln(10)

    # Добавляем заголовки колонок
    #pdf.set_font("Arial", style="B", size=12)
    #pdf.set_font(font_name, style="B", size=14)
    pdf.set_font(font_name, size=12)
    headers = ["Filepath", "File", "Line", "Comment"]
    column_widths = [60, 40, 20, 70]  # Ширина колонок в PDF
    for header, width in zip(headers, column_widths):
        pdf.cell(width, 10, header, border=1, align="C")
    pdf.ln()

    # Добавляем содержимое таблицы
    #pdf.set_font("Arial", size=10)
    #pdf.set_font(font_name, style="B", size=12)
    pdf.set_font(font_name, size=12)
    for row in results:
        for i, width in zip(row, column_widths):
            #pdf.cell(width, 10, str(i), border=1)
            #pdf.cell(width, 10, str(row[i]), border=1)
            # Используем multi_cell для автоматического переноса текста
            x, y = pdf.get_x(), pdf.get_y()
            pdf.multi_cell(width, 10, str(row[i]), border=1, align="L")
            pdf.set_xy(x + width, y)  # Переходим к следующей ячейке
            
        pdf.ln()

    # Сохраняем PDF файл
    pdf.output(output_file)
    print(f"Результат сохранён в файл: {output_file}")    

#results - массив строк
#table_header - заголовок документа
#output_file - имя выходного файла
def save_results_to_pdf_v3(results, table_header, output_file="output.pdf"):
    """
    Сохраняет массив results в PDF файл в виде списка строк.
    
    :param results: массив, содержащий элементы - массивы из 4 полей: [filepath, file, line, comment]
    :param table_header: строка, используемая как заголовок таблицы
    :param output_file: имя выходного PDF файла
    """
    #font_name="Arial"
    font_name="Сalibri"
    #font_name="Tahoma"
    #font_name="Times New Roman"
    
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    #pdf.set_font("Arial", size=12)
    pdf.add_font("Сalibri", "", "calibri.ttf", uni=True)
    pdf.set_font(font_name, size=12)

    # Добавляем заголовок таблицы
    #pdf.set_font("Arial", style="B", size=14)
    #pdf.set_font(font_name, style="B", size=14)
    #pdf.set_font(font_name, size=12)
    #pdf.cell(0, 10, table_header, ln=True, align="C")
    #pdf.ln(10)

    # Добавляем заголовки колонок
    #pdf.set_font("Arial", style="B", size=12)
    #pdf.set_font(font_name, style="B", size=14)
    #pdf.set_font(font_name, size=12)
    #headers = ["Filepath", "File", "Line", "Comment"]
    #column_widths = [60, 40, 20, 70]  # Ширина колонок в PDF
    #for header, width in zip(headers, column_widths):
    #    pdf.cell(width, 10, header, border=1, align="C")
    #pdf.ln()

    # Добавляем содержимое таблицы
    #pdf.set_font("Arial", size=10)
    #pdf.set_font(font_name, style="B", size=12)
    pdf.set_font(font_name, size=12)
    for row in results:
        for index in row:
            #pdf.cell(width, 10, str(i), border=1)
            #pdf.cell(width, 10, str(row[i]), border=1)
            # Используем multi_cell для автоматического переноса текста
            #x, y = pdf.get_x(), pdf.get_y()
            #pdf.multi_cell(width, 10, str(row[i]), border=1, align="L")
            #pdf.set_xy(x + width, y)  # Переходим к следующей ячейке
            cell_value=str(row[index])
            pdf.cell(200, 5, txt=f"{index}: {cell_value}", ln=True, align="C")
            #pdf.ln(10)
            
        pdf.ln(10)

    # Сохраняем PDF файл
    pdf.output(output_file)
    print(f"Результат сохранён в файл: {output_file}")    


# Пример использования
#filepath = "/path/to/your_file_name_123.py"
#output_pdf = "output.pdf"
#save_result_to_pdf_v1(filepath, output_pdf)

# Примеры использования
#print(is_snake_case("/path/to/your_file_name_123.py"))  # True
#print(is_snake_case("/path/to/YourFileName123.py"))     # False
#print(is_snake_case("/path/to/__init__.py"))            # True

# Примеры использования
#filepath1 = "/path/to/MyCamelCaseFile.py"
#filepath2 = "/path/to/not_camel_case.py"
#filepath3 = "/path/to/AnotherExample123.py"

#print(is_camel_case(filepath1))  # True
#print(is_camel_case(filepath2))  # False
#print(is_camel_case(filepath3))  # True

