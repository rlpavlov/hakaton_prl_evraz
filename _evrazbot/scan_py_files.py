import os
import re

# Путь к папке с Python-файлами
#directory_path = "./path_to_your_folder"
directory_path = "./FlaskApiEcommerce-master"
# Путь к файлу вывода
output_file_path = "./output_py.txt"

# Регулярные выражения
review_comment_regex = r"# <REVIEW>(.*)</REVIEW>"  # Поиск комментариев <REVIEW>
todo_comment_regex = r"# TODO:(.*)"  # Поиск комментариев # TODO
docstring_regex = r'^\s*("""|\'\'\')'  # Поиск строки документации для функций, классов, методов

# Списки для хранения результатов
#problems = []
review_comments = []
todo_comments = []

# Функция для анализа файла
def analyze_file(file_path):
    problems = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Проверка классов, функций и методов на наличие комментариев
    for index, line in enumerate(lines):
        # Проверяем начало класса, функции или метода
        class_match = re.match(r"^\s*class (\w+)", line)
        function_match = re.match(r"^\s*def (\w+)", line)

        if class_match or function_match:
            # Определяем текущую сущность (класс или функция)
            entity_name = class_match.group(1) if class_match else function_match.group(1)
            entity_type = "Class" if class_match else "Function"
            
            # Проверяем, есть ли строка документации
            if index + 1 < len(lines) and not re.match(docstring_regex, lines[index + 1]):
                problems.append({
                    "filepath": file_path,
                    "file": os.path.basename(file_path),
                    "line": index + 1,
                    "description": f"Нет комментария для {entity_type} '{entity_name}'"
                })
    return problems            

# Функция для рекурсивного обхода папки
def scan_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                analyze_file(os.path.join(root, file))

# Функция для записи результатов в файл
def write_results_to_file():
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("\n=== <REVIEW> Comments ===\n")
        for review in review_comments:
            output_file.write(f"File: {review['file']}, Line: {review['line']}, Comment: {review['comment']}\n")

        output_file.write("\n=== TODO Comments ===\n")
        for todo in todo_comments:
            output_file.write(f"File: {todo['file']}, Line: {todo['line']}, Comment: {todo['comment']}\n")

# Запуск анализа
#scan_directory(directory_path)
#write_results_to_file()

#print(f"Analysis complete. Results saved to {output_file_path}")