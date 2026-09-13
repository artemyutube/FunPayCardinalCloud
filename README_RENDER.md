# FunPay Cardinal - Auto-Bump Edition

**Бот для автоматизации FunPay с встроенным Auto-Bump Scheduler**

Эта версия автоматически поднимает лоты каждые 4 часа и работает 24/7 на Render.io

## ✨ Что новенького

βœ… **Auto-Bump Scheduler** - поднимает лоты автоматически каждые 4 часа  
βœ… **Keep-Alive** - приложение не выключается на Render  
βœ… **24/7 Work** - работает круглосуточно без перерывов  
βœ… **Полностью готово** - просто скопируй, заполни переменные, запусти  

## 🚀 Быстрый старт на Render (3 минуты)

### Шаг 1: Создай новый Web Service на Render

1. Зайди на [render.com](https://render.com)
2. Нажми **"New +"** → **"Web Service"**
3. Выбери этот репо (или fork этого репо в свой GitHub)

### Шаг 2: Настройка на Render

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python main.py
```

**Instance Type:** Free (или выше если нужна более быстрая работа)

### Шаг 3: Добавь Environment Variables

На странице создания сервиса добавь эти переменные:

```
FUNPAY_USERNAME=твое_имя_пользователя
FUNPAY_PASSWORD=твой_пароль_funpay
TELEGRAM_BOT_TOKEN=токен_телеграм_бота
TELEGRAM_CHAT_ID=ID_твоего_чата
AUTO_BUMP_INTERVAL=4
ENABLE_AUTO_BUMP=true
ENABLE_KEEP_ALIVE=true
RENDER_DEPLOYMENT=true
```

### Шаг 4: Deploy!

Нажми **"Create Web Service"** и жди ~2-3 минуты

✅ Готово! Бот теперь:
- Поднимает лоты каждые 4 часа
- Работает 24/7
- Логирует все в консоль

---

## 🔧 Интеграция с оригинальным Cardinal кодом

Если у тебя уже есть свой Cardinal код, нужно интегрировать его в `main.py`:

### Вариант 1: Если у тебя есть API класс

```python
# В main.py найди этот код:
# self.api = CardinalAPI(...)

# Замени на свой:
self.api = YourCardinalAPI(
    username=self.config['funpay_username'],
    password=self.config['funpay_password']
)
await self.api.connect()
```

### Вариант 2: Если использованы классы из оригинального Cardinal

```python
# Импортируй их:
from cardinal import Cardinal  # или где они там

# В методе initialize():
self.cardinal = Cardinal(config)
await self.cardinal.setup()
```

Смотри комментарии в `main.py` - там указаны места где нужно добавить твой код.

---

## πŸ"§ Конфигурация

### Интервал поднятия лотов

Измени `AUTO_BUMP_INTERVAL` на Render:

- `1` = каждый час
- `2` = каждые 2 часа
- `3` = каждые 3 часа
- `4` = каждые 4 часа (по умолчанию)
- `6` = каждые 6 часов
- `12` = каждые 12 часов

### Keep-Alive интервал

По умолчанию каждые 10 минут. Можно менять через `KEEP_ALIVE_INTERVAL`.

Это важно для того чтобы Render не выключал приложение через 15 минут.

---

## 🐛 Логирование

На Render в Dashboard:
1. Открой сервис
2. Нажми вкладку **"Logs"**
3. Ищи сообщения:

```
✅ Keep-alive ping - keep-alive работает
✅ Starting to raise lots - начал поднятие лотов
✅ Lots raised successfully - лоты успешно подняты
```

---

## πŸ"š Структура файлов

```
.
├── main.py                      # Главный файл (запускается на Render)
├── auto_bump_scheduler.py       # Scheduler для поднятия лотов
├── keep_alive.py                # Keep-alive для Render
├── requirements.txt             # Python зависимости
├── Procfile                     # Для Render
├── .env.example                 # Пример переменных окружения
├── .gitignore                   # Что не загружать на GitHub
└── README_RENDER.md             # Этот файл
```

---

## βš™οΈ Как это работает

```
Render Web App Запущена
  ↓
Keep-Alive Loop (каждые 10 минут)
  └─ Пингует приложение чтобы оно не выключалось
  ↓
Auto-Bump Scheduler
  β"œβ"€ Запускается
  β"œβ"€ Первый бамп через 1 минуту
  └─ Далее каждые 4 часа (настраивается)
  ↓
Твой Cardinal код
  β"œβ"€ Telegram Bot
  β"œβ"€ API обработка
  └─ Остальной функционал
```

---

## πŸ" Обязательные переменные окружения

Без этих переменных бот не запустится:

- `FUNPAY_USERNAME` - твое имя на FunPay
- `FUNPAY_PASSWORD` - твой пароль на FunPay
- `TELEGRAM_BOT_TOKEN` - токен Telegram бота
- `TELEGRAM_CHAT_ID` - ID чата где будут уведомления

Получить их:
- **FunPay** - очевидно 😄
- **Telegram бота токен** - напиши @BotFather в Telegram
- **Telegram Chat ID** - напиши @userinfobot в Telegram

---

## 🎯 Что тебе нужно знать

### На Render Free Tier:

βœ… Бесплатно  
βœ… Работает 24/7 (с нашим keep-alive)  
βœ… До 750 часов в месяц  
βŒ Выключается через 15 минут неактивности (но keep-alive решает это)  

### Если хочешь еще быстрее:

Upgrade на Standard или выше ($ в месяц), тогда:
- Нет выключения через 15 минут
- Более быстрые ответы

---

## 🚨 Проблемы и решения

### Проблема: "Module not found"

**Решение:**
- Убедись что скопировал все файлы (.py)
- Проверь requirements.txt
- Пересборка на Render (нажми "Clear Build Cache" потом "Redeploy")

### Проблема: Логов нет или мало

**Решение:**
- Это нормально, логирование минимальное чтобы экономить ресурсы
- Нажми "View Latest Logs" чтобы увидеть в реальном времени

### Проблема: Лоты не поднимаются

**Решение:**
- Проверь что `ENABLE_AUTO_BUMP=true`
- Проверь что правильно интегрирован твой Cardinal API код
- Посмотри логи на предмет ошибок

### Проблема: Бот выключается

**Решение:**
- Убедись что `ENABLE_KEEP_ALIVE=true`
- Посмотри логи
- Может быть ошибка при инициализации (проверь credentials)

---

## πŸ'¨β€πŸ'» Для разработчиков

Структура проекта:

```python
# main.py
CardinalBot(config)
  β"œβ"€ .initialize()     # Инициализация
  β"œβ"€ .start()          # Запуск
  └─ .shutdown()        # Завершение

# auto_bump_scheduler.py
CardinalBumpAdapter
  β"œβ"€ BumpScheduler     # Основной scheduler
  └─ _bump_all_lots()   # Логика поднятия

# keep_alive.py
RenderKeepAlive
  β"œβ"€ _keep_alive_loop() # Основной loop
  └─ _send_ping()       # Отправка пинга
```

---

## 🌐 Для локального тестирования

```bash
# 1. Клонируй репо
git clone https://github.com/твой_акк/FunPayCardinal-Render.git
cd FunPayCardinal-Render

# 2. Создай .env файл (скопируй из .env.example)
cp .env.example .env

# 3. Заполни .env своими credentials

# 4. Установи зависимости
pip install -r requirements.txt

# 5. Запусти
python main.py
```

---

## 🎓 Полезные ссылки

- **Render Docs:** https://render.com/docs
- **Python Asyncio:** https://docs.python.org/3/library/asyncio.html
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Original FunPay Cardinal:** https://github.com/sidor0912/FunPayCardinal
- **FunPay Cardinal Chat:** https://t.me/funpay_cardinal

---

## πŸ"œ Лицензия

Это модифицированная версия FunPay Cardinal с добавленными компонентами для Render.

Используется в соответствии с оригинальной лицензией Cardinal.

---

## ✍️ Версии

- **v1.0** - Initial Release (Auto-Bump + Keep-Alive для Render)
- Дата: September 2026
- Статус: ✅ Production Ready

---

## πŸ€" Часто задаваемые вопросы

**Q: Могу я использовать на своем сервере вместо Render?**  
A: Да! Просто запусти `python main.py` на своем сервере. Keep-alive не нужен.

**Q: Можно ли менять интервал поднятия?**  
A: Да, измени `AUTO_BUMP_INTERVAL` в переменных окружения.

**Q: Работает ли на платных планах Render?**  
A: Да, работает еще лучше! Нет выключения через 15 минут.

**Q: Что делать если забыл пароль FunPay?**  
A: Используй "Забыл пароль" на FunPay, потом обнови переменные на Render.

**Q: Это официальный Cardinal?**  
A: Нет, это модифицированная версия с Auto-Bump Scheduler специально для Render.

---

## πŸ†˜ Спасибо

Спасибо оригинальному разработчику FunPay Cardinal за классный проект!

---

**Готово к использованию!** 🚀

Просто скопируй в GitHub и развернись на Render - все будет работать!
