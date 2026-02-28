# Environment Variables Template

## Polymarket
```bash
POLYGON_WALLET_PRIVATE_KEY="<YOUR_PRIVATE_KEY>"
OPENAI_API_KEY="<YOUR_OPENAI_KEY>"
POLYGON_RPC_URL="https://polygon-rpc.com"
HTTPS_PROXY=""  # Optional: for geo-restriction bypass
HTTP_PROXY=""   # Optional: for geo-restriction bypass
```

## Security Notes
- NEVER commit actual .env to git
- Use `chmod 600 .env` to restrict permissions
- Rotate keys regularly
- Use separate keys for testing vs production

**Last Updated**: 2026-02-28
