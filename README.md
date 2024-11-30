# hakaton_prl_evraz

Проект чат-бота Телеграм для Хакатона Евраз 3.0
Чат-бот позволяет загрузить архивы (в форматах ZIP-*.zip, 7Z-*.7z) или отдельные файлы с кодом на языках C#(*.cs), Python(*.py), TypeScript(*.ts, *.tsx)
и выполнить определенный набор проверок кода для проверки качества кода и проекта в целом.
Текущая реализация позволяет выполнять следующие проверки:
~наличие комментариев к классам, методам классов, функциям (для файлов *.cs, *.py, *.ts, *.tsx)
~следование нотации CamelCase для файлов *.ts, *.tsx

Отчет по анализу архива выгружается в файле report_many.pdf
Отчет по анализу отдельного файла выгружается в файле report_one.pdf
Используемые технологии: Python 3.12 + библиотеки:
aiogram==3.11.0
python-decouple~=3.8
telebot~=0.0.5
requests~=2.31.0
rarfile
py7zr
requests
fpdf

Автор: Павлов Р.Л.
