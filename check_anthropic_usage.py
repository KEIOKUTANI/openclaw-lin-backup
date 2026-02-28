#!/usr/bin/env python3
"""
Check Anthropic API usage and send alerts when $2 thresholds are crossed
"""
import os
import json
import requests
from datetime import datetime

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TRACKER_FILE = "/root/openclaw_data/lin/data/anthropic_usage.json"

def load_tracker():
    """Load usage tracker"""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, 'r') as f:
            return json.load(f)
    return {
        "last_total": 0.0,
        "last_alert_at": 0.0,
        "alert_threshold": 2.0,
        "checks": []
    }

def save_tracker(data):
    """Save usage tracker"""
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_anthropic_usage():
    """
    Get usage from Anthropic API
    Note: Anthropic doesn't provide a public usage API endpoint yet.
    You need to check the dashboard: https://console.anthropic.com/settings/billing
    
    For now, this is a placeholder that you can update with manual input.
    """
    print("⚠️  Anthropicは現在、プログラムで使用量を取得するAPIを提供していません")
    print("📊 使用量を確認: https://console.anthropic.com/settings/billing")
    print()
    
    # Manual input option
    response = input("現在の累計使用額（USD）を入力してください（スキップする場合はEnter）: ")
    
    if response.strip():
        try:
            return float(response.strip().replace('$', ''))
        except ValueError:
            print("無効な金額です")
            return None
    
    return None

def check_and_alert():
    """Check usage and alert if threshold crossed"""
    tracker = load_tracker()
    
    print("💰 Claude API 使用量チェック")
    print("=" * 50)
    
    current_total = get_anthropic_usage()
    
    if current_total is None:
        print("\n使用量の取得をスキップしました")
        return
    
    # Record check
    tracker["checks"].append({
        "timestamp": datetime.now().isoformat(),
        "total": current_total
    })
    
    last_total = tracker["last_total"]
    last_alert = tracker["last_alert_at"]
    threshold = tracker["alert_threshold"]
    
    spent_since_last_check = current_total - last_total
    spent_since_last_alert = current_total - last_alert
    
    print(f"\n現在の累計: ${current_total:.2f}")
    print(f"前回チェック時: ${last_total:.2f}")
    print(f"前回からの増加: ${spent_since_last_check:.2f}")
    print(f"前回アラートから: ${spent_since_last_alert:.2f}")
    
    # Check if we crossed $2 threshold
    if spent_since_last_alert >= threshold:
        print(f"\n🚨 アラート: ${threshold:.0f}以上使用しました！")
        
        # Save alert
        alert_message = f"""💰 Claude API使用料アラート

累計使用額: ${current_total:.2f}
前回アラートから: ${spent_since_last_alert:.2f}

チェック時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        alert_file = "/root/openclaw_data/lin/data/cost_alert.txt"
        with open(alert_file, 'w') as f:
            f.write(alert_message)
        
        print(alert_message)
        
        # Update last alert marker
        tracker["last_alert_at"] = current_total
    else:
        remaining = threshold - spent_since_last_alert
        print(f"\n次のアラートまで: ${remaining:.2f}")
    
    # Update tracker
    tracker["last_total"] = current_total
    save_tracker(tracker)
    
    print("\n✅ 記録を更新しました")

if __name__ == "__main__":
    check_and_alert()
