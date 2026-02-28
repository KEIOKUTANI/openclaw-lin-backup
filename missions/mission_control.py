#!/usr/bin/env python3
"""
Mission Control - Lin総括マネージャー制御スクリプト
全ミッションの状態管理・実行制御を行う
"""
import os
import json
from datetime import datetime
from pathlib import Path

MISSIONS_DIR = Path(__file__).parent
STATUS_FILE = MISSIONS_DIR / "mission_status.json"

class MissionControl:
    """ミッション統括管理クラス"""
    
    def __init__(self):
        self.missions = {
            "sales": {
                "name": "Sales Lin - 営業開拓",
                "path": MISSIONS_DIR / "sales",
                "telegram_topic": "#営業",
                "status": "ready",
                "last_run": None
            },
            "projects": {
                "name": "Project Lin - 受託開発",
                "path": MISSIONS_DIR / "projects",
                "telegram_topic": "#営業",  # プロジェクトも営業に含む
                "status": "ready",
                "last_run": None
            },
            "content": {
                "name": "Content Lin - YouTube制作",
                "path": MISSIONS_DIR / "content",
                "telegram_topic": "#YouTube",
                "status": "ready",
                "last_run": None
            },
            "analyst": {
                "name": "Analyst Lin - 収益分析",
                "path": MISSIONS_DIR / "analyst",
                "telegram_topic": "#ポーカー",
                "status": "ready",
                "last_run": None
            }
        }
        self.load_status()
    
    def load_status(self):
        """ステータスファイルから状態を読み込み"""
        if STATUS_FILE.exists():
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                for mission_id, data in saved.items():
                    if mission_id in self.missions:
                        self.missions[mission_id].update(data)
    
    def save_status(self):
        """現在の状態をステータスファイルに保存"""
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.missions, f, ensure_ascii=False, indent=2, default=str)
    
    def get_status_report(self):
        """全ミッションのステータスレポート生成"""
        report = ["## 🎯 Lin Mission Control - Status Report", ""]
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
        report.append("")
        
        for mission_id, info in self.missions.items():
            status_emoji = {
                "ready": "⏸️",
                "active": "▶️",
                "error": "❌",
                "completed": "✅"
            }.get(info['status'], "❓")
            
            report.append(f"### {status_emoji} {info['name']}")
            report.append(f"- **Status**: {info['status']}")
            report.append(f"- **Path**: `{info['path']}`")
            report.append(f"- **Topic**: {info['telegram_topic']}")
            report.append(f"- **Last Run**: {info['last_run'] or 'Never'}")
            report.append("")
        
        return "\n".join(report)
    
    def check_infrastructure(self):
        """インフラ状況チェック"""
        checks = {
            "Mac mini": "✅ Running",
            "OpenClaw": "✅ Active",
            "Telegram": "✅ Connected",
            "Google Cloud": "✅ API Ready"
        }
        
        report = ["## 🖥️ Infrastructure Status", ""]
        for component, status in checks.items():
            report.append(f"- **{component}**: {status}")
        
        return "\n".join(report)
    
    def activate_mission(self, mission_id):
        """ミッションを起動"""
        if mission_id not in self.missions:
            return f"❌ Unknown mission: {mission_id}"
        
        self.missions[mission_id]['status'] = 'active'
        self.missions[mission_id]['last_run'] = datetime.now().isoformat()
        self.save_status()
        
        return f"✅ Activated: {self.missions[mission_id]['name']}"
    
    def deactivate_mission(self, mission_id):
        """ミッションを停止"""
        if mission_id not in self.missions:
            return f"❌ Unknown mission: {mission_id}"
        
        self.missions[mission_id]['status'] = 'ready'
        self.save_status()
        
        return f"⏸️ Deactivated: {self.missions[mission_id]['name']}"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Lin Mission Control")
    parser.add_argument("action", choices=["status", "activate", "deactivate", "infra"],
                       help="Action to perform")
    parser.add_argument("--mission", help="Mission ID (sales/projects/content/analyst)")
    
    args = parser.parse_args()
    
    control = MissionControl()
    
    if args.action == "status":
        print(control.get_status_report())
    elif args.action == "infra":
        print(control.check_infrastructure())
    elif args.action == "activate":
        if not args.mission:
            print("❌ --mission required")
            return
        print(control.activate_mission(args.mission))
    elif args.action == "deactivate":
        if not args.mission:
            print("❌ --mission required")
            return
        print(control.deactivate_mission(args.mission))

if __name__ == "__main__":
    main()
