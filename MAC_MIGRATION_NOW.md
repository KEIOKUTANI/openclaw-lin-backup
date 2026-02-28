# Mac移行 - 今すぐ実行

**日時**: 2026-02-28 04:21 JST  
**サーバーIP**: 167.172.64.35  
**バックアップ**: /root/lin_brain_backup_20260228_033949.tar.gz (285KB)

---

## Mac miniで今すぐ実行すること

### Step 1: バックアップダウンロード（3分）

**Macのターミナルで：**
```bash
# Downloadsフォルダにダウンロード
cd ~/Downloads
scp root@167.172.64.35:/root/lin_brain_backup_20260228_033949.tar.gz ./

# パスワード入力が必要な場合はDigitalOceanのパスワード
```

---

### Step 2: 展開・配置（2分）

```bash
# ワークスペース作成
mkdir -p ~/openclaw_data
cd ~/openclaw_data

# 展開
tar -xzf ~/Downloads/lin_brain_backup_20260228_033949.tar.gz

# 確認
ls -la LIN_UNIFIED_BRAIN/
```

---

### Step 3: OpenClawインストール（5分）

```bash
# Homebrewインストール（まだなら）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node.js & OpenClawインストール
brew install node
npm install -g openclaw

# 確認
openclaw --version
```

---

### Step 4: Python環境セットアップ（10分）

```bash
cd ~/openclaw_data/LIN_UNIFIED_BRAIN/05_CODE/polymarket-agents

# pyenvインストール（Pythonバージョン管理）
brew install pyenv

# Python 3.9インストール
pyenv install 3.9.25
pyenv local 3.9.25

# 仮想環境作成
python -m venv .venv
source .venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt
```

---

### Step 5: 環境変数設定（3分）

```bash
cd ~/openclaw_data/LIN_UNIFIED_BRAIN/05_CODE/polymarket-agents

# .envファイル作成（重要な秘密鍵等）
nano .env

# 以下を貼り付け（DigitalOceanの.envから）：
```

**重要な環境変数**:
```bash
POLYGON_WALLET_PRIVATE_KEY="4594bcb8121684cf625345d4cc5d18e92c5f94cbad50c941fd80fb3b4a72c080"
OPENAI_API_KEY="***REDACTED***"
POLYGON_RPC_URL="https://polygon-rpc.com"
HTTPS_PROXY=""
HTTP_PROXY=""
```

保存: `Ctrl+O` → Enter → `Ctrl+X`

---

### Step 6: Polymarket接続テスト（2分）

```bash
cd ~/openclaw_data/LIN_UNIFIED_BRAIN/05_CODE/polymarket-agents
source .venv/bin/activate

# 残高確認（地域制限チェック）
python check_balance.py

# 市場取得テスト
curl https://gamma-api.polymarket.com/markets?limit=1
```

**期待結果**:
- ✅ 200 OK（地域制限なし！）
- ✅ 残高表示（$0でもOK）

---

### Step 7: OpenClaw起動（1分）

```bash
# OpenClaw Gateway起動
openclaw gateway start

# 確認
openclaw gateway status

# ワークスペース設定
openclaw config set workspace ~/openclaw_data/LIN_UNIFIED_BRAIN
```

---

### Step 8: Polymarket監視開始（1分）

```bash
cd ~/openclaw_data/LIN_UNIFIED_BRAIN/05_CODE/polymarket-agents
source .venv/bin/activate

# 監視開始（バックグラウンド）
nohup python monitor_arbitrage.py --continuous --interval 60 > monitor.log 2>&1 &

# ログ確認
tail -f monitor.log
```

---

## 移行完了チェックリスト

- [ ] バックアップダウンロード完了
- [ ] OpenClawインストール完了
- [ ] Python 3.9環境セットアップ完了
- [ ] .env設定完了
- [ ] Polymarket接続成功（地域制限なし確認）
- [ ] OpenClaw Gateway起動
- [ ] 監視ボット起動

---

## トラブルシューティング

### Polymarketで403エラー（地域制限）
```bash
# Mac mini（日本）なら通常問題なし
# もしエラーが出たら：
curl https://gamma-api.polymarket.com/markets?limit=1
# → 200 OKなら問題なし
```

### Python依存関係エラー
```bash
# pysha3エラーの場合
brew install gmp
pip install pysha3

# その他
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## DigitalOcean側（バックグラウンド実行中）

### 現在実行中のタスク
1. ✅ **Polymarket監視ボット**（60秒ごとにスキャン）
   - ログ: `/root/openclaw_data/lin/logs/polymarket_monitor.log`
   - 確認: `tail -f /root/openclaw_data/lin/logs/polymarket_monitor.log`

2. ✅ **統合済みの脳**（Mac転送準備完了）

### Mac移行後のDigitalOcean
**選択肢**:
- **Option A**: 削除して節約（全てMacに移行）
- **Option B**: バックアップとして維持（月$6）
- **Option C**: 軽量監視のみ継続（Mac + DO並行）

---

## 次のステップ（Mac移行後）

### 即座にやること
1. **Polymarket $1テスト取引**
2. **Lancers/ココナラ登録**
3. **Grok API取得 → Twitter自動化**

### 1週間でやること
4. **初案件獲得**（¥30,000-50,000）
5. **Polymarketスケール**（$10 → $50）
6. **ブログ記事3本**

---

## 所要時間

- **基本セットアップ**: 30分
- **テスト・確認**: 15分
- **トラブル対応予備**: 15分

**合計**: 約1時間

---

**Ready?** Mac miniで上記のStep 1から始めてください！

質問があればいつでもどうぞ。
