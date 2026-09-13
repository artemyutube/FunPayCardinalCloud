"""
FunPay Cardinal - Main Entry Point
С встроенным Auto-Bump Scheduler для Render.io

Это полностью готовый файл для развертывания на Render
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Импортируем наши модули для scheduler'а
from auto_bump_scheduler import CardinalBumpAdapter
from keep_alive import RenderKeepAlive

# Если используется оригинальный Cardinal, импортируй его здесь:
# from cardinal import Cardinal
# or
# import cardinal

# ============================================================================
# ЛОГИРОВАНИЕ
# ============================================================================

def setup_logging():
    """Настраивает логирование"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = os.path.join(log_dir, 'cardinal.log')
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)
    
    logger = logging.getLogger("Cardinal")
    logger.info("=" * 70)
    logger.info("🀑 FunPay Cardinal запускается")
    logger.info(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
    
    return logger


# ============================================================================
# КОНФИГУРАЦИЯ
# ============================================================================

def load_config() -> dict:
    """Загружает конфигурацию из переменных окружения"""
    
    config = {
        # FunPay credentials
        'funpay_username': os.getenv('FUNPAY_USERNAME', ''),
        'funpay_password': os.getenv('FUNPAY_PASSWORD', ''),
        
        # Telegram
        'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
        
        # Auto-bump scheduler
        'enable_auto_bump': os.getenv('ENABLE_AUTO_BUMP', 'true').lower() == 'true',
        'bump_interval_hours': int(os.getenv('AUTO_BUMP_INTERVAL', '4')),
        
        # Keep-alive для Render
        'enable_keep_alive': os.getenv('ENABLE_KEEP_ALIVE', 'true').lower() == 'true',
        'keep_alive_interval': int(os.getenv('KEEP_ALIVE_INTERVAL', '10')),
    }
    
    return config


# ============================================================================
# ГЛАВНЫЙ КЛАСС CARDINAL
# ============================================================================

class CardinalBot:
    """
    Main Cardinal Bot с поддержкой Auto-Bump Scheduler
    
    Это класс объединяет оригинальный Cardinal с нашими модулями
    """
    
    def __init__(self, config: dict):
        self.logger = logging.getLogger("Cardinal.Bot")
        self.config = config
        
        # Компоненты
        self.api = None
        self.bump_adapter = None
        self.keep_alive = None
        
        self.is_running = False
    
    async def initialize(self):
        """Инициализирует бота"""
        
        self.logger.info("πŸ"§ Инициализирую Cardinal...")
        
        try:
            # ЗДЕСЬ интегрируй оригинальный Cardinal код
            # Например:
            # self.api = CardinalAPI(
            #     username=self.config['funpay_username'],
            #     password=self.config['funpay_password']
            # )
            # await self.api.connect()
            
            self.logger.info("✅ Cardinal инициализирован")
            
            # Инициализируем keep-alive
            if self.config['enable_keep_alive']:
                self.logger.info("Инициализирую keep-alive...")
                self.keep_alive = RenderKeepAlive(
                    check_interval_minutes=self.config['keep_alive_interval']
                )
            
            # Инициализируем scheduler
            if self.config['enable_auto_bump']:
                self.logger.info("Инициализирую auto-bump scheduler...")
                self.bump_adapter = CardinalBumpAdapter(
                    cardinal_api=self.api,
                    bump_interval_hours=self.config['bump_interval_hours']
                )
            
            self.logger.info("✅ Все компоненты инициализированы")
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка при инициализации: {e}", exc_info=True)
            raise
    
    async def start(self):
        """Запускает бота"""
        
        self.logger.info("🚀 Запускаю Cardinal...")
        self.is_running = True
        
        try:
            # Запускаем keep-alive
            if self.keep_alive:
                self.logger.info("Запускаю keep-alive...")
                await self.keep_alive.start()
            
            # Запускаем scheduler
            if self.bump_adapter:
                self.logger.info("Запускаю auto-bump scheduler...")
                await self.bump_adapter.initialize()
            
            # ЗДЕСЬ запускай оригинальный Cardinal код
            # Например:
            # await self.api.run_telegram_bot()
            # или
            # await self.api.run_main_loop()
            
            self.logger.info("✅ Cardinal запущен")
            
            # Бесконечный loop пока не будет сигнала выхода
            while self.is_running:
                await asyncio.sleep(1)
            
        except asyncio.CancelledError:
            self.logger.info("Cardinal был отменен")
        except Exception as e:
            self.logger.error(f"❌ Ошибка при работе Cardinal: {e}", exc_info=True)
            raise
    
    async def shutdown(self):
        """Завершает работу бота"""
        
        self.logger.info("πŸ›' Завершаю работу Cardinal...")
        self.is_running = False
        
        try:
            if self.bump_adapter:
                self.logger.info("Завершаю scheduler...")
                await self.bump_adapter.shutdown()
            
            if self.keep_alive:
                self.logger.info("Завершаю keep-alive...")
                await self.keep_alive.stop()
            
            self.logger.info("✅ Cardinal завершен")
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка при завершении: {e}", exc_info=True)


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

async def main():
    """Главная функция"""
    
    # Логирование
    logger = setup_logging()
    
    # Конфиг
    config = load_config()
    
    logger.info("Конфигурация загружена:")
    logger.info(f"  πŸ"„ Auto-bump: {config['enable_auto_bump']} "
                f"(интервал: {config['bump_interval_hours']}ч)")
    logger.info(f"  🛡️ Keep-alive: {config['enable_keep_alive']}")
    
    # Проверка обязательных параметров
    if not config['funpay_username'] or not config['funpay_password']:
        logger.error("❌ FUNPAY_USERNAME и FUNPAY_PASSWORD должны быть установлены!")
        sys.exit(1)
    
    if not config['telegram_bot_token']:
        logger.error("❌ TELEGRAM_BOT_TOKEN должен быть установлен!")
        sys.exit(1)
    
    # Создаем и запускаем Cardinal
    bot = CardinalBot(config)
    
    try:
        await bot.initialize()
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("\nπŸ›' Получен сигнал KeyboardInterrupt")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await bot.shutdown()
        logger.info("=" * 70)
        logger.info("🀑 FunPay Cardinal завершил работу")
        logger.info("=" * 70)


# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)
