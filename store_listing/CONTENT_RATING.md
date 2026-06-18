# Google Play — Data Safety Form (готовые ответы)

Google заполняет эту анкету сам, форма в Console → Policy → App content → Data safety. Ниже — **готовые ответы** для каждой категории, копируй как есть.

---

## Data safety form — ARGOS Mobile Client

### Data collection and security

**Does your app collect or share any of the required user data types?**
→ **No**

(We do not collect or share any user data. All data stays on the user's device or on the user's own server. There is no telemetry, no analytics, no crash reporter, no advertising SDK.)

### Account creation

**Does your app allow users to create an account?**
→ **No**

### In-app purchases

**Does your app contain in-app purchases?**
→ **No**

### Ads

**Does your app contain ads?**
→ **No**

### Other actions

**Does your app allow users to generate content that other users can see?**
→ **No**

**Does your app allow users to send data to other users or share it outside the app?**
→ **No**

**Does your app use any of the following data types?** (Сheckbox list, all of them):
- Account info → unchecked
- App activity → unchecked
- App info and performance → unchecked
- Device or other IDs → unchecked
- Location → unchecked
- Messages → unchecked
- Audio files → unchecked
- Photos and videos → unchecked
- Files and docs → unchecked
- Calendar → unchecked
- Contacts → unchecked
- Health and fitness → unchecked
- Web browsing → unchecked
- App info and performance → unchecked
- Contacts → unchecked
- Personal info → unchecked
- Financial info → unchecked

**Data handling across all categories: all collected data is...**
- Encrypted in transit? → N/A (we don't collect)
- Encrypted at rest? → N/A
- User can request that data is deleted? → N/A
- Followed data deletion request policy? → N/A

### Data deletion URL

**Provide a URL where users can request data deletion:**
→ https://github.com/AvaSiG/argos/blob/main/store_listing/PRIVACY_POLICY.md
(поменяй на реальный URL после публикации Privacy Policy на GitHub Pages)

### Summary for Play Store

"ARGOS does not collect or share any user data. All data stays on the user's device or on the user's own self-hosted server. The developer has no access to any user data."

---

## App content rating (IARC questionnaire)

Заполни в Console → Policy → App content → Content rating → Start questionnaire → Application category = **Utility/Productivity** (Утилиты/Продуктивность).

| Вопрос | Ответ | Обоснование |
|--------|-------|-------------|
| Violence | No | Утилита без графики насилия |
| Sexual content | No | — |
| Language | No | — |
| Controlled substances | No | — |
| Gambling | No | — |
| User-generated content | No | Приложение не позволяет пользователям публиковать контент для других |
| Location sharing | No | — |
| Data sharing with third parties | No | — |
| In-app purchases for digital goods | No | — |
| Ads | No | — |
| Sensitive topics | No | — |
| Mature themes | No | — |
| Horror | No | — |
| Weapons | No | — |
| Tobacco | No | — |

**IARC rating:** Everyone (ESRB) / 3+ (PEGI) / 0+ (USK) — потому что это утилита.

---

## Government / Health / Financial declarations (Console → App content)

- Is this a government app? → **No**
- Is this a health app? → **No**
- Does this app access financial accounts or transactions? → **No**
- Is this app designed for children under 13? → **No, not designed primarily for children** (поставь "Not designed primarily for children"; будет показан на странице приложения)

---

## Privacy policy URL (required)

**Privacy policy URL:** `https://<your-github-pages-url>/PRIVACY_POLICY.md`
Пока не поднял GitHub Pages — подними в репо AvaSiG/argos через gh-pages branch (есть в настройках репо). Либо используй https://raw.githubusercontent.com/AvaSiG/argos/main/store_listing/PRIVACY_POLICY.md как fallback (Google обычно принимает raw GitHub URL).
