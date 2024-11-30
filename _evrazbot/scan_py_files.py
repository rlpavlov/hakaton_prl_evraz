import os
import re

# Функция для анализа файла

# Путь к папке с Python-файлами
#directory_path = "c:\\Ruslan_python\\_evraz_py"
#directory_path = "./FlaskApiEcommerce-master"
directory_path = "c:\\Ruslan_python\\_evraz_files\\FlaskApiEcommerce-master" 

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

def is_comment(line):
    """
    Проверяет, является ли строка комментарием.
    """
    stripped = line.strip()
    return stripped.startswith('#') or stripped.startswith('"""')

def find_comment(lines, index):
    """
    Ищет комментарий перед или после текущей строки.
    """
    # Ищем комментарий перед объявлением
    i = index - 1
    while i >= 0 and lines[i].strip() == '':
        i -= 1
    if i >= 0 and is_comment(lines[i]):
        return True

    # Ищем комментарий после объявления
    i = index + 1
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    if i < len(lines) and is_comment(lines[i]):
        return True

    return False

def check_comments(file_path, file_bytes=""):
    """Анализируем файл на питоне"""
    #print(f"Обрабатывается файл: {file_path}")
    problems = []

    if isinstance(file_bytes, bytes):
        # Преобразование bytes в массив строк
        string_data = file_bytes.decode('utf-8')  # Декодируем bytes в строку
        lines = string_data.split('\n')  # Разделяем строку на массив по символу новой строки    
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

    #with open(file_path, "r", encoding="utf-8") as file:
    #    lines = file.readlines()
    # Проверка классов, функций и методов на наличие комментариев
    for index, line in enumerate(lines):
        # Проверяем начало класса, функции или метода
        class_match = re.match(r"^\s*class (\w+)", line)
        function_match = re.match(r"^\s*def (\w+)", line)

        if class_match or function_match:
            # Определяем текущую сущность (класс или функция)
            entity_name = class_match.group(1) if class_match else function_match.group(1)
            entity_type = "Class" if class_match else "Function"
            #print(f"Найдено: {entity_type}:{entity_name}")
            
            # Проверяем, есть ли строка документации
            #if index + 1 < len(lines) and not re.match(docstring_regex, lines[index + 1]):
            
            # Проверяем комментарий
            if not find_comment(lines, index):
                #print(f"Найдена проблема: {entity_type}:{entity_name}")
                #missing_comments.append((elem_type, name, i + 1))            
                problems.append({
                    "filepath": file_path,
                    "file": os.path.basename(file_path),
                    "line": index + 1,
                    "description": f"Нет комментария для {entity_type} '{entity_name}'"
                })
                #print(problems)
    return problems            

# Функция для рекурсивного обхода папки
def scan_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                check_comments(os.path.join(root, file))

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
#result_lines = check_comments("scan_py_files.py")
#result_lines = scan_directory(directory_path)
#result_comments = []
#result_comments.extend(result_lines)
#print(result_lines)
#review_comments = result
#write_results_to_file()

#result = check_comments("scan_py_files.py")
#if result:
#    print("Следующие элементы отсутствуют комментарии:")
#    for file_path, file, index, description in result:
#        print(f"{file_path} '{description}' на строке {index}")
            
#print(f"Analysis complete. Results saved to {output_file_path}")

