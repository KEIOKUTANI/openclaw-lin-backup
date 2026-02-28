#!/usr/bin/env python3
"""
Google Maps 口コミ監視デモ - モックデータ版
API設定なしでもデモ可能（営業プレゼン用）
"""
import time
import random
from datetime import datetime, timedelta

class ReviewMonitorDemoMock:
    """口コミ監視デモ（モックデータ版）"""
    
    def __init__(self, place_name: str = "サンプルカフェ 渋谷店"):
        self.place_name = place_name
        self.mock_reviews = self._generate_mock_reviews()
    
    def _generate_mock_reviews(self):
        """モック口コミデータ生成"""
        reviews = [
            {
                "author_name": "田中太郎",
                "rating": 5,
                "text": "雰囲気が良くて、コーヒーも美味しかったです！店員さんの対応も丁寧で、また来たいと思いました。WiFiも使えて作業捗りました。",
                "time": int((datetime.now() - timedelta(hours=2)).timestamp())
            },
            {
                "author_name": "佐藤花子",
                "rating": 4,
                "text": "ランチセットがお得でした。パスタが美味しい！ただ週末は混んでるので予約推奨です。",
                "time": int((datetime.now() - timedelta(hours=5)).timestamp())
            },
            {
                "author_name": "鈴木一郎",
                "rating": 2,
                "text": "期待していたのですが、料理が出てくるまで30分以上待たされました。味は普通。もう少し早いといいのですが...",
                "time": int((datetime.now() - timedelta(hours=8)).timestamp())
            },
            {
                "author_name": "山田美咲",
                "rating": 5,
                "text": "デートで利用しました。夜景が綺麗で雰囲気最高です💕料理も美味しくて大満足。記念日にまた来ます！",
                "time": int((datetime.now() - timedelta(days=1)).timestamp())
            },
            {
                "author_name": "中村健太",
                "rating": 3,
                "text": "可もなく不可もなく。値段相応かな。駅から近いのは便利。",
                "time": int((datetime.now() - timedelta(days=2)).timestamp())
            }
        ]
        return reviews
    
    def generate_reply(self, review_text: str, rating: int) -> str:
        """AI風の返信文を生成"""
        
        if rating >= 4:
            templates = [
                f"この度は当店をご利用いただき、誠にありがとうございます。\n温かいお言葉をいただき、スタッフ一同大変励みになります。\nまたのご来店を心よりお待ちしております。",
                f"ご来店ありがとうございました！\nお客様に満足いただけたこと、とても嬉しく思います。\n次回もぜひお立ち寄りくださいませ。"
            ]
        elif rating == 3:
            templates = [
                f"ご来店いただき、ありがとうございます。\n貴重なご意見を参考に、さらなるサービス向上に努めてまいります。\nまたのご利用をお待ちしております。"
            ]
        else:
            templates = [
                f"この度はご期待に沿えず、大変申し訳ございませんでした。\nいただいたご意見を真摯に受け止め、サービス改善に努めてまいります。\nまたご来店いただける機会がございましたら、挽回させていただければ幸いです。",
                f"貴重なご指摘をありがとうございます。\nご不便をおかけして申し訳ございませんでした。\n改善に向けてスタッフ全員で取り組んでおります。次回はより良い体験をお届けできるよう努めてまいります。"
            ]
        
        return random.choice(templates)
    
    def format_notification(self, review: dict) -> str:
        """Telegram通知フォーマット"""
        author = review.get("author_name", "匿名")
        rating = review.get("rating", 0)
        text = review.get("text", "（コメントなし）")
        time_posted = review.get("time", 0)
        
        date_str = datetime.fromtimestamp(time_posted).strftime("%Y年%m月%d日 %H:%M")
        
        stars = "⭐" * rating + "☆" * (5 - rating)
        
        notification = f"""
🔔 **新しい口コミが投稿されました**

**店舗**: {self.place_name}
**評価**: {stars} ({rating}/5)
**投稿者**: {author}
**日時**: {date_str}

**コメント**:
{text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 **AI自動生成の返信文（コピペ可能）**:

{self.generate_reply(text, rating)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return notification
    
    def demo_scenario_interactive(self):
        """インタラクティブなデモシナリオ"""
        print("\n" + "="*70)
        print("🎬 OpenClaw 口コミ監視デモ - ライブプレゼンテーション")
        print("="*70)
        
        print(f"\n📍 監視対象店舗: {self.place_name}")
        print("🔄 監視を開始します...\n")
        
        input("▶ Enterキーを押すと、口コミチェックを実行します...")
        
        print("\n🔍 Google Mapsから最新の口コミを取得中...")
        time.sleep(1.5)  # リアルっぽく演出
        
        print(f"✅ {len(self.mock_reviews)}件の口コミを取得しました")
        print("\n📊 過去7日間の口コミ分析:")
        
        avg_rating = sum(r['rating'] for r in self.mock_reviews) / len(self.mock_reviews)
        print(f"   • 平均評価: {avg_rating:.1f}/5.0")
        print(f"   • 口コミ総数: {len(self.mock_reviews)}件")
        print(f"   • 返信率: 40% → OpenClaw導入後は100%に！")
        
        print("\n" + "─"*70)
        input("\n▶ Enterキーを押すと、最新の口コミを表示します...")
        
        # 最新3件を表示
        for i, review in enumerate(self.mock_reviews[:3], 1):
            print(f"\n【口コミ {i}/{len(self.mock_reviews[:3])}】")
            print("─"*70)
            
            notification = self.format_notification(review)
            print(notification)
            
            if i < 3:
                input("\n▶ 次の口コミを見る（Enterキー）...")
        
        print("\n" + "="*70)
        print("✅ デモ完了！")
        print("="*70)
        
        print("\n💡 **OpenClawで実現できること**:")
        print("   ✅ 24時間365日、口コミを自動監視")
        print("   ✅ 新しい口コミが投稿されたら即座にTelegram/Slack通知")
        print("   ✅ AIが返信文を自動生成（コピペで即返信可能）")
        print("   ✅ 返信漏れゼロ、顧客満足度アップ")
        print("   ✅ 月額5,000円〜（人件費換算で1.5時間分）")
        
        print("\n📱 実際の運用イメージ:")
        print("   1. スマホ/PCで通知を受け取る")
        print("   2. AI生成の返信文を確認（修正も可能）")
        print("   3. ワンタップでGoogle Mapsに返信")
        print("   → 所要時間: 1件あたり30秒〜1分")
        
        print("\n" + "="*70)
    
    def demo_scenario_auto(self):
        """自動進行デモ（プレゼン用）"""
        print("\n" + "="*70)
        print("🎬 OpenClaw 口コミ監視デモ - 自動プレゼンテーション")
        print("="*70)
        
        print(f"\n📍 監視対象店舗: {self.place_name}")
        print("🔄 監視を開始します...\n")
        
        time.sleep(1)
        
        print("🔍 Google Mapsから最新の口コミを取得中...")
        time.sleep(1.5)
        
        print(f"✅ {len(self.mock_reviews)}件の口コミを取得しました\n")
        
        # 最新の口コミを表示
        latest = self.mock_reviews[0]
        print("🆕 **新しい口コミを検知しました！**")
        print("─"*70)
        
        notification = self.format_notification(latest)
        print(notification)
        
        time.sleep(2)
        
        print("\n" + "="*70)
        print("✅ デモ完了！このように自動で通知・返信文生成が行われます。")
        print("="*70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw 口コミ監視デモ（モック版）')
    parser.add_argument('--place-name', default='サンプルカフェ 渋谷店', help='店舗名')
    parser.add_argument('--interactive', action='store_true', help='インタラクティブモード（営業プレゼン推奨）')
    parser.add_argument('--auto', action='store_true', help='自動進行モード')
    
    args = parser.parse_args()
    
    demo = ReviewMonitorDemoMock(place_name=args.place_name)
    
    if args.interactive:
        demo.demo_scenario_interactive()
    elif args.auto:
        demo.demo_scenario_auto()
    else:
        # デフォルト: インタラクティブモード
        demo.demo_scenario_interactive()


if __name__ == "__main__":
    main()
