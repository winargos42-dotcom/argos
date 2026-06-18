# ARGOS → Google Play Console — пошаговая публикация

Это **инструкция для тебя** (Всеволода), что нажимать в Play Console после верификации личности. Не надо гадать — открой Console, иди по пунктам сверху вниз.

---

## 0. До начала (нужны заранее)

- [x] Google-аккаунт **winargos42@gmail.com** (Argoswin) — есть
- [x] Оплата $25 — сделана
- [ ] **Верификация личности** — загрузить паспорт РФ (внутр. или загран). Жми "Начать" на той странице, что сейчас на телефоне. 1-3 дня.
- [ ] **Иконка приложения 512×512 PNG** (без прозрачности, без альфа-канала). Можешь взять текущий round_icon из `llama.cpp/examples/llama.android/app/src/main/res/.../ic_launcher_round.png` и сгенерировать нужные размеры через Android Studio Image Asset Studio или aapt2.
- [ ] **Feature graphic 1024×500 PNG** — баннер для Play Store.
- [ ] **Минимум 2 скриншота** телефона (можно сделать через `adb exec-out screencap -p` после того как соберёшь APK и установишь на телефон).
- [ ] **App bundle (AAB) для загрузки** — Android Studio → Build → Generate Signed Bundle / APK. Подпишешь своим keystore (создай новый, сохрани в надёжном месте).
- [ ] **Privacy Policy URL** — поднять `store_listing/PRIVACY_POLICY.md` на GitHub Pages репозитория AvaSiG/argos, ветка `gh-pages`.

---

## 1. Create app

Play Console → "Все приложения" → "Создать приложение"
- App name: `ARGOS — Local AI Console`
- Default language: Russian (русский)
- App or game: **App**
- Free or paid: **Free**

Жми "Создать".

---

## 2. Set up your app (левая панель внизу — "Настроить приложение")

### 2.1 App access
- All functionality is available without special access? → **No** (требуется доступ к твоему собственному серверу)
- Поля: добавь инструкцию, что юзер должен запустить ARGOS-сервер на своём оборудовании

### 2.2 Ads
- Contains ads? → **No**

### 2.3 Content rating
- Заполни IARC questionnaire (готовые ответы — в `CONTENT_RATING.md`)

### 2.4 Government app
- Is this a government app? → **No**

### 2.5 Health apps
- Is this a health app? → **No**

### 2.6 Data safety
- Заполни Data Safety form (готовые ответы — в `CONTENT_RATING.md`)
- Privacy policy URL: `https://<твой-gh-pages>/PRIVACY_POLICY.md`
- Data deletion URL: тот же

### 2.7 Financial features
- App facilitates transactions for digital goods? → **No**
- App purchases physical goods? → **No**
- App facilitates financial transactions? → **No**

### 2.8 Families
- Designed primarily for children? → **No** (отметь "Not designed primarily for children")

### 2.9 App category
- Category: Tools
- Tags: developer-tools, networking

### 2.10 Store listing
- Short description: см. `STORE_LISTING.md`
- Full description: см. `STORE_LISTING.md`
- App icon: 512×512 PNG
- Feature graphic: 1024×500 PNG
- Phone screenshots: минимум 2

### 2.11 Contact details
- Email: winargos42@gmail.com
- Website: https://github.com/AvaSiG/argos (поменяй на реальный)
- Phone: оставь пустым (необязательно)

### 2.12 Pricing & distribution
- App is free: **Yes**
- Countries: выбери **Россия + весь мир** или конкретные
- Contains ads: **No**
- Designed for children: **No**

---

## 3. Release → Production → Create new release

- Upload AAB (App Bundle)
- Release name: `1.0.0`
- Release notes (What's new): "Initial public release."
- Rollout: 100% (или начни с 5% для теста)

Жми "Review release" → "Start rollout to Production".

---

## 4. Review and roll out

Все разделы настройки (Setup) должны быть зелёными (галочки). Если что-то красное — спрашивай, я подскажу, какой пункт не закрыт.

---

## 5. После публикации

- Google отправит на winargos42@gmail.com уведомление
- Через 1-3 дня приложение появится в Play Store
- Имя пакета (applicationId) лучше иметь в стиле `ru.argos.console` или `com.avasig.argos.client`

---

## Если что-то отказывают

Google редко отказывает, но если пришёл отказ:
- **"Privacy policy URL not accessible"** — проверь, что URL открывается без логина
- **"App does not declare required permissions in manifest"** — пришли манифест своего APK, посмотрим
- **"Icon does not meet guidelines"** — иконка 512×512 PNG, без альфа-канала, без скруглений (Play Store их сам добавляет)
- **"Description contains prohibited content"** — убери все обещания "100% uptime", "best", "AI-powered" в превосходной степени

Если что-то непонятно — скинь мне скриншот того, что Google пишет.
