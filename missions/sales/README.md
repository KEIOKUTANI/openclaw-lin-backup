# Sales Lin - 営業開拓ミッション

## 概要
Google Maps APIを活用し、Webサイト未設定の店舗を特定して営業開拓を行います。

## 目標
- 特定エリアの店舗データ取得
- Webサイト未設定店舗の抽出
- 日本式ビジネスマナーでの営業文作成
- #営業トピックへの報告

## API情報
- **Google Cloud Project ID**: `hardy-operator-373511`
- **Maps API Key**: `AIzaSyA9U8vz3LGSdKcTFDbYYaudtRwqi2XDnIE`

## スクリプト
- `store_finder.py`: 店舗検索・抽出スクリプト
- `sales_letter_generator.py`: 営業文生成スクリプト

## ワークフロー
1. エリア指定で店舗検索
2. Webサイト未設定店舗をフィルタ
3. 店舗情報をCSV出力
4. 営業文テンプレート生成
5. #営業トピックへ報告

## データ保存先
- `data/stores_*.csv`: 店舗リスト
- `data/sales_letters_*.json`: 営業文データ

## 実行例
```bash
python3 store_finder.py --area "渋谷区" --category "レストラン"
python3 sales_letter_generator.py --input data/stores_latest.csv
```

**作成日**: 2026-02-28
