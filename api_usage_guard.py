#!/usr/bin/env python3
"""
API Usage Guard - Prevent abnormal API consumption
Monitors usage patterns and alerts on anomalies
"""
import json
import os
from datetime import datetime, timedelta

class UsageGuard:
    """Protect against abnormal API usage"""
    
    def __init__(self, data_file="/root/openclaw_data/lin/data/usage_guard.json"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        self.data = self._load_data()
        
        # Safety thresholds
        self.limits = {
            "tokens_per_session": 100000,      # 100K tokens/session (約$0.50)
            "tokens_per_hour": 200000,         # 200K tokens/hour (約$1.00)
            "tokens_per_day": 1000000,         # 1M tokens/day (約$5.00)
            "cost_per_session": 0.50,          # $0.50/session
            "cost_per_hour": 1.00,             # $1.00/hour
            "cost_per_day": 5.00,              # $5.00/day
        }
    
    def _load_data(self):
        """Load tracking data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {
            "sessions": [],
            "daily_totals": {},
            "alerts": []
        }
    
    def _save_data(self):
        """Save tracking data"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_session(self, tokens_in: int, tokens_out: int, cost: float):
        """Record a session"""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        session = {
            "timestamp": now.isoformat(),
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "total_tokens": tokens_in + tokens_out,
            "cost": cost
        }
        
        self.data["sessions"].append(session)
        
        # Update daily total
        if today not in self.data["daily_totals"]:
            self.data["daily_totals"][today] = {
                "tokens": 0,
                "cost": 0.0,
                "sessions": 0
            }
        
        self.data["daily_totals"][today]["tokens"] += session["total_tokens"]
        self.data["daily_totals"][today]["cost"] += cost
        self.data["daily_totals"][today]["sessions"] += 1
        
        # Check for anomalies
        self._check_anomalies(session, today)
        
        self._save_data()
    
    def _check_anomalies(self, session: dict, today: str):
        """Check for abnormal usage"""
        alerts = []
        
        # Check session limit
        if session["total_tokens"] > self.limits["tokens_per_session"]:
            alerts.append(f"⚠️ セッション上限超過: {session['total_tokens']:,} tokens (制限: {self.limits['tokens_per_session']:,})")
        
        if session["cost"] > self.limits["cost_per_session"]:
            alerts.append(f"⚠️ セッションコスト上限超過: ${session['cost']:.2f} (制限: ${self.limits['cost_per_session']:.2f})")
        
        # Check hourly limit
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_sessions = [
            s for s in self.data["sessions"]
            if datetime.fromisoformat(s["timestamp"]) > one_hour_ago
        ]
        hourly_tokens = sum(s["total_tokens"] for s in recent_sessions)
        hourly_cost = sum(s["cost"] for s in recent_sessions)
        
        if hourly_tokens > self.limits["tokens_per_hour"]:
            alerts.append(f"⚠️ 1時間の上限超過: {hourly_tokens:,} tokens (制限: {self.limits['tokens_per_hour']:,})")
        
        if hourly_cost > self.limits["cost_per_hour"]:
            alerts.append(f"⚠️ 1時間のコスト上限超過: ${hourly_cost:.2f} (制限: ${self.limits['cost_per_hour']:.2f})")
        
        # Check daily limit
        daily = self.data["daily_totals"][today]
        if daily["tokens"] > self.limits["tokens_per_day"]:
            alerts.append(f"🚨 1日の上限超過: {daily['tokens']:,} tokens (制限: {self.limits['tokens_per_day']:,})")
        
        if daily["cost"] > self.limits["cost_per_day"]:
            alerts.append(f"🚨 1日のコスト上限超過: ${daily['cost']:.2f} (制限: ${self.limits['cost_per_day']:.2f})")
        
        # Save alerts
        if alerts:
            alert_entry = {
                "timestamp": datetime.now().isoformat(),
                "alerts": alerts
            }
            self.data["alerts"].append(alert_entry)
            
            # Write to alert file
            self._write_alert(alerts)
    
    def _write_alert(self, alerts: list):
        """Write alert to file"""
        alert_file = "/root/openclaw_data/lin/data/usage_alert.txt"
        
        message = f"""🚨 API使用量アラート
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{chr(10).join(alerts)}

推奨アクション:
1. 現在の作業を一時停止
2. 使用状況を確認: python3 api_usage_guard.py status
3. 必要に応じて制限を調整

詳細: /root/openclaw_data/lin/data/usage_guard.json
"""
        
        with open(alert_file, 'w') as f:
            f.write(message)
        
        print(message)
    
    def get_status(self):
        """Get current usage status"""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        # Daily stats
        daily = self.data["daily_totals"].get(today, {
            "tokens": 0,
            "cost": 0.0,
            "sessions": 0
        })
        
        # Hourly stats
        one_hour_ago = now - timedelta(hours=1)
        recent_sessions = [
            s for s in self.data["sessions"]
            if datetime.fromisoformat(s["timestamp"]) > one_hour_ago
        ]
        hourly_tokens = sum(s["total_tokens"] for s in recent_sessions)
        hourly_cost = sum(s["cost"] for s in recent_sessions)
        
        # Recent alerts
        recent_alerts = [
            a for a in self.data["alerts"]
            if datetime.fromisoformat(a["timestamp"]) > now - timedelta(days=1)
        ]
        
        return {
            "today": {
                "tokens": daily["tokens"],
                "cost": daily["cost"],
                "sessions": daily["sessions"],
                "limit_tokens": self.limits["tokens_per_day"],
                "limit_cost": self.limits["cost_per_day"],
                "percentage_tokens": (daily["tokens"] / self.limits["tokens_per_day"]) * 100,
                "percentage_cost": (daily["cost"] / self.limits["cost_per_day"]) * 100,
            },
            "last_hour": {
                "tokens": hourly_tokens,
                "cost": hourly_cost,
                "sessions": len(recent_sessions),
                "limit_tokens": self.limits["tokens_per_hour"],
                "limit_cost": self.limits["cost_per_hour"],
            },
            "recent_alerts": recent_alerts
        }


def print_status():
    """Print usage status"""
    guard = UsageGuard()
    status = guard.get_status()
    
    print("📊 API使用状況")
    print("=" * 60)
    
    print("\n【今日の使用量】")
    today = status["today"]
    print(f"トークン: {today['tokens']:,} / {today['limit_tokens']:,} ({today['percentage_tokens']:.1f}%)")
    print(f"コスト:   ${today['cost']:.2f} / ${today['limit_cost']:.2f} ({today['percentage_cost']:.1f}%)")
    print(f"セッション数: {today['sessions']}")
    
    print("\n【過去1時間】")
    hour = status["last_hour"]
    print(f"トークン: {hour['tokens']:,} / {hour['limit_tokens']:,}")
    print(f"コスト:   ${hour['cost']:.2f} / ${hour['limit_cost']:.2f}")
    print(f"セッション数: {hour['sessions']}")
    
    if status["recent_alerts"]:
        print("\n【最近のアラート】")
        for alert in status["recent_alerts"][-3:]:
            timestamp = datetime.fromisoformat(alert["timestamp"]).strftime("%m-%d %H:%M")
            print(f"\n{timestamp}:")
            for msg in alert["alerts"]:
                print(f"  {msg}")
    else:
        print("\n✅ アラートなし")
    
    print("\n" + "=" * 60)
    
    # Safety check
    if today['percentage_cost'] > 80:
        print("\n🚨 警告: 今日のコストが上限の80%を超えています！")
    elif today['percentage_cost'] > 50:
        print("\n⚠️  注意: 今日のコストが上限の50%を超えています")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            print_status()
        
        elif command == "record":
            # Example: python api_usage_guard.py record 10000 5000 0.15
            tokens_in = int(sys.argv[2])
            tokens_out = int(sys.argv[3])
            cost = float(sys.argv[4])
            
            guard = UsageGuard()
            guard.record_session(tokens_in, tokens_out, cost)
            print(f"✅ 記録しました: {tokens_in + tokens_out:,} tokens, ${cost:.2f}")
        
        elif command == "reset":
            data_file = "/root/openclaw_data/lin/data/usage_guard.json"
            if os.path.exists(data_file):
                os.remove(data_file)
            print("✅ リセットしました")
    
    else:
        print_status()
