import os
import re
from scan_utils import is_camel_case

# Путь к папке с файлами TypeScript
#directory_path = "./path_to_your_folder"
directory_path = "./abctasks-client-main"
#directory_path = "c:\Ruslan_python\02_hakaton_prl_evraz_Задача\py\abctasks-client-main"
# Путь к файлу вывода
output_file_path = "output_ts.txt"

# Регулярные выражения
comment_regex = r"///|/\*\*.*\*/"  # Комментарии к классам/методам/функциям
review_comment_regex = r"// <REVIEW>(.*)</REVIEW>"  # Комментарии с тегом <REVIEW>

# Списки для хранения найденных проблем и <REVIEW> комментариев
#problems = []
review_comments = []

# Функция для анализа файла
def check_comments(file_path, file_bytes=""):
    problems = []
    file_name = os.path.basename(file_path)
    if(is_camel_case(file_name)):
        problems.append({
            "filepath": file_path,
            "file": file_name,
            "line": 0,
            "description": f"Неверное имя файла (должно быть в CamelCase) для {file_name}"    
        })
    
    #with open(file_path, "r", encoding="utf-8") as file:
    #    lines = file.readlines()
    if isinstance(file_bytes, bytes):
        # Преобразование bytes в массив строк
        string_data = file_bytes.decode('utf-8')  # Декодируем bytes в строку
        lines = string_data.split('\n')  # Разделяем строку на массив по символу новой строки    
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    
    # Поиск комментариев <REVIEW>
    for index, line in enumerate(lines):
        review_match = re.search(review_comment_regex, line)
        if review_match:
            review_comments.append({
                "filepath": file_path,
                "file": os.path.basename(file_path),
                "line": index + 1,
                "comment": review_match.group(1).strip()
            })
    
    inside_class_or_function = False
    expecting_comment = False
    current_name = ""

    for index, line in enumerate(lines):
        # Проверка начала класса или функции
        class_match = re.search(r"class (\w+)", line)
        function_match = re.search(r"function (\w+)", line)
        method_match = re.search(r"(\w+)\([\w\s,]*\)\s*{", line)

        if class_match or function_match or method_match:
            inside_class_or_function = True
            expecting_comment = True
            current_name = class_match.group(1) if class_match else function_match.group(1) if function_match else method_match.group(1)

        # Проверка наличия комментария перед классом, функцией или методом
        if expecting_comment:
            if index == 0 or not re.search(comment_regex, lines[index - 1].strip()):
                problems.append({
                    "filepath": file_path,
                    "file": os.path.basename(file_path),
                    "line": index + 1,
                    "description": f"Нет комментария для {current_name}"
                })
            expecting_comment = False

        if inside_class_or_function and "}" in line:
            inside_class_or_function = False

    return problems            


# Функция для рекурсивного обхода папки
def scan_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ts") or file.endswith(".tsx"):
                check_comments(os.path.join(root, file))

# Функция для записи результатов в файл
def write_results_to_file():
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("=== Missing Comments ===\n")
        for problem in problems:
            output_file.write(f"File: {problem['file']}, Line: {problem['line']}, Description: {problem['description']}\n")

        output_file.write("\n=== <REVIEW> Comments ===\n")
        for review in review_comments:
            output_file.write(f"File: {review['file']}, Line: {review['line']}, Comment: {review['comment']}\n")

# Запуск анализа
#scan_directory(directory_path)
#write_results_to_file()

#print(f"Analysis complete. Results saved to {output_file_path}")
