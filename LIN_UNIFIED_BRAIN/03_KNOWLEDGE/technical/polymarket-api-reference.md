# Polymarket API リファレンス

## 📡 API 概要

Polymarket は **CLOB（Central Limit Order Book）** を採用した分散型取引所です。

### 特徴：
- **ハイブリッド分散型**：オフチェーンでマッチング、オンチェーンで決済
- **非カストディアル**：資金は自分のウォレットで管理
- **EIP712署名**：注文は構造化データとして署名
- **REST + WebSocket API**：リアルタイムデータ取得可能

---

## 🔐 認証方法

### 必要な情報：
1. **Polygon ウォレットの秘密鍵**（Private Key）
2. **API認証情報**（L1認証から生成）
3. **Funderアドレス**（オプション）

### Python での認証例：

```python
from py_clob_client.client import ClobClient
import os

# CLOBクライアントの初期化
client = ClobClient(
    host="https://clob.polymarket.com",
    chain_id=137,  # Polygon Mainnet
    key=os.getenv("PRIVATE_KEY"),  # 秘密鍵
    signature_type=1,
    funder=os.getenv("FUNDER_ADDRESS")  # オプション
)

# 注文を作成して送信
order = await client.create_and_post_order(
    {
        "token_id": "123456",
        "price": 0.65,
        "size": 100,
        "side": "BUY"
    },
    {
        "tick_size": "0.01",
        "neg_risk": False
    }
)
```

---

## 🔗 API エンドポイント

### 1. **REST API**
- **ベースURL**: `https://clob.polymarket.com`
- 用途：市場データ取得、注文送信、履歴確認

### 2. **WebSocket API**
- **URL**: `wss://clob.polymarket.com`
- 用途：リアルタイム価格更新、注文ブック監視

### 3. **Gamma API**
- 市場メタデータ取得
- イベント情報取得

---

## 📊 主要な操作

### 1. **市場データ取得**

```python
# すべての市場を取得
markets = await client.get_markets()

# 特定の市場を取得
market = await client.get_market(market_id="market_123")

# 注文ブックを取得
orderbook = await client.get_orderbook(token_id="123456")
```

### 2. **注文の作成**

#### Buy（買い）注文：
```python
buy_order = await client.create_and_post_order(
    {
        "token_id": "123456",
        "price": 0.60,  # 60セント
        "size": 50,     # 50株
        "side": "BUY"
    },
    {
        "tick_size": "0.01",
        "neg_risk": False
    }
)
```

#### Sell（売り）注文：
```python
sell_order = await client.create_and_post_order(
    {
        "token_id": "123456",
        "price": 0.70,
        "size": 50,
        "side": "SELL"
    },
    {
        "tick_size": "0.01",
        "neg_risk": False
    }
)
```

### 3. **注文のキャンセル**

```python
# 特定の注文をキャンセル
await client.cancel_order(order_id="order_123")

# すべての注文をキャンセル
await client.cancel_all_orders()
```

### 4. **残高確認**

```python
# USDC残高を確認
balance = await client.get_balance()

# ポジション確認
positions = await client.get_positions()
```

---

## 🏗️ 注文の種類

### 1. **Limit Order（指値注文）**
- 指定した価格で買い/売り
- 最も一般的な注文タイプ

### 2. **Market Order（成行注文）**
- 現在の市場価格で即座に執行
- スリッページに注意

### 3. **Post-Only Order**
- メイカー注文のみ（流動性を提供）
- テイカーにならない

---

## 💰 手数料構造

### メイカー手数料：
- 注文ブックに流動性を追加する側
- 通常：**0%〜-0.02%**（リベートがもらえる場合あり）

### テイカー手数料：
- 既存の注文を消費する側
- 通常：**0.02%〜0.1%**

### ガス代（Polygon）：
- オンチェーン決済時のみ発生
- 通常：**$0.01〜$0.50**（Polygonは安い）

---

## ⚠️ リスク管理

