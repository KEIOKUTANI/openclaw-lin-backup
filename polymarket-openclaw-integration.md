# OpenClaw × Polymarket 統合ガイド

## 🎯 目標

OpenClaw（AI Agent）を使って、Polymarketで自動取引を行う。

---

## 🔄 統合アプローチ

### オプション1：Pythonスクリプト直接実行（推奨・最も簡単）

OpenClawの`exec`ツールを使って、Polymarket AgentsのPythonスクリプトを直接実行します。

#### メリット：
- ✅ 最も簡単
- ✅ 公式フレームワークをそのまま利用
- ✅ コード量が少ない

#### デメリット：
- ❌ OpenClawのスキルシステムとの統合が限定的

#### 実装例：
```python
# OpenClawからPolymarket Agentsのスクリプトを実行
await exec(
    command="cd /root/polymarket-agents && python agents/application/trade.py",
    env={
        "POLYGON_WALLET_PRIVATE_KEY": "0x...",
        "OPENAI_API_KEY": "sk-..."
    }
)
```

---

### オプション2：カスタムスキル作成（推奨・最も統合的）

OpenClawのスキルシステムを使って、Polymarket専用のスキルを作成します。

#### メリット：
- ✅ OpenClawのエコシステムに完全統合
- ✅ 他のスキルと連携可能
- ✅ 再利用可能

#### デメリット：
- ❌ 初期開発に時間がかかる

#### スキル構成例：
```
skills/polymarket/
├── SKILL.md              # スキルのドキュメント
├── setup.sh              # セットアップスクリプト
├── trade.py              # 取引実行スクリプト
├── market_data.py        # 市場データ取得
├── requirements.txt      # Python依存関係
└── .env.example          # 環境変数のサンプル
```

---

### オプション3：APIラッパーサーバー（高度）

Polymarket AgentsをAPIサーバーとして起動し、OpenClawからHTTPリクエストで呼び出します。

#### メリット：
- ✅ OpenClawとPolymarketを分離
- ✅ 複数のクライアントから利用可能
- ✅ スケーラブル

#### デメリット：
- ❌ サーバー管理が必要
- ❌ 複雑度が高い

---

## 🔧 実装：オプション1（Pythonスクリプト直接実行）

### ステップ1：Polymarket Agentsのインストール

```bash
# サーバー（DigitalOcean）にSSH接続
ssh root@your-server-ip

# リポジトリをクローン
cd /root
git clone https://github.com/Polymarket/agents.git polymarket-agents
cd polymarket-agents

# Python仮想環境を作成
python3.9 -m venv .venv
source .venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
nano .env  # 秘密鍵とAPIキーを設定
```

### ステップ2：OpenClawからの実行

OpenClawのチャットで以下を実行：

```python
# 市場データを取得
result = await exec(
    command="cd /root/polymarket-agents && source .venv/bin/activate && python scripts/python/cli.py get-all-markets --limit 10",
    pty=True
)
print(result)

# 取引を実行
result = await exec(
    command="cd /root/polymarket-agents && source .venv/bin/activate && python agents/application/trade.py",
    pty=True
)
print(result)
```

---

## 🔧 実装：オプション2（カスタムスキル作成）

### SKILL.md テンプレート

```markdown
# Polymarket Trading Skill

## Description
Automated trading on Polymarket prediction markets using AI agents.

## Usage
\`\`\`
# Get market data
python market_data.py --market-id "market_123"

# Execute a trade
python trade.py --market-id "market_123" --side "BUY" --price 0.65 --size 10

# Get portfolio balance
python balance.py
\`\`\`

## Requirements
- Python 3.9+
- Polygon wallet with USDC
- Polymarket API access

## Setup
\`\`\`bash
./setup.sh
\`\`\`

## Configuration
Edit `.env` file with your credentials:
\`\`\`
POLYGON_WALLET_PRIVATE_KEY=0x...
OPENAI_API_KEY=sk-...
\`\`\`
```

### setup.sh スクリプト

```bash
#!/bin/bash
set -e

echo "Setting up Polymarket skill..."

# Check Python version
python_version=$(python3.9 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.9 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Clone Polymarket Agents if not exists
if [ ! -d "polymarket-agents" ]; then
    echo "Cloning Polymarket Agents..."
    git clone https://github.com/Polymarket/agents.git polymarket-agents
fi

echo "Setup complete!"
echo "Please configure your .env file before running."
```

### trade.py スクリプト（簡易版）

```python
#!/usr/bin/env python3
"""
Polymarket trading script for OpenClaw
"""
import os
import sys
import asyncio
from py_clob_client.client import ClobClient

async def main():
    # 環境変数から認証情報を取得
    private_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY")
    if not private_key:
        print("Error: POLYGON_WALLET_PRIVATE_KEY not set")
        sys.exit(1)
    
    # CLOBクライアントを初期化
    client = ClobClient(
        host="https://clob.polymarket.com",
        chain_id=137,
        key=private_key,
        signature_type=1
    )
    
    # 市場データを取得
    markets = await client.get_markets()
    print(f"Found {len(markets)} markets")
    
    # 残高を確認
    balance = await client.get_balance()
    print(f"USDC Balance: ${balance.get('usdc', 0)}")
    
    # ここに取引ロジックを追加...

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🤖 OpenClawからの利用例

### 市場データ取得：
```
OpenClaw: Polymarketで人気の市場を5つ教えて

[OpenClawがスキルを実行]
→ python scripts/python/cli.py get-all-markets --limit 5

