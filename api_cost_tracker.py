#!/usr/bin/env python3
"""
API Cost Tracker for Claude/OpenAI usage
Alerts when $2 increments are reached
"""
import json
import os
from datetime import datetime

class APICostTracker:
    """Track API costs and alert on thresholds"""
    
    def __init__(self, tracker_file="/root/openclaw_data/lin/data/api_costs.json"):
        self.tracker_file = tracker_file
        os.makedirs(os.path.dirname(tracker_file), exist_ok=True)
        self.data = self._load_data()
    
    def _load_data(self):
        """Load tracking data"""
        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        return {
            "total_spent": 0.0,
            "last_alert_at": 0.0,
            "alert_threshold": 2.0,  # $2
            "sessions": [],
            "last_updated": None
        }
    
    def _save_data(self):
        """Save tracking data"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.tracker_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_usage(self, model: str, input_tokens: int, output_tokens: int, cost_usd: float):
        """
        Record API usage
        
        Args:
            model: Model name (e.g., 'claude-sonnet-4')
            input_tokens: Input token count
            output_tokens: Output token count
            cost_usd: Cost in USD
        """
        session = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost_usd
        }
        
        self.data["sessions"].append(session)
        self.data["total_spent"] += cost_usd
        
        # Check if we crossed $2 threshold
        if self._should_alert():
            self._send_alert()
        
        self._save_data()
    
    def _should_alert(self) -> bool:
        """Check if we should send an alert"""
        total = self.data["total_spent"]
        last_alert = self.data["last_alert_at"]
        threshold = self.data["alert_threshold"]
        
        # Alert every $2
        return (total - last_alert) >= threshold
    
    def _send_alert(self):
        """Send cost alert"""
        total = self.data["total_spent"]
        last_alert = self.data["last_alert_at"]
        spent_since = total - last_alert
        
        message = f"""💰 API Cost Alert
        
Total spent: ${total:.2f}
Since last alert: ${spent_since:.2f}

Recent usage:
{self._format_recent_sessions()}
"""
        
        print(message)
        
        # Write to alert file for OpenClaw to pick up
        alert_file = "/root/openclaw_data/lin/data/cost_alert.txt"
        with open(alert_file, 'w') as f:
            f.write(message)
        
        # Update last alert marker
        self.data["last_alert_at"] = total
        self._save_data()
    
    def _format_recent_sessions(self, limit=5) -> str:
        """Format recent sessions"""
        sessions = self.data["sessions"][-limit:]
        lines = []
        for s in sessions:
            lines.append(f"- {s['model']}: {s['input_tokens']}→{s['output_tokens']} tokens (${s['cost_usd']:.4f})")
        return "\n".join(lines)
    
    def get_summary(self) -> dict:
        """Get cost summary"""
        return {
            "total_spent": self.data["total_spent"],
            "session_count": len(self.data["sessions"]),
            "last_updated": self.data["last_updated"]
        }


def calculate_claude_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate Claude API cost
    
    Pricing (as of 2024):
    - Claude Sonnet 3.5: $3/MTok input, $15/MTok output
    - Claude Sonnet 4: Similar (check latest)
    """
    # Pricing per million tokens
    pricing = {
        "claude-sonnet-3.5": {"input": 3.0, "output": 15.0},
        "claude-sonnet-4": {"input": 3.0, "output": 15.0},  # Update if different
        "claude-opus": {"input": 15.0, "output": 75.0},
    }
    
    # Default to sonnet pricing
    rates = pricing.get(model, {"input": 3.0, "output": 15.0})
    
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    
    return input_cost + output_cost


if __name__ == "__main__":
    import sys
    
    tracker = APICostTracker()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "summary":
            summary = tracker.get_summary()
            print(f"Total spent: ${summary['total_spent']:.2f}")
            print(f"Sessions: {summary['session_count']}")
            print(f"Last updated: {summary['last_updated']}")
        
        elif command == "record":
            # Example: python api_cost_tracker.py record claude-sonnet-4 1000 500
            model = sys.argv[2]
            input_tokens = int(sys.argv[3])
            output_tokens = int(sys.argv[4])
            cost = calculate_claude_cost(model, input_tokens, output_tokens)
            tracker.record_usage(model, input_tokens, output_tokens, cost)
            print(f"Recorded: ${cost:.4f}")
        
        elif command == "reset":
            os.remove(tracker.tracker_file)
            print("Tracker reset")
    
    else:
        summary = tracker.get_summary()
        print(f"💰 API Cost Tracker\n")
        print(f"Total spent: ${summary['total_spent']:.2f}")
        print(f"Sessions: {summary['session_count']}")
