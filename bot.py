import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

from stopgame import StopGame

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

# инициализируем парсер
sg = StopGame('lastkey.txt')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await bot.send_message(message.from_user.id,"Привет, меня зовут Recent News Bot\n\nИ я помогу вам оставаться в курсе последних событий игровой сферы\n\nЧтобы узнать список моих команд введите /help")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	await bot.send_message(message.from_user.id, "Список команд:\n\n/subscribe - Подписаться на рассылку\n/unsubscribe - Отписаться от рассылки")


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel')
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.callback_query_handler(lambda call:True)
async def answer(call):
	if call.data == 'lastnews':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = sg.game_info()

		await bot.send_photo(
			call.message.chat.id,
			open(sg.download_image(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")


# проверяем наличие новых игр и делаем рассылки
async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_games = sg.new_games()

		if(new_games):

			# парсим инфу о новой игре
			nfo = sg.game_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions()

			# отправляем всем новость
			
			for id in subscriptions:
				await bot.send_photo(
					id[1],
					open(sg.download_image(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				
				# обновляем ключ
			sg.update_lastkey()

# запускаем лонг поллинг
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(10)) 
	executor.start_polling(dp, skip_updates=True)