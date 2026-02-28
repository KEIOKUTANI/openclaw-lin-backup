#!/usr/bin/env python3
"""
Create comprehensive market comparison table
"""

# Based on research data
markets = [
    {
        "name": "Trump Deportation: 500K-750K Range (2025)",
        "category": "Politics",
        "polymarket_price": 0.0325,
        "external_probability": 0.90,
        "reasoning": "DHS reported 675K deportations as of Jan 20, 2026. Market severely underpricing. Additional 2.5M total departures (605K deported + 1.9M self-deported) supports this range.",
        "end_date": "2026-03-31",
        "ev_calculation": (0.90 * (1/0.0325 - 1) - 0.10),
        "confidence": "High"
    },
    {
        "name": "2026 Winter Olympics: Norway Most Gold Medals",
        "category": "Sports",
        "polymarket_price": 0.99,
        "external_probability": 0.95,
        "reasoning": "Supercomputer predicts 18 gold medals for Norway, historical dominance. Currently leading at halfway point with 20 medals. However, market price at 99% leaves minimal EV.",
        "end_date": "2026-02-22",
        "ev_calculation": (0.95 * (1/0.99 - 1) - 0.05),
        "confidence": "Medium-High"
    },
    {
        "name": "2026 Winter Olympics: Ice Hockey Gold - Canada",
        "category": "Sports",
        "polymarket_price": None,  # Need to find actual price
        "external_probability": 0.65,
        "reasoning": "Stacked roster with McDavid, Crosby, MacKinnon. Historically strong. However, competition from USA, Russia, Sweden. Estimated 60-70% chance.",
        "end_date": "2026-02-23",
        "ev_calculation": None,
        "confidence": "Medium"
    },
    {
        "name": "Super Bowl LX: Seahawks Win",
        "category": "Sports",
        "polymarket_price": None,  # Need to find actual price  
        "external_probability": 0.54,
        "reasoning": "Seahawks favored at -230 (implied 69.7%). However, this is close to game time, efficient market. Limited edge expected.",
        "end_date": "2026-02-08",
        "ev_calculation": None,
        "confidence": "Low"
    },
    {
        "name": "S&P 500 Daily Direction (Next Trading Day)",
        "category": "Finance",
        "polymarket_price": 0.50,
        "external_probability": 0.52,
        "reasoning": "Analyst consensus bullish for 2026 (+9% YoY). However, daily direction is near coin-flip. Minimal edge, high transaction costs.",
        "end_date": "2026-02-19",
        "ev_calculation": (0.52 * (1/0.50 - 1) - 0.48),
        "confidence": "Very Low"
    }
]

print("=" * 120)
print("POLYMARKET MARKET ANALYSIS - EXPECTED VALUE COMPARISON")
print("=" * 120)
print()

for i, m in enumerate(markets, 1):
    print(f"{i}. {m['name']}")
    print(f"   Category: {m['category']}")
    print(f"   Polymarket Price: ${m['polymarket_price']:.4f}" if m['polymarket_price'] else "   Polymarket Price: [Need to verify]")
    print(f"   Implied Probability: {m['polymarket_price']*100:.1f}%" if m['polymarket_price'] else "   Implied Probability: [TBD]")
    print(f"   True Probability (Estimated): {m['external_probability']*100:.1f}%")
    
    if m['ev_calculation'] is not None:
        ev = m['ev_calculation']
        print(f"   Expected Value: ${ev:.4f} per $1.00 bet ({ev*100:.2f}% ROI)")
        
        # Calculate payouts for $1 bet
        win_payout = 1.00 / m['polymarket_price']
        expected_profit = ev * 1.00
        print(f"   If Win: ${win_payout:.2f} | Expected Profit: ${expected_profit:.2f}")
    else:
        print(f"   Expected Value: [Need price data]")
    
    print(f"   Resolution Date: {m['end_date']}")
    print(f"   Confidence Level: {m['confidence']}")
    print(f"   \n   Reasoning: {m['reasoning']}")
    print()
    print("-" * 120)
    print()

# Summary recommendations
print("\n" + "=" * 120)
print("RECOMMENDATIONS (Conservative Strategy)")
print("=" * 120)
print()
print("1. HIGHEST EV: Trump Deportation 500K-750K")
print("   - Expected Value: +$26.69 per $1.00 (2,669% ROI)")
print("   - Risk: Medium (data interpretation, policy changes)")
print("   - Recommendation: ✅ STRONG BUY at $1.00 test")
print()
print("2. MODERATE EV: Canada Ice Hockey Gold")
print("   - Need to verify Polymarket price")
print("   - If priced below 60%, potential value")
print("   - Recommendation: ⏳ RESEARCH MORE")
print()
print("3. LOW EV: Norway Gold Medal Count")
print("   - Market efficiently priced at 99%")
print("   - Minimal upside despite high confidence")
print("   - Recommendation: ❌ PASS (insufficient edge)")
print()
print("4. LOW EV: S&P 500 Daily")
print("   - Near coin-flip with transaction costs")
print("   - Recommendation: ❌ PASS")
print()
print("5. UNKNOWN: Super Bowl")
print("   - Market likely efficient close to game")
print("   - Recommendation: ❌ PASS (event already resolved)")
print()

print("\n" + "=" * 120)
print("NEXT STEPS")
print("=" * 120)
print("1. Verify current Polymarket prices for all markets")
print("2. Implement Quarter-Kelly / Half-Kelly bet sizing")
print("3. Execute $1.00 test trade on Trump Deportation market")
print("4. Monitor market for price changes")
print()
