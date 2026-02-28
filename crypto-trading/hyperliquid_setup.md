# Hyperliquid セットアップ計画

**優先度**: 最高（Bybitより優先）  
**理由**: OpenClaw実例多数、Aaron使用中、DEX（セルフカストディ）

## Hyperliquidの特徴

### なぜHyperliquid？

✅ **OpenClaw実例多数** - Aaron (Coin Bureau)が実際に使用  
✅ **超高速執行** - サブ秒の取引確定  
✅ **セルフカストディ** - 資産は自分で管理（取引所リスクなし）  
✅ **優秀なAPI** - bot運用に最適化  
✅ **低手数料** - DEXとしては異例の低コスト  
✅ **高流動性** - DEXなのに主要CEXに匹敵

### 技術情報

- **種類**: DEX (Decentralized Exchange)
- **チェーン**: Hyperliquid L1
- **ウォレット**: EVM互換（MetaMask可）
- **API**: REST + WebSocket
- **ドキュメント**: https://hyperliquid.xyz/docs

## セットアップ手順

### 1. アカウント作成（5分）

1. https://app.hyperliquid.xyz にアクセス
2. MetaMask接続（または新規ウォレット作成）
3. Arbitrumブリッジから入金（推奨）

**または**：直接入金（ETH/USDC）

### 2. API設定（3分）

Hyperliquidは**秘密鍵ベース**（APIキー不要）:
- ウォレットの秘密鍵で署名
- MetaMaskエクスポートで取得可能

### 3. Python SDK

公式SDK: `hyperliquid-python-sdk`

```bash
pip install hyperliquid-python-sdk eth-account
```

### 4. 最小限のコード

```python
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from eth_account import Account

# 情報取得（公開API）
info = Info()
markets = info.all_mids()
print(markets)

# 取引実行（秘密鍵必要）
account = Account.from_key('YOUR_PRIVATE_KEY')
exchange = Exchange(account)

# 成行注文
exchange.market_order('BTC', True, 0.01)  # Buy 0.01 BTC
```

## 推奨入金額

- **テスト**: $50-100
- **本格運用**: $500-1000（$1,850の半分程度）
- **Polymarketと並行**: Hyperliquid $925 + Polymarket $50

## リスク

⚠️ **新しいプラットフォーム** - 歴史が浅い  
⚠️ **スマートコントラクトリスク** - DEX特有  
⚠️ **流動性変動** - 急激な市場変化に弱い可能性

✅ **軽減策**: 少額テストから開始、分散投資

## 次のステップ

1. **アカウント確認**
   - Hyperliquidアカウント持ってる？
   - ウォレットアドレスは？

2. **入金確認**
   - 残高あり？なければ入金必要

3. **秘密鍵取得**
   - MetaMaskから安全にエクスポート
   - `.env`に設定

4. **統合開発**
   - `hyperliquid_connector.py` 作成
   - Bybitと同じインターフェースで実装
   - 戦略を両方で実行可能に

## Bybit vs Hyperliquid

| 項目 | Hyperliquid | Bybit |
|------|-------------|-------|
| 種類 | DEX | CEX |
| 資産管理 | セルフカストディ | 取引所預託 |
| 速度 | サブ秒 | 高速 |
| 手数料 | 低い | 低い（メイカーリベート） |
| 流動性 | 高い | 非常に高い |
| OpenClaw実例 | ✅ 多数 | ⏳ 中程度 |
| 優先度 | 🥇 | 🥈 |

**結論**: Hyperliquid優先、Bybitはバックアップ

## 今後の計画

**Phase 1**: Hyperliquid接続テスト  
**Phase 2**: 簡単な戦略実行（RSI）  
**Phase 3**: Polymarketと並行運用  
**Phase 4**: Bybit追加（オプション）
