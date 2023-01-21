import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from loader import dp
from . import main_handler


@dp.message_handler(Text(contains="⬅️"), state="*")
async def back_handler(message: Message, state: FSMContext):
    current_stat = await state.get_state()
    logging.info(current_stat)
    if current_stat == "order" or current_stat is None or current_stat == 'settings':
        await main_handler.main_manu(message)
        return

    elif current_stat == 'enter_name' or current_stat == 'enter_phone' or current_stat == "confirm_address":
        await main_handler.main_manu(message)
        return

    elif current_stat == "comment":
        await main_handler.confirm_address(message, state)
        return

    elif current_stat == "get_address":
        logging.info(f"current state : [{current_stat}]")
        await main_handler.main_manu(message)
        return

    elif current_stat == "order":
        await main_handler.main_manu(message)
        return

    elif current_stat == "get_lunch" or current_stat == "get_dinner":
        await main_handler.get_event(message, state)
        return

    elif current_stat == "order_lunch_par" or current_stat == 'order_lunch_full':
        await main_handler.get_launch_markup(message, state)
        return

    elif current_stat == 'order_dinner_full' or current_stat == 'order_dinner_par':
        await main_handler.get_dinner_(message, state)
        return

    await main_handler.main_manu(message)
