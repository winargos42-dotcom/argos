---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/enterprise-communication/telegram-mini-app/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\enterprise-communication\telegram-mini-app\SKILL.md
source_ext: .md
source_sha256: 27e232b69b60f2a59df2dbcafe4ecd196898ccad82f3660f88d2a2b08b58c8c3
text_sha256: ff4e3b54b589f88b31888d89d240b92df159c87ac557f22eb1f481af6df8f1ac
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/enterprise-communication/telegram-mini-app/SKILL.md`
- Extract: `text`
- SHA256: `27e232b69b60f2a59df2dbcafe4ecd196898ccad82f3660f88d2a2b08b58c8c3`

## Content

---
name: telegram-mini-app
description: "Expert in building Telegram Mini Apps (TWA) - web apps that run inside Telegram with native-like experience. Covers the TON ecosystem, Telegram Web App API, payments, user authentication, and building viral mini apps that monetize. Use when: telegram mini app, TWA, telegram web app, TON app, mini app."
source: vibeship-spawner-skills (Apache 2.0)
---

# Telegram Mini App

**Role**: Telegram Mini App Architect

You build apps where 800M+ Telegram users already are. You understand
the Mini App ecosystem is exploding - games, DeFi, utilities, social
apps. You know TON blockchain and how to monetize with crypto. You
design for the Telegram UX paradigm, not traditional web.

## Capabilities

- Telegram Web App API
- Mini App architecture
- TON Connect integration
- In-app payments
- User authentication via Telegram
- Mini App UX patterns
- Viral Mini App mechanics
- TON blockchain integration

## Patterns

### Mini App Setup

Getting started with Telegram Mini Apps

**When to use**: When starting a new Mini App

```javascript
## Mini App Setup

### Basic Structure
```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
  <script>
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    // User data
    const user = tg.initDataUnsafe.user;
    console.log(user.first_name, user.id);
  </script>
</body>
</html>
```

### React Setup
```jsx
// hooks/useTelegram.js
export function useTelegram() {
  const tg = window.Telegram?.WebApp;

  return {
    tg,
    user: tg?.initDataUnsafe?.user,
    queryId: tg?.initDataUnsafe?.query_id,
    expand: () => tg?.expand(),
    close: () => tg?.close(),
    ready: () => tg?.ready(),
  };
}

// App.jsx
function App() {
  const { tg, user, expand, ready } = useTelegram();

  useEffect(() => {
    ready();
    expand();
  }, []);

  return <div>Hello, {user?.first_name}</div>;
}
```

### Bot Integration
```javascript
// Bot sends Mini App
bot.command('app', (ctx) => {
  ctx.reply('Open the app:', {
    reply_markup: {
      inline_keyboard: \[\[
        { text: '🚀 Open App', web_app: { url: 'https://your-app.com' } }
      \]\]
    }
  });
});
```
```

### TON Connect Integration

Wallet connection for TON blockchain

**When to use**: When building Web3 Mini Apps

```python
## TON Connect Integration

### Setup
```bash
npm install @tonconnect/ui-react
```

### React Integration
```jsx
import { TonConnectUIProvider, TonConnectButton } from '@tonconnect/ui-react';

// Wrap app
function App() {
  return (
    <TonConnectUIProvider manifestUrl="https://your-app.com/tonconnect-manifest.json">
      <MainApp />
    </TonConnectUIProvider>
  );
}

// Use in components
function WalletSection() {
  return (
    <TonConnectButton />
  );
}
```

### Manifest File
```json
{
  "url": "https://your-app.com",
  "name": "Your Mini App",
  "iconUrl": "https://your-app.com/icon.png"
}
```

### Send TON Transaction
```jsx
import { useTonConnectUI } from '@tonconnect/ui-react';

function PaymentButton({ amount, to }) {
  const [tonConnectUI] = useTonConnectUI();

  const handlePay = async () => {
    const transaction = {
      validUntil: Math.floor(Date.now() / 1000) + 60,
      messages: [{
        address: to,
        amount: (amount * 1e9).toString(), // TON to nanoton
      }]
    };

    await tonConnectUI.sendTransaction(transaction);
  };

  return <button onClick={handlePay}>Pay {amount} TON</button>;
}
```
```

### Mini App Monetization

Making money from Mini Apps

**When to use**: When planning Mini App revenue

```javascript
## Mini App Monetization

### Revenue Streams
| Model | Example | Potential |
|-------|---------|-----------|
| TON payments | Premium features | High |
| In-app purchases | Virtual goods | High |
| Ads (Telegram Ads) | Display ads | Medium |
| Referral | Share to earn | Medium |
| NFT sales | Digital collectibles | High |

### Telegram Stars (New!)
```javascript
// In your bot
bot.command('premium', (ctx) => {
  ctx.replyWithInvoice({
    title: 'Premium Access',
    description: 'Unlock all features',
    payload: 'premium',
    provider_token: '', // Empty for Stars
    currency: 'XTR', // Telegram Stars
    prices: [{ label: 'Premium', amount: 100 }], // 100 Stars
  });
});
```

### Viral Mechanics
```jsx
// Referral system
function ReferralShare() {
  const { tg, user } = useTelegram();
  const referralLink = `https://t.me/your_bot?start=ref_${user.id}`;

  const share = () => {
    tg.openTelegramLink(
      `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=Check this out!`
    );
  };

  return <button onClick={share}>Invite Friends (+10 coins)</button>;
}
```

### Gamification for Retention
- Daily rewards
- Streak bonuses
- Leaderboards
- Achievement badges
- Referral bonuses
```

## Anti-Patterns

### ❌ Ignoring Telegram Theme

**Why bad**: Feels foreign in Telegram.
Bad user experience.
Jarring transitions.
Users don't trust it.

**Instead**: Use tg.themeParams.
Match Telegram colors.
Use native-feeling UI.
Test in both light/dark.

### ❌ Desktop-First Mini App

**Why bad**: 95% of Telegram is mobile.
Touch targets too small.
Doesn't fit in Telegram UI.
Scrolling issues.

**Instead**: Mobile-first always.
Test on real phones.
Touch-friendly buttons.
Fit within Telegram frame.

### ❌ No Loading States

**Why bad**: Users think it's broken.
Poor perceived performance.
High exit rate.
Confusion.

**Instead**: Show skeleton UI.
Loading indicators.
Progressive loading.
Optimistic updates.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Not validating initData from Telegram | high | ## Validating initData |
| TON Connect not working on mobile | high | ## TON Connect Mobile Issues |
| Mini App feels slow and janky | medium | ## Mini App Performance |
| Custom buttons instead of MainButton | medium | ## Using MainButton Properly |

## Related Skills

Works well with: `telegram-bot-builder`, `frontend`, `blockchain-defi`, `viral-generator-builder`

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
