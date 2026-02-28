# Project Lin - 受託開発自動化ミッション

## 概要
クラウドワークス等の受託開発案件をリアルタイム監視し、Python/データ分析案件に自動応募・実行します。

## 目標
- クラウドワークス新着案件の監視
- Python/データ分析案件の自動フィルタリング
- 要件定義から納品まで完結
- 収益の最大化

## 対象プラットフォーム
- クラウドワークス（主要）
- ランサーズ
- ココナラ

## スクリプト
- `crowdworks_monitor.py`: クラウドワークス監視
- `project_analyzer.py`: 案件分析・適合性判定
- `auto_proposal.py`: 自動提案文生成・応募

## ワークフロー
1. 新着案件のスクレイピング
2. Python/データ分析案件のフィルタリング
3. 難易度・報酬・納期の分析
4. 自動応募可能な案件の抽出
5. 提案文生成・応募
6. 受注後の要件定義・実装・納品

## データ保存先
- `data/projects_*.json`: 案件リスト
- `data/proposals_*.json`: 提案履歴
- `data/awarded_*.json`: 受注案件

## 実行例
```bash
# 監視開始（デーモンモード）
python3 crowdworks_monitor.py --daemon

# 手動スキャン
python3 crowdworks_monitor.py --scan-once
```

## 注意事項
- API認証情報は `.env` で管理
- 自動応募は慎重に実施（品質重視）
- 受注率・評価を最優先

**作成日**: 2026-02-28
