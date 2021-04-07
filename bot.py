import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

from google_trans_new import google_translator

transl = google_translator()

from yandexfreetranslate import YandexFreeTranslate
yt = YandexFreeTranslate()

from stopgame import StopGame
from calend import Calend
from eng import Eng
from anime import Anime
from tech import Tech
from sale import Sale
from sport import Sport
from kinopoisk import Kinopoisk
from mus import Music

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

# инициализируем парсер
sg = StopGame('lastkey.txt')

cd = Calend()

engame = Eng('lastkey_eng.txt')

anime = Anime('lastkey_anime.txt')

sale = Sale('lastkey_sale.txt')

tech = Tech('lastkey_tech.txt')

sport = Sport('lastkey_sport.txt')

kino = Kinopoisk('lastkey_kino.txt')

mus = Music('lastkey_mus.txt')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await bot.send_message(message.from_user.id,"Привет, меня зовут Recent News Bot\n\nИ я помогу вам оставаться в курсе последних событий игровой сферы\n\nЧтобы узнать список моих команд введите /help")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	await bot.send_message(message.from_user.id, "Список команд:\n\n/subscribe - Подписаться на рассылку игровых новостей stopgame\n/unsubscribe - Отписаться от рассылки игровых новостей stopgame\n/subscribe_eng - Подписаться на рассылки игровых новостей theverge\n/unsubscribe_eng - Отписаться от рассылки игровых новостей theverge\n/history_calendar - Календарь событий\n/subscribe_anime - Подписаться на рассылку аниме новостей\n/unsubscribe_anime - Отписаться от рассылки аниме новостей\n/subscribe_tech - Подписаться на рассылку новостей техники и высоких технологий\n/unsubscribe_tech - Отписаться от новостей техники и высоких технологий\n/subscribe_sale - Подписаться на рассылку игровых скидок\n/unsubscribe_sale - Отписаться от рассылки игровых скидок\n/subscribe_sport - Подписаться на рассылку спортивных новостей\n/unsubscribe_sport - Отписаться от рассылки спортивных новостей\n/subscribe_kino - Подписаться на рассылку новостей мира кино\n/unsubscribe_kino - Отписаться от рассылки новостей мира кино\n/subscribe_mus - Подписаться на рассылку музыкальных новостей\n/unsubscribe_mus - Отписаться от рассылки музыкальных новостей")


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

