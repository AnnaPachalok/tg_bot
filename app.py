from aiogram import Bot, Dispatcher, types
import asyncio
from handlers.private_handlers import private_router
from handlers.group_handlers import group_router

TOKEN = "8153469126:AAF0zQyTaOiYqfCntnD1rclCv6_YUiovocs"


bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(private_router)
dp.include_router(group_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await print("Bot is running...")

if __name__ == "__main__":
    asyncio.run(main())