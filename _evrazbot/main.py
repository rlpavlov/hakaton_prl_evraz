import io
from zipfile import ZipFile

from decouple import config
from telebot import TeleBot

from scan_zip import process_zip_archive
from scan_zip import process_file_from_archive
from scan_utils import save_results_to_pdf_v3 as scan_utils_save_to_pdf

# Загрузка конфигурации из .env файла
TOKEN = config('TELEGRAM_TOKEN')

def create_report(report_path, contents):
#Здесь будет создание pdf-файла
    # Для создания файла репорта, можно править для ваших потребностей
    with open(report_path, "w") as file:
        file.write(contents)
    return report_path

def process_file(file_path, file_bytes) -> str:
# Функция для обработки файлов и создания репортов
    print(file_path)  #для отладки
    # Здесь должна быть логика обработки файла
    #print("Processing file:", file_bytes)
   
    all_results = process_file_from_archive(file_path, file_bytes)
    report = "report_for_onefile.pdf"

    if all_results:
        scan_utils_save_to_pdf(all_results, "Результаты сканирования", report)
    else:
        all_results = []
        scan_utils_save_to_pdf(all_results, "Нет проблем в файле или файл пустой", report)
        
    #report = create_report("report.txt", "Hello world")
    return report


def process_archive(file_path, file_bytes):
# Функция для обработки архивов
    print(file_path)  #для отладки
    #print(f"Тип переменной: {type(file_path)}")
    #print(f"Тип переменной: {type(zip_file)}")   

    try:
        #print(file_bytes)  #для отладки
        #with ZipFile(io.BytesIO(file_bytes), 'r') as archive:
        #    for file in archive.namelist():
        #        print(f"Обработаем файл: {file}")  #для отладки
        #        with archive.open(file) as nested_file:
        #            file_contents = nested_file.readlines()
        #            # Здесь должна быть логика обработки архива
        #
        #report = create_report("report.txt", "Hello world")
        
        report = "report_for_archive.pdf"
        all_results = process_zip_archive(file_path, file_bytes)
        if all_results:
            scan_utils_save_to_pdf(all_results, "Результаты сканирования", report)
        else:
            all_results = []
            scan_utils_save_to_pdf(all_results, "Нет проблем в файлах проекта или архив пустой", report)
    except Exception as write_error:
        #print(f"Ошибка обработки файла={file_path}: {write_error}")
        report = create_report("error.txt", f"Не удалось обработать файл: {write_error}")    

    return report


# Создание бота и обработка сообщений
bot = TeleBot(TOKEN)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    #Загружаем файл
    file_info = bot.get_file(message.document.file_id)
    #print("fФайл: {file_info}")
    downloaded_file = bot.download_file(file_info.file_path)

    if message.document.file_name.endswith('.zip') or message.document.file_name.endswith('.7z') or message.document.file_name.endswith('.rar'):
        #Обработка архива
        #result_report = process_archive(file_info.file_path, downloaded_file)
        result_report = process_archive(message.document.file_name, downloaded_file)
        r_type = "архив"
    else:
        #Обработка одиночного файла
        #result_report = process_file(file_info.file_path, downloaded_file)
        result_report = process_file(message.document.file_name, downloaded_file)
        r_type = "файл"

    bot.reply_to(message, f"Ваш {r_type} был обработан, результаты прикреплены к сообщению.")
    with open(result_report, "rb") as report_file:
        bot.send_document(chat_id=message.chat.id, document=report_file)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для проверки проектов ЕВРАЗ. Отправьте мне файл(*.cs,*.py,*.ts,*.tsx) или архив(*.zip,*.7z) для обработки.")


@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Я не знаю, что делать с этим. Пожалуйста, отправьте мне файл(*.cs,*.py,*.ts,*.tsx) или архив(*.zip,*.7z) для обработки.")

if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()
