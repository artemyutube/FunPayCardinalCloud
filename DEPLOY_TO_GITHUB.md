# 🚀 Как загрузить на GitHub и развернуть на Render

## ШАГ 1: Подготовка на GitHub

### Вариант A: Создание нового репо (рекомендуется)

1. **Зайди на GitHub**: https://github.com/new

2. **Заполни форму**:
   - Repository name: `FunPayCardinal-Render` (или свое имя)
   - Description: "FunPay Cardinal с автоматическим поднятием лотов на Render"
   - Выбери `Public` или `Private`
   - ☐ Не создавай README (у нас уже есть)
   - ☐ Не создавай .gitignore (у нас уже есть)

3. **Нажми "Create repository"**

### Вариант B: Fork существующего репо

Если хочешь форкнуть оригинальный Cardinal:
1. Зайди на https://github.com/sidor0912/FunPayCardinal
2. Нажми кнопку "Fork"
3. Клонируй forked репо к себе

---

## ШАГ 2: Загрузка файлов на GitHub

### Вариант A: Через Git в командной строке (лучше)

```bash
# 1. Создай папку для проекта
mkdir FunPayCardinal-Render
cd FunPayCardinal-Render

# 2. Инициализируй Git репо
git init

# 3. Добавь вели из GitHub (скопируй URL со страницы репо)
git remote add origin https://github.com/ТВОЙ_НИК/FunPayCardinal-Render.git

# 4. Создай основную ветку
git branch -M main

# 5. Скопируй ВСЕ ЭТИ ФАЙЛЫ в эту папку:
#    - main.py
#    - auto_bump_scheduler.py
#    - keep_alive.py
#    - requirements.txt
#    - Procfile
#    - .env.example
#    - .gitignore
#    - README_RENDER.md
#    - (и другие файлы если есть)

# 6. Добавь файлы в Git
git add .

# 7. Сделай первый коммит
git commit -m "Initial commit: FunPay Cardinal with Auto-Bump Scheduler for Render"

# 8. Загрузи на GitHub
git push -u origin main
```

### Вариант B: Через веб-интерфейс GitHub

Если нет Git на компе:

1. Открой свой репо на GitHub
2. Нажми **"Add file"** → **"Upload files"**
3. Перетащи или выбери файлы:
   - main.py
   - auto_bump_scheduler.py
   - keep_alive.py
   - requirements.txt
   - Procfile
   - .env.example
   - .gitignore
   - README_RENDER.md
4. Напиши сообщение: "Initial commit: Add Cardinal with Auto-Bump"
5. Нажми **"Commit changes"**

---

## ШАГ 3: Развертывание на Render

### 1. Зайди на Render

Перейди на https://render.com

Если нет аккаунта - создай (можно через GitHub, это удобнее)

### 2. Создай новый Web Service

1. Нажми **"New +"** в левом меню
2. Выбери **"Web Service"**
3. Нажми **"Connect a repository"** и авторизируй GitHub
4. Выбери свой репо `FunPayCardinal-Render`
5. Нажми **"Connect"**

### 3. Настройка сервиса

Заполни поля:

**Name:**
```
funpay-cardinal-bot
```

**Environment:**
```
Python 3
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python main.py
```

**Instance Type:**
```
Free (можешь позже upgrade)
```

### 4. Добавь Environment Variables

Нажми **"Add Environment Variable"** и добавь:

```
FUNPAY_USERNAME = твое_имя_funpay
FUNPAY_PASSWORD = твой_пароль_funpay
TELEGRAM_BOT_TOKEN = твой_токен_бота
TELEGRAM_CHAT_ID = твой_чат_ID
AUTO_BUMP_INTERVAL = 4
ENABLE_AUTO_BUMP = true
ENABLE_KEEP_ALIVE = true
RENDER_DEPLOYMENT = true
```

**Как получить значения:**

- **FUNPAY_USERNAME** и **FUNPAY_PASSWORD**:
  - Твои учетные данные на FunPay.com
  
- **TELEGRAM_BOT_TOKEN**:
  1. Напиши @BotFather в Telegram
  2. Команда `/newbot`
  3. Следуй инструкциям
  4. Скопируй токен
  
