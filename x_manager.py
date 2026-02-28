#!/usr/bin/env python3
"""
X (Twitter) Account Manager for Lin
Supports content creation, scheduling, and engagement
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

class XManager:
    """
    Manage X/Twitter account operations
    """
    
    def __init__(self, content_file="/root/openclaw_data/lin/x_content_queue.json"):
        self.content_file = content_file
        self.queue = self._load_queue()
    
    def _load_queue(self) -> Dict:
        """Load content queue"""
        if os.path.exists(self.content_file):
            with open(self.content_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "scheduled": [],
            "drafts": [],
            "posted": [],
            "templates": {}
        }
    
    def _save_queue(self):
        """Save content queue"""
        with open(self.content_file, 'w', encoding='utf-8') as f:
            json.dump(self.queue, f, indent=2, ensure_ascii=False)
    
    def create_morning_post(self, stats: Dict = None) -> str:
        """
        Generate morning status update
        
        Args:
            stats: Dictionary with OpenClaw stats
        """
        if not stats:
            stats = {
                "markets_monitored": 0,
                "opportunities_found": 0,
                "reports_generated": 0
            }
        
        post = f"""おはようございます☀️

今日のOpenClaw稼働状況：
📊 監視市場: {stats.get('markets_monitored', 0)}
🎯 検出機会: {stats.get('opportunities_found', 0)}
📈 分析完了: {stats.get('reports_generated', 0)}レポート

本日も24時間フル稼働でサポートします💪

