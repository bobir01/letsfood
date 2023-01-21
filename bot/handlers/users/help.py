from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from .info_getter import info_handler

from aiogram.types import ContentTypes
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
import re

from keyboards.default.contact_keyboard import contact_markup
from keyboards.default.settings_keyboard import *
from keyboards.inline.lang_inline_keyboard import lang_inline, lang_call
from loader import dp, db, _





@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await info_handler(message)




@dp.message_handler(Text(contains="⚙️"), state='*')  # , state="*")
async def edit_settings(message: Message, state: FSMContext, lang=None):
    if lang :
        await message.answer(_("Change settings", locale=lang), reply_markup=make_settings(lang))
        await state.set_state("settings")
        return
    await message.answer(_("Change settings"), reply_markup=make_settings())
    await state.set_state("settings")



@dp.message_handler(Text(contains="✏️"), state='settings')
async def edit_name(message: Message, state: FSMContext):
    await message.answer(_("Enter your name:"))
    await state.set_state('enter_name')


@dp.message_handler(state='enter_name')
async def enter_name(message: Message, state: FSMContext):
    await db.update_name(message.from_user.id, message.text)
    await message.answer(_("Your name has been changed!"))
    await edit_settings(message, state)
    await state.set_state('settings')


@dp.message_handler(Text(contains="📱"), state='settings')
async def edit_phone(message: Message, state: FSMContext):
    phone = await db.select_phone(message.from_user.id)

    await message.answer(_("Enter your phone number or share your contact:\nExample: 90 123 45 67\n"
                           "Your current phone {}").format(phone),
                         reply_markup=contact_markup())
    await state.set_state('enter_phone')


@dp.message_handler(state='enter_phone', content_types=ContentTypes.CONTACT | ContentTypes.TEXT)
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
    await message.answer(_("Your phone number has been changed!"))
    await edit_settings(message, state)
    await state.set_state('settings')

@dp.message_handler(Text(contains="🇷🇺"), state='settings')
@dp.message_handler(Text(contains="🇺🇸"), state='settings')
@dp.message_handler(Text(contains="🇺🇿"), state='settings')
async def edit_lang(message: Message, state: FSMContext):
    await message.answer(_("Choose your language:"), reply_markup=lang_inline)
    await state.set_state('enter_lang')

