#!/usr/bin/env python3
"""
Hyperliquid Connector
Hyperliquid DEX統合（優先プラットフォーム）
"""
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

try:
    from hyperliquid.info import Info
    from hyperliquid.exchange import Exchange
    from eth_account import Account
    HYPERLIQUID_AVAILABLE = True
except ImportError:
    HYPERLIQUID_AVAILABLE = False
    print("⚠️  hyperliquid-python-sdk not installed")
    print("   Run: pip install hyperliquid-python-sdk eth-account")

load_dotenv()


class HyperliquidConnector:
    """Hyperliquid DEX接続クラス"""
    
    def __init__(self):
        """初期化"""
        if not HYPERLIQUID_AVAILABLE:
            raise ImportError("hyperliquid-python-sdk not installed")
        
        self.info = Info()  # 公開API（価格取得等）
        
        # 秘密鍵取得（取引実行用）
        private_key = os.getenv('HYPERLIQUID_PRIVATE_KEY') or os.getenv('POLYGON_WALLET_PRIVATE_KEY')
        
        if private_key:
            self.account = Account.from_key(private_key)
            self.exchange = Exchange(self.account)
            print(f"✅ Hyperliquid connected: {self.account.address}")
        else:
            self.account = None
            self.exchange = None
            print("⚠️  Private key not found - Read-only mode")
    
    def get_balance(self) -> Dict:
        """残高取得"""
        if not self.account:
            return {'error': 'No account connected'}
        
        try:
            # アカウント情報取得
            user_state = self.info.user_state(self.account.address)
            
            balances = {}
            if 'balances' in user_state:
                for balance in user_state['balances']:
                    coin = balance['coin']
                    total = float(balance['total'])
                    balances[coin] = total
            
            return {
                'address': self.account.address,
                'balances': balances,
            }
        except Exception as e:
            print(f"❌ Balance fetch failed: {e}")
            return {'error': str(e)}
    
    def get_ticker(self, symbol: str) -> Dict:
        """
        現在価格取得
        
        Args:
            symbol: コイン名（例: BTC, ETH, SOL）
        """
        try:
            # 全市場の中間価格取得
            all_mids = self.info.all_mids()
            
            if symbol not in all_mids:
                return {'error': f'Symbol {symbol} not found'}
            
            price = float(all_mids[symbol])
            
            # メタ情報取得
            meta = self.info.meta()
            
            universe = meta.get('universe', [])
            coin_info = next((c for c in universe if c['name'] == symbol), None)
            
            return {
                'symbol': symbol,
                'last': price,
                'mid': price,
                'info': coin_info,
            }
        except Exception as e:
            print(f"❌ Ticker fetch failed: {e}")
            return {'error': str(e)}
    
    def get_orderbook(self, symbol: str) -> Dict:
        """
        板情報取得
        
        Args:
            symbol: コイン名
        """
        try:
            l2_book = self.info.l2_snapshot(symbol)
            
            return {
                'bids': l2_book['levels'][0][:5] if l2_book['levels'] else [],
                'asks': l2_book['levels'][1][:5] if len(l2_book['levels']) > 1 else [],
                'timestamp': l2_book.get('time'),
            }
        except Exception as e:
            print(f"❌ Orderbook fetch failed: {e}")
            return {'error': str(e)}
    
    def get_candles(self, symbol: str, interval: str = '1h', lookback: int = 100) -> List:
        """
        ヒストリカルデータ取得
        
        Args:
            symbol: コイン名
            interval: 時間足（1m, 15m, 1h, 1d）
            lookback: 取得数
        """
        try:
            candles = self.info.candles_snapshot(symbol, interval, lookback)
            
            # OHLCV形式に変換
            ohlcv = []
            for candle in candles:
                ohlcv.append([
                    candle['t'],  # timestamp
                    float(candle['o']),  # open
                    float(candle['h']),  # high
                    float(candle['l']),  # low
                    float(candle['c']),  # close
                    float(candle.get('v', 0)),  # volume
                ])
            
            return ohlcv
        except Exception as e:
            print(f"❌ Candles fetch failed: {e}")
            return []
    
    def place_market_order(self, symbol: str, is_buy: bool, size: float) -> Dict:
        """
        成行注文
        
        Args:
            symbol: コイン名
            is_buy: True=買い、False=売り
            size: 数量
        """
        if not self.exchange:
            return {'error': 'No exchange connected - need private key'}
        
        try:
            result = self.exchange.market_order(symbol, is_buy, size)
            print(f"✅ Market order executed: {result}")
            return result
        except Exception as e:
            print(f"❌ Order failed: {e}")
            return {'error': str(e)}
    
    def place_limit_order(self, symbol: str, is_buy: bool, size: float, price: float) -> Dict:
        """
        指値注文
        
        Args:
            symbol: コイン名
            is_buy: True=買い、False=売り
            size: 数量
            price: 価格
        """
        if not self.exchange:
            return {'error': 'No exchange connected - need private key'}
        
        try:
            result = self.exchange.limit_order(symbol, is_buy, size, price)
            print(f"✅ Limit order placed: {result}")
            return result
        except Exception as e:
            print(f"❌ Order failed: {e}")
            return {'error': str(e)}


def test_connection():
    """接続テスト"""
    print("🔌 Testing Hyperliquid connection...\n")
    
    if not HYPERLIQUID_AVAILABLE:
        print("❌ SDK not installed. Run:")
        print("   pip install hyperliquid-python-sdk eth-account")
        return
    
    connector = HyperliquidConnector()
    
    print("\n📊 BTC Ticker:")
    ticker = connector.get_ticker('BTC')
    if 'error' not in ticker:
        print(f"   Price: ${ticker['last']:,.2f}")
    else:
        print(f"   Error: {ticker['error']}")
    
    print("\n💰 Account Balance:")
    balance = connector.get_balance()
    if 'error' not in balance:
        print(f"   Address: {balance.get('address', 'N/A')}")
        if balance.get('balances'):
            for coin, amount in balance['balances'].items():
                print(f"   {coin}: {amount}")
        else:
            print("   No balances or read-only mode")
    else:
        print(f"   Error: {balance['error']}")
    
    print("\n✅ Connection test complete!")


if __name__ == '__main__':
    test_connection()
