# 🏎💨 Subaru Welcome Bot

Интерактивный Telegram-бот для модерации и создания атмосферы в Subaru-клубе. Написан на `aiogram 3.x`, полностью упакован в `Docker` и готов к быстрому развертыванию.

## ✨ Ключевые фичи

* **Гей-капча на входе:** Автоматически ограничивает права новых пользователей и предлагает пройти проверку на «истинного субариста». При успехе — встречает легендарным видео `welcome_to_the_club.mp4`. При провале — отправляет в бан.
* **Автоматические триггеры:** Живо реагирует стикерами и цитатами в формате HTML-блоков на ключевые слова (грязь/одобрялово, VPN/прокси, Рок, Русский рэп, Борода, Тёма).
* **Логирование в реальном времени:** Отключена буферизация Python для мгновенного отображения логов в Docker.

---

## 🚀 Быстрый старт (Деплой одной командой)

Скрипт сам создаст нужные директории в `/opt`, склонирует репозиторий, интерактивно запросит переменные окружения (`.env`) и поднимет Docker-контейнеры.

Запустите на вашем Ubuntu-сервере:
```bash
curl -sSL [https://raw.githubusercontent.com/DanielZubov/SubaruWelcomeBot/refs/heads/main/install-BSB.sh](https://raw.githubusercontent.com/DanielZubov/SubaruWelcomeBot/refs/heads/main/install-BSB.sh) -o manage.sh && chmod +x manage.sh && sudo ./manage.sh
```

## 🛠 Ручной деплой (Docker)
### Если вы хотите развернуть бота вручную:

1. Клонируйте репозиторий:

```bash
git clone [https://github.com/DanielZubov/SubaruWelcomeBot.git](https://github.com/DanielZubov/SubaruWelcomeBot.git)
cd SubaruWelcomeBot
```
2. Создайте файл ```.env``` и заполните его:

```bash
SUBARU_BOT_TOKEN=ваш_токен_бота
VIDEO_PATH=/app/media/welcome_to_the_club.mp4
PYTHONUNBUFFERED=1
```
3. Положите ваше приветственное видео в корень папки под именем ```welcome_to_the_club.mp4```.

4. Запустите контейнер:

```bash
docker compose up -d --build
```


Обливайся маслом и погнали! 🏎💨
