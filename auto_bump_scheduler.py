"""
Модуль автоматического поднятия лотов для FunPay Cardinal
Поднимает все активные лоты каждые 4 часа
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from abc import ABC, abstractmethod

logger = logging.getLogger("AutoBumpScheduler")


class BumpScheduler:
    """
    Scheduler для автоматического поднятия лотов
    """
    
    def __init__(self, bump_interval_hours: int = 4):
        """
        Args:
            bump_interval_hours: интервал между поднятиями лотов в часах (по умолчанию 4)
        """
        self.bump_interval = timedelta(hours=bump_interval_hours)
        self.last_bump_time: Optional[datetime] = None
        self.is_running = False
        self.is_bumping = False
        self._bump_task: Optional[asyncio.Task] = None
        self.bump_callback = None
        
    async def start(self, bump_callback):
        """
        Запускает scheduler
        
        Args:
            bump_callback: async функция, которая поднимает лоты.
                          Должна быть способна обработать ошибки
        """
        self.bump_callback = bump_callback
        self.is_running = True
        logger.info(f"Scheduler запущен. Интервал: {self.bump_interval.total_seconds() / 3600} часов")
        
        self._bump_task = asyncio.create_task(self._scheduler_loop())
        
    async def stop(self):
        """Останавливает scheduler"""
        self.is_running = False
        if self._bump_task:
            self._bump_task.cancel()
            try:
                await self._bump_task
            except asyncio.CancelledError:
                pass
        logger.info("Scheduler остановлен")
    
    async def _scheduler_loop(self):
        """Основной цикл scheduler'а"""
        try:
            # Первый бамп через минуту после запуска
            await asyncio.sleep(60)
            await self._perform_bump()
            
            while self.is_running:
                # Вычисляем, сколько нужно подождать до следующего бампа
                if self.last_bump_time:
                    next_bump_time = self.last_bump_time + self.bump_interval
                    now = datetime.now()
                    wait_seconds = (next_bump_time - now).total_seconds()
                    
                    if wait_seconds > 0:
                        logger.info(
                            f"Следующий бамп будет в {next_bump_time.strftime('%Y-%m-%d %H:%M:%S')} "
                            f"({wait_seconds / 3600:.1f} часов)"
                        )
                        await asyncio.sleep(wait_seconds)
                
                await self._perform_bump()
                
        except asyncio.CancelledError:
            logger.debug("Scheduler loop был отменен")
            raise
        except Exception as e:
            logger.error(f"Ошибка в scheduler loop: {e}", exc_info=True)
            # Возобновляем работу после ошибки
            if self.is_running:
                await asyncio.sleep(300)  # Ждем 5 минут и пробуем снова
                await self._scheduler_loop()
    
    async def _perform_bump(self):
        """Выполняет поднятие лотов"""
        if self.is_bumping:
            logger.warning("Бамп уже выполняется, пропускаем этот цикл")
            return
        
        self.is_bumping = True
        try:
            logger.info("Начинаем поднятие лотов...")
            self.last_bump_time = datetime.now()
            
            if self.bump_callback:
                await self.bump_callback()
            
            logger.info(f"Лоты подняты успешно в {self.last_bump_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logger.error(f"Ошибка при поднятии лотов: {e}", exc_info=True)
        finally:
            self.is_bumping = False
    
    async def manual_bump(self):
        """
        Ручное поднятие лотов (не сбрасывает таймер).
        Полезно для команд из Telegram
        """
        if self.is_bumping:
            logger.warning("Бамп уже выполняется")
            return False
        
        await self._perform_bump()
        return True
    
    def get_status(self) -> dict:
        """Возвращает статус scheduler'а"""
        return {
            "is_running": self.is_running,
            "is_bumping": self.is_bumping,
            "last_bump_time": self.last_bump_time.isoformat() if self.last_bump_time else None,
            "next_bump_time": (
                (self.last_bump_time + self.bump_interval).isoformat()
                if self.last_bump_time else None
            ),
            "bump_interval_hours": self.bump_interval.total_seconds() / 3600
        }


class CardinalBumpAdapter:
    """
    Адаптер для интеграции с FunPay Cardinal
    Преобразует операции Cardinal в вызовы scheduler'а
    """
    
    def __init__(self, cardinal_api, bump_interval_hours: int = 4):
        """
        Args:
            cardinal_api: API объект Cardinal'а
            bump_interval_hours: интервал поднятия лотов в часах
        """
        self.api = cardinal_api
        self.scheduler = BumpScheduler(bump_interval_hours)
    
    async def initialize(self):
        """Инициализирует scheduler и запускает его"""
        await self.scheduler.start(self._bump_all_lots)
    
    async def shutdown(self):
        """Останавливает scheduler"""
        await self.scheduler.stop()
    
    async def _bump_all_lots(self):
        """
        Поднимает все активные лоты через API Cardinal'а
        
        Эта функция должна быть адаптирована под ваш конкретный API
        """
        try:
            # Пример для типичного API структурированного как Cardinal
            # Адаптируйте под вашу реальную реализацию API
            
            if hasattr(self.api, 'raise_all_lots'):
                await self.api.raise_all_lots()
            elif hasattr(self.api, 'bump_all'):
                await self.api.bump_all()
            else:
                # Альтернативный способ - перебираем все лоты и поднимаем их
                await self._raise_lots_manually()
                
        except Exception as e:
            logger.error(f"Ошибка при поднятии лотов через API: {e}", exc_info=True)
            raise
    
    async def _raise_lots_manually(self):
        """
        Ручное поднятие лотов, если API не имеет встроенного метода
        Адаптируйте этот код под вашу реальную структуру
        """
        try:
            # Получаем все лоты
            if hasattr(self.api, 'get_lots'):
                lots = await self.api.get_lots()
            elif hasattr(self.api, 'get_active_lots'):
                lots = await self.api.get_active_lots()
            else:
                logger.warning("Не удалось получить список лотов")
                return
            
            if not lots:
                logger.info("Нет активных лотов для поднятия")
                return
            
            # Поднимаем каждый лот
            raised_count = 0
            for lot in lots:
                try:
                    if hasattr(lot, 'raise'):
                        await lot.raise()
                    elif hasattr(lot, 'bump'):
                        await lot.bump()
                    else:
                        logger.warning(f"Лот {lot} не имеет метода raise/bump")
                        continue
                    
                    raised_count += 1
                    # Небольшая задержка между поднятиями для избежания rate limiting
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Ошибка при поднятии лота: {e}")
                    continue
            
            logger.info(f"Поднято {raised_count} лотов из {len(lots)}")
            
        except Exception as e:
            logger.error(f"Ошибка при ручном поднятии лотов: {e}", exc_info=True)
            raise
    
    def get_status(self) -> dict:
        """Возвращает статус scheduler'а"""
        return self.scheduler.get_status()
