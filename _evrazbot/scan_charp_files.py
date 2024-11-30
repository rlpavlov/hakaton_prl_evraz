import re
import zipfile
import os
import tempfile

def check_comments(file_path, file_bytes=""):
    """Проверка наличия комментариев в файле C# с указанием имен классов и методов."""
    # Регулярные выражения для поиска классов, методов и комментариев
    class_pattern = re.compile(r'^\s*public\s+(?:class|struct|interface)\s+(\w+)')
    method_pattern = re.compile(r'^\s*public\s+(?:static\s+)?(?:\w+\s+)?(\w+)\s*\([^)]*\)\s*')
    comment_pattern = re.compile(r'^\s*///')

    #with open(file_path, 'r', encoding='utf-8') as file:
    #    lines = file.readlines()
    if isinstance(file_bytes, bytes):
        # Преобразование bytes в массив строк
        string_data = file_bytes.decode('utf-8')  # Декодируем bytes в строку
        lines = string_data.split('\n')  # Разделяем строку на массив по символу новой строки    
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

    results = []
    for i, line in enumerate(lines):
        # Проверка на класс
        class_match = class_pattern.match(line)
        if class_match:
            class_name = class_match.group(1)
            if i == 0 or not comment_pattern.match(lines[i - 1]):
                #results.append(f"Нет комментария к классу '{class_name}' на строке {i + 1}")
                results.append({
                    "filepath": file_path,
                    "file": os.path.basename(file_path),
                    "line": i + 1,
                    "description": f"Нет комментария к классу '{class_name}'"
                })

        # Проверка на метод
        method_match = method_pattern.match(line)
        if method_match:
            method_name = method_match.group(1)
            if i == 0 or not comment_pattern.match(lines[i - 1]):
                #results.append(f"Нет комментария к методу '{method_name}' на строке {i + 1}")
                results.append({
                    "filepath": file_path,
                    "file": os.path.basename(file_path),
                    "line": i + 1,
                    "description": f"Нет комментария к методу '{method_name}'"
                })
    return results

def process_zip_archive(zip_path):
    """Обработка zip-архива, поиск файлов .cs и проверка их комментариев."""
    results = []
    with tempfile.TemporaryDirectory() as temp_dir:
        # Распаковываем архив во временную папку
        with zipfile.ZipFile(zip_path, 'r') as archive:
            archive.extractall(temp_dir)

        # Рекурсивно ищем файлы .cs
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)
                    file_results = check_comments(file_path)
                    if file_results:
                        results.append((file_path, file_results))

    return results

def process_multiple_archives(zip_paths):
    """Обработка нескольких zip-архивов."""
    all_results = []
    for zip_path in zip_paths:
        print(f"Обрабатывается архив: {zip_path}")
        archive_results = process_zip_archive(zip_path)
        all_results.extend(archive_results)
    return all_results

# Укажите пути к zip-архивам
#zip_paths = ["archive1.zip", "archive2.zip"]  # Замените на свои архивы

# Запуск обработки
#all_results = process_multiple_archives(zip_paths)

# Вывод результатов
#if all_results:
#    for file_path, issues in all_results:
#        print(f"\nПроблемы в файле: {file_path}")
#        for issue in issues:
#            print(f"  - {issue}")
#else:
#    print("Все файлы во всех архивах имеют комментарии.")

