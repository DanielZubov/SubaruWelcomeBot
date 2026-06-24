import re
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- НАСТРОЙКИ ---
TOKEN = os.getenv("SUBARU_BOT_TOKEN")
# Видео будет лежать внутри контейнера в папке /app/media/
VIDEO_PATH = os.getenv("VIDEO_PATH", "/app/media/welcome_to_the_club.mp4")

# ID стикеров
APPROVE_STICKER = "CAACAgIAAxkBAAIfeGn4WJx1o0xO6f_9si-tYZdei2WHAAKsHwAChUAxSW8HXeM311e3OwQ"
GOODBYE_STICKER = "CAACAgIAAxkBAAIfNGnzP3PmOesVY0Ycu_sKBR8xge7GAALpGgACVc45SZhCKLcX0z3UOwQ"
RAP_STICKER = "CAACAgIAAxkBAAIfOGnzQbQUwDjfh9oxJLbUTUrLSaplAAI2AANGwaMOVzViA7uyUJ47BA"
ROCK_STICKER = "CAACAgIAAxkBAAIfPGnzQp92O_r1N1m3gtFvu-x6s7FEAALNAAMVKwACbZaMyfgfXPY7BA"
BORODA_STICKER = "CAACAgIAAxkBAAIgSWoEgor0_WPoj0VojxOjGCEBqcsMAAKDoAAC7NEpSOdudaC1LzbhOwQ"
TEMA_STICKER = "CAACAgIAAxkBAAIjAmo7gqxy3xGFx4uVRyzwfB_eexGCAAKhowACFq_hSaGqvB-1dME3PAQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def get_welcome_text(user_name):
    return (
        f"Привет, {user_name}! Добро пожаловать в наш Subaru-клуб! ✌️💨\n\n"
        f"📜 **ПРАВИЛА ГРУППЫ:**\n"
        f"1️⃣ **Никакой политики.** Ну его нахуй....\n"
        f"2️⃣ **Уважение.** Без оскорблений. Конфликты — строго в ЛС.\n"
        f"3️⃣ **Знакомство.** Представься чату: Имя, машина (фото), город.\n\n"
        f"Обливайся маслом и погнали! 🏎💨"
    )

# --- ХЕНДЛЕРЫ ---

