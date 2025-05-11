from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, filters, MessageHandler

TOKEN = '7186692461:AAHWyOQC1Hcc3dQtIQy0tjCnLwHHBm4HNPM'
CHANNEL_USERNAME = '@taekwondo_iran_rezania'
ADMIN_CHAT_ID = '246873587'

async def check_membership(user_id: int, context: CallbackContext) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not await check_membership(user_id, context):
        keyboard = [[InlineKeyboardButton("عضو شدم", callback_data='check_membership')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f'برای استفاده از ربات، ابتدا باید در کانال زیر عضو شوید، سپس دوباره (استارت) را بزنید:\n{CHANNEL_USERNAME}',
            reply_markup=reply_markup
        )
    else:
        await show_options(update.message, context)

async def show_options(message, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("پرداخت شهریه ، سالن قدس", callback_data='hall_quds')],
        [InlineKeyboardButton("پرداخت شهریه ، سالن شهید عباسی", callback_data='hall_abbasi')],
        [InlineKeyboardButton("چاپ احکام", callback_data='print_orders')],
        [InlineKeyboardButton("خرید اسامی تکواندو", callback_data='buy_taekwondo')],
        [InlineKeyboardButton("کلاس خصوصی", callback_data='12345')],
        [InlineKeyboardButton("تهیه وسایل تکواندو", callback_data='123_456')],
        [InlineKeyboardButton("بیمه ورزشی", callback_data='sport_insurance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text('روی یکی از موارد انتخابی زیر کلیک کنید:', reply_markup=reply_markup)

async def check_membership_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if await check_membership(user_id, context):
        await query.answer(text="شما با موفقیت عضو کانال شدید.", show_alert=True)
        await show_options(query.message, context)
    else:
        await query.answer(text="هنوز عضو کانال نشده‌اید. لطفاً عضو شوید و دوباره تلاش کنید.", show_alert=True)

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "برای دریافت پشتیبانی می‌توانید از طریق راه‌های زیر با ما در تماس باشید:\n"
        "شماره تماس: 09143517593\n"
        "پشتیبانی: .... /@behnam_tkd_iran ... "
        "جهت داشتن هرگونه سوال از طریق پشتیبانی اقدام نمایید")
    await update.message.reply_text(help_text)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'hall_quds':
        response_text = (
            "هزینه هر ماه 250,000 تومان برای پرداخت از درگاه بانکی زیر استفاده کنید:\n"
            "_ https://zarinp.al/bwraham _"
            "بعد از پرداخت، نام خانوادگی، تصویر رسید، ماه شهریه پرداخت شده را ارسال کنید."
        )
    elif data == 'hall_abbasi':
        response_text = (
            "هزینه هر ماه 300,000T برای پرداخت از درگاه بانکی زیر استفاده کنید:\n"
            "_ https://zarinp.al/bwraham _"
            "بعد از پرداخت، نام خانوادگی ، تصویر رسید، (ماه) شهریه پرداخت شده را ارسال کنید."
        )
    elif data == 'buy_taekwondo':
        response_text = (
            "هزینه خرید جزوه تکواندو 100,00T ، جهت پرداخت از درگاه بانکی زیر استفاده نمایید:\n"
            "_ https://zarinp.al/bwraham _"
            "بعد از پرداخت، نام خانوادگی را همراه رسید ارسال نمایید."
        )
    elif data == 'sport_insurance':
        response_text = ("هزینه پرداخت بیمه ورزشی ، 95,000 ، جهت پرداخت از درگاه بانکی زیر اقدام نمایید."
                           "_ https://zarinp.al/bwraham _"
                           "بعد از پرداخت، نام خانوادگی ، تصویر رسید را ارسال نمایید.")
    elif data == '12345':
        response_text = ("برای ثبت نام و هماهنگی در کلاس خصوصی لطفا با شماره زیر تماس بگیرید"
                         "شماره موبایل: 09143517593")

    elif data == '123_456':
        response_text = (
            "وسایل تکواندو ما شامل لباس تکواندو ( ساده ، حرفه ای) _ هوگو _ روپا (ساده ، الکترونیکی) _ دستکش _"
            "ساق بند _ ساعد بند _ کاپ _ کلاه (ساده ، حرفه ای) _ میت بالشی _ میت راکتی _ کمربند (ساده ، حرفه ای) "
            "برای سفارش لطفا تعداد و نام هرکدام از وسایل تکواندو را که میخواهید همراه با نام خانوادگی ارسال نمایید .")
    elif data == 'print_orders':
        keyboard = [
            [InlineKeyboardButton("زرد", callback_data='yellow_belt')],
            [InlineKeyboardButton("سبز", callback_data='green_belt')],
            [InlineKeyboardButton("آبی", callback_data='blue_belt')],
            [InlineKeyboardButton("قرمز", callback_data='red_belt')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="لطفا کمربند مورد نظر خود را برای چاپ احکام انتخاب کنید:",
                                      reply_markup=reply_markup)
    elif data == 'yellow_belt':
        await query.edit_message_text(text="قیمت حکم کمر زرد: 40,000T\n\n"
                                           "برای پرداخت لطفا از درگاه بانکی زیر استفاده کنید:\n"
                                           "_ https://zarinp.al/bwraham _"
                                           "بعد از پرداخت ، نام خانوادگی و تصویر رسید را ارسال نمایید")
    elif data == 'green_belt':
        await query.edit_message_text(text="قیمت حکم کمر سبز: 45,000T\n\n"
                                           "برای پرداخت لطفا از درگاه بانکی زیر استفاده کنید:\n"
                                           "_ https://zarinp.al/bwraham _"
                                           "بعد از پرداخت ، نام خانوادگی و تصویر رسید را ارسال نمایید")
    elif data == 'blue_belt':
        await query.edit_message_text(text="قیمت حکم کمر آبی: 50,000T\n\n"
                                           "برای پرداخت لطفا از درگاه بانکی زیر استفاده کنید:\n"
                                           "_ https://zarinp.al/bwraham _"
                                           "بعد از پرداخت ، نام خانوادگی و تصویر رسید را ارسال نمایید")
    elif data == 'red_belt':
        await query.edit_message_text(text="قیمت حکم کمر قرمز: 55,000T\n\n"
                                           "برای پرداخت لطفا از درگاه بانکی زیر استفاده کنید:\n"
                                           "_ https://zarinp.al/bwraham _"
                                           "بعد از پرداخت ، نام خانوادگی و تصویر رسید را ارسال نمایید")


    await query.edit_message_text(text=response_text)

async def forward_to_admin(update: Update, context: CallbackContext) -> None:
    
    await update.message.forward(chat_id=ADMIN_CHAT_ID)

async def receive_photo(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1]  
    file_id = photo.file_id
    caption = update.message.caption or "بدون کپشن"

    await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=file_id, caption=caption)


async def start_payment(update: Update, context: CallbackContext) -> None:

  
    payment_url = "https://your-payment-gateway.com/pay?token=abc123"

    keyboard = [[InlineKeyboardButton("پرداخت", url=payment_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفا برای پرداخت روی دکمه زیر کلیک کنید:", reply_markup=reply_markup)





def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CallbackQueryHandler(check_membership_callback, pattern='check_membership'))
    application.add_handler(MessageHandler(filters.ALL, forward_to_admin))
    application.add_handler(MessageHandler(filters.PHOTO, receive_photo))  # Handler برای دریافت عکس
    application.add_handler(CommandHandler("start_payment", start_payment))


    application.run_polling()

if __name__ == '__main__':
    main()