#OpenClaw #AI #自動化"""
        
        return post
    
    def create_insight_thread(self, topic: str, points: List[str]) -> List[str]:
        """
        Create thread about a topic
        
        Args:
            topic: Main topic
            points: List of points to cover
        """
        thread = []
        
        # Thread starter
        thread.append(f"{topic}について解説します🧵\n\n#OpenClaw #AI活用")
        
        # Each point as a tweet
        for i, point in enumerate(points, 1):
            thread.append(f"{i}/ {point}")
        
        # Conclusion
        thread.append(f"まとめ：{topic}を活用することで、〇〇が可能になります。\n\n質問・相談はDMへ📩")
        
        return thread
    
    def create_result_post(self, achievement: str, details: str = "") -> str:
        """
        Create achievement announcement post
        """
        post = f"""🎉 {achievement}

{details}

OpenClawでここまで自動化できました💡

興味ある方はDMください👉

#OpenClaw #AI #自動化 #成果報告"""
        
        return post
    
    def create_consulting_pitch(self, service: str, price: str = "応相談") -> str:
        """
        Create consulting service pitch
        """
        post = f"""【AIコンサル受付中】

サービス: {service}
料金: {price}
納期: 1-2週間

OpenClawを活用した業務自動化で、
あなたの時間を解放します⏰

✅ 24時間稼働
✅ 高精度分析
✅ 完全自動化

ご相談はDMへ📩

#AIコンサル #業務自動化 #OpenClaw"""
        
        return post
    
    def schedule_post(self, content: str, scheduled_time: str = None, post_type: str = "normal"):
        """
        Schedule a post
        
        Args:
            content: Post content
            scheduled_time: ISO format datetime string
            post_type: normal, thread, reply
        """
        post = {
            "content": content,
            "scheduled_time": scheduled_time or datetime.now().isoformat(),
            "post_type": post_type,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        self.queue["scheduled"].append(post)
        self._save_queue()
        
        print(f"✅ Post scheduled for {scheduled_time or 'ASAP'}")
        return post
    
    def save_draft(self, content: str, notes: str = ""):
        """Save post as draft"""
        draft = {
            "content": content,
            "notes": notes,
            "created_at": datetime.now().isoformat()
        }
        
        self.queue["drafts"].append(draft)
        self._save_queue()
        
        print(f"💾 Draft saved")
        return draft
    
    def generate_daily_schedule(self) -> List[Dict]:
        """
        Generate suggested posting schedule for today
        """
        now = datetime.now()
        schedule = []
        
        # Morning post (8:00)
        morning = now.replace(hour=8, minute=0, second=0)
        if morning > now:
            schedule.append({
                "time": morning.isoformat(),
                "type": "morning_status",
                "content": self.create_morning_post()
            })
        
        # Insight thread (12:00)
        noon = now.replace(hour=12, minute=0, second=0)
        if noon > now:
            schedule.append({
                "time": noon.isoformat(),
                "type": "insight_thread",
                "content": "[Topic TBD] - Use create_insight_thread()"
            })
        
        # Achievement post (18:00)
        evening = now.replace(hour=18, minute=0, second=0)
        if evening > now:
            schedule.append({
                "time": evening.isoformat(),
                "type": "achievement",
                "content": "[Achievement TBD] - Use create_result_post()"
            })
        
        # Evening status (21:00)
        night = now.replace(hour=21, minute=0, second=0)
        if night > now:
            schedule.append({
                "time": night.isoformat(),
                "type": "evening_status",
                "content": "今日の成果まとめ"
            })
        
        return schedule
    
    def generate_consulting_content(self) -> List[str]:
        """
        Generate content ideas for consulting promotion
        """
        ideas = [
            "OpenClawで業務自動化した実例5選",
            "AIコンサルの裏側：こうやって分析してます",
            "24時間稼働AIエージェントの威力",
            "従来の外注 vs OpenClaw：コスト比較",
            "AIに任せるべき業務・任せちゃダメな業務",
            "初回相談無料キャンペーン告知",
            "クライアント事例紹介（許可取得済み前提）",
            "Q&A：よくある質問に答えます"
        ]
        
        return ideas
    
    def analyze_best_posting_times(self) -> Dict:
        """
        Analyze best times to post (placeholder)
        In production, would analyze past engagement data
        """
        return {
            "weekday_morning": "7:00-9:00",
            "weekday_lunch": "12:00-13:00",
            "weekday_evening": "20:00-22:00",
            "weekend_morning": "9:00-11:00",
            "weekend_evening": "19:00-21:00"
        }
    
    def list_scheduled(self):
        """List scheduled posts"""
        if not self.queue["scheduled"]:
            print("📭 No scheduled posts")
            return
        
        print(f"\n📅 Scheduled Posts ({len(self.queue['scheduled'])}):\n")
        for i, post in enumerate(self.queue["scheduled"], 1):
            print(f"{i}. [{post['scheduled_time']}]")
            print(f"   Type: {post['post_type']}")
            print(f"   Content: {post['content'][:60]}...")
            print()
    
    def list_drafts(self):
        """List draft posts"""
        if not self.queue["drafts"]:
            print("📭 No drafts")
            return
        
        print(f"\n📝 Drafts ({len(self.queue['drafts'])}):\n")
        for i, draft in enumerate(self.queue["drafts"], 1):
            print(f"{i}. {draft['content'][:60]}...")
            if draft.get('notes'):
                print(f"   Notes: {draft['notes']}")
            print()


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='X Account Manager')
    subparsers = parser.add_subparsers(dest='command')
    
    # Morning post
    subparsers.add_parser('morning', help='Generate morning post')
    
    # Thread
    thread_parser = subparsers.add_parser('thread', help='Create insight thread')
    thread_parser.add_argument('topic', help='Thread topic')
    thread_parser.add_argument('--points', nargs='+', help='Points to cover')
    
    # Consulting pitch
    pitch_parser = subparsers.add_parser('pitch', help='Create consulting pitch')
    pitch_parser.add_argument('service', help='Service description')
    pitch_parser.add_argument('--price', default='応相談')
    
    # Schedule
    subparsers.add_parser('schedule', help='Show daily schedule suggestion')
    
    # Ideas
    subparsers.add_parser('ideas', help='Generate content ideas')
    
    # List
    subparsers.add_parser('list-scheduled', help='List scheduled posts')
    subparsers.add_parser('list-drafts', help='List drafts')
    
    args = parser.parse_args()
    
    manager = XManager()
    
    if args.command == 'morning':
        post = manager.create_morning_post()
        print(f"\n{post}\n")
        manager.save_draft(post, "Morning status")
        
    elif args.command == 'thread':
        points = args.points or ["ポイント1", "ポイント2", "ポイント3"]
        thread = manager.create_insight_thread(args.topic, points)
        print(f"\n🧵 Thread ({len(thread)} tweets):\n")
        for i, tweet in enumerate(thread, 1):
            print(f"{i}/ {tweet}\n")
        
    elif args.command == 'pitch':
        post = manager.create_consulting_pitch(args.service, args.price)
        print(f"\n{post}\n")
        manager.save_draft(post, "Consulting pitch")
        
    elif args.command == 'schedule':
        schedule = manager.generate_daily_schedule()
        print(f"\n📅 Suggested Posting Schedule:\n")
        for item in schedule:
            print(f"⏰ {item['time']}")
            print(f"   Type: {item['type']}")
            print(f"   Content: {item['content'][:60]}...")
            print()
            
    elif args.command == 'ideas':
        ideas = manager.generate_consulting_content()
        print(f"\n💡 Content Ideas for Consulting Promotion:\n")
        for i, idea in enumerate(ideas, 1):
            print(f"{i}. {idea}")
        print()
        
    elif args.command == 'list-scheduled':
        manager.list_scheduled()
        
    elif args.command == 'list-drafts':
        manager.list_drafts()
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
