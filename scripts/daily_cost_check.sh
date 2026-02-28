#!/bin/bash
# Daily API cost check - run this every morning

echo "📊 今日のAPI使用状況チェック"
echo "================================"
echo ""

# Show usage guard status
python3 /root/openclaw_data/lin/api_usage_guard.py status

echo ""
echo "💡 ヒント:"
echo "  - 1日の推奨上限: $5.00"
echo "  - 20ドルで約4日間使用可能"
echo "  - 会話は簡潔に、必要な時だけ"
echo ""

# Check for alerts
ALERT_FILE="/root/openclaw_data/lin/data/usage_alert.txt"
if [ -f "$ALERT_FILE" ]; then
    echo "🚨 アラートあり！"
    cat "$ALERT_FILE"
fi

echo ""
echo "詳細ガイド: /root/openclaw_data/lin/SAFETY_GUIDELINES.md"
