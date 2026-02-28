# Crypto Auto Trading System

**作成日**: 2026-02-28
**ステータス**: セットアップ完了 → テスト準備中

## 概要

AIエージェント（OpenClaw Lin）が市場分析・自動売買を実行するシステム

## セットアップ完了項目

✅ Python仮想環境（.venv）  
✅ ccxt（取引所統合ライブラリ）  
✅ ExchangeConnector（Bybit等）  
✅ RiskManager（バンクロール管理）  
✅ SimpleStrategy（RSIベース）

## ファイル構成

```
crypto-trading/
├── .env                    # API keys（作成必要）
├── .env.example           # 設定例
├── setup_plan.md          # セットアップ計画
├── exchange_connector.py  # 取引所接続
├── risk_manager.py        # リスク管理
├── simple_strategy.py     # RSI戦略
└── README.md              # このファイル
```

## 次のステップ

### 1. APIキー設定（ユーザー）

`.env`ファイルを作成：

```bash
cd /root/openclaw_data/lin/crypto-trading
cp .env.example .env
nano .env
```

必要な情報：
- BYBIT_API_KEY
- BYBIT_API_SECRET

APIキー権限：Read + Trade（Withdrawは不要）

### 2. 接続テスト

```bash
source .venv/bin/activate
python3 exchange_connector.py
```

期待する出力：
- 残高表示
- BTC/USDT価格表示
- "Connection test complete!"

### 3. Dry Run（シミュレーション）

```bash
python3 simple_strategy.py
```

リアルマネーは使用せず、シグナルのみ確認

### 4. 実運用開始

`simple_strategy.py`内の`dry_run=False`に変更

## リスク管理設定

- **軍資金**: $1,850
- **リスク倍率**: 50倍（2% per trade）
- **最大ポジションサイズ**: $37/取引
- **最大エクスポージャー**: 60%（$1,110）

## 戦略（RSI）

- **買いシグナル**: RSI < 30（売られすぎ）
- **売りシグナル**: RSI > 70（買われすぎ）
- **ストップロス**: 2%
- **テイクプロフィット**: 4%（2:1 risk/reward）

## 使い方（OpenClawから）

```bash
cd /root/openclaw_data/lin/crypto-trading
source .venv/bin/activate

# Dry run
python3 simple_strategy.py

# Live trading（リアルマネー）
python3 simple_strategy.py --live  # TODO: 実装予定
```

## サポート対象取引所

- ✅ Bybit（優先）
- ⏳ Binance（準備中）
- ⏳ OKX（準備中）

## パフォーマンストラッキング

取引履歴は自動記録され、以下で確認可能：

```python
from risk_manager import RiskManager
rm = RiskManager()
rm.print_status()
```

## 今後の拡張

- [ ] 複数戦略（MACD, ボリンジャー等）
- [ ] バックテスト機能
- [ ] Telegram通知
- [ ] OpenClaw完全統合
- [ ] ポートフォリオ管理

## 注意事項

⚠️ **実運用は自己責任**  
⚠️ **少額テストから開始**  
⚠️ **ストップロス必須**  
⚠️ **APIキーは厳重管理**