- **TELEGRAM_CHAT_ID**:
  1. Напиши @userinfobot в Telegram
  2. Он пришлет твой ID
  3. Используй это значение

### 5. Deploy!

Нажми кнопку **"Create Web Service"**

Жди 2-3 минуты пока приложение собирается...

✅ **Готово!**

---

## ✅ Проверка работы

### На странице Render

1. Открой свой сервис
2. Переходи в вкладку **"Logs"**
3. Ищи эти сообщения:

```
🀑 FunPay Cardinal запускается
✅ Cardinal инициализирован
✅ Все компоненты инициализированы
🚀 Запускаю Cardinal...
✅ Keep-alive запущен
✅ Scheduler инициализирован
πŸ"„ Keep-alive ping - АКТИВНО
```

Если видишь эти сообщения - **ВСЕ РАБОТАЕТ!** 🎉

---

## πŸ"„ Обновления кода

Если нужно обновить код:

### Через Git

```bash
# 1. Сделай изменения в файлах

# 2. Добавь их в Git
git add .

# 3. Сделай коммит
git commit -m "Updated: [описание изменений]"

# 4. Загрузи на GitHub
git push

# Render автоматически пересборит приложение!
```

### Через веб-интерфейс

1. На GitHub отредактируй нужные файлы
2. Коммитни изменения
3. Render автоматически пересборит через несколько минут

Проверь логи чтобы убедиться что все ОК.

---

## πŸ›' Остановка/Перезапуск

На странице сервиса на Render есть кнопки:

- **Restart** - перезапустить приложение
- **Suspend** - приостановить (останавливает начисления)
- **Delete** - удалить сервис

---

## πŸ'° Стоимость

**Free Tier:**
- ✅ Бесплатно до 750 часов в месяц
- βœ… Достаточно для одного бота 24/7
- ⚠️ Выключается через 15 минут неактивности (наш keep-alive решает)

**Если нужно лучше:**
- **Standard**: $7/месяц - нет выключения, лучше перформанс
- **Pro**: $12/месяц - еще лучше

---

## 🚨 Проблемы при развертывании

### "Build failed"

**Решения:**
1. Проверь requirements.txt - нет ли опечаток
2. Нажми на Render "Clear Build Cache" потом "Redeploy"
3. Посмотри весь лог ошибок (там будет указано что не так)

### "Service can't start"

**Решения:**
1. Проверь что все environment variables заполнены
2. Проверь что Python version 3.8+
3. Посмотри логи ошибок в разделе "Logs"

### "No module named..."

**Решения:**
1. Убедись что нужный модуль в requirements.txt
2. Clear Build Cache на Render
3. Redeploy

### Бот запускается но ничего не делает

**Решения:**
1. Проверь что environment variables верные
2. Посмотри логи на предмет ошибок
3. Убедись что в main.py правильно интегрирован твой API код

---

## πŸ"— Полезные команды для Git

```bash
# Посмотреть статус
git status

# Посмотреть что изменилось
git diff

# Посмотреть историю коммитов
git log

# Откатить последний коммит (если нужно)
git reset --soft HEAD~1

# Посмотреть список файлов в репо
git ls-files
```

---

## πŸ"' Безопасность

⚠️ **ВАЖНО:**
- **Никогда** не добавляй пароли прямо в код
- Используй только Environment Variables на Render
- Если случайно добавил пароль в Git:
  1. Смени пароль FunPay
  2. Смени токен Telegram бота
  3. Удали старый коммит (сложнее, гугли "git filter-branch")

---

## πŸ"ž Если что-то не работает

1. **Посмотри логи** на Render (вкладка "Logs")
2. **Убедись** что все Environment Variables заполнены
3. **Проверь** что репо на GitHub имеет все нужные файлы
4. **Restart** сервис на Render
5. **Написать** в чат Cardinal если совсем помощь нужна

---

## πŸŽ‰ Готово!

Твой бот теперь:
- ✅ Запущен на Render
- ✅ Поднимает лоты каждые 4 часа
- ✅ Работает 24/7
- ✅ Не выключается на Render

**Удачи!** 🚀

---

**Вопросы?**
- Telegram: https://t.me/funpay_cardinal
- GitHub Issues: https://github.com/твой_ник/FunPayCardinal-Render/issues
