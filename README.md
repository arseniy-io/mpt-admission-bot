# Telegram-бот "Приемная комиссия МПТ"

Рабочий MVP Telegram-бота для приемной комиссии Московского приборостроительного техникума РЭУ им. Г.В. Плеханова. Бот работает как интерактивный справочник: показывает главное меню, открывает разделы, вопросы, ответы, карточки специальностей, полезные ссылки и принимает вопросы для администраторов.

## Что уже реализовано

- Команда `/start`.
- Главное меню через Inline-кнопки.
- Разделы из ТЗ: поступление, документы, специальности, вступительные испытания, обучение, сроки приема, общежитие, контакты, частые вопросы, полезные ссылки, задать вопрос.
- Кнопки `Назад` и `Главное меню`.
- База знаний в `data/knowledge_base.json`.
- Список специальностей в `data/specialties.json`.
- Полезные ссылки в `data/links.json`.
- Отправка вопроса пользователя администраторам из `.env`.

## Структура проекта

```text
bot/
  main.py                  # запуск бота
  config.py                # настройки из .env
  keyboards.py             # Inline-кнопки
  messages.py              # основные тексты
  handlers/
    start.py               # /start
    menu.py                # разделы, вопросы, ответы
    ask_question.py        # сценарий "Задать вопрос"
  services/
    content.py             # загрузка JSON-данных
data/
  knowledge_base.json      # вопросы и ответы
  specialties.json         # специальности
  links.json               # полезные ссылки
```

## Установка

Нужен Python 3.10 или новее. В текущей рабочей папке проверена версия Python 3.12.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` рядом с `.env.example`:

```env
BOT_TOKEN=ваш_токен_бота
ADMIN_IDS=123456789,987654321
DATA_DIR=data
TELEGRAM_PROXY_URL=
```

Токен создается через BotFather в Telegram. `ADMIN_IDS` - это Telegram ID администраторов, которым будут приходить вопросы от пользователей. Если администраторы пока неизвестны, поле можно оставить пустым, бот не упадет, но вопросы не будут отправляться приемной комиссии.

Если Telegram API не доступен напрямую, но работает через локальный прокси, заполните `TELEGRAM_PROXY_URL`. Например: `TELEGRAM_PROXY_URL=http://127.0.0.1:10809`.

## Запуск

```bash
python -m bot.main
```

После запуска откройте бота в Telegram и отправьте `/start`.

## Деплой на Koyeb

Проект подготовлен для деплоя через Dockerfile. В Koyeb нужно создать сервис из GitHub-репозитория и указать переменные окружения:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&builder=dockerfile&repository=github.com/arseniy-io/mpt-admission-bot&branch=master&name=mpt-admission-bot&service_type=worker&dockerfile=Dockerfile&env%5BDATA_DIR%5D=data&env%5BTELEGRAM_PROXY_URL%5D=)

```env
BOT_TOKEN=ваш_токен_бота
ADMIN_IDS=
DATA_DIR=data
TELEGRAM_PROXY_URL=
```

На облачном сервере `TELEGRAM_PROXY_URL` обычно должен быть пустым. Локальный прокси `127.0.0.1:10809` нужен только на текущем компьютере, если Telegram API напрямую не открывается.

## Деплой на Render

Render на бесплатном тарифе лучше использовать через webhook, а не через постоянный polling. В проект добавлен `render.yaml`, поэтому Render сможет создать сервис по настройкам из репозитория.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/arseniy-io/mpt-admission-bot)

При создании сервиса Render попросит значение `BOT_TOKEN`. Остальные важные переменные уже описаны в `render.yaml`:

```env
BOT_MODE=webhook
ADMIN_IDS=6360613956
DATA_DIR=data
TELEGRAM_PROXY_URL=
WEBHOOK_PATH=/webhook
```

На Render локальный прокси не нужен, поэтому `TELEGRAM_PROXY_URL` должен быть пустым.

## Как редактировать ответы

Основные тексты лежат не в коде, а в JSON-файлах:

- вопросы и ответы - `data/knowledge_base.json`;
- специальности - `data/specialties.json`;
- полезные ссылки - `data/links.json`.

После изменения JSON-файлов перезапустите бота.

## Что нужно дозаполнить перед реальным запуском

- Точный телефон приемной комиссии.
- Email приемной комиссии.
- Официальный сайт колледжа или ссылка на раздел приемной комиссии.
- Telegram-канал.
- VK.
- Ссылка на карту.
- Telegram ID администраторов.
- Полные карточки специальностей: срок обучения, форма обучения, места, бюджет, вступительные испытания.
- Стоимость обучения.
- Количество бюджетных и платных мест.
- Точные даты вступительных испытаний, публикации рейтингов и приказов, если они будут обновляться ежегодно.

## Источники

Тексты собраны по двум исходным файлам из корня проекта:

- `ТЗ для тг бота.docx`;
- `ответы на вопросы для бота.docx`.

Если информации в документах не было, в боте оставлена заглушка с пометкой, что данные нужно уточнить.
