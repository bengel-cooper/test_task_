# test_task_DataInsight
В репозитории находятся выполненные тестовые задания (основное и дополнительное задания).

В качестве базы данных используется локальная база PostgreSQL, в которой с помощью Python кода создается схема 'test' и таблица 'gplay_stats'.

Скриншот таблицы из базового задания:
![Скриншот таблицы из базового задания](https://github.com/bengel-cooper/test_task_DataInsight/blob/main/table_screenshot.PNG)

Скриншот таблицы из дополнительного задания:
![Скриншот таблицы из дополнительного задания](https://github.com/bengel-cooper/test_task_DataInsight/blob/main/optional_table_screenshot.PNG)


В скрипт test_task_optional.py были добавлены 3 дополнительных поля: description, updated, rating
- В поле description содержится краткая информация из описания страницы
- В поле updated указана дата последнего обновления приложения в Google Play
- В поле rating указан рейтинг приложения. Важно обратить внимание на то, что рейтинг представлен в системе <a href="https://support.google.com/googleplay/android-developer/answer/9859655?hl=en">IARC Generic</a> и подходит для данного задания, но в случае использования других региональных настроек (не Армения и некоторые другие страны), код, вероятно, необходимо будет отредактировать, убрав обрезку строки для данного поля в dataframe, а также увеличив максимальный размер ячейки в поле PosgreSQL таблицы(сейчас он составляет 5 символов). Обрезка строки была добавлена для упрощения чтения данных.