### 1. **注文サイズの制限**
```python
MAX_ORDER_SIZE = 100  # USDCベース
MIN_ORDER_SIZE = 1

# 注文前にサイズをチェック
if order_size > MAX_ORDER_SIZE:
    print("Order size exceeds maximum")
```

### 2. **価格範囲の制限**
```python
# 明らかに不合理な価格をフィルタ
if price < 0.01 or price > 0.99:
    print("Invalid price range")
```

### 3. **レート制限**
- API呼び出しには制限あり
- 過度なリクエストは避ける

---

## 🔄 WebSocket ストリーミング

### リアルタイム価格監視：

```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Price update: {data}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    # 特定の市場を購読
    ws.send(json.dumps({
        "type": "subscribe",
        "channel": "orderbook",
        "market_id": "market_123"
    }))

ws = websocket.WebSocketApp(
    "wss://clob.polymarket.com",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open
)

ws.run_forever()
```

---

## 🛠️ トラブルシューティング

### よくあるエラー：

#### 1. **"Insufficient funds"**
```python
# 原因：USDC残高不足
# 解決：残高を確認して入金
balance = await client.get_balance()
print(f"USDC Balance: {balance['usdc']}")
```

#### 2. **"Invalid signature"**
```python
# 原因：秘密鍵が間違っている
# 解決：秘密鍵を確認（0xで始まるか確認）
private_key = os.getenv("PRIVATE_KEY")
if not private_key.startswith("0x"):
    private_key = "0x" + private_key
```

#### 3. **"Order rejected: Price out of range"**
```python
# 原因：価格が0.01〜0.99の範囲外
# 解決：価格を調整
price = max(0.01, min(0.99, price))
```

#### 4. **"Rate limit exceeded"**
```python
# 原因：API呼び出しが多すぎる
# 解決：リクエスト間に遅延を追加
import time
time.sleep(0.5)  # 500ms待機
```

---

## 📚 関連ライブラリ

### 1. **py-clob-client**
```bash
pip install py-clob-client
```
- Polymarket CLOB用のPythonクライアント
- GitHub: https://github.com/Polymarket/py-clob-client

### 2. **python-order-utils**
```bash
pip install python-order-utils
```
- 注文の生成と署名ユーティリティ
- GitHub: https://github.com/Polymarket/python-order-utils

### 3. **web3.py**
```bash
pip install web3
```
- Ethereum/Polygon ブロックチェーン操作
- 秘密鍵管理、トランザクション送信

---

## 🌐 ネットワーク情報

### Polygon Mainnet：
- **Chain ID**: 137
- **RPC URL**: `https://polygon-rpc.com/`
- **通貨**: MATIC
- **ブロックエクスプローラー**: https://polygonscan.com/

### USDC Contract：
- **アドレス**: `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`
- **Decimals**: 6

---

## 📖 公式ドキュメント

- **Polymarket Docs**: https://docs.polymarket.com/
- **CLOB API**: https://docs.polymarket.com/developers/CLOB/introduction
- **認証ガイド**: https://docs.polymarket.com/developers/CLOB/authentication

---

## 🔒 セキュリティベストプラクティス

### 1. **秘密鍵の管理**
```python
# ❌ 悪い例：ハードコード
private_key = "0x1234567890abcdef..."

# ✅ 良い例：環境変数
import os
private_key = os.getenv("PRIVATE_KEY")

# ✅ さらに良い例：暗号化して保存
from cryptography.fernet import Fernet
# 暗号化ロジック...
```

### 2. **ログに秘密情報を出力しない**
```python
# ❌ 悪い例
print(f"Private key: {private_key}")

# ✅ 良い例
print(f"Wallet address: {wallet_address}")
```

### 3. **環境ごとに異なるウォレットを使用**
```python
if os.getenv("NODE_ENV") == "production":
    private_key = os.getenv("PROD_PRIVATE_KEY")
else:
    private_key = os.getenv("DEV_PRIVATE_KEY")
```

---

## 📅 作成日時
2026-02-15

## 🔄 最終更新
2026-02-15
