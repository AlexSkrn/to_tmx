# Пакет с несколькими скриптами для конвертации txt-файлов в tmx-файлы

Эти скрипты я написал для собственного использования. Они позволяют токенизировать
текстовые файлы на предложения, а затем конвертировать получившиеся файлы в формат
tmx (translation memory exchange, а по сути -- xml-файлы), в том числе в формат,
понимаемый программой SDL Trados Studio 2017.

## Установка в Windows в терминале Git Bash

```
$ git clone https://github.com/AlexSkrn/to_tmx.git
$ python -m venv .venv
$ source .venv/bin/activate  # в терминале Anaconda Prompt: .venv\Scripts\activate.bat
$ python to_tmx/setup.py sdist bdist_wheel
$ pip install to_tmx
```

## Внешние зависимости

Пакет устанавливает NLTK.

## Использование

Примеры исходных, промежуточных и финальных файлов лежатт в папке ```data/```.

### Токенизация файлов на предложения
```
$ python -m to_tmx.sent_tok data/"Madrid System_eng.txt" english  # английский по умолчанию
$ python -m to_tmx.sent_tok data/"Madrid System_rus.txt" russian
```
На выходе получаем два токенизированных на предложения файла, ```Madrid System_eng.txt_sent_tok```
и ```Madrid System_rus.txt_sent_tok```.

Их следует открыть в текстовом редакторе (я для этого использую Notepad++) и проверить,
что все токенизировалось правильно. Обычно ошибок хватает. Нужно, чтобы количество
строк в обоих файлов стало одинаковым.

### Конвертация в tmx
```
$ python -m to_tmx.to_tmx data/"Madrid System_eng.txt_sent_tok" data/"Madrid System_rus.txt_sent_tok"
```
Скрипт создаст файл ```data/"Madrid System_eng-Madrid System_rus.tmx"```.

### Конвертация в tmx, понимаемый программой SDL Trados Studio 2017
```
$ python to_tmx.tmx_tradosizer data/"Madrid System_eng-Madrid System_rus.tmx data/madrid_system_trados_style.tmx"
```
Первый аргумент -- исходный tmx-файл (полученный на предыдущем этапе), второй аргумент -- путь
и желаемое название выходящего файла.

Кроме того, есть скрипт ```to_tmx.tmx_batch_tradosizder```, который попросит выбрать
папку с несколькими tmx-файлами, а результат сохранит в папку ```tmx-trados-style/```
