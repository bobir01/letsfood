import asyncio
import logging
from . import main_handler
from aiogram.types import Message, CallbackQuery, ForceReply, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.dispatcher import FSMContext
from aiogram.dispatcher import FSMContext
from keyboards.default.confirm_markup import get_confrim_markup
from keyboards.inline.food_inline_keyboard import make_food_markup, make_basket, basket_call
from loader import dp, db, _, bot


@dp.message_handler(Text(contains="🛒"), state='*')
async def call_basket(message: Message, state: FSMContext):
    user_basket = await db.get_basket_user(message.from_user.id)
    lang = await db.get_lang(message.from_user.id)
    txt = _("<b>Here is your basket</b>:\n")
    await message.answer(text=txt, reply_markup=get_confrim_markup())
    txt = ""
    total = 0
    for j, item in enumerate(user_basket, start=1):
        txt += f"{j}. "
        if item['menu_type'] == 'full':
            i = f'{item["event"]} :   {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['full_text'] + "\n"
        else:
            i = f'{item["event"]} :  {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['par_text'] + "\n"

    txt += _("\n<b>Total: </b>{0:,}").format(total)

    await message.answer(text=txt, reply_markup=await make_basket(user_basket))


async def delete_item_from_basket(callback: CallbackQuery, item_id, **kwargs):
    await db.delete_basket_item(item_id)
    await asyncio.sleep(0.5)
    user_basket = await db.get_basket_user(callback.from_user.id)
    lang = await db.get_lang(callback.from_user.id)
    txt = _("<b>Here is your basket</b>:\n")
    total = 0
    for j, item in enumerate(user_basket, start=1):
        txt += f"{j}. "
        if item['menu_type'] == 'full':
            i = f'{item["event"]} :  {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['full_text'] + "\n"
        else:
            i = f'{item["event"]} :  {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['par_text'] + "\n"

    txt += _("\n<b>Total: </b>{0:,}").format(total)

    await callback.message.edit_text(text=txt, reply_markup=await make_basket(user_basket))


async def plus_basket_item(callback: CallbackQuery, item_id, plus, **kwargs):
    await db.increase_quantity(item_id)
    await asyncio.sleep(0.2)
    total = 0
    user_basket = await db.get_basket_user(callback.from_user.id)
    lang = await db.get_lang(callback.from_user.id)
    txt = _("<b>Here is your basket</b>:\n")
    total = 0
    for j, item in enumerate(user_basket, start=1):
        txt += f"{j}. "
        if item['menu_type'] == 'full':
            i = f'{item["event"]} :  {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['full_text'] + "\n"
        else:
            i = f'{item["event"]} :  {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['par_text'] + "\n"

    txt += _("\n<b>Total: </b>{0:,}").format(total)

    await callback.message.edit_text(text=txt, reply_markup=await make_basket(user_basket))


async def minus_basket_item(callback: CallbackQuery, item_id, minus, **kwargs):
    await db.decrease_quantity(item_id)  # comes with "-" action and requests to db update quantity-=1
    await asyncio.sleep(0.2)
    total = 0
    user_basket = await db.get_basket_user(callback.from_user.id)

    lang = await db.get_lang(callback.from_user.id)
    txt = _("<b>Here is your basket</b>:\n")
    total = 0
    for j, item in enumerate(user_basket, start=1):
        if item['quantity'] == 0:
            await db.delete_basket_item(item_id)
            continue

        txt += f"{j}. "
        if item['menu_type'] == 'full':
            i = f'{item["event"]}  : {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['full_text'] + "\n"
        else:
            i = f'{item["event"]} :  {item["quantity"]} * {item["price"]:,} = '
            i += "{0:,}\n".format(item["quantity"] * item["price"])
            txt += i
            total += item["quantity"] * item["price"]
            txt += item['par_text'] + "\n"
    if total == 0:
        await callback.message.edit_text(_("Your basket is empty"))
        return
    txt += _("\n<b>Total: </b>{0:,}").format(total)

    await callback.message.edit_text(text=txt, reply_markup=await make_basket(user_basket))


@dp.callback_query_handler(basket_call.filter(), state="*")
async def manage_basket_callbacks(call: CallbackQuery, callback_data: dict):
    data = await db.get_basket_user(call.from_user.id)

    item_id = int(callback_data.get("id"))

    print(f"item_id : {item_id}")
    action = callback_data.get("action")
    plus_action = action
    print(f"plus : {plus_action}")

    minus_action = action
    print(f"minus : {minus_action}")
    logging.info(data)
    logging.info(call)

    my_function = None
    for item in data:
        if item['id'] == item_id and plus_action != "+" and minus_action != "-":
            my_function = delete_item_from_basket
        if item['id'] == item_id and plus_action == "+":
            my_function = plus_basket_item
        if item['id'] and minus_action == "-":
            my_function = minus_basket_item

    logging.info(callback_data)

    logging.info(my_function)

    await my_function(call, item_id=item_id, minus=minus_action, plus=plus_action)
