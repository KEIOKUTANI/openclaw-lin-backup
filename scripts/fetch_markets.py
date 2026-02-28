#!/usr/bin/env python3
"""
Fetch trending markets from Polymarket for analysis
"""
import requests
import json
from datetime import datetime

def fetch_markets():
    """Fetch active markets from Polymarket"""
    
    # Polymarket public API endpoint
    url = "https://gamma-api.polymarket.com/markets"
    
    params = {
        "limit": 50,
        "active": "true",
        "closed": "false",
        "order": "volume24hr",  # Sort by 24hr volume
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        markets = response.json()
        
        print("=== Top 20 Active Markets by Volume ===\n")
        
        for i, market in enumerate(markets[:20], 1):
            question = market.get('question', 'N/A')
            volume = market.get('volume', 0)
            volume_24hr = market.get('volume24hr', 0)
            liquidity = market.get('liquidity', 0)
            end_date = market.get('endDate', 'N/A')
            
            # Get outcome prices
            outcomes = market.get('outcomePrices', [])
            
            print(f"{i}. {question}")
            print(f"   Volume: ${float(volume):,.0f} (24h: ${float(volume_24hr):,.0f})")
            print(f"   Liquidity: ${float(liquidity):,.0f}")
            
            if outcomes:
                print(f"   Prices: {', '.join([f'{float(p):.3f}' for p in outcomes])}")
            
            if end_date != 'N/A':
                try:
                    dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    print(f"   End: {dt.strftime('%Y-%m-%d')}")
                except:
                    print(f"   End: {end_date}")
            
            print()
        
        # Save to file for later analysis
        with open('/root/openclaw_data/lin/data/markets_snapshot.json', 'w') as f:
            json.dump(markets[:20], f, indent=2)
        
        print("✅ Data saved to data/markets_snapshot.json")
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    fetch_markets()
