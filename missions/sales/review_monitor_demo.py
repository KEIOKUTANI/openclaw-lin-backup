#!/usr/bin/env python3
"""
Google Maps 口コミ監視デモ - OpenClaw営業用
デモシナリオで動作する簡易版
"""
import os
import json
import time
from datetime import datetime
import requests

# Google Maps API設定
MAPS_API_KEY = "AIzaSyA9U8vz3LGSdKcTFDbYYaudtRwqi2XDnIE"
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"

class ReviewMonitorDemo:
    """口コミ監視デモクラス"""
    
    def __init__(self, place_id: str, place_name: str = "サンプル店舗"):
        self.place_id = place_id
        self.place_name = place_name
        self.known_reviews = []
    
    def fetch_reviews(self):
        """Google Mapsから口コミを取得"""
        print(f"🔍 {self.place_name} の口コミを取得中...")
        
        params = {
            "place_id": self.place_id,
            "fields": "name,rating,reviews",
            "key": MAPS_API_KEY,
            "language": "ja"
        }
        
        try:
            response = requests.get(PLACES_API_URL, params=params)
            data = response.json()
            
            if data.get("status") == "OK":
                result = data.get("result", {})
                reviews = result.get("reviews", [])
                
                print(f"✅ {len(reviews)}件の口コミを取得")
                return reviews
            else:
                print(f"❌ API Error: {data.get('status')}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def check_new_reviews(self):
        """新しい口コミをチェック"""
        current_reviews = self.fetch_reviews()
        
        if not self.known_reviews:
            # 初回実行時
            self.known_reviews = current_reviews
            print("📝 初回データ登録完了")
            return []
        
        # 新規口コミを特定
        known_ids = {r.get("time") for r in self.known_reviews}
        new_reviews = [r for r in current_reviews if r.get("time") not in known_ids]
        
        if new_reviews:
            print(f"🆕 新しい口コミ: {len(new_reviews)}件")
            self.known_reviews = current_reviews
        
        return new_reviews
    
    def generate_reply(self, review_text: str, rating: int) -> str:
        """AI風の返信文を生成（デモ用簡易版）"""
        
        if rating >= 4:
            # 高評価の場合
            templates = [
                f"この度は当店をご利用いただき、誠にありがとうございます。\n{review_text[:20]}...とのお言葉、スタッフ一同大変励みになります。\nまたのご来店を心よりお待ちしております。",
                f"温かいお言葉をいただき、ありがとうございます！\nお客様に満足いただけたこと、スタッフ一同嬉しく思います。\n今後ともよろしくお願いいたします。"
            ]
        else:
            # 低評価の場合
            templates = [
                f"この度はご期待に沿えず、大変申し訳ございませんでした。\nいただいたご意見を真摯に受け止め、サービス改善に努めてまいります。\nまたご来店いただける機会がございましたら、挽回させていただければ幸いです。",
                f"貴重なご意見をありがとうございます。\nご指摘いただいた点につきまして、スタッフ全員で共有し改善に取り組んでおります。\n次回はより良い体験をお届けできるよう努めてまいります。"
            ]
        
        import random
        return random.choice(templates)
    
    def format_notification(self, review: dict) -> str:
        """Telegram通知フォーマット"""
        author = review.get("author_name", "匿名")
        rating = review.get("rating", 0)
        text = review.get("text", "（コメントなし）")
        time_posted = review.get("time", 0)
        
        # タイムスタンプ変換
        date_str = datetime.fromtimestamp(time_posted).strftime("%Y-%m-%d %H:%M")
        
        # 星評価
        stars = "⭐" * rating + "☆" * (5 - rating)
        
        notification = f"""
🔔 **新しい口コミが投稿されました**

**店舗**: {self.place_name}
**評価**: {stars} ({rating}/5)
**投稿者**: {author}
**日時**: {date_str}

**コメント**:
{text}

---

**AI推奨返信**:
{self.generate_reply(text, rating)}
"""
        return notification
    
    def demo_scenario(self):
        """デモシナリオ実行"""
        print("\n" + "="*70)
        print("🎬 OpenClaw 口コミ監視デモ - スタート")
        print("="*70)
        
        print(f"\n📍 監視対象: {self.place_name}")
        print(f"🆔 Place ID: {self.place_id}")
        
        # Step 1: 初回データ取得
        print("\n【Step 1】初回データ取得")
        self.check_new_reviews()
        
        # Step 2: 最新の口コミを1つ表示（デモ）
        print("\n【Step 2】最新の口コミを通知（デモ）")
        reviews = self.fetch_reviews()
        
        if reviews:
            latest = reviews[0]
            notification = self.format_notification(latest)
            
            print("\n" + "─"*70)
            print("📱 Telegram通知（イメージ）")
            print("─"*70)
            print(notification)
            print("─"*70)
        else:
            print("⚠️  口コミが見つかりませんでした")
        
        print("\n" + "="*70)
        print("✅ デモ完了！")
        print("="*70)
        
        print("\n💡 実際の運用では...")
        print("   • 5分ごとに自動チェック")
        print("   • 新しい口コミがあれば即座にTelegram通知")
        print("   • AI返信文を自動生成")
        print("   • ワンクリックでGoogle Mapsに返信可能")
    
    def continuous_monitor(self, interval_seconds: int = 300):
        """継続監視モード（実運用版）"""
        print(f"🚀 継続監視モード開始（{interval_seconds}秒間隔）")
        print("   Ctrl+C で停止")
        
        try:
            while True:
                new_reviews = self.check_new_reviews()
                
                for review in new_reviews:
                    notification = self.format_notification(review)
                    print("\n" + "="*70)
                    print("📱 新しい口コミを検知！")
                    print("="*70)
                    print(notification)
                    
                    # TODO: 実際はTelegram APIで送信
                    # send_telegram_notification(notification)
                
                print(f"\n💤 次回チェック: {interval_seconds}秒後...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  監視を停止しました")


def demo_starbucks_shibuya():
    """渋谷スタバのデモ"""
    # スターバックス渋谷マークシティ店（例）
    PLACE_ID = "ChIJi1eOPOWLGGARYKYqwq_I0BA"  # 実際のPlace IDに置き換え
    
    demo = ReviewMonitorDemo(
        place_id=PLACE_ID,
        place_name="スターバックス 渋谷マークシティ店"
    )
    
    demo.demo_scenario()


def demo_custom_place(place_id: str, place_name: str):
    """カスタム店舗のデモ"""
    demo = ReviewMonitorDemo(place_id=place_id, place_name=place_name)
    demo.demo_scenario()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw 口コミ監視デモ')
    parser.add_argument('--place-id', help='Google Maps Place ID')
    parser.add_argument('--place-name', help='店舗名')
    parser.add_argument('--demo', action='store_true', help='デモモード（渋谷スタバ）')
    parser.add_argument('--monitor', action='store_true', help='継続監視モード')
    parser.add_argument('--interval', type=int, default=300, help='チェック間隔（秒）')
    
    args = parser.parse_args()
    
    if args.demo or (not args.place_id):
        # デフォルトデモ
        demo_starbucks_shibuya()
    
    elif args.place_id:
        demo = ReviewMonitorDemo(
            place_id=args.place_id,
            place_name=args.place_name or "指定店舗"
        )
        
        if args.monitor:
            demo.continuous_monitor(args.interval)
        else:
            demo.demo_scenario()


if __name__ == "__main__":
    main()
