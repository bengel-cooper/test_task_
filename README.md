# test_task_DataInsight
В репозитории находится выполненные тестовые задания (основное и дополнительное задания).

В качестве базы данных используется локальная база PostgreSQL, в которой с помощью Python кода создается схема 'test' и таблица 'gplay_stats'.

![Скриншот таблицы из базового задания](https://github.com/bengel-cooper/test_task_DataInsight/blob/main/table_screenshot.PNG)
![Скриншот таблицы из дополнительного задания](https://github.com/bengel-cooper/test_task_DataInsight/blob/main/optional_table_screenshot.PNG)


В скрипт test_task_optional.py были добавлены 3 дополнительных поля: description, updated, rating
- В поле description содержится краткая информация из описания страницы
- В поле updated указана дата последнего обновления таблицы
- В поле rating указан рейтинг приложения. Важно обратить внимание на то, что рейтинг представлен в формате ![IARC Generic](https://support.google.com/googleplay/android-developer/answer/9859655?hl=en) и подходит для данного задания, но в случае использования других региональных настроек (не РФ, Армения), код, вероятно, необходимо будет отредактировать, убрав обрезку строки для данного поля в dataframe. Обрезка строки была добавлена для упрощения чтения данных.
