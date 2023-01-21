import asyncio
from datetime import datetime
import logging
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentTypes
from aiogram.types import Message, CallbackQuery

import data.config
from data.config import ADMINS
from keyboards.default import basket_keyboard
from keyboards.default.contact_keyboard import contact_markup
from keyboards.default.lanch import make_event_keyboard
from keyboards.default.main_keyboard import make_menu, address_markup
from keyboards.default.menu_keybord import make_numbers
from keyboards.default.menu_type_markup import make_menu_type_keyboard
from keyboards.inline.lang_inline_keyboard import lang_inline, lang_call
from loader import dp, db, _, bot
from .confrim_order import get_order_text

# MENU_ID = datetime.day %15
MENU_ID = 1


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: Message, state: FSMContext):

    stat = await state.get_state()
    if stat:
        await state.finish()
        await message.answer(_("Here is our menu"), reply_markup=make_menu())
        return
    try:
        await db.add_user(full_name=message.from_user.full_name,
                          telegram_id=message.from_user.id,
                          username=message.from_user.username)
        await message.answer("""Здравствуйте! Добро пожаловать в наш бот! 
Давайте для начала выберем язык обслуживания!
        
Assalomu aleykum! Botimizga xush kelibsiz! 
Keling, avvaliga xizmat ko’rsatish tilini tanlab olaylik. 
        
Hello! Welcome to our Bot! 
Let's choose the language of service first""", reply_markup=lang_inline)
        await bot.send_message(ADMINS[0],
                               f"{message.from_user.full_name} {message.from_user.id} @{message.from_user.username} joined "
                               f"in db {await db.count_users()} users")
    except Exception as e:
        await message.answer(_("Here is our menu"), reply_markup=make_menu())


async def main_manu(message: Message, lang=None):
    if lang:
        await message.answer(_("Here is our offers", locale=lang), reply_markup=make_menu(lang))
        return
    await message.answer(_("Here is our menu offers"), reply_markup=make_menu())