# 1. ФИЛЬТР НА ВСТУПЛЕНИЕ (КАПЧА)
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def welcome_captcha(event: types.ChatMemberUpdated):
    user_id = event.from_user.id
    chat_id = event.chat.id
    user_name = event.from_user.first_name or "Субарист"

    try:
        await bot.restrict_chat_member(
            chat_id, user_id, 
            permissions=types.ChatPermissions(can_send_messages=False)
        )
        
        builder = InlineKeyboardBuilder()
        builder.button(text="Конечно субару!", callback_data=f"captcha_ok_{user_id}")
        builder.button(text="ХЗ, я гей", callback_data=f"captcha_fail_{user_id}")
        
        await bot.send_message(
            chat_id, 
            f"Добро пожаловать, {user_name}! Ответь на вопрос, чтобы войти:\n<b>Лучшая марка авто?</b>",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка в капче: {e}")

@dp.callback_query(F.data.startswith("captcha_"))
async def process_captcha(callback: types.CallbackQuery):
    action, status, target_id = callback.data.split("_")
    target_id = int(target_id)
    
    if callback.from_user.id != target_id:
        return await callback.answer("А тебя не спрашивали😒!", show_alert=True)

    if status == "ok":
        await bot.restrict_chat_member(
            callback.message.chat.id, target_id,
            permissions=types.ChatPermissions(
                can_send_messages=True, can_send_media_messages=True,
                can_send_other_messages=True, can_add_web_page_previews=True
            )
        )
        await callback.message.delete()
        
        welcome_text = get_welcome_text(callback.from_user.first_name)
        if os.path.exists(VIDEO_PATH):
            await bot.send_video(
                callback.message.chat.id, 
                video=types.FSInputFile(VIDEO_PATH), 
                caption=welcome_text, 
                parse_mode="Markdown"
            )
        else:
            await bot.send_message(callback.message.chat.id, welcome_text, parse_mode="Markdown")
    else:
        await callback.answer("Гей-детектив сработал! Прощай.", show_alert=True)
        await bot.ban_chat_member(callback.message.chat.id, target_id)
        await bot.unban_chat_member(callback.message.chat.id, target_id)
        await callback.message.delete()

# 2. ХЕНДЛЕР НА ВЫХОД
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def goodbye_member(event: types.ChatMemberUpdated):
    target_user = event.new_chat_member.user
    user_name = target_user.first_name or "Субарист"
    try:
        await bot.send_sticker(chat_id=event.chat.id, sticker=GOODBYE_STICKER)
        await bot.send_message(
            chat_id=event.chat.id, 
            text=f"{user_name} не вывез этого всего и съебал в закат от ваших гейских шуток... Ну и иди поплачь в рубашку своему парню, {user_name}! 😤"
        )
    except Exception as e:
        print(f"Ошибка в goodbye_handler: {e}")

# 3. ХЕНДЛЕР НА ГРЯЗЬ И ОДОБРЕНИЕ (ОЧКА, АНАЛ, ГЕЙ, СТИ и т.д.)
@dp.message(F.text.lower().regexp(r".*(очк[ао]|анал|гей|сти|sti|гачи|дядя богдан|жоп[аоыу]|ass|асс|член).*"))
async def approve_handler(message: types.Message):
    try:
        await message.answer_sticker(APPROVE_STICKER)
        match = re.search(r"(\S*(очк[ао]|анал|гей|сти|sti|гачи|дядя богдан|жоп[аоыу]|ass|асс|член)\S*)", message.text, re.IGNORECASE)
        whole_word = match.group(1).strip('.,!?;:"') if match else "одобряю"
        await message.answer(text=f"<blockquote>{whole_word}</blockquote>\n<b>Одобряю</b>", parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка в approve_handler: {e}")

# 4. ХЕНДЛЕР НА VPN / PROXY
@dp.message(F.text.lower().regexp(r".*(vpn|впн|квн|proxy|прокси|прокся).*"))
async def vpn_proxy_handler(message: types.Message):
    try:
        text = (
            "Вот список актуальных прокси для ТГ: https://t.me/c/1694988575/1/173784\n\n"
            "Так же можешь воспользоваться нашим партнерским ВПН @Leon_VPNbot 😎"
        )
        await message.reply(text, disable_web_page_preview=False)
    except Exception as e:
        print(f"Ошибка в vpn_proxy_handler: {e}")

# 5. ХЕНДЛЕР НА "РУССКИЙ РЭП"
@dp.message(F.text.lower().contains("русский рэп"))
async def anti_rap_handler(message: types.Message):
    try:
        await message.reply("🤢 Бляя... Пиздец, паешь гавна!")
        await message.answer_sticker(RAP_STICKER)
    except Exception as e:
        print(f"Ошибка в anti_rap_handler: {e}")

# 6. ХЕНДЛЕР НА "РОК" (Только отдельное слово)
@dp.message(F.text.lower().regexp(r".*\bрок\b.*"))
async def rock_handler(message: types.Message):
    try:
        await message.reply("😎🤘🏻 Ели мясо мужики, пивом запивали! Кто-то вякнул БэМэВэ - в жопу ноги запихали!")
        await message.answer_sticker(ROCK_STICKER)
    except Exception as e:
        print(f"Ошибка в rock_handler: {e}")

# 7. ХЕНДЛЕР НА "Борода" (Только отдельное слово)
# Используем поиск по всей строке, а не строгое соответствие началу
@dp.message(F.text.lower().regexp(r".*\bборода\b.*"))
async def boroda_handler(message: types.Message):
    try:
        await message.reply("Сюда иди!!!")
        await message.answer_sticker(BORODA_STICKER)
    except Exception as e:
        print(f"Ошибка в boroda_handler: {e}")

# 7. ХЕНДЛЕР НА "ТЁМА"
@dp.message(F.text.lower().regexp(r".*(тём[ауы]|тёмой).*"))
async def tema_handler(message: types.Message):
    try:
        await message.answer_sticker(TEMA_STICKER)
        match = re.search(r"(\S*(тём[ауы]|тёмой)", message.text, re.IGNORECASE)
        whole_word = match.group(1).strip('.,!?;:"') if match else "Чё нада?"
        await message.answer(text=f"<blockquote>{whole_word}</blockquote>\n<b>Чё нада?</b>", parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка в approve_handler: {e}")

async def main():
    print("Subaru Bot запущен и на бусте! 🚀")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
