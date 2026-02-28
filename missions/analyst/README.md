# Analyst Lin - 収益分析・ポーカー管理ミッション

## 概要
ポーカーのGTO分析、トレーディング分析、プレイ時間管理を行い、収益を守り最大化します。

## 目標
- Poker GTO分析の実施
- プレイ時間管理（目標250時間）
- 収益・損益トラッキング
- トレーディング戦略分析

## 分析領域
1. **Poker GTO**: 最適戦略の計算・分析
2. **時間管理**: プレイ時間の記録・目標管理
3. **収益分析**: 損益グラフ・統計
4. **トレーディング**: Polymarket等の戦略分析

## スクリプト
- `poker_tracker.py`: ポーカープレイ記録
- `gto_analyzer.py`: GTO分析ツール
- `revenue_dashboard.py`: 収益ダッシュボード
- `trading_analyzer.py`: トレーディング分析

## ワークフロー

### Poker管理
1. プレイセッション記録
2. ハンドヒストリー分析
3. GTO計算
4. 時間管理（250時間目標）
5. #ポーカートピックへ報告

### Trading分析
1. ポジション記録
2. 市場動向分析
3. 収益/損失トラッキング
4. 戦略調整提案

## データ保存先
- `data/poker_sessions_*.json`: プレイ記録
- `data/gto_analysis_*.json`: GTO分析結果
- `data/trading_log_*.json`: トレーディング記録
- `data/revenue_*.csv`: 収益データ

## 実行例
```bash
# ポーカーセッション記録
python3 poker_tracker.py --hours 3 --result +150

# GTO分析
python3 gto_analyzer.py --hand-history sample.txt

# 収益ダッシュボード表示
python3 revenue_dashboard.py --period month
```

## 統計指標
- Total Hours: 0/250時間
- Win Rate: BB/100
- ROI: %
- Monthly Revenue: $

**作成日**: 2026-02-28