@dp.message_handler(state='enter_phone_initial', content_types=ContentTypes.CONTACT | ContentTypes.TEXT)
async def enter_phone(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number

    else:
        if re.match(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', message.text):
            phone = message.text
        else:
            await message.answer(_("Please enter a valid phone number!"))
            return
    await db.update_phone(phone, message.from_user.id)
    await get_pre_geolocation(message, state)
    return


@dp.callback_query_handler(lang_call.filter(), state="*", chat_type="private")
async def lang_inline_callback(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    await db.update_lang(call.from_user.id, lang)
    await call.message.edit_text(_("Language changed to 🇺🇸", lang))
    await asyncio.sleep(1)
    await call.message.delete()
    await call.message.answer(_("Here is our offers", locale=lang), reply_markup=make_menu(lang))


@dp.message_handler(Text(equals=["Order 🛍", "Заказать 🛍", "Buyurtma berish 🛍"]), state="*")
async def get_pre_geolocation(message: Message, state: FSMContext):
    if datetime.now().time() > datetime.strptime('11:00:00', '%H:%M:%S').time():
        await message.answer(_("Sorry our service is not available after 11:00 !"))
        return


    if await db.select_phone(message.from_user.id):

        data = await state.get_data()
        if data.get('address'):
            await get_event(message, state)
            return

        await message.answer(_("Where do you want to get your order?📍"), reply_markup=address_markup())
        await state.set_state("get_address")
        return
    await message.answer(_("Looks like you didn't provide your phone number, please enter it here: "),
                         reply_markup=contact_markup())
    await state.set_state("enter_phone_initial")


@dp.message_handler(content_types=ContentTypes.LOCATION, state="get_address")
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.location)
    await message.answer(_("Confirm address✅\nIf this is incorrect resend it📍"),
                         reply_markup=address_markup(confrim=True))
    await state.set_state("confirm_address")


@dp.message_handler(content_types=ContentTypes.TEXT | ContentTypes.LOCATION, state="confirm_address")
async def confirm_address(message: Message, state: FSMContext):
    if message.content_type == ContentTypes.LOCATION:
        await state.update_data(address=message.location)
        await message.answer(_("Confirm address✅\nIf this is incorrect resend it📍"),
                             reply_markup=address_markup(confrim=True))
        await state.set_state("confirm_address")
        return
    if message.text == _("Confirm address✅"):
        await get_event(message, state)
        return
    if message.text == _("Comment to address (optional)"):
        await message.answer(_("Send your comment"))
        await state.set_state("comment")
        return
    await message.answer(_("Where do you want to get your order? 📍"), reply_markup=address_markup())


async def get_event(message: Message, state: FSMContext):
    await message.answer(_("Select time of meal"), reply_markup=make_event_keyboard())
    await state.set_state("order")


@dp.message_handler(content_types=ContentTypes.TEXT, state="comment")
async def comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.answer(_("Comment added"))

    await message.answer(_("Select time of meal"), reply_markup=make_event_keyboard())
    await state.set_state("order")


@dp.message_handler(Text(contains="🍽"), state='order')
async def get_dinner_(message: Message, state: FSMContext):
    await message.answer(_("For Dinner 🍽"), reply_markup=make_menu_type_keyboard())
    await state.set_state("get_dinner")


@dp.message_handler(Text(contains="🍲"), state='order')
async def get_launch_markup(message: Message, state: FSMContext):
    await message.answer(_("For Lunch🍲"), reply_markup=make_menu_type_keyboard())
    await state.set_state("get_lunch")


@dp.message_handler(state='get_lunch')
async def get_launch(message: Message, state: FSMContext):
    if message.text in ["Partial set", "Полсет"]:  ##TODO be carefull with translations here
        menu = MENU_ID
        await state.update_data(event="lunch")
        today_menu = await db.get_menu_with_id_lunch(menu, message.from_user.id)
        menu_text = today_menu["text_par"] + _("\n{} sum").format(today_menu['price_par'])
        await message.answer_photo(photo=today_menu["photo"],
                                   caption=menu_text)

        await message.answer(_("Choose the number of portions or type it"))
        await state.update_data(price=today_menu['price_par'])
        await state.update_data(type='par')
        await state.set_state("order_lunch_par")  # stat of order with full set
    else:
        menu = MENU_ID
        today_menu = await db.get_menu_with_id_dinner(menu, message.from_user.id)
        await state.update_data(event="lunch")
        menu_text = today_menu["text_full"] + _("\n{} sum").format(today_menu['price_full'])
        await message.answer_photo(photo=today_menu["photo"],
                                   caption=menu_text)

        await message.answer(_("Choose the number of portions or type it"))
        await state.update_data(price=today_menu['price_full'])
        await state.update_data(type='full')
        await state.set_state("order_lunch_full")  # state of order with par set


@dp.message_handler(state='get_dinner')
async def get_dinner_order(message: Message, state: FSMContext):
    # today = datetime.today().day
    # menu = today % 15
    # if menu == 0:
    #     menu += 15
    if message.text in ["Ceт", "Full set"]:
        menu = MENU_ID
        logging.info(await state.get_state())
        await state.update_data(event="dinner")
        today_menu = await db.get_menu_with_id_dinner(menu, message.from_user.id)
        menu_text = today_menu["text_full"] + _("\n{} sum").format(today_menu['price_full'])
        await message.answer_photo(photo=today_menu["photo"],
                                   caption=menu_text
                                   )

        await message.answer(_("Choose the number of portions or type it"))
        await state.update_data(price=today_menu['price_full'])
        await state.update_data(type='full')
        await state.set_state("order_dinner_full")  # stat of order with full set

    else:
        menu = MENU_ID
        logging.info(await state.get_state())
        today_menu = await db.get_menu_with_id_dinner(menu, message.from_user.id)
        menu_text = today_menu["text_par"] + _("\n{} sum").format(today_menu['price_par'])
        await message.answer_photo(photo=today_menu["photo"],
                                   caption=menu_text
                                   )
        logging.info(await state.get_state())
        await message.answer(_("Choose the number of portions or type it"))
        await state.update_data(price=today_menu['price_par'])
        await state.update_data(type='par')
        await state.set_state("order_dinner_par")  # state of order with par set


@dp.message_handler(regexp=r'[1-9]|10', state="order_lunch_par")
async def pre_order_quantity_partial(message: Message, state: FSMContext):
    if int(message.text) < 5:
        await message.answer(_("You can only order at least 5 portions !"))
        return
    await message.answer(_("Added to basket 🛒"))
    await state.update_data(quantity=int(message.text))
    logging.info(await state.get_state())
    await message.answer(_("What else do you want to order?"), reply_markup=basket_keyboard.getbacket())
    data = await state.get_data()
    logging.info(data)
    await db.add_basket(message.from_user.id, MENU_ID, data.get('type'), data.get('address').latitude,
                        data.get('address').longitude,
                        int(message.text),
                        data.get('price'),
                        data.get('comment'),
                        data.get('event'))

    logging.info(await state.get_state())


@dp.message_handler(regexp=r'[1-9]|10', state="order_lunch_full")
async def pre_order_quantity_partial(message: Message, state: FSMContext):
    if int(message.text) < 5:
        await message.answer(_("You can only order at least 5 portions !"))
        return
    await message.answer(_("Added to basket 🛒"))
    await state.update_data(quantity=int(message.text))
    logging.info(await state.get_state())
    await message.answer(_("What else do you want to order?"), reply_markup=basket_keyboard.getbacket())
    data = await state.get_data()
    await db.add_basket(message.from_user.id, MENU_ID, data.get('type'), data.get('address').latitude,
                        data.get('address').longitude,
                        int(message.text),
                        data.get('price'),
                        data.get('comment'),
                        data.get('event'))


@dp.message_handler(regexp=r'[1-9]|10', state="order_dinner_par")
async def pre_order_quantity_partial(message: Message, state: FSMContext):
    if int(message.text) < 5:
        await message.answer(_("You can only order at least 5 portions !"))
        return
    await message.answer(_("Added to basket 🛒"))
    await state.update_data(quantity=int(message.text))
    logging.info(await state.get_state())
    await message.answer(_("What else do you want to order?"), reply_markup=basket_keyboard.getbacket())
    data = await state.get_data()
    await db.add_basket(message.from_user.id, MENU_ID, data.get('type'), data.get('address').latitude,
                        data.get('address').longitude,
                        int(message.text),
                        data.get('price'),
                        data.get('comment'),
                        data.get('event'))


@dp.message_handler(regexp=r'[1-9]|10', state="order_dinner_full")
async def pre_order_quantity_full(message: Message, state: FSMContext):
    if int(message.text) < 5:
        await message.answer(_("You can only order at least 5 portions !"))
        return
    await message.answer(_("Added to basket 🛒"))
    await state.update_data(quantity=int(message.text))

    await message.answer(_("What else do you want to order?"), reply_markup=basket_keyboard.getbacket())
    data = await state.get_data()
    await db.add_basket(message.from_user.id, MENU_ID, data.get('type'), data.get('address').latitude,
                        data.get('address').longitude,
                        int(message.text),
                        data.get('price'),
                        data.get('comment'),
                        data.get('event'))
