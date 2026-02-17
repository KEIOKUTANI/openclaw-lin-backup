# Polymarket 自動取引セットアップガイド

## 📋 現在の状況

### ✅ 完了：
- MetaMask ウォレット作成・設定完了
- リカバリーフレーズ保存済み
- Polymarket アカウント接続完了
- USDC $27.81 入金済み（Polygon ネットワーク）
- ウォレットアドレス: 0x1011cd7171...

### ⏳ 準備中：
- OpenClaw からの自動取引セットアップ

---

## 🔧 Polymarket 自動取引の実装方法

### オプション1：公式 Polymarket Agents フレームワーク（推奨）

**GitHub:** https://github.com/Polymarket/agents

#### 特徴：
- ✅ Polymarket 公式のAI Agentフレームワーク
- ✅ Python 3.9 ベース
- ✅ API統合済み
- ✅ RAG（Retrieval-Augmented Generation）サポート
- ✅ CLI ツール付き
- ✅ MITライセンス（オープンソース）

#### 必要な環境変数：
```bash
POLYGON_WALLET_PRIVATE_KEY=""  # MetaMaskの秘密鍵
OPENAI_API_KEY=""              # OpenAI APIキー（またはAntigravity経由）
```

#### セットアップ手順（概要）：
1. リポジトリをクローン
   ```bash
   git clone https://github.com/Polymarket/agents.git
   cd agents
   ```

2. Python仮想環境を作成
   ```bash
   virtualenv --python=python3.9 .venv
   source .venv/bin/activate  # Linux/macOS
   # または .venv\Scripts\activate  # Windows
   ```

3. 依存関係をインストール
   ```bash
   pip install -r requirements.txt
   ```

4. 環境変数を設定
   ```bash
   cp .env.example .env
   # .envファイルを編集して必要な値を設定
   ```

5. CLIツールでテスト
   ```bash
   python scripts/python/cli.py get-all-markets --limit 5
   ```

6. 取引を実行
   ```bash
   python agents/application/trade.py
   ```

---

## 🔐 セキュリティ注意事項

### ⚠️ 秘密鍵の取り扱い：
- MetaMaskの秘密鍵（Private Key）は**絶対に公開しない**
- `.env`ファイルは`.gitignore`に追加（リポジトリにコミットしない）
- 秘密鍵は暗号化して保存することを推奨

### 🛡️ リスク管理：
- 初期テストは**少額**（$1-5程度）で行う
- 自動取引の上限額を設定
- 定期的に残高とトランザクションを確認

---

## 🤖 OpenClaw との統合

### 実装方法：

#### 1. **Pythonスクリプトを直接実行**
OpenClawの`exec`ツールを使って、Polymarket Agentsのスクリプトを実行：
```python
exec("cd /path/to/polymarket-agents && python agents/application/trade.py")
```

#### 2. **APIラッパーを作成**
Polymarket AgentsをAPIサーバーとして起動し、OpenClawから呼び出す

#### 3. **カスタムスキルを作成**
OpenClawのスキルシステムを使って、Polymarket取引専用のスキルを作成

---

## 📊 取引戦略の例

### 1. **マーケットメイキング（流動性提供）**
- 買い側と売り側の両方に注文を出す
- スプレッド（価格差）で利益を得る
- 低ボラティリティ市場に適している

### 2. **アービトラージ（裁定取引）**
- 同じ結果に対する異なる市場間の価格差を利用
- 例：「トランプが勝つ」市場と「バイデンが負ける」市場の価格差

### 3. **イベント駆動取引**
- ニュースやイベントに反応して取引
- Polymarket Agentsは自動的にニュースを収集・分析

### 4. **コピートレード**
- 成功しているトレーダーの注文を自動的にコピー
- 公式ドキュメントにも言及されている手法

---

## 🔗 参考リンク

### 公式リソース：
- **Polymarket Agents GitHub**: https://github.com/Polymarket/agents
- **Polymarket API ドキュメント**: https://docs.polymarket.com/
- **Gamma API**: 市場データ取得用API
- **CLOB API**: 注文実行用API

### 関連リポジトリ：
- **py-clob-client**: https://github.com/Polymarket/py-clob-client
- **python-order-utils**: https://github.com/Polymarket/python-order-utils

### コミュニティリソース：
- **YouTube チュートリアル**: Polymarket bot開発のビデオガイド多数
- **Polymarket 公式ブログ**: 自動マーケットメイキングの記事あり

---

## ⚖️ 法的注意事項

**重要：** Polymarketの利用規約により、**米国居住者および特定の管轄区域の居住者は取引禁止**です。

データの閲覧は全世界で可能ですが、取引（UI・API・AI Agent経由を含む）は制限されています。

必ず自身の居住地の法律とPolymarketの利用規約を確認してください。

---

## 📝 次のステップ（優先順位順）

### 1. 秘密鍵の安全な取得
- MetaMaskから秘密鍵をエクスポート
- 安全な場所に保存（暗号化推奨）

### 2. Polymarket Agents のセットアップ
- サーバー（DigitalOcean）またはローカルにインストール
- 環境変数の設定

### 3. テスト取引の実行
- CLI ツールで市場情報を取得
- 少額（$1-5）でテスト取引

### 4. OpenClaw との統合
- スキル作成またはPythonスクリプト統合
- 自動取引ロジックの実装

### 5. 戦略の最適化
- 取引データの分析
- 戦略の調整とバックテスト

---

## 🆘 トラブルシューティング

### よくある問題：

#### 1. **「POLYGON_WALLET_PRIVATE_KEY が無効」エラー**
- 秘密鍵が正しくコピーされているか確認
- 先頭に`0x`が付いているか確認

#### 2. **「insufficient funds」エラー**
- ガス代（MATIC）が不足している可能性
- Polygon MATICを少額（$1-2程度）入手

#### 3. **API認証エラー**
- Polymarket APIキーの設定を確認
- OAuth認証が正しく設定されているか確認

---

## 📅 作成日時
2026-02-15

## 🔄 最終更新
2026-02-15
