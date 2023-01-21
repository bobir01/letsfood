import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.callback_data import CallbackData
from loader import _

basket_call = CallbackData("basket", "user_id", "action", "id")
food_call = CallbackData("food", "type", "user_id")


def make_food_call(type='', user_id=''):
    return food_call.new(type=type, user_id=user_id)


def basket_callback(action='', id='', user_id=''):
    return basket_call.new(user_id=user_id, action=action, id=id)


async def make_basket(record):
    markup = InlineKeyboardMarkup(row_width=5)

    buttons = []
    for x in range(len(record)):
        for i in range(len(record[x])):

            if len(buttons) == 3:
                buttons.clear()
            else:
                if i == 0:
                    buttons.append(
                        InlineKeyboardButton(text=" {} ❌".format(x+1), callback_data=basket_callback(
                            id=f"{record[x][0]}")))
                if i == 1:
                    buttons.append(InlineKeyboardButton(text="➕",
                                                        callback_data=basket_callback(id=f"{record[x][0]}",
                                                                                      action="+")))
                if i == 2:  # len(buttons)==2:
                    buttons.append(InlineKeyboardButton(text=f"{record[x][5]}", callback_data="quantity"))
                if i == 3:
                    buttons.append(InlineKeyboardButton(text=f"➖",
                                                        callback_data=basket_callback(id=f"{record[x][0]}",
                                                                                      action="-")))

                if len(buttons) == 2:
                    continue
                if not (i == 1 and len(buttons) == 1):
                    markup.add(*buttons)
                if i == 0:
                    buttons.clear()
    return markup


def make_food_markup(user_id, full=True, par=False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    if full:
        markup.insert(
            InlineKeyboardButton(text=_("Full ✅"), callback_data=make_food_call(type='full', user_id=user_id)))
        markup.insert(
            InlineKeyboardButton(text=_("Partial"), callback_data=make_food_call(type='par', user_id=user_id)))
        return markup
    markup.insert(InlineKeyboardButton(text=_("Full"), callback_data=make_food_call(type='full', user_id=user_id)))
    markup.insert(InlineKeyboardButton(text=_("Partial ✅"), callback_data=make_food_call(type='par', user_id=user_id)))
    return markup
