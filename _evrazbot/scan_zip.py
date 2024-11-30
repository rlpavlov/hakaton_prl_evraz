import io
import re
import zipfile
import os
import tempfile
import py7zr
import rarfile
from scan_utils import save_results_to_pdf_v3 as scan_utils_save_to_pdf

# Путь к папке с архивами
#directory_path = "c:\Ruslan_python\_evraz_py\zip_files"
directory_path = "c:\\Ruslan_evraz\\20241127_Задание\\Готовые проекты" 
#directory_path = "./"

#def check_comments(file_path):
from scan_charp_files import check_comments as scan_charp_check_comments
#def analyze_file(file_path):
from scan_ts_files import analyze_file as scan_ts_check_comments
#def analyze_file(file_path):
from scan_py_files import analyze_file as scan_py_check_comments

#Распаковывает указанный архив zip_path, выполняет анализ и возвращает результаты в массиве results[]
def process_zip_archive(zip_path, zip_file):
    """Обработка zip-архива, поиск файлов .cs и проверка их комментариев."""
    results = []  #[file, file_results[filepath, file, line ,description]]
    results_lines = []  #[filepath, file, line ,description]
    with tempfile.TemporaryDirectory() as temp_dir:
        # Распаковываем архив во временную папку
        if zip_path.endswith("zip"):
            if isinstance(zip_file, bytes):
                with zipfile.ZipFile(io.BytesIO(zip_file), 'r') as archive:
                    archive.extractall(temp_dir)
            else:
                with zipfile.ZipFile(zip_path, 'r') as archive:
                    archive.extractall(temp_dir)
        # Распаковка архива 7z
        if zip_path.endswith("7z"):
            if isinstance(zip_file, bytes):
                with py7zr.SevenZipFile(io.BytesIO(zip_file), 'r') as archive:
                    archive.extractall(temp_dir)
            else:
                with py7zr.SevenZipFile(zip_path, mode='r') as archive:
                    archive.extractall(temp_dir)               
        # Распаковка архива rar
        if zip_path.endswith("rar"):
            if isinstance(zip_file, bytes):
                with rarfile.RarFile(io.BytesIO(zip_file), 'r') as archive:
                    archive.extractall(temp_dir)
            else:
                with rarfile.RarFile(zip_path) as archive:
                    archive.extractall(temp_dir)
        #return results
        # Рекурсивно ищем файлы .cs, .py, .ts, .tsx
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                #print(f"Обрабатывается файл: {file_path}")
                try:
                    if file.endswith('.cs'):
                        #print(f"Обрабатывается файл: {file_path}")
                        file_results = scan_charp_check_comments(file_path)
                        if file_results:
                            results.append((file_path, file_results))
                            results_lines.extend(file_results)
                    if file.endswith(".py"):
                        #print(f"Обрабатывается файл: {file_path}")
                        file_results = scan_py_check_comments(file_path)
                        if file_results:
                            results.append((file_path, file_results))
                            results_lines.extend(file_results)
                            
                    if file.endswith(".ts") or file.endswith(".tsx"):
                        #print(f"Обрабатывается файл: {file_path}")
                        file_results = scan_ts_check_comments(file_path)
                        if file_results:
                            results.append((file_path, file_results))
                            results_lines.extend(file_results)
                            
                except Exception as write_error:
                    #print(f"Ошибка обработки файла={file_path}: {write_error}")
                    file_results = []
                    file_results.append({
                        "filepath": file_path,
                        "file": os.path.basename(file_path),
                        "line": 0,
                        "description": f"error {write_error}"
                    })                                             
                    results.append((file_path, file_results))
                    results_lines.extend(file_results)

    #return results
    return results_lines

def process_multiple_archives(zip_paths):
    """Обработка нескольких zip-архивов."""
    all_results = []
    for zip_path in zip_paths:
        print(f"Обрабатывается архив: {zip_path}")
        archive_results = process_zip_archive(zip_path)
        all_results.extend(archive_results)
    return all_results
    
# Функция для рекурсивного обхода папки
def scan_directory(directory):
    """Рекурсивная обработка папки с архивами."""
    all_results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith("zip") or file.endswith("rar") or file.endswith("7z"):
                zip_path=os.path.join(root, file)
                print(f"Обрабатывается архив: {zip_path}")
                archive_results = process_zip_archive(zip_path)
                all_results.extend(archive_results)
    return all_results

# Укажите пути к zip-архивам
#zip_paths = ["archive1.zip", "archive2.zip", "archive3.zip"]  # Замените на свои архивы

# Запуск обработки
#all_results = process_multiple_archives(zip_paths)
#all_results = scan_directory(directory_path)

# Вывод результатов
#if all_results:
#    scan_utils_save_to_pdf(all_results, "Результаты сканирования", "results.pdf")
    #iCount = 0
    #for file_path, issues in all_results:  #[file, file_results]
    #    print(f"\nПроблемы в файле: {file_path}")
    #    file = os.path.basename(file_path)
    #    iCount=iCount+1
        #scan_utils_save_to_pdf(issues, file_path, f"results_{file}_[{iCount}].pdf")
        #for issue in issues:
        #    print(f"  - {issue}")
#else:
#    print("Все файлы во всех архивах имеют комментарии.")
