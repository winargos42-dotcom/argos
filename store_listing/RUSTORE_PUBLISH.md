# ARGOS Universal OS — Публикация в RuStore

**Дата:** 2026-06-02
**Статус:** Подготовлен полный пакет, ждёт загрузки.
**Владелец:** ООО "ARGOS" (юрлицо) / ИП / самозанятый — уточни при регистрации.

---

## 1. Что такое RuStore

Российский магазин приложений (VK). Работает с РФ-юрлицами и физлицами **без санкций**, **без $25**, **без проблем с ID verification**.

**Сайт:** https://rustore.ru
**Консоль разработчика:** https://console.rustore.ru

---

## 2. Что нужно подготовить ДО регистрации

- [ ] **ИНН** организации (юрлицо) или физлица (самозанятый / ИП)
- [ ] **ЕГРЮЛ** (для ООО) или **паспорт РФ директора** (для ООО) / **паспорт РФ** (для физлица)
- [ ] **Корпоративная карта** или карта физлица для верификации (RuStore может списать/вернуть 1₽ для проверки)
- [ ] **APK** файл (или AAB) — собираем через `buildozer android release`
- [ ] **Описания** — есть в `STORE_LISTING.md`
- [ ] **Графика** — есть в `assets/`
- [ ] **Privacy Policy URL** — `https://winargos42-dotcom.github.io/argos-play-store/PRIVACY_POLICY.md`

---

## 3. Сборка APK

Проект уже настроен:

```bash
cd /home/ava/Projects/argoss
buildozer android release
```

Файл появится в `.buildozer/android/platform/build/dists/release/bin/argos_universal-2.1.3-release.apk`.

**Подпись:** используй `argos-release.keystore` (есть в репо). Параметры:
- alias: argos
- password: `argos2024` (проверь в buildozer.spec)
- key password: `argos2024`

---

## 4. Регистрация в RuStore Console

### Шаг 1: Создать аккаунт разработчика
1. Открой https://console.rustore.ru
2. Войди через **VK ID** или **Госуслуги** (рекомендую — для юрлиц)
3. Подтверди email и телефон

### Шаг 2: Заполнить профиль разработчика
- **Тип:** Юридическое лицо
- **Полное наименование:** ООО "ARGOS" (как в ЕГРЮЛ)
- **ИНН:** ...
- **КПП:** ...
- **ОГРН:** ...
- **Юридический адрес:** ...
- **Контактное лицо:** Всеволод (или ФИО директора)
- **Email для связи:** winargos42@gmail.com
- **Телефон:** +7...

### Шаг 3: Загрузить документы
- Скан **ЕГРЮЛ** (выписка, не старше 3 месяцев)
- Скан **паспорта директора** (разворот с фото + прописка)
- Если действуешь по доверенности — **доверенность**

### Шаг 4: Подписать соглашение
- Прочитать и принять **оферту RuStore** для разработчиков
- Соглашение о персональных данных

**Срок рассмотрения:** 1-3 рабочих дня.

---

## 5. Загрузка приложения

### Шаг 1: Создать карточку приложения
1. Console → **Мои приложения** → **Добавить приложение**
2. Заполни:
   - **Название:** ARGOS Universal OS
   - **Краткое описание** (до 80 символов): `Local AI · P2P mesh · IoT · Self-heal`
   - **Полное описание** (до 4000 символов): см. `STORE_LISTING.md`
   - **Категория:** Инструменты / Продуктивность
   - **Возрастная категория:** 12+

### Шаг 2: Загрузить графику
- **Иконка 512×512:** `assets/icon_512.png` ✅
- **Скриншоты** (до 8 шт, минимум 2): `assets/screenshots/*.png` ✅
- **Feature graphic 1024×500:** `assets/feature_graphic_1024x500.png` ✅
- **Промо-видео** (опционально): не готово

### Шаг 3: Загрузить APK
- **Версия:** 2.1.3
- **package:** `org.iliyaqdrwalqu.argos`
- Загрузить `.apk` файл
- Указать **targetSdk** (Android 13 / API 33 для современных)
- Заполнить чек-лист самопроверки

### Шаг 4: Privacy Policy
- URL: `https://winargos42-dotcom.github.io/argos-play-store/PRIVACY_POLICY.md`
- ✅ уже опубликовано

### Шаг 5: Отправить на модерацию
- **Срок:** 1-3 рабочих дня
- **Комментарий для модератора:** «Local AI orchestrator, P2P mesh, IoT control panel. No data collection beyond local network.»

---

## 6. После публикации

- Скачивание начнётся автоматически
- Статистика: Console → Аналитика
- Обновления: загружаешь новую версию APK + changelog
- Монетизация: реклама VK Ads / подписки (если нужны)

---

## 7. Что я (Hermes) уже подготовил

- ✅ `STORE_LISTING.md` — все тексты (RU + EN)
- ✅ `PRIVACY_POLICY.md` — политика конфиденциальности
- ✅ `CONTENT_RATING.md` — возрастной рейтинг (12+)
- ✅ `PUBLISH_GUIDE.md` — общий гайд
- ✅ `assets/icon_512.png` + 192, 48
- ✅ `assets/feature_graphic_1024x500.png`
- ✅ `assets/promo_1024x500.png`
- ✅ `assets/tv_banner_1280x720.png`
- ✅ `assets/tablet_7_landscape.png`
- ✅ `assets/tablet_10_landscape.png`
- ✅ `assets/adaptive_icon_foreground_432.png`
- ✅ `assets/adaptive_icon_background_432.png`
- ✅ `assets/screenshots/01_dashboard.png` ... `05_heal.png`
- ✅ `buildozer.spec` — конфиг сборки
- ✅ `argos-release.keystore` — ключ подписи
- ✅ Privacy Policy хостится на GitHub Pages (200 OK)

## 8. Что нужно от тебя

- [ ] Зайти в https://console.rustore.ru
- [ ] Зарегистрировать ООО "ARGOS" как разработчика
- [ ] Загрузить ЕГРЮЛ + паспорт директора
- [ ] Дождаться верификации (1-3 дня)
- [ ] Создать карточку приложения
- [ ] Скопировать тексты из STORE_LISTING.md
- [ ] Загрузить APK
- [ ] Отправить на модерацию

---

## 9. Бонус: альтернативные магазины (для подстраховки)

Параллельно можно опубликовать в:
- **F-Droid** (open-source, бесплатно, https://f-droid.org) — нужен публичный Git-репо
- **Huawei AppGallery** (https://developer.huawei.com) — бесплатно, паспорт РФ = ОК
- **Samsung Galaxy Store** (https://seller.samsungapps.com) — бесплатно
- **APK direct** — загрузить APK на свой сайт + QR-код (полный контроль)

**Все эти варианты НЕ требуют $25 и принимают паспорт РФ для ООО "ARGOS".**
