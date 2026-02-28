#!/usr/bin/env python3
"""
Risk Management System
バンクロール管理・ポジションサイズ計算
"""
import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class RiskManager:
    """リスク管理システム"""
    
    def __init__(self, bankroll: float = None, risk_multiplier: int = 50):
        """
        Args:
            bankroll: 総資金（USD）
            risk_multiplier: リスク倍率（50 = 2%、60 = 1.67%）
        """
        self.bankroll = bankroll or float(os.getenv('BANKROLL_USD', 1850))
        self.risk_multiplier = risk_multiplier
        self.max_position_size = self.bankroll / self.risk_multiplier
        
        # トレード履歴
        self.trades = []
        self.current_positions = {}
        
    def calculate_position_size(self, 
                               entry_price: float,
                               stop_loss_price: float,
                               risk_percent: Optional[float] = None) -> Dict:
        """
        ポジションサイズ計算
        
        Args:
            entry_price: エントリー価格
            stop_loss_price: ストップロス価格
            risk_percent: リスク率（Noneの場合はdefault使用）
        
        Returns:
            Dict with position_size_usd, position_size_tokens, risk_usd
        """
        if risk_percent is None:
            risk_usd = self.max_position_size
        else:
            risk_usd = self.bankroll * (risk_percent / 100)
        
        # Stop loss幅
        price_risk = abs(entry_price - stop_loss_price)
        price_risk_percent = (price_risk / entry_price) * 100
        
        # ポジションサイズ（USD）
        position_size_usd = min(risk_usd / (price_risk_percent / 100), self.max_position_size)
        
        # トークン数
        position_size_tokens = position_size_usd / entry_price
        
        return {
            'position_size_usd': round(position_size_usd, 2),
            'position_size_tokens': round(position_size_tokens, 6),
            'risk_usd': round(risk_usd, 2),
            'stop_loss_distance': round(price_risk_percent, 2),
            'max_loss_usd': round(position_size_usd * (price_risk_percent / 100), 2),
        }
    
    def can_open_position(self, position_size_usd: float) -> bool:
        """新規ポジション可否判定"""
        total_exposure = sum(pos['size_usd'] for pos in self.current_positions.values())
        
        # 最大エクスポージャー：バンクロールの60%
        max_exposure = self.bankroll * 0.6
        
        if total_exposure + position_size_usd > max_exposure:
            return False
        
        return True
    
    def record_trade(self, trade_data: Dict):
        """取引記録"""
        self.trades.append(trade_data)
        
        # 損益計算
        if trade_data.get('exit_price'):
            pnl = self._calculate_pnl(trade_data)
            self.bankroll += pnl
            
            print(f"📊 Trade recorded: {trade_data['symbol']}")
            print(f"   Entry: ${trade_data['entry_price']:.2f}")
            print(f"   Exit: ${trade_data['exit_price']:.2f}")
            print(f"   PnL: ${pnl:.2f} ({(pnl/trade_data['size_usd'])*100:.2f}%)")
            print(f"   New bankroll: ${self.bankroll:.2f}")
    
    def _calculate_pnl(self, trade_data: Dict) -> float:
        """損益計算"""
        entry = trade_data['entry_price']
        exit_price = trade_data['exit_price']
        size = trade_data['size_tokens']
        side = trade_data['side']
        
        if side == 'buy':
            pnl = (exit_price - entry) * size
        else:  # sell/short
            pnl = (entry - exit_price) * size
        
        return pnl
    
    def get_performance_stats(self) -> Dict:
        """パフォーマンス統計"""
        if not self.trades:
            return {'total_trades': 0}
        
        wins = [t for t in self.trades if self._calculate_pnl(t) > 0]
        losses = [t for t in self.trades if self._calculate_pnl(t) <= 0]
        
        total_pnl = sum(self._calculate_pnl(t) for t in self.trades)
        win_rate = (len(wins) / len(self.trades)) * 100 if self.trades else 0
        
        return {
            'total_trades': len(self.trades),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': round(win_rate, 2),
            'total_pnl': round(total_pnl, 2),
            'current_bankroll': round(self.bankroll, 2),
            'roi': round((total_pnl / 1850) * 100, 2),
        }
    
    def print_status(self):
        """現在の状態を表示"""
        print("\n" + "="*60)
        print("💰 Risk Management Status")
        print("="*60)
        print(f"Bankroll: ${self.bankroll:,.2f}")
        print(f"Risk Multiplier: {self.risk_multiplier}x")
        print(f"Max Position Size: ${self.max_position_size:.2f} ({100/self.risk_multiplier:.2f}%)")
        print(f"Open Positions: {len(self.current_positions)}")
        
        if self.current_positions:
            total_exposure = sum(pos['size_usd'] for pos in self.current_positions.values())
            print(f"Total Exposure: ${total_exposure:.2f} ({(total_exposure/self.bankroll)*100:.1f}%)")
        
        stats = self.get_performance_stats()
        if stats['total_trades'] > 0:
            print(f"\n📊 Performance:")
            print(f"   Total Trades: {stats['total_trades']}")
            print(f"   Win Rate: {stats['win_rate']}%")
            print(f"   Total PnL: ${stats['total_pnl']:+.2f}")
            print(f"   ROI: {stats['roi']:+.2f}%")
        
        print("="*60 + "\n")


def test_risk_manager():
    """リスクマネージャーのテスト"""
    rm = RiskManager(bankroll=1850, risk_multiplier=50)
    
    rm.print_status()
    
    print("📐 Position Size Calculation Example:")
    print("\nScenario: BTC entry at $95,000, stop loss at $93,000")
    
    position = rm.calculate_position_size(
        entry_price=95000,
        stop_loss_price=93000
    )
    
    print(f"\n   Position Size: ${position['position_size_usd']} USD")
    print(f"   Tokens: {position['position_size_tokens']} BTC")
    print(f"   Stop Loss Distance: {position['stop_loss_distance']}%")
    print(f"   Max Loss: ${position['max_loss_usd']}")
    print(f"\n   Can open? {rm.can_open_position(position['position_size_usd'])}")


if __name__ == '__main__':
    test_risk_manager()
