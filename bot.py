import os
import sys
import django
import asyncio
import logging
from datetime import datetime

# Налаштування Django середовища
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'building.settings')
django.setup()

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from restoran.models import Service, Category, Review

TOKEN = "9171871903:AAFwMf2YgpgZYo5us-p-36SMgO_Zm3J7mD0"
ADMIN_TELEGRAM_ID = 1988776608  # Твій підтверджений ID

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_TELEGRAM_ID


# --- КЛАВІАТУРИ ---
def user_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛠 Каталог послуг"), KeyboardButton(text="💰 Калькулятор / Ціни")],
            [KeyboardButton(text="⭐ Відгуки"), KeyboardButton(text="📞 Контакти")],
            [KeyboardButton(text="✍️ Залишити заявку")]
        ],
        resize_keyboard=True
    )


def admin_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Керування послугами"), KeyboardButton(text="📊 Статистика сайту")],
            [KeyboardButton(text="⚙️ Змінити код файлу"), KeyboardButton(text="⬅️ Меню користувача")]
        ],
        resize_keyboard=True
    )


# --- КОРИСТУВАЦЬКА ЧАСТИНА ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("Вітаю, Шефе! 👑 Ви в панелі супер-адміна.", reply_markup=admin_main_menu())
    else:
        await message.answer("Вітаємо у будівельній компанії **«МартинБуд»**! Чим можемо допомогти?",
                             reply_markup=user_main_menu(), parse_mode="Markdown")


@dp.message(F.text == "⬅️ Меню користувача")
async def back_to_user(message: types.Message):
    if not is_admin(message.from_user.id): return
    await message.answer("Перемикаю у звичайний режим:", reply_markup=user_main_menu())


@dp.message(F.text == "🛠 Каталог послуг")
async def show_services(message: types.Message):
    services = Service.objects.all()[:15]
    if not services:
        await message.answer("Послуги наразі оновлюються.")
        return
    text = "🛠 **Популярні послуги компанії «МартинБуд»:**\n\n"
    for s in services:
        text += f"• **{s.title}** — `ціна: {s.price}`\n"
    await message.answer(text, parse_mode="Markdown")


@dp.message(F.text == "💰 Калькулятор / Ціни")
async def show_calc(message: types.Message):
    await message.answer(
        "💰 Орієнтовна вартість робіт:\n- Капітальний ремонт: від 4500 грн/м²\n- Ремонт під ключ: від 6500 грн/м²\n\nСкористайтеся повним калькулятором на сайті!")


@dp.message(F.text == "⭐ Відгуки")
async def show_reviews(message: types.Message):
    reviews = Review.objects.all()[:5]
    text = "⭐ **Останні відгуки клієнтів:**\n\n"
    for r in reviews:
        text += f"▪️ **{r.name}** ({r.rating}★): {r.text}\n\n"
    await message.answer(text, parse_mode="Markdown")


@dp.message(F.text == "📞 Контакти")
async def show_contacts(message: types.Message):
    await message.answer(
        "📞 **ТзОВ «МартинБуд»**\nКерівник: Мартин Іван Васильович\nТел: +380 97 043 09 60\nРегіон: Львів та область")


# --- СТАН ДЛЯ ЗАЯВОК ВІД КОРИСТУВАЧІВ ---
class ClientOrder(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_comment = State()


@dp.message(F.text == "✍️ Залишити заявку")
async def start_order(message: types.Message, state: FSMContext):
    await message.answer("Введіть ваше ім'я:")
    await state.set_state(ClientOrder.waiting_for_name)


@dp.message(ClientOrder.waiting_for_name)
async def get_client_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть ваш номер телефону (наприклад, +380...):")
    await state.set_state(ClientOrder.waiting_for_phone)


@dp.message(ClientOrder.waiting_for_phone)
async def get_client_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Опишіть коротко завдання чи об'єкт:")
    await state.set_state(ClientOrder.waiting_for_comment)


@dp.message(ClientOrder.waiting_for_comment)
async def get_client_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    phone = data['phone']
    comment = message.text

    admin_msg = (
        f"🚨 **УВАГА! Нова заявка з сайту/бота!** 🚨\n\n"
        f"👤 Ім'я: `{name}`\n"
        f"📞 Телефон: `{phone}`\n"
        f"💬 Коментар: `{comment}`"
    )
    try:
        await bot.send_message(ADMIN_TELEGRAM_ID, admin_msg, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Не вдалося надіслати адміну: {e}")

    await message.answer("✅ Вашу заявку успішно надіслано! Наш менеджер зв'яжеться з вами найближчим часом.",
                         reply_markup=user_main_menu())
    await state.clear()


# --- АДМІН-ПАНЕЛЬ ТА ЗМІНА КОДУ ---
class CodeUpdateState(StatesGroup):
    waiting_for_filename = State()
    waiting_for_code = State()


@dp.message(F.text == "⚙️ Змінити код файлу")
async def admin_change_code(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await message.answer(
        "Введіть шлях до файлу, який треба змінити (наприклад: `restoran/views.py` або `restoran/models.py`):")
    await state.set_state(CodeUpdateState.waiting_for_filename)


@dp.message(CodeUpdateState.waiting_for_filename)
async def get_filename(message: types.Message, state: FSMContext):
    await state.update_data(filename=message.text.strip())
    await message.answer("Надішліть новий код або текст, який буде записано у цей файл:")
    await state.set_state(CodeUpdateState.waiting_for_code)


@dp.message(CodeUpdateState.waiting_for_code)
async def save_new_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    filename = data['filename']
    new_code = message.text

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_code)
        await message.answer(f"✅ Файл `{filename}` успішно оновлено через бота!", reply_markup=admin_main_menu())
    except Exception as e:
        await message.answer(f"❌ Помилка запису у файл: {e}", reply_markup=admin_main_menu())

    await state.clear()


@dp.message(F.text == "📊 Статистика сайту")
async def admin_stats(message: types.Message):
    if not is_admin(message.from_user.id): return
    s_count = Service.objects.count()
    r_count = Review.objects.count()
    await message.answer(
        f"📊 Статистика «МартинБуд»:\n- Послуг у базі: {s_count}\n- Відгуків: {r_count}\n- Статус сайту: Працює 🟢",
        parse_mode="Markdown")


# --- ФОНОВІ ЗАДАЧІ (Звіти) ---
async def background_scheduler():
    while True:
        now = datetime.now()
        if now.hour == 21 and now.minute == 0:
            s_count = Service.objects.count()
            r_count = Review.objects.count()
            report = f"📈 **Щоденний звіт «МартинБуд»** ({now.strftime('%d.%m.%Y')}):\n- Послуг: {s_count}\n- Відгуків: {r_count}\n- Сайт працює стабільно 🟢"
            try:
                await bot.send_message(ADMIN_TELEGRAM_ID, report, parse_mode="Markdown")
            except:
                pass
            await asyncio.sleep(65)
        await asyncio.sleep(30)


async def main():
    asyncio.create_task(background_scheduler())
    print("Бот успішно запущено і готовий до роботи!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())