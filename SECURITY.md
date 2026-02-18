# セキュリティチェックリスト

## 参考事例
- [Moltbook APIキー漏洩事件](https://zenn.dev/helloworld/articles/5c69b2981d5199)
  - 150万APIキー漏洩
  - Gitへのコミットが原因

## 定期チェック（月次推奨）

### 1. Gitリポジトリの確認
```bash
# センシティブファイルがコミットされていないか
cd /root/openclaw_data/lin
git ls-files | grep -E "\.env|secret|key|token|credential"
# ⚠️ 何も表示されなければOK
```

### 2. 過去の履歴スキャン
```bash
# 過去のコミットにAPIキーが含まれていないか
git log --all --full-history -- "*.env*" "*.key"
# ⚠️ 何も表示されなければOK
```

### 3. .envファイルの確認
```bash
# .envファイルが適切に除外されているか
git check-ignore -v .env polymarket-agents/.env
# ✅ .gitignore:... と表示されればOK
```

### 4. リモートリポジトリの確認
```bash
# リモートがプライベートか確認
git remote -v
# ⚠️ GitHub/GitLabでPrivate設定を確認
```

## インシデント対応

### APIキーが漏洩した場合

1. **即座に無効化**
   - OpenAI: https://platform.openai.com/api-keys
   - Tavily: https://tavily.com/dashboard
   - Polymarket: ウォレットの秘密鍵は即座に移動

2. **Gitから完全削除**
   ```bash
   # BFG Repo-Cleaner または git-filter-repo を使用
   # 参考: https://docs.github.com/ja/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
   ```

3. **新しいキーで再設定**
   ```bash
   cd /root/openclaw_data/lin/polymarket-agents
   cp .env.example .env
   # 新しいAPIキーを設定
   ```

4. **バックアップの確認**
   ```bash
   # バックアップファイルにも古いキーがないか確認
   grep -r "sk-\|tvly-" ~/.backup/ 2>/dev/null
   ```

## ベストプラクティス

### ✅ DO
- `.env` ファイルは必ず `.gitignore` に追加
- リモートリポジトリは必ずプライベート
- APIキーは環境変数で管理
- 定期的にセキュリティスキャン実施

### ❌ DON'T
- コードやMarkdownにAPIキーを直接記述
- `.env.example` に実際のキーを記載
- パブリックリポジトリに `.env` をコミット
- Discordやチャットにキーを貼り付け

## 自動化（推奨）

### Git hooks でコミット前チェック
```bash
# .git/hooks/pre-commit を作成
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
if git diff --cached --name-only | grep -E "\.env$"; then
    echo "❌ Error: Attempting to commit .env file!"
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

## APIキーローテーション履歴

### OpenAI API Key
- **現在のキー設定日**: 不明（初期設定時）
- **最終レビュー**: 2026-02-18
- **ステータス**: ⚠️ Telegramメッセージで一度送信（削除済み）
- **次回ローテーション推奨**: 2026-05-18（3ヶ月後）
- **優先度**: 中

**対応履歴:**
- 2026-02-18: Telegramメッセージから削除完了
- 2026-02-18: ユーザー判断により即座の変更は保留

**次回ローテーション時の手順:**
1. OpenAI Platform → 現在のキーをRevoke
2. 新しいキーを生成
3. `/root/openclaw_data/lin/polymarket-agents/.env` を更新
4. Polymarket-agentsサービスを再起動

## 最終確認日
- 最終確認: 2026-02-18
- 次回確認予定: 2026-03-18
- 次回キーローテーション推奨: 2026-05-18
