"""
AETP Configuration Module
Centralized configuration management with environment variable support
"""
import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TradingConfig:
    """Configuration for trading parameters"""
    # Genetic Algorithm
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.15
    crossover_rate: float = 0.8
    elitism_count: int = 2
    
    # Trading Parameters
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.02  # 2% risk per trade
    commission_rate: float = 0.001  # 0.1% commission
    max_position_size: float = 0.1  # 10% of capital
    
    # Timeframes
    data_timeframe: str = "1h"  # 1-hour candles
    lookback_period: int = 100  # 100 periods for indicators
    
    # Stop Loss/Take Profit
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.04  # 4% take profit

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "aetp-trading")
    collection_strategies: str = "evolved_strategies"
    collection_market_data: str = "market_data_stream"
    collection_performance: str = "strategy_performance"
    
    # Real-time update intervals (seconds)
    update_interval: int = 60
    
    def validate(self) -> bool:
        """Validate Firebase configuration"""
        required_vars = ["FIREBASE_PROJECT_ID", "GOOGLE_APPLICATION_CREDENTIALS"]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            logging.warning(f"Missing Firebase environment variables: {missing}")
            return False
        return True

@dataclass
class ExchangeConfig:
    """Exchange API configuration"""
    exchange_id: str = "binance"
    api_key: Optional[str] = os.getenv("EXCHANGE_API_KEY")
    api_secret: Optional[str] = os.getenv("EXCHANGE_API_SECRET")
    
    # Rate limiting
    requests_per_second: int = 10
    retry_attempts: int = 3
    retry_delay: int = 5
    
    # Symbols to trade
    symbols: list = field(default_factory=lambda: [
        "BTC/USDT",
        "ETH/USDT",
        "BNB/USDT"
    ])
    
    def validate(self) -> bool:
        """Validate exchange credentials"""
        if not self.api_key or not self.api_secret:
            logging.error("Exchange API credentials not configured")
            return False
        return True

class ConfigManager:
    """Centralized configuration manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize configuration from environment"""
        self.trading = TradingConfig()
        self.firebase = FirebaseConfig()
        self.exchange = ExchangeConfig()
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        # Logging configuration
        log_level = logging.DEBUG if self.environment == "development" else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def validate_all(self) -> Dict[str, bool]:
        """Validate all configuration sections"""
        return {
            "trading": True,
            "firebase": self.firebase.validate(),
            "exchange": self.exchange.validate()
        }
    
    def get_config_summary(self) -> str:
        """Get configuration summary for logging"""
        return f"""
        AETP Configuration Summary:
        Environment: {self.environment}
        Trading Parameters:
          - Population Size: {self.trading.population_size}
          - Initial Capital: ${self.trading.initial_capital}
          - Risk per Trade: {self.trading.risk_per_trade*100}%
        
        Exchange: {self.exchange.exchange_id}
        Symbols: {', '.join(self.exchange.symbols[:3])}
        """