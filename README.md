# Боты, интегрированные с DialogFlow от Google
Умеют общаться через телеграм или вк, приветствовать и распознавать запрос о поиске работы.
Но всему можно научить при помощи DialogFlow!

- `tg_support_bot.py` - запускает бота в телеграме
- `vk_support_bot.py` - запускает бота в вк
- `telegram_monitoring.py` - модуль для подключения мониторинга ботов и отправке логов в телеграм
- `dialogflow.py` - подбирает ответ через DialogFlow
- `dialogflow_trainer/train_dialogflow.py` модуль по обучению DialogFlow (см. пример `dialogflow_trainer/questions.json`)

## Демо
Телеграм: [@n1k0dinsupport_bot](https://t.me/n1k0dinsupport_bot)

![ТГ](images/demo_tg_bot.gif "ТГ")

ВК: Пишите в ЛС [группы](https://vk.com/club209574488)

![ТГ](images/demo_vk_bot.gif "ТГ")

## Установка и настройка

Для работы необходим Python 3.9 или новее!

### Подготовка скрипта

1. Скачайте код и перейдите в папку проекта.
    ```bash
    git clone https://github.com/n1k0din/support-bot
    ```  
    ```bash
    cd support-bot
    ```
2. Установите вирт. окружение.
    ```bash
    python -m venv venv
    ```
3. Активируйте.
    ```bash
    venv\Scripts\activate.bat
    ```
    или
    ```bash
    source venv/bin/activate
    ```
4. Установите необходимые пакеты.
    ```bash
    pip install -r requirements.txt
    ```

## Подготовьте переменные окружения

Установите следующие переменные окружения (см. `.env.example`):
- `TG_BOT_TOKEN` - Токен ТГ бота получить от [Отца ботов](https://telegram.me/BotFather)
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу с учетными данным для DialogFlow получить от
[google cloud](https://cloud.google.com/docs/authentication/getting-started)
- `DIALOGFLOW_PROJECT_ID` - ИД проекта DialogFlow получить там же
- `VK_TOKEN` - ключ доступа из настроек группы ВК, раздел Работа с API
- `TG_MONITORING_BOT_TOKEN` - Токен ТГ бота для мониторинга
- `TG_NOTIFICATIONS_CHAT_ID` - ИД получателя оповещений получить от [специального бота](https://telegram.me/userinfobot)

## Запуск

```bash
python tg_support_bot.py
```

```bash
python vk_support_bot.py
```

## Деплой на Heroku
- Зарегистрироваться на heroku.com
- [Настроить интеграцию с github](https://devcenter.heroku.com/articles/github-integration)
- Установить переменные окружения во вкладке Settings -> Config vars
   - Для работы с json-ключами от Google см.
[Stackoverflow](https://stackoverflow.com/questions/47446480/how-to-use-google-api-credentials-json-on-heroku) и
[корректный buildpack](https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack)
- Выполнить Manual Deploy -> Deploy Branch
- Не забыть активировать Dyno во вкладке Resources

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