@dp.message_handler(commands=['subscribe_eng'])
async def subscribe_eng(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'englastnews')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'engcancel')
	if(not db.subscriber_exists_eng(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber_eng(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_eng(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_anime'])
async def subscribe_anime(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_anime')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_anime')
	if(not db.subscriber_exists_anime(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber_anime(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_anime(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_tech'])
async def subscribe_tech(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_tech')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_tech')
	if(not db.subscriber_exists_tech(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber_tech(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_tech(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_sale'])
async def subscribe_sale(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_sale')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_sale')
	if(not db.subscriber_exists_sale(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber_sale(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_sale(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_sport'])
async def subscribe_sport(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_sport')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_sport')
	if(not db.subscriber_exists_sport(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber_sport(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_sport(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_kino'])
async def subscribe_kino(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_kino')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_kino')
	if(not db.subscriber_exists_kino(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber_kino(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_kino(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_mus'])
async def subscribe_mus(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_mus')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_mus')
	if(not db.subscriber_exists_mus(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber_mus(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_mus(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

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

@dp.message_handler(commands=['unsubscribe_eng'])
async def unsubscribe_eng(message: types.Message):
	if(not db.subscriber_exists_eng(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber_eng(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_eng(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")		

@dp.message_handler(commands=['unsubscribe_anime'])
async def unsubscribe_anime(message: types.Message):
	if(not db.subscriber_exists_anime(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber_anime(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_anime(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_tech'])
async def unsubscribe_tech(message: types.Message):
	if(not db.subscriber_exists_tech(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber_tech(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_tech(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_sale'])
async def unsubscribe_sale(message: types.Message):
	if(not db.subscriber_exists_sale(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber_sale(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_sale(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_sport'])
async def unsubscribe_sport(message: types.Message):
	if(not db.subscriber_exists_sport(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber_sport(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_sport(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_kino'])
async def unsubscribe_kino(message: types.Message):
	if(not db.subscriber_exists_kino(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber_kino(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_kino(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_mus'])
async def unsubscribe_mus(message: types.Message):
	if(not db.subscriber_exists_mus(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber_mus(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription_mus(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")		

@dp.message_handler(commands=['history_calendar'])
async def history_calendar(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'Date')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancelDate')
	markup_inline.add(item_news,item_cancel)
	await message.answer("Хотите узнать что произошло сегодня?", reply_markup = markup_inline)

@dp.callback_query_handler(lambda call:True)
async def answercal(call):
	if call.data == 'Date':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = cd.calend_info()

		for i in range(len(nfo["title"])):
			await bot.send_photo(
				call.message.chat.id,
				open(cd.download_image_cal(nfo['image'][i].find('a').find('img').get('src')), 'rb'),
				caption = nfo['title'][i].find('a').get_text()+ " " + nfo['year'][i].get_text() + " год",
				disable_notification = True
			)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancelDate':
		await call.message.edit_reply_markup(reply_markup=None)

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

	if call.data == 'englastnews':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = engame.daily_info()
		markup_inline = types.InlineKeyboardMarkup()
		item_newsg = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'google_ru')
		item_newsy = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'yanfex_ru')
		item_cancelr = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'cancel_ru')
		markup_inline.add(item_newsg,item_newsy,item_cancelr)
		await bot.send_photo(
			call.message.chat.id,
			open(engame.download_image_eng(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'engcancel':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'google_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = engame.daily_info()

		await bot.send_photo(
			call.message.chat.id,
			open(engame.download_image_eng(nfo['image']), 'rb'),
			caption = "Перевод:"+ "\n\n" + transl.translate(nfo['title'],lang_tgt='ru') +"\n\n" + transl.translate(nfo['text'],lang_tgt='ru'),
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")

	if call.data == 'yanfex_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = engame.daily_info()

		await bot.send_photo(
			call.message.chat.id,
			open(engame.download_image_eng(nfo['image']), 'rb'),
			caption = "Перевод:" + "\n\n" + yt.translate("en", "ru", nfo['title']) + "\n\n" + yt.translate("en", "ru", nfo['text']),
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")

	if call.data == 'cancel_ru':
		await call.message.edit_reply_markup(reply_markup=None)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")

	if call.data == 'lastnews_anime':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = anime.anime_info()

		await bot.send_photo(
			call.message.chat.id,
			open(anime.download_image_anime(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_anime':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_tech':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = tech.tech_info()

		await bot.send_photo(
			call.message.chat.id,
			open(tech.download_image_tech(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_tech':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_sale':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = sale.sale_info()

		await bot.send_photo(
			call.message.chat.id,
			open(sale.download_image_sale(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_sale':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_sport':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = sport.sport_info()

		await bot.send_photo(
			call.message.chat.id,
			open(sport.download_image_sport(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_sport':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_kino':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = kino.kino_info()

		await bot.send_photo(
			call.message.chat.id,
			open(kino.download_image_kino(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_kino':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_mus':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = mus.mus_info()

		await bot.send_photo(
			call.message.chat.id,
			open(mus.download_image_mus(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_mus':
		await call.message.answer("Ждите, скоро выйдут новые статьи и вы узнаете о них первыми =)")
		await call.message.edit_reply_markup(reply_markup=None)





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
				try:
					await bot.send_photo(
					id[1],
					open(sg.download_image(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			sg.update_lastkey()


async def scheduled_eng(wait_for):
	markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
	markup_inline = types.InlineKeyboardMarkup()
	item_newsg = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'google_ru')
	item_newsy = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'yanfex_ru')
	item_cancelr = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'cancel_ru')
	markup_inline.add(item_newsg,item_newsy,item_cancelr)
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_games = engame.new_daily()

		if(new_games):

			# парсим инфу о новой игре
			nfo = engame.daily_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_eng()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(engame.download_image_eng(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			engame.update_lastkey_eng()


async def scheduled_anime(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_anime = anime.new_anime()

		if(new_anime):

			# парсим инфу о новой игре
			nfo = anime.anime_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_anime()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(anime.download_image_anime(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			anime.update_lastkey_anime()


async def scheduled_tech(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_tech = tech.new_tech()

		if(new_tech):

			# парсим инфу о новой игре
			nfo = tech.tech_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_tech()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(tech.download_image_tech(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			tech.update_lastkey_tech()

async def scheduled_sale(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_sale = sale.new_sale()

		if(new_sale):

			# парсим инфу о новой игре
			nfo = sale.sale_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_sale()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(sale.download_image_sale(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			sale.update_lastkey_sale()

async def scheduled_sport(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_sport = sport.new_sport()

		if(new_sport):

			# парсим инфу о новой игре
			nfo = sport.sport_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_sale()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(sport.download_image_sport(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			sport.update_lastkey_sport()

async def scheduled_kino(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_kino = kino.new_kino()

		if(new_kino):

			# парсим инфу о новой игре
			nfo = kino.kino_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_sale()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(kino.download_image_kino(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			kino.update_lastkey_kino()

async def scheduled_mus(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_mus = mus.new_mus()

		if(new_mus):

			# парсим инфу о новой игре
			nfo = mus.mus_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_sale()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(mus.download_image_mus(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			mus.update_lastkey_mus()

# запускаем лонг поллинг
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(10))
	loop.create_task(scheduled_eng(10))
	loop.create_task(scheduled_anime(10))
	loop.create_task(scheduled_tech(10))
	loop.create_task(scheduled_sale(10))
	loop.create_task(scheduled_sport(10))
	loop.create_task(scheduled_kino(10))
	loop.create_task(scheduled_mus(10))
	executor.start_polling(dp, skip_updates=True)