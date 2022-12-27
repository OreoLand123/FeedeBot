import keyboard
from create_bot import bot
from state import FSMAdmin, FSMContext
import functions
from aiogram.types import InlineKeyboardMarkup


async def start_message(message):
    await bot.send_message(message.from_user.id, "Пройдите регистрацию")
    await bot.send_message(message.from_user.id, "Введите имя")
    await FSMAdmin.register_number.set()

async def register_number(message, state: FSMContext):
    async with state.proxy() as data:
        name = message.text
        data['name'] = name
    await FSMAdmin.register_number_2.set()
    await bot.send_message(message.from_user.id, "Введите номер телефона")

async def register_number_2(message, state:FSMContext):
    async with state.proxy() as data:
        name = data["name"]
    if functions.number_cheak(message.text):
        await bot.send_message(message.from_user.id, f"Спасибо за регистрацию {name}", reply_markup=keyboard.kb_1)
        functions.db_register(name=name, tg_name=message.from_user.username, number=message.text, tg_id=str(message.from_user.id))
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, f"Проверьте номер ещё раз")
        await FSMAdmin.register_number_2.set()

async def feed_handler(message):
    inline_feed_butt = InlineKeyboardMarkup()
    call_list = functions.list_bd_feed(flag=True)
    keyboard.inline_feed_list(call_list, inline_feed_butt)
    await bot.send_message(message.from_user.id, "Список наших кормов", reply_markup=inline_feed_butt)

async def feed_handler_count(call):
    await bot.edit_message_text(
        text=functions.db_title(call.data),
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard.butt_back_prod
    )


async def back_inline_handler(call):
    inline_feed_butt = InlineKeyboardMarkup()
    call_list = functions.list_bd_feed(flag=True)
    keyboard.inline_feed_list(call_list, inline_feed_butt)
    await bot.edit_message_text(
        text="Список наших кормов",
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=inline_feed_butt
    )



async def buy_handler(message):
    inline_buy_butt = InlineKeyboardMarkup()
    call_list_buy = functions.list_bd_feed(flag=False)
    keyboard.inline(call_list_buy, inline_buy_butt)
    await bot.send_message(message.from_user.id, f"Список кормов в наличии:", reply_markup=inline_buy_butt)


async def buy_handler_count(call, state: FSMContext):
    call_list = functions.list_bd_feed(flag=True)
    name_feed = call_list[int(call.data[-1]) - 1]
    await bot.send_message(call.message.chat.id, f"Введите кол-во мешков {name_feed}", reply_markup=keyboard.kb_2)
    await FSMAdmin.reason.set()
    async with state.proxy() as data:
        data['name'] = name_feed

async def buy_examination(message, state: FSMContext):
    try:
        int(message.text)
        count = message.text
        async with state.proxy() as data:
            name_feed = data['name']
            data['count'] = count
        cheak = functions.cheak_db_anction(num=int(count), name_feed=name_feed, flag=True)
        if cheak == True:
            await bot.send_message(message.from_user.id, f"Ваш заказ {name_feed} кол-во {count} \n О корме: {functions.cheak_db_anction(num=int(count), name_feed=name_feed, flag=False)}", reply_markup=keyboard.kb_3)
            await FSMAdmin.reason_2.set()
        else:
            inline_buy_butt = InlineKeyboardMarkup()
            call_list_buy = functions.list_bd_feed(flag=False)
            keyboard.inline(call_list_buy, inline_buy_butt)
            await bot.send_message(message.from_user.id, f"На складе столько корма нет\n корма на складе: {cheak}", reply_markup=inline_buy_butt)
            await state.finish()
    except ValueError:
        if message.text.lower() == "назад":
            await bot.send_message(message.from_user.id, "хорошо", reply_markup=keyboard.kb_1)
            await state.finish()
        else:
            inline_buy_butt = InlineKeyboardMarkup()
            call_list_buy = functions.list_bd_feed(flag=False)
            keyboard.inline(call_list_buy, inline_buy_butt)
            await bot.send_message(message.from_user.id, "введите цифру")
            await FSMAdmin.reason.set()


async def yes_and_no_handler(message, state: FSMContext):
    if message.text == "Подтвердить заказ":
        async with state.proxy() as data:
            name_feed = data['name']
            count = data['count']
        action = functions.cheak_db_anction(num=int(count), name_feed=name_feed, flag=None)
        if action == True:
            await bot.send_message(message.from_user.id, "Заказ подтверждён с вами свяжутся", reply_markup=keyboard.kb_1)
            await bot.send_message("2023643840", functions.get_userdata(str(message.from_user.id)), reply_markup=keyboard.cancel_inline)
            await state.finish()
        else:
            inline_buy_butt = InlineKeyboardMarkup()
            call_list_buy = functions.list_bd_feed(flag=False)
            keyboard.inline(call_list_buy, inline_buy_butt)
            await bot.send_message(message.from_user.id, f"На складе столько корма нет\n корма на складе: {functions.cheak_db_anction(num=int(count), name_feed=name_feed, flag=True)}",
                                   reply_markup=inline_buy_butt)
            await state.finish()
    elif message.text == "Отменить заказ":
        await bot.send_message(message.from_user.id, "Заказ отменён", reply_markup=keyboard.kb_1)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Такого варианта нет", reply_markup=keyboard.kb_3)


async def action_admin(call):
    await bot.edit_message_text(
        text="Выберите причину отказа",
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard.causes_inline
    )

async def write_causes_user(call):
    await bot.edit_message_text(

    )


def register_handler(dp):
    call_list_buy = functions.list_bd_feed(flag=False)
    call_list = functions.list_bd_feed(flag=True)
    dp.register_message_handler(start_message, commands=["start"])
    dp.register_message_handler(feed_handler, lambda message: "наши корма" in message.text.lower(), state=None)
    dp.register_callback_query_handler(feed_handler_count, lambda callback: callback.data in [f"feed_{i + 1}" for i in range(len(call_list))], state=None)
    dp.register_message_handler(buy_handler, lambda message: "преобрести корм" in message.text.lower(), state=None)
    dp.register_callback_query_handler(buy_handler_count, lambda callback: callback.data in [f"buy_{i + 1}" for i in range(len(call_list_buy))], state=None)
    dp.register_message_handler(buy_examination, lambda message: message.text, state=FSMAdmin.reason)
    dp.register_message_handler(yes_and_no_handler, lambda message: message.text, state=FSMAdmin.reason_2)
    dp.register_message_handler(register_number, lambda message: message.text, state=FSMAdmin.register_number)
    dp.register_message_handler(register_number_2, lambda message: message.text, state=FSMAdmin.register_number_2)
    dp.register_callback_query_handler(back_inline_handler, lambda callback: callback.data == "back_prod", state=None)
    dp.register_callback_query_handler(action_admin, lambda callback: callback.data == "cancel", state=None)




