#!/usr/bin/env python3
"""
Crypto Exchange Connector
統合取引所APIラッパー（Bybit優先）
"""
import ccxt
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class ExchangeConnector:
    """統合取引所接続クラス"""
    
    def __init__(self, exchange_name: str = 'bybit'):
        """
        Args:
            exchange_name: 取引所名（bybit, binance, okx等）
        """
        self.exchange_name = exchange_name
        self.exchange = self._initialize_exchange()
        
    def _initialize_exchange(self):
        """取引所クライアント初期化"""
        api_key = os.getenv(f'{self.exchange_name.upper()}_API_KEY')
        api_secret = os.getenv(f'{self.exchange_name.upper()}_API_SECRET')
        
        if not api_key or not api_secret:
            print(f"⚠️  {self.exchange_name.upper()} API keys not found in .env")
            print(f"   Set: {self.exchange_name.upper()}_API_KEY and {self.exchange_name.upper()}_API_SECRET")
        
        exchange_class = getattr(ccxt, self.exchange_name)
        
        config = {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',  # spot or future
            }
        }
        
        return exchange_class(config)
    
    def get_balance(self) -> Dict:
        """残高取得"""
        try:
            balance = self.exchange.fetch_balance()
            return {
                'total': balance['total'],
                'free': balance['free'],
                'used': balance['used'],
            }
        except Exception as e:
            print(f"❌ Balance fetch failed: {e}")
            return {}
    
    def get_ticker(self, symbol: str) -> Dict:
        """
        現在価格取得
        
        Args:
            symbol: 通貨ペア（例: BTC/USDT）
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high': ticker['high'],
                'low': ticker['low'],
                'volume': ticker['quoteVolume'],
            }
        except Exception as e:
            print(f"❌ Ticker fetch failed for {symbol}: {e}")
            return {}
    
    def get_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """板情報取得"""
        try:
            orderbook = self.exchange.fetch_order_book(symbol, limit)
            return {
                'bids': orderbook['bids'][:5],  # Top 5 bids
                'asks': orderbook['asks'][:5],  # Top 5 asks
                'timestamp': orderbook['timestamp'],
            }
        except Exception as e:
            print(f"❌ Orderbook fetch failed: {e}")
            return {}
    
    def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List:
        """
        ヒストリカルデータ取得（OHLCV）
        
        Args:
            symbol: 通貨ペア
            timeframe: 時間足（1m, 5m, 15m, 1h, 4h, 1d）
            limit: 取得数
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            print(f"❌ OHLCV fetch failed: {e}")
            return []
    
    def place_market_order(self, symbol: str, side: str, amount: float) -> Dict:
        """
        成行注文
        
        Args:
            symbol: 通貨ペア
            side: buy or sell
            amount: 数量
        """
        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            return order
        except Exception as e:
            print(f"❌ Order failed: {e}")
            return {}
    
    def place_limit_order(self, symbol: str, side: str, amount: float, price: float) -> Dict:
        """
        指値注文
        
        Args:
            symbol: 通貨ペア
            side: buy or sell
            amount: 数量
            price: 価格
        """
        try:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            return order
        except Exception as e:
            print(f"❌ Order failed: {e}")
            return {}


def test_connection():
    """接続テスト"""
    print("🔌 Testing exchange connection...")
    
    connector = ExchangeConnector('bybit')
    
    print("\n💰 Balance:")
    balance = connector.get_balance()
    if balance:
        for currency, amount in balance['free'].items():
            if amount > 0:
                print(f"   {currency}: {amount}")
    
    print("\n📊 BTC/USDT Ticker:")
    ticker = connector.get_ticker('BTC/USDT')
    if ticker:
        print(f"   Last: ${ticker['last']:,.2f}")
        print(f"   24h High: ${ticker['high']:,.2f}")
        print(f"   24h Low: ${ticker['low']:,.2f}")
        print(f"   Volume: ${ticker['volume']:,.0f}")
    
    print("\n✅ Connection test complete!")


if __name__ == '__main__':
    test_connection()
