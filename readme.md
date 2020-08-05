# Пакет с несколькими скриптами для конвертации txt-файлов в tmx-файлы

Эти скрипты позволяют токенизировать текстовые файлы на предложения, а затем
конвертировать получившиеся файлы в формат tmx (translation memory exchange,
по сути -- xml-файлы), в том числе в формат, понимаемый программой SDL Trados Studio 2017.

## Установка в Windows в терминале Anaconda Prompt

```
$ python -m venv .venv
$ .venv\Scripts\activate.bat  # в терминале Git Bash: source .venv/Scripts/activate
$ python -m pip install --upgrade pip
$ pip install to-tmx
$ python -m nltk.downloader punkt  # для токенизации на русском языке
```
## Внешние зависимости

Пакет устанавливает NLTK. Кроме того, последняя строчка в разделе про установку
скачивает модели для токенизации на предложения из NLTK Corpora. Эта команда может
выдывать предупреждение при исполнении, но все равно работает.

## Использование

Примеры исходных, промежуточных и финальных файлов лежат в репозитории проекта
на Гитхабе в папке ```data/```.

### Токенизация файлов на предложения
```
$ sent-tok "path\file name.txt" language  # английский по умолчанию
```
Например:
```
$ sent-tok "data\Madrid System_eng.txt" english
$ sent-tok "data\Madrid System_rus.txt" russian
```
На выходе получаем два токенизированных на предложения файла, ```Madrid System_eng.txt_sent_tok``` и ```Madrid System_rus.txt_sent_tok```.

Их следует открыть в текстовом редакторе (Notepad++) и проверить, что все токенизировалось
правильно. Обычно ошибок хватает. Нужно, чтобы количество строк в обоих файлов стало одинаковым.

### Конвертация в tmx
```
$ to-tmx "path\file name_eng.txt_sent_tok" "path\file name_rus.txt_sent_tok"
```
Например:
```
$ to-tmx "data\Madrid System_eng.txt_sent_tok" "data\Madrid System_rus.txt_sent_tok"
```
Скрипт создаст файл ```"data\Madrid System_eng-Madrid System_rus.tmx"```.

### Конвертация в tmx, понимаемый программой SDL Trados Studio 2017
```
$ tmx-tradosize "path\file name_eng-file name_rus.tmx "path\file_name_trados_style.tmx"
```
Первый аргумент -- исходный tmx-файл (полученный на предыдущем этапе), второй аргумент -- путь и желаемое название выходящего файла. Например:
```
$ tmx-tradosize "data\Madrid System_eng-Madrid System_rus.tmx" "data\madrid_system_trados_style.tmx"
```

### Конвертация многих файлов в tmx-файлы, понимаемые программой SDL Trados Studio 2017

Команда ```tmx-batch-tradosize``` попросит выбрать папку с несколькими tmx-файлами,
а результат сохранит в папку ```tmx-trados-style\```
