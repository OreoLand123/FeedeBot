from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup,  InlineKeyboardButton, KeyboardButton




butt_feed = KeyboardButton("Наши корма")
butt_price = KeyboardButton("Скидки и акции")
butt_questions = KeyboardButton("Часто задаваемые вопросы")
butt_buy = KeyboardButton("Преобрести корм")
kb_1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_1.row(butt_feed, butt_price, butt_questions, butt_buy)

def inline_feed_list(call_list, inline_feed_butt):
    for i, feed in enumerate(call_list):
        inline_feed_butt.add(InlineKeyboardButton(feed, callback_data=f"feed_{i + 1}"))


def inline(call_list_buy, inline_buy_butt):
    for i_2, buy in enumerate(call_list_buy):
        inline_buy_butt.add(InlineKeyboardButton(buy, callback_data=f"buy_{i_2 + 1}"))


butt_back = KeyboardButton("Назад")
kb_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_2.row(butt_back)

butt_yes = KeyboardButton("Подтвердить заказ")
butt_no = KeyboardButton("Отменить заказ")
kb_3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_3.row(butt_yes, butt_no)


back_inline = InlineKeyboardButton("Назад", callback_data="back_prod")
butt_back_prod = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(back_inline)

cancel_inline = InlineKeyboardButton("Отказ", callback_data="cancel")
butt_cancel = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cancel_inline)


causes_inline = InlineKeyboardMarkup()
causes_list = ['Недозвон', 'Товара нет']
for i, cause in enumerate(causes_list):
    causes_inline.add(InlineKeyboardButton(cause, callback_data=f'cause_{i+1}'))