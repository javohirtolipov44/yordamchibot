from aiogram import Dispatcher
from .start import router as start_router
from .service import router as service_router
from .anti_spam import router as anti_spam_router

def register_handlers(dp: Dispatcher):
    # Tartib muhim: avval buyruqlar va servis xabarlari, so'ng anti-spam
    dp.include_router(start_router)
    dp.include_router(service_router)
    dp.include_router(anti_spam_router)

