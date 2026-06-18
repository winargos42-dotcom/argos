---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/draw-io/references/layout-guidelines.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\draw-io\references\layout-guidelines.md
source_ext: .md
source_sha256: 28d887d4857ab60b054fc70450ceb7deb2efb9317906e1651f0974d97cab4ccd
text_sha256: 501fbf61f47b08f578f39a03fcd655af7986277028dd92469a99ba835526d0d8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:34
---

# layout-guidelines.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/draw-io/references/layout-guidelines.md`
- Extract: `text`
- SHA256: `28d887d4857ab60b054fc70450ceb7deb2efb9317906e1651f0974d97cab4ccd`

## Content

# レイアウトガイドライン

## 1. グループ化の原則

- AWS Cloud グループを最外層とする
- 機能単位でサブグループを作成
- グループは横並びを基本とし、データフローに沿って配置

### 1.1. グループの階層構造

```text
AWS Cloud (最外層)
├── VPC
│   ├── Public Subnet
│   │   └── ALB, NAT Gateway など
│   └── Private Subnet
│       └── ECS, RDS など
├── S3
├── CloudWatch
└── その他のサービス
```

## 2. 接続線のルール

### 2.1. 線種の使い分け

| フロー種別 | 線種 | 用途 |
|-----------|------|------|
| Ingestion Flow | 破線 | データ取り込み |
| Query Flow | 実線 | クエリ・参照 |
| Control Flow | 点線 | 制御・管理 |

### 2.2. 矢印の方向

- 矢印はデータの流れる方向に従う
- 双方向通信は双方向矢印を使用

## 3. 配置の原則

### 3.1. 左から右へのフロー

```text
[データソース] → [処理] → [ストレージ] → [分析/可視化]
```

### 3.2. 上から下へのフロー (代替)

```text
[ユーザー/クライアント]
        ↓
[ロードバランサー]
        ↓
[アプリケーション]
        ↓
[データベース]
```

## 4. 視認性の確保

- ラベルは要素の近くに配置
- 矢印が交差しないように配置を調整
- 関連する要素はグループ化して近くに配置
- 余白を適切に確保して見やすくする

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
