import logging

import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.default.main_keyboard import make_menu

from loader import dp, db, _


@dp.message_handler(Text(contains="🚖"), state="*")
async def get_order_confirmation(message: Message, state: FSMContext):
    is_empty = await db.basket_is_empty(message.from_user.id)

    if is_empty == 0:
        await message.answer(_("Your basket is empty"))
        return
    order_txt, pay_link = await get_order_text(message)

    payme_button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Pay with PayMe 🚀"), url=pay_link)
        ]
    ])
    await message.answer(_("Thanks for your purchase here is details:"), reply_markup=make_menu())
    await db.clear_basket(message.from_user.id)
    await message.answer(order_txt, reply_markup=payme_button)
    await state.finish()


async def get_order_text(message: Message = None, paid: bool = False):
    order_data = await db.insert_orders(message.from_user.id)
    logging.info(order_data)
    order_txt = _("<b> Order number № {0} ☑️\n</b>").format(order_data[0]['order_id'])
    total = 0
    for i, record in enumerate(order_data, start=1):
        order_txt += f"{i}. " + f"{record['menu_type']}" + _(" menu № ") + str(record['menu_id'])
        if record['event'] == 'lunch':
            order_txt += _(" for lunch \n")
            total += record['price'] * record['quantity']
            order_txt += f"{record['price']:,} * {record['quantity']:,} = {(record['price'] * record['quantity']):,}\n "
        else:
            order_txt += _(" for dinner \n")
            total += record['price'] * record['quantity']
            order_txt += f"{record['price']:,} * {record['quantity']:,} = {(record['price'] * record['quantity']):,}\n "

    order_txt += _(" Total: {0:,} \n").format(total)

    if paid:
        order_txt += _("💸Is paid: YES")
    else:
        order_txt += _("💸Is paid: NO")

    order_txt += "\n\n"

    order_txt += _("🛂Customer:") + order_data[0]['full_name']
    order_txt += _("\nPhone:") + " <code> " + order_data[0]['phone'] + "</code>\n"

    order_txt += f"<a href='https://www.google.com/maps/search/?api=1&query={order_data[0]['address_lat']},{order_data[0]['address_lon']}'>"  #
    order_txt += _("📍Address</a>\n")
    if order_data[0]['comment']:
        order_txt += _("Comment:") + order_data[0]['comment'] + "\n"

    order_txt += _("For extra information: +99890 000 00 00")
    pay_link = ""
    if paid is False:
        pay_link = requests.get(
            f"http://letsfood.bobir.tech/payme/merchant?order_id={order_data[0]['order_id']}&amount={total}&user_id={message.from_user.id}")

        logging.info(pay_link.json())
        pay_link = pay_link.json().get('url')

        logging.info(f"url : {pay_link}")

    return order_txt, pay_link
