"""
Keep-alive механизм для Render.io
Предотвращает автоматическое выключение приложения через 15 минут неактивности
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import Optional

logger = logging.getLogger("KeepAlive")


class RenderKeepAlive:
    """
    Keep-alive механизм для Render.io
    
    Render выключает бесплатные приложения через 15 минут неактивности.
    Этот класс генерирует логи/активность, чтобы приложение не выключалось.
    """
    
    def __init__(self, check_interval_minutes: int = 10):
        """
        Args:
            check_interval_minutes: интервал между проверками в минутах (по умолчанию 10)
        """
        self.check_interval = check_interval_minutes * 60  # в секундах
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self.ping_count = 0
    
    async def start(self):
        """Запускает keep-alive loop"""
        self.is_running = True
        self._task = asyncio.create_task(self._keep_alive_loop())
        logger.info(
            f"πŸ" Keep-alive запущен (проверка каждые {self.check_interval / 60:.0f} минут)"
        )
    
    async def stop(self):
        """Останавливает keep-alive loop"""
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"πŸ›' Keep-alive остановлен (всего пингов: {self.ping_count})")
    
    async def _keep_alive_loop(self):
        """
        Основной цикл keep-alive
        Периодически логирует информацию о состоянии приложения
        """
        try:
            while self.is_running:
                await asyncio.sleep(self.check_interval)
                await self._send_ping()
                
        except asyncio.CancelledError:
            logger.debug("Keep-alive loop был отменен")
            raise
        except Exception as e:
            logger.error(f"❌ Ошибка в keep-alive loop: {e}", exc_info=True)
            # Пытаемся восстановиться
            if self.is_running:
                logger.info("Перезапускаю keep-alive через 60 секунд...")
                await asyncio.sleep(60)
                await self._keep_alive_loop()
    
    async def _send_ping(self):
        """
        Отправляет ping (генерирует активность логирования)
        """
        self.ping_count += 1
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Логируем активность (это генерирует системную активность на Render)
        logger.info(f"πŸ"„ Keep-alive ping #{self.ping_count} в {current_time}")
        
        # Вывод в stdout тоже помогает Render видеть активность
        print(f"[{current_time}] Keep-alive #{self.ping_count} - приложение активно", 
              file=sys.stdout, flush=True)


class RenderKeepAliveWithHealthCheck(RenderKeepAlive):
    """
    Расширенная версия keep-alive с проверками здоровья приложения
    """
    
    def __init__(self, 
                 check_interval_minutes: int = 10,
                 health_check_callback=None):
        """
        Args:
            check_interval_minutes: интервал между проверками в минутах
            health_check_callback: async функция для проверки здоровья (опционально)
        """
        super().__init__(check_interval_minutes)
        self.health_check_callback = health_check_callback
        self.health_check_fails = 0
    
    async def _send_ping(self):
        """
        Отправляет ping и проверяет здоровье приложения
        """
        await super()._send_ping()
        
        # Выполняем проверку здоровья если она определена
        if self.health_check_callback:
            try:
                result = await self.health_check_callback()
                if result:
                    logger.debug("βœ… Проверка здоровья пройдена")
                    self.health_check_fails = 0
                else:
                    logger.warning("⚠️ Проверка здоровья провалена")
                    self.health_check_fails += 1
                    
                    if self.health_check_fails >= 3:
                        logger.error(
                            "❌ Приложение нездорово! 3 неудачные проверки подряд"
                        )
            except Exception as e:
                logger.error(f"❌ Ошибка при проверке здоровья: {e}")
                self.health_check_fails += 1


# ============================================================================
# Вспомогательные функции
# ============================================================================

async def create_keep_alive_for_render(
    render_mode: bool = True,
    check_interval_minutes: int = 10
) -> Optional[RenderKeepAlive]:
    """
    Создает и возвращает keep-alive если приложение работает на Render
    
    Args:
        render_mode: включена ли поддержка Render (по умолчанию True)
        check_interval_minutes: интервал проверок в минутах
    
    Returns:
        RenderKeepAlive экземпляр или None
    """
    if not render_mode:
        logger.debug("Keep-alive отключен")
        return None
    
    keep_alive = RenderKeepAlive(check_interval_minutes=check_interval_minutes)
    await keep_alive.start()
    return keep_alive


async def shutdown_keep_alive(keep_alive: Optional[RenderKeepAlive]):
    """
    Корректно завершает работу keep-alive
    
    Args:
        keep_alive: RenderKeepAlive экземпляр для завершения
    """
    if keep_alive:
        await keep_alive.stop()


# ============================================================================
# Пример использования
# ============================================================================

if __name__ == "__main__":
    """
    Тестовое запускание keep-alive
    """
    
    # Настройка логирования
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    async def test_health_check() -> bool:
        """Простая проверка здоровья для теста"""
        return True
    
    async def main():
        """Тестовая main функция"""
        
        # Создаем keep-alive с проверкой здоровья
        keep_alive = RenderKeepAliveWithHealthCheck(
            check_interval_minutes=1,  # Каждую минуту для теста
            health_check_callback=test_health_check
        )
        
        await keep_alive.start()
        
        try:
            print("Keep-alive запущен. Нажмите Ctrl+C чтобы остановить...")
            # Слушаем 5 минут
            await asyncio.sleep(300)
        except KeyboardInterrupt:
            print("\nПолучен сигнал на остановку")
        finally:
            await keep_alive.stop()
            print("Done!")
    
    asyncio.run(main())