[結果を解析して返答]
現在の人気市場：
1. トランプ勝利（2024大統領選）- 52%
2. ビットコイン $100k到達 - 38%
3. AI進化（GPT-5） - 65%
...
```

### 自動取引：
```
OpenClaw: ビットコインが$90kを超える確率が30%以下なら買いポジションを取って

[OpenClawが条件をチェック]
→ python market_data.py --market "BTC-90k"
→ 現在の確率: 28%

[条件を満たすので取引実行]
→ python trade.py --market-id "12345" --side "BUY" --price 0.28 --size 10

[結果を報告]
✅ 買い注文を実行しました
- 市場: BTC $90k到達
- 価格: $0.28（28%）
- サイズ: 10 USDC
```

---

## 🧠 AI取引戦略の実装

### 戦略1：ニュースベースの取引

```python
# OpenClawがニュースを収集
news = await web_search("Bitcoin price prediction")

# LLMで分析
analysis = await llm_analyze(news)

# 取引判断
if analysis['confidence'] > 0.7:
    await execute_trade(
        market_id="btc-market",
        side="BUY" if analysis['sentiment'] == 'bullish' else "SELL",
        size=10
    )
```

### 戦略2：価格乖離の検出

```python
# 複数の市場で同じイベントの価格を比較
prices = []
for market in related_markets:
    price = await get_market_price(market['id'])
    prices.append((market, price))

# 価格差が5%以上なら裁定取引
if max(prices) - min(prices) > 0.05:
    await arbitrage_trade(prices)
```

### 戦略3：時系列分析

```python
# 過去の価格データを取得
historical_prices = await get_price_history(market_id)

# トレンドを分析
trend = analyze_trend(historical_prices)

# トレンドに従って取引
if trend == 'upward':
    await execute_trade(market_id, side="BUY", size=5)
```

---

## 📊 モニタリングとログ

### ログファイルの設定：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('polymarket_trading.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 使用例
logger.info("Executing trade: BUY 10 USDC at 0.65")
logger.error("Trade failed: Insufficient funds")
```

### OpenClawでのログ確認：

```bash
# 最新のログを確認
tail -n 50 /root/polymarket-agents/polymarket_trading.log

# リアルタイムでログを監視
tail -f /root/polymarket-agents/polymarket_trading.log
```

---

## ⚡ パフォーマンス最適化

### 1. **キャッシング**
```python
import functools
import time

@functools.lru_cache(maxsize=100)
def get_market_data_cached(market_id, ttl=60):
    # TTL（Time To Live）付きキャッシュ
    return get_market_data(market_id)
```

### 2. **並列処理**
```python
import asyncio

# 複数の市場を並列で取得
async def get_multiple_markets(market_ids):
    tasks = [get_market_data(mid) for mid in market_ids]
    return await asyncio.gather(*tasks)
```

### 3. **WebSocket for リアルタイムデータ**
```python
# REST APIより高速
ws_client = WebSocketClient("wss://clob.polymarket.com")
ws_client.subscribe("orderbook", market_id)
```

---

## 🔒 セキュリティ対策

### 1. **秘密鍵の暗号化**

```python
from cryptography.fernet import Fernet
import os

# 暗号化キーを生成（1回だけ）
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 秘密鍵を暗号化
private_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY")
encrypted_key = cipher_suite.encrypt(private_key.encode())

# 暗号化された鍵をファイルに保存
with open("encrypted_key.bin", "wb") as f:
    f.write(encrypted_key)

# 使用時に復号化
with open("encrypted_key.bin", "rb") as f:
    encrypted_key = f.read()
decrypted_key = cipher_suite.decrypt(encrypted_key).decode()
```

### 2. **取引制限の設定**

```python
# config.py
TRADING_LIMITS = {
    "max_order_size": 100,      # 最大注文サイズ（USDC）
    "max_daily_volume": 500,    # 1日の最大取引量
    "max_position_size": 200,   # 最大ポジションサイズ
    "min_profit_threshold": 0.02 # 最小利益率（2%）
}

# 注文前にチェック
def validate_order(order):
    if order['size'] > TRADING_LIMITS['max_order_size']:
        raise ValueError("Order size exceeds limit")
```

### 3. **エラーハンドリング**

```python
import time

async def execute_trade_with_retry(order, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = await client.create_and_post_order(order)
            logger.info(f"Trade executed successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Trade failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

---

## 📅 次のアクションアイテム

### 1. 環境準備（優先度：高）
- [ ] Polymarket Agentsをサーバーにインストール
- [ ] MetaMaskから秘密鍵をエクスポート
- [ ] 環境変数を安全に設定

### 2. テスト実行（優先度：高）
- [ ] CLI で市場データ取得テスト
- [ ] 少額（$1-2）でテスト取引
- [ ] ログとエラーハンドリングの確認

### 3. OpenClaw統合（優先度：中）
- [ ] スキルを作成 or Pythonスクリプト直接実行
- [ ] OpenClawからの実行テスト
- [ ] 自動取引ロジックの実装

### 4. 戦略開発（優先度：中）
- [ ] ニュースベースの取引戦略
- [ ] 価格乖離検出ロジック
- [ ] バックテスト環境の構築

### 5. 本番運用（優先度：低）
- [ ] モニタリングダッシュボード
- [ ] アラート設定
- [ ] パフォーマンスレポート自動生成

---

## 📅 作成日時
2026-02-15

## 🔄 最終更新
2026-02-15
