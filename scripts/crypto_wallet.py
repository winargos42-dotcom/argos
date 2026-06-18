#!/usr/bin/env python3
"""
ARGOS Crypto Wallet — хранит адреса для разных сетей.
Приватные ключи НЕ хранятся в файлах. Только:
  - публичные адреса
  - баланс (ручной ввод/импорт через API)
  - история транзакций (через block explorer API)
"""
import json, re, requests
from pathlib import Path
from datetime import datetime

MEM_DIR = Path("/home/ava/Projects/argoss/data/mempalace")
MEM_DIR.mkdir(parents=True, exist_ok=True)
WALLET_FILE = MEM_DIR / "crypto_wallet.json"

CHAINS = {
    "btc": {"name": "Bitcoin", "explorer": "https://blockchain.info/rawaddr/ADDR"},
    "eth": {"name": "Ethereum", "explorer": "https://api.etherscan.io/api?module=account&action=balance&address=ADDR&tag=latest"},
    "trx": {"name": "Tron", "explorer": "https://apilist.tronscanapi.com/api/account/wallet"},
    "ltc": {"name": "Litecoin", "explorer": "https://api.blockcypher.com/v1/ltc/main/addrs/ADDR"},
}

class CryptoWallet:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if WALLET_FILE.exists():
            return json.loads(WALLET_FILE.read_text(encoding="utf-8"))
        return {"addresses": {}, "balances": {}, "transactions": []}

    def save(self):
        WALLET_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def add_address(self, chain: str, address: str, label: str = ""):
        """Добавить публичный адрес для мониторинга."""
        if chain not in self.data["addresses"]:
            self.data["addresses"][chain] = []
        # Check format
        if not self._validate_address(chain, address):
            print(f"[Wallet] ⚠️ Invalid address format for {chain}")
            return False
        self.data["addresses"][chain].append({"address": address, "label": label, "added": datetime.now().isoformat()})
        self.save()
        print(f"[Wallet] ✅ Added {chain} address: {address[:8]}...")
        return True

    def _validate_address(self, chain, addr):
        patterns = {
            "btc": r"^1[a-zA-Z0-9]{25,34}$|^3[a-zA-Z0-9]{25,34}$|^bc1[a-zA-Z0-9]{38,59}$",
            "eth": r"^0x[a-fA-F0-9]{40}$",
            "trx": r"^T[a-zA-Z0-9]{33}$",
            "ltc": r"^[LM3][a-km-zA-HJ-NP-Z1-9]{25,34}$",
        }
        return bool(re.match(patterns.get(chain, r".*"), addr))

    def update_balance(self, chain: str, address: str, balance: float):
        """Ручное обновление баланса (или через API)."""
        key = f"{chain}:{address}"
        old = self.data["balances"].get(key, 0)
        self.data["balances"][key] = balance
        if old != balance:
            tx = {
                "ts": datetime.now().isoformat(),
                "chain": chain, "address": address,
                "old": old, "new": balance, "diff": round(balance - old, 8)
            }
            self.data["transactions"].append(tx)
        self.save()
        print(f"[Wallet] 💰 {chain.upper()}: {balance}")

    def total_usd_estimate(self, prices=None):
        """Оценка стоимости портфеля. prices={'btc':65000, 'eth':3500...}"""
        if not prices:
            # Mock prices if no real API
            prices = {"btc": 65000, "eth": 3500, "trx": 0.12, "ltc": 80}
        total = 0
        for chain, addrs in self.data["addresses"].items():
            price = prices.get(chain, 0)
            for a in addrs:
                key = f"{chain}:{a['address']}"
                bal = self.data["balances"].get(key, 0)
                total += bal * price
        return round(total, 2)

    def report(self):
        addrs_count = sum(len(v) for v in self.data["addresses"].values())
        total = self.total_usd_estimate()
        return f"[Wallet] Addresses: {addrs_count} | Est. Value: ${total}"

if __name__ == "__main__":
    import sys
    w = CryptoWallet()
    if len(sys.argv) > 2 and sys.argv[1] == "add":
        w.add_address(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif len(sys.argv) > 3 and sys.argv[1] == "balance":
        w.update_balance(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    else:
        print(w.report())
