#!/bin/bash
# Switch default model to Claude Haiku (cheaper)

echo "🔄 Switching to Claude Haiku 3.5 (cost-efficient mode)"
echo "=========================================="
echo ""

# Check OpenClaw config location
CONFIG_DIR="$HOME/.config/openclaw"
CONFIG_FILE="$CONFIG_DIR/config.json"

if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating config directory..."
    mkdir -p "$CONFIG_DIR"
fi

# Create/update config
cat > "$CONFIG_FILE" << 'EOF'
{
  "default_model": "anthropic/claude-haiku-3.5",
  "models": {
    "haiku": "anthropic/claude-haiku-3.5",
    "sonnet": "anthropic/claude-sonnet-4",
    "opus": "anthropic/claude-opus"
  },
  "cost_optimization": true
}
EOF

echo "✅ Default model set to: Claude Haiku 3.5"
echo ""
echo "💰 Cost savings: ~70% cheaper than Sonnet"
echo ""
echo "📊 Pricing:"
echo "  Haiku:  \$0.80/MTok input, \$4.00/MTok output"
echo "  Sonnet: \$3.00/MTok input, \$15.00/MTok output"
echo ""
echo "🔧 Usage:"
echo "  Normal: Just chat normally (uses Haiku)"
echo "  Complex: Prefix with '@sonnet' for hard tasks"
echo ""
echo "Example:"
echo "  'hi' → Haiku"
echo "  '@sonnet design new system' → Sonnet"
echo ""
echo "📖 Full guide: /root/openclaw_data/lin/MODEL_PRICING.md"
