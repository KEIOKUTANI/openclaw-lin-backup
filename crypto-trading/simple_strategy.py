#!/usr/bin/env python3
"""
Simple Trading Strategy - RSI Based
シンプルなRSI戦略（テスト用）
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from exchange_connector import ExchangeConnector
from risk_manager import RiskManager


class RSIStrategy:
    """RSI戦略（買われすぎ・売られすぎ）"""
    
    def __init__(self, 
                 exchange: ExchangeConnector,
                 risk_manager: RiskManager,
                 rsi_period: int = 14,
                 rsi_oversold: float = 30,
                 rsi_overbought: float = 70):
        """
        Args:
            exchange: 取引所接続
            risk_manager: リスク管理
            rsi_period: RSI期間
            rsi_oversold: 売られすぎライン
            rsi_overbought: 買われすぎライン
        """
        self.exchange = exchange
        self.risk_manager = risk_manager
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
    
    def calculate_rsi(self, prices: List[float]) -> float:
        """
        RSI計算
        
        Args:
            prices: 終値リスト
        
        Returns:
            RSI値（0-100）
        """
        if len(prices) < self.rsi_period + 1:
            return 50.0  # デフォルト
        
        deltas = np.diff(prices)
        gain = np.where(deltas > 0, deltas, 0)
        loss = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gain[-self.rsi_period:])
        avg_loss = np.mean(loss[-self.rsi_period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def analyze(self, symbol: str, timeframe: str = '1h') -> Dict:
        """
        市場分析
        
        Args:
            symbol: 通貨ペア（例: BTC/USDT）
            timeframe: 時間足
        
        Returns:
            分析結果
        """
        # OHLCV取得
        ohlcv = self.exchange.get_ohlcv(symbol, timeframe, limit=100)
        
        if not ohlcv:
            return {'signal': 'WAIT', 'reason': 'データ取得失敗'}
        
        # 終値抽出
        closes = [candle[4] for candle in ohlcv]
        current_price = closes[-1]
        
        # RSI計算
        rsi = self.calculate_rsi(closes)
        
        # シグナル判定
        signal = 'WAIT'
        reason = f'RSI: {rsi:.1f}'
        
        if rsi < self.rsi_oversold:
            signal = 'BUY'
            reason = f'RSI oversold: {rsi:.1f} < {self.rsi_oversold}'
        elif rsi > self.rsi_overbought:
            signal = 'SELL'
            reason = f'RSI overbought: {rsi:.1f} > {self.rsi_overbought}'
        
        # ストップロス設定（2%）
        if signal == 'BUY':
            stop_loss = current_price * 0.98
            take_profit = current_price * 1.04  # 2:1 risk/reward
        elif signal == 'SELL':
            stop_loss = current_price * 1.02
            take_profit = current_price * 0.96
        else:
            stop_loss = None
            take_profit = None
        
        return {
            'signal': signal,
            'reason': reason,
            'rsi': round(rsi, 2),
            'current_price': current_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'symbol': symbol,
        }
    
    def execute_signal(self, analysis: Dict, dry_run: bool = True) -> Optional[Dict]:
        """
        シグナル実行
        
        Args:
            analysis: analyze()の結果
            dry_run: Trueの場合はシミュレーション
        
        Returns:
            注文結果
        """
        signal = analysis['signal']
        
        if signal == 'WAIT':
            print(f"⏸️  No action: {analysis['reason']}")
            return None
        
        # ポジションサイズ計算
        position = self.risk_manager.calculate_position_size(
            entry_price=analysis['current_price'],
            stop_loss_price=analysis['stop_loss']
        )
        
        # 実行可否チェック
        if not self.risk_manager.can_open_position(position['position_size_usd']):
            print("❌ Cannot open position: Max exposure reached")
            return None
        
        print(f"\n{'🔍 [DRY RUN]' if dry_run else '🚀 [LIVE]'} {signal} Signal")
        print(f"   Symbol: {analysis['symbol']}")
        print(f"   Price: ${analysis['current_price']:,.2f}")
        print(f"   RSI: {analysis['rsi']}")
        print(f"   Position Size: ${position['position_size_usd']} ({position['position_size_tokens']:.6f})")
        print(f"   Stop Loss: ${analysis['stop_loss']:,.2f}")
        print(f"   Take Profit: ${analysis['take_profit']:,.2f}")
        print(f"   Max Loss: ${position['max_loss_usd']}")
        
        if dry_run:
            print("   ✅ Dry run - No actual order placed")
            return {
                'dry_run': True,
                'signal': signal,
                'analysis': analysis,
                'position': position,
            }
        
        # 実注文（リアルマネー）
        side = 'buy' if signal == 'BUY' else 'sell'
        order = self.exchange.place_market_order(
            symbol=analysis['symbol'],
            side=side,
            amount=position['position_size_tokens']
        )
        
        if order:
            print("   ✅ Order executed!")
            
            # 記録
            self.risk_manager.record_trade({
                'symbol': analysis['symbol'],
                'side': side,
                'entry_price': analysis['current_price'],
                'size_usd': position['position_size_usd'],
                'size_tokens': position['position_size_tokens'],
                'stop_loss': analysis['stop_loss'],
                'take_profit': analysis['take_profit'],
            })
        
        return order


def test_strategy():
    """戦略テスト（Dry Run）"""
    print("🧪 Testing RSI Strategy (Dry Run)\n")
    
    exchange = ExchangeConnector('bybit')
    risk_manager = RiskManager(bankroll=1850, risk_multiplier=50)
    strategy = RSIStrategy(exchange, risk_manager)
    
    # 複数通貨ペアで分析
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    for symbol in symbols:
        print(f"\n{'='*60}")
        print(f"Analyzing: {symbol}")
        print('='*60)
        
        analysis = strategy.analyze(symbol, timeframe='1h')
        
        if analysis:
            print(f"Signal: {analysis['signal']}")
            print(f"Reason: {analysis['reason']}")
            print(f"Current Price: ${analysis['current_price']:,.2f}")
            
            if analysis['signal'] != 'WAIT':
                strategy.execute_signal(analysis, dry_run=True)
        else:
            print("❌ Analysis failed")
    
    print("\n" + "="*60)
    risk_manager.print_status()


if __name__ == '__main__':
    test_strategy()
