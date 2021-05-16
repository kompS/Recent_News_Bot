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
from space import Space
from mmo import Mmo
from mobile import Mobile
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
space = Space('lastkey_space.txt')
mmo = Mmo('lastkey_mmo.txt')
mob = Mobile('lastnews_mob.txt')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await bot.send_message(message.from_user.id,"Привет, меня зовут Recent News Bot\n\nИ я помогу вам оставаться в курсе последних событий из различных сфер жизнидеятельности человека\n\nЧтобы продолжить введите /menu или /help")

@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
	markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = types.KeyboardButton('Игры')
	item2 = types.KeyboardButton('Аниме')
	item3 = types.KeyboardButton('Спорт')
	item4 = types.KeyboardButton('Кино')
	item5 = types.KeyboardButton('Космос')
	item6 = types.KeyboardButton('Гаджеты')
	item7 = types.KeyboardButton('Музыка')
	item8 = types.KeyboardButton('Календарь')
	item9 = types.KeyboardButton('Выход')
	markup_reply.add(item1,item2,item3,item4,item5,item6,item7,item8,item9)
	await bot.send_message(message.from_user.id,"Выберите интересующую вас тему", reply_markup = markup_reply)



@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	await bot.send_message(message.from_user.id, "Список команд:\n\n/subscribe - Подписаться на рассылку игровых новостей stopgame\n/unsubscribe - Отписаться от рассылки игровых новостей stopgame\n/subscribe_eng - Подписаться на рассылки игровых новостей theverge\n/unsubscribe_eng - Отписаться от рассылки игровых новостей theverge\n/history_calendar - Календарь событий\n/subscribe_anime - Подписаться на рассылку аниме новостей\n/unsubscribe_anime - Отписаться от рассылки аниме новостей\n/subscribe_tech - Подписаться на рассылку новостей техники и высоких технологий\n/unsubscribe_tech - Отписаться от новостей техники и высоких технологий\n/subscribe_sale - Подписаться на рассылку игровых скидок\n/unsubscribe_sale - Отписаться от рассылки игровых скидок\n/subscribe_sport - Подписаться на рассылку спортивных новостей\n/unsubscribe_sport - Отписаться от рассылки спортивных новостей\n/subscribe_kino - Подписаться на рассылку новостей мира кино\n/unsubscribe_kino - Отписаться от рассылки новостей мира кино\n/subscribe_mus - В разработке\n/unsubscribe_mus - В разработке")

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
		db.add_subscriber_mus(message.from_user.id)
	else:
		db.update_subscription_mus(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_space'])
async def subscribe_space(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_space')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_space')
	if(not db.subscriber_exists_space(message.from_user.id)):
		db.add_subscriber_space(message.from_user.id)
	else:
		db.update_subscription_space(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_mmo'])
async def subscribe_mmo(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_mmo')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_mmo')
	if(not db.subscriber_exists_mmo(message.from_user.id)):
		db.add_subscriber_mmo(message.from_user.id)
	else:
		db.update_subscription_mmo(message.from_user.id, True)
	markup_inline.add(item_news,item_cancel)
	await message.answer("Вы успешно подписались на рассылку!\n\nХотите получить последнюю новость?", reply_markup = markup_inline)

@dp.message_handler(commands=['subscribe_mob'])
async def subscribe_mob(message: types.Message):
	markup_inline = types.InlineKeyboardMarkup()
	item_news = types.InlineKeyboardButton(text = 'Да',callback_data = 'lastnews_mob')
	item_cancel = types.InlineKeyboardButton(text = 'Нет',callback_data = 'cancel_mob')
	if(not db.subscriber_exists_mob(message.from_user.id)):
		db.add_subscriber_mob(message.from_user.id)
	else:
		db.update_subscription_mob(message.from_user.id, True)
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
		db.add_subscriber_mus(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		db.update_subscription_mus(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_space'])
async def unsubscribe_space(message: types.Message):
	if(not db.subscriber_exists_space(message.from_user.id)):
		db.add_subscriber_space(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		db.update_subscription_space(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_mmo'])
async def unsubscribe_mmo(message: types.Message):
	if(not db.subscriber_exists_mmo(message.from_user.id)):
		db.add_subscriber_mmo(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		db.update_subscription_mmo(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler(commands=['unsubscribe_mob'])
async def unsubscribe_mob(message: types.Message):
	if(not db.subscriber_exists_mob(message.from_user.id)):
		db.add_subscriber_mob(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		db.update_subscription_mob(message.from_user.id, False)
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
		item_newsy = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'yandex_ru')
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
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'google_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = engame.daily_info()

		await bot.send_photo(
			call.message.chat.id,
			open(engame.download_image_eng(nfo['image']), 'rb'),
			caption = "Перевод:"+ "\n\n" + transl.translate(nfo['title'],lang_tgt='ru') +"\n\n" + transl.translate(nfo['text'],lang_tgt='ru'),
			disable_notification = True
		)

	if call.data == 'yandex_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = engame.daily_info()

		await bot.send_photo(
			call.message.chat.id,
			open(engame.download_image_eng(nfo['image']), 'rb'),
			caption = "Перевод:" + "\n\n" + yt.translate("en", "ru", nfo['title']) + "\n\n" + yt.translate("en", "ru", nfo['text']),
			disable_notification = True
		)

	if call.data == 'cancel_ru':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_anime':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = anime.anime_info()

		await bot.send_photo(
			call.message.chat.id,
			open(anime.download_image_anime(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_anime':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_tech':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		markup_inline = types.InlineKeyboardMarkup()
		item_newsgt = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'tgoogle_ru')
		item_newsyt = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'tyandex_ru')
		item_cancelrt = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'tcancel_ru')
		markup_inline.add(item_newsgt,item_newsyt,item_cancelrt)
		nfo = tech.tech_info()

		await bot.send_photo(
			call.message.chat.id,
			open(tech.download_image_tech(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],reply_markup = markup_inline,
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_tech':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_sale':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = sale.sale_info()

		await bot.send_photo(
			call.message.chat.id,
			open(sale.download_image_sale(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_sale':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_sport':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = sport.sport_info()

		await bot.send_photo(
			call.message.chat.id,
			open(sport.download_image_sport(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_sport':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_kino':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = kino.kino_info()

		await bot.send_photo(
			call.message.chat.id,
			open(kino.download_image_kino(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_kino':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_mus':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mus.mus_info()
		markup_inline = types.InlineKeyboardMarkup()
		item_newsgm = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'mgoogle_ru')
		item_newsym = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'myandex_ru')
		item_cancelrm = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'mcancel_ru')
		markup_inline.add(item_newsgm,item_newsym,item_cancelrm)
		await bot.send_photo(
			call.message.chat.id,
			open(mus.download_image_mus(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'engcancel':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'mgoogle_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mus.mus_info()

		await bot.send_photo(
			call.message.chat.id,
			open(mus.download_image_mus(nfo['image']), 'rb'),
			caption = "Перевод:"+ "\n\n" + transl.translate(nfo['title'],lang_tgt='ru') +"\n\n" + transl.translate(nfo['text'],lang_tgt='ru'),
			disable_notification = True
		)

	if call.data == 'myandex_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mus.mus_info()

		await bot.send_photo(
			call.message.chat.id,
			open(mus.download_image_mus(nfo['image']), 'rb'),
			caption = "Перевод:" + "\n\n" + yt.translate("en", "ru", nfo['title']) + "\n\n" + yt.translate("en", "ru", nfo['text']),
			disable_notification = True
		)

	if call.data == 'mcancel_ru':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_space':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = space.space_info()
		markup_inline = types.InlineKeyboardMarkup()
		item_newsgs = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'sgoogle_ru')
		item_newsys = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'syandex_ru')
		item_cancelrs = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'scancel_ru')
		markup_inline.add(item_newsgs,item_newsys,item_cancelrs)
		await bot.send_photo(
			call.message.chat.id,
			open(space.download_image_space(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'spacecancel':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'sgoogle_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = space.space_info()

		await bot.send_photo(
			call.message.chat.id,
			open(space.download_image_space(nfo['image']), 'rb'),
			caption = "Перевод:"+ "\n\n" + transl.translate(nfo['title'],lang_tgt='ru') +"\n\n" + transl.translate(nfo['text'],lang_tgt='ru'),
			disable_notification = True
		)

	if call.data == 'syandex_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = space.space_info()

		await bot.send_photo(
			call.message.chat.id,
			open(space.download_image_space(nfo['image']), 'rb'),
			caption = "Перевод:" + "\n\n" + yt.translate("en", "ru", nfo['title']) + "\n\n" + yt.translate("en", "ru", nfo['text']),
			disable_notification = True
		)

	if call.data == 'scancel_ru':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_mmo':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mmo.mmo_info()

		await bot.send_photo(
			call.message.chat.id,
			open(mmo.download_image_mmo(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_mmo':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'lastnews_mob':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mob.mob_info()
		markup_inline = types.InlineKeyboardMarkup()
		item_newsmob = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'mobgoogle_ru')
		item_newsmoby = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'mobyandex_ru')
		item_cancelmob = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'mobcancel_ru')
		markup_inline.add(item_newsmob,item_newsmoby,item_cancelmob)
		await bot.send_photo(
			call.message.chat.id,
			open(mob.download_image_mob(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'] , reply_markup = markup_inline,
			disable_notification = True
		)
		await call.message.edit_reply_markup(reply_markup=None)
	elif call.data == 'cancel_mob':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'mobgoogle_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mob.mob_info()

		await bot.send_photo(
			call.message.chat.id,
			open(mob.download_image_mob(nfo['image']), 'rb'),
			caption = "Перевод:"+ "\n\n" + transl.translate(nfo['title'],lang_tgt='ru') +"\n\n" + transl.translate(nfo['text'],lang_tgt='ru'),
			disable_notification = True
		)

	if call.data == 'mobyandex_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mob.mob_info()

		await bot.send_photo(
			call.message.chat.id,
			open(mob.download_image_mob(nfo['image']), 'rb'),
			caption = "Перевод:" + "\n\n" + yt.translate("en", "ru", nfo['title']) + "\n\n" + yt.translate("en", "ru", nfo['text']),
			disable_notification = True
		)

	if call.data == 'tcancel_ru':
		await call.message.edit_reply_markup(reply_markup=None)

	if call.data == 'tgoogle_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = tech.tech_info()

		await bot.send_photo(
			call.message.chat.id,
			open(tech.download_image_tech(nfo['image']), 'rb'),
			caption = "Перевод:"+ "\n\n" + transl.translate(nfo['title'],lang_tgt='ru') +"\n\n" + transl.translate(nfo['text'],lang_tgt='ru'),
			disable_notification = True
		)

	if call.data == 'mobyandex_ru':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = tech.tech_info()

		await bot.send_photo(
			call.message.chat.id,
			open(tech.download_image_tech(nfo['image']), 'rb'),
			caption = "Перевод:" + "\n\n" + yt.translate("en", "ru", nfo['title']) + "\n\n" + yt.translate("en", "ru", nfo['text']),
			disable_notification = True
		)

	if call.data == 'tcancel_ru':
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
	item_newsy = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'yandex_ru')
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
	markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
	markup_inline = types.InlineKeyboardMarkup()
	item_newsgt = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'tgoogle_ru')
	item_newsyt = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'tyandex_ru')
	item_cancelrt = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'tcancel_ru')
	markup_inline.add(item_newsgt,item_newsyt,item_cancelrt)
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
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],reply_markup = markup_inline,
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
			subscriptions = db.get_subscriptions_sport()

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
	markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
	markup_inline = types.InlineKeyboardMarkup()
	item_newsgm = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'mgoogle_ru')
	item_newsym = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'myandex_ru')
	item_cancelrm = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'mcancel_ru')
	markup_inline.add(item_newsgm,item_newsym,item_cancelrm)
	while True:
		await asyncio.sleep(wait_for)

		new_mus = mus.new_mus()

		if(new_mus):

			
			nfo = mus.mus_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_mus()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(mus.download_image_mus(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			mus.update_lastkey_mus()

async def scheduled_space(wait_for):
	markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
	markup_inline = types.InlineKeyboardMarkup()
	item_newsgs = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'sgoogle_ru')
	item_newsys = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'syandex_ru')
	item_cancelrs = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'scancel_ru')
	markup_inline.add(item_newsgs,item_newsys,item_cancelrs)
	while True:
		await asyncio.sleep(wait_for)

		new_space = space.new_space()

		if(new_space):

			
			nfo = space.space_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_space()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(space.download_image_space(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			space.update_lastkey_space()

async def scheduled_mmo(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_mmo = mmo.new_mmo()

		if(new_mmo):

			# парсим инфу о новой игре
			nfo = mmo.mmo_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_mmo()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(mmo.download_image_mmo(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			mmo.update_lastkey_mmo()


async def scheduled_mob(wait_for):
	markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
	markup_inline = types.InlineKeyboardMarkup()
	item_newsmob = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'mobgoogle_ru')
	item_newsmoby = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'mobyandex_ru')
	item_cancelmob = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'mobcancel_ru')
	markup_inline.add(item_newsmob,item_newsmoby,item_cancelmob)
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_mob = mob.new_mob()

		if(new_mob):

			# парсим инфу о новой игре
			nfo = mob.mob_info()

			# получаем список подписчиков ботаs
			subscriptions = db.get_subscriptions_mob()

			# отправляем всем новость
		
			for id in subscriptions:
				try:
					await bot.send_photo(
					id[1],
					open(mob.download_image_mob(nfo['image']), 'rb'),
					caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
					disable_notification = True
				)
				except: 
					print('Bot was blocked by the user!')
				# обновляем ключ
			mob.update_lastkey_mob()

@dp.message_handler(content_types = ['text'])
async def get_text(message):
	if message.text == 'Игры':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item1 = types.KeyboardButton('Общие игровые новости')
		item2 = types.KeyboardButton('Мобильные игры')
		item3 = types.KeyboardButton('Игровые скидки')
		item4 = types.KeyboardButton('Мморпг')
		item5 = types.KeyboardButton('Зарубежные игровые новости')
		item6 = types.KeyboardButton(text = 'Меню')
		item7 = types.KeyboardButton(text = 'Выход')
		markup_reply.add(item1,item2,item3,item4,item5,item6,item7)
		await message.answer("Выберите рассылку, которую хотите получать", reply_markup = markup_reply)

	if message.text == "Общие игровые новости":
		item1 = types.KeyboardButton(text = 'Подписаться на stopgame')
		item2 = types.KeyboardButton(text = 'Отписаться от stopgame')
		item3 = types.KeyboardButton(text = 'Последняя новость stopgame')
		item4 = types.KeyboardButton(text = 'Назад')
		item5 = types.KeyboardButton(text = 'Меню')
		item6 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5,item6)
		await message.answer("Список доступных тем на игровую тематику",reply_markup = markup_reply)

	if message.text == "Мобильные игры":
		item1 = types.KeyboardButton(text = 'Подписаться на мобильные игры')
		item2 = types.KeyboardButton(text = 'Отписаться от мобильные игры')
		item3 = types.KeyboardButton(text = 'Последняя новость мобильных игр')
		item4 = types.KeyboardButton(text = 'Назад')
		item5 = types.KeyboardButton(text = 'Меню')
		item6 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5,item6)
		await message.answer("Список доступных тем на игровую тематику",reply_markup = markup_reply)

	if message.text == "Игровые скидки":
		item1 = types.KeyboardButton(text = 'Подписаться на игровые скидки')
		item2 = types.KeyboardButton(text = 'Отписаться от игровых скидок')
		item3 = types.KeyboardButton(text = 'Последняя новость игровых скидок')
		item4 = types.KeyboardButton(text = 'Назад')
		item5 = types.KeyboardButton(text = 'Меню')
		item6 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5,item6)
		await message.answer("Список доступных тем на игровую тематику",reply_markup = markup_reply)

	if message.text == "Мморпг":
		item1 = types.KeyboardButton(text = 'Подписаться на Мморпг')
		item2 = types.KeyboardButton(text = 'Отписаться от Мморпг')
		item3 = types.KeyboardButton(text = 'Последняя новость Мморпг')
		item4 = types.KeyboardButton(text = 'Назад')
		item5 = types.KeyboardButton(text = 'Меню')
		item6 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5,item6)
		await message.answer("Список доступных тем на игровую тематику",reply_markup = markup_reply)

	if message.text == "Зарубежные игровые новости":
		item1 = types.KeyboardButton(text = 'Подписаться на зарубежные игровые новости')
		item2 = types.KeyboardButton(text = 'Отписаться от зарубежных игровых новостей')
		item3 = types.KeyboardButton(text = 'Последняя зарубежная новость')
		item4 = types.KeyboardButton(text = 'Назад')
		item5 = types.KeyboardButton(text = 'Меню')
		item6 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5,item6)
		await message.answer("Список доступных тем на игровую тематику",reply_markup = markup_reply)

	if message.text == "Аниме":
		item1 = types.KeyboardButton(text = 'Подписаться на Аниме')
		item2 = types.KeyboardButton(text = 'Отписаться от Аниме')
		item3 = types.KeyboardButton(text = 'Последняя Аниме новость')
		item4 = types.KeyboardButton(text = 'Меню')
		item5 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5)
		await message.answer("Выберите действие",reply_markup = markup_reply)

	if message.text == "Спорт":
		item1 = types.KeyboardButton(text = 'Подписаться на Спорт')
		item2 = types.KeyboardButton(text = 'Отписаться от Спорт')
		item3 = types.KeyboardButton(text = 'Последняя Спортивная новость')
		item4 = types.KeyboardButton(text = 'Меню')
		item5 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5)
		await message.answer("Выберите действие",reply_markup = markup_reply)

	if message.text == "Кино":
		item1 = types.KeyboardButton(text = 'Подписаться на Кино')
		item2 = types.KeyboardButton(text = 'Отписаться от Кино')
		item3 = types.KeyboardButton(text = 'Последняя Кино-новость')
		item4 = types.KeyboardButton(text = 'Меню')
		item5 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5)
		await message.answer("Выберите действие",reply_markup = markup_reply)

	if message.text == "Космос":
		item1 = types.KeyboardButton(text = 'Подписаться на Космос')
		item2 = types.KeyboardButton(text = 'Отписаться от Космоса')
		item3 = types.KeyboardButton(text = 'Последняя новость Космоса')
		item4 = types.KeyboardButton(text = 'Меню')
		item5 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5)
		await message.answer("Выберите действие",reply_markup = markup_reply)

	if message.text == "Гаджеты":
		item1 = types.KeyboardButton(text = 'Подписаться на Гаджеты')
		item2 = types.KeyboardButton(text = 'Отписаться от Гаджетов')
		item3 = types.KeyboardButton(text = 'Последняя новость Гаджетов')
		item4 = types.KeyboardButton(text = 'Меню')
		item5 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5)
		await message.answer("Выберите действие",reply_markup = markup_reply)

	if message.text == "Музыка":
		item1 = types.KeyboardButton(text = 'Подписаться на Музыку')
		item2 = types.KeyboardButton(text = 'Отписаться от Музыки')
		item3 = types.KeyboardButton(text = 'Последняя новость Музыки')
		item4 = types.KeyboardButton(text = 'Меню')
		item5 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2).add(item3).add(item4,item5)
		await message.answer("Выберите действие",reply_markup = markup_reply)

	if message.text == "Календарь":
		item1 = types.KeyboardButton(text = 'Получить события за сегодня')
		item2 = types.KeyboardButton(text = 'Меню')
		item3 = types.KeyboardButton(text = 'Выход')
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1).add(item2,item3)
		await message.answer("Выберите действие",reply_markup = markup_reply)

	if message.text == "Назад":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item1 = types.KeyboardButton('Общие игровые новости')
		item2 = types.KeyboardButton('Мобильные игры')
		item3 = types.KeyboardButton('Игровые скидки')
		item4 = types.KeyboardButton('Мморпг')
		item5 = types.KeyboardButton('Зарубежные игровые новости')
		item6 = types.KeyboardButton(text = 'Меню')
		item7 = types.KeyboardButton(text = 'Выход')
		markup_reply.add(item1,item2,item3,item4,item5,item6,item7)
		await message.answer("Выберите рассылку, которую хотите получать", reply_markup = markup_reply)

	if message.text == "Подписаться на stopgame":
		if(not db.subscriber_exists(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!\n\n ВНИМАНИЕ❗️❗️❗️\n\nМожет содержать изображения жестокости и насилия")

	if message.text == "Отписаться от stopgame":
		if(not db.subscriber_exists(message.from_user.id)):
			db.add_subscriber(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя новость stopgame":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = sg.game_info()

		await bot.send_photo(
			message.chat.id,
			open(sg.download_image(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)

	if message.text == "Подписаться на мобильные игры":
		if(not db.subscriber_exists_mob(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_mob(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_mob(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")

	if message.text == "Отписаться от мобильные игры":
		if(not db.subscriber_exists_mob(message.from_user.id)):
			db.add_subscriber_mob(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_mob(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя новость мобильных игр":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		markup_inline = types.InlineKeyboardMarkup()
		item_newsmob = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'mobgoogle_ru')
		item_newsmoby = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'mobyandex_ru')
		item_cancelmob = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'mobcancel_ru')
		markup_inline.add(item_newsmob,item_newsmoby,item_cancelmob)

		nfo = mob.mob_info()
		
		await bot.send_photo(
			message.chat.id,
			open(mob.download_image_mob(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'] , reply_markup = markup_inline,
			disable_notification = True
		)

	if message.text == "Подписаться на игровые скидки":
		if(not db.subscriber_exists_sale(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_sale(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_sale(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")

	if message.text == "Отписаться от игровых скидок":
		if(not db.subscriber_exists_sale(message.from_user.id)):
			db.add_subscriber_sale(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_sale(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя новость игровых скидок":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = sale.sale_info()

		await bot.send_photo(
			message.chat.id,
			open(sale.download_image_sale(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)

	if message.text == "Подписаться на Мморпг":
		if(not db.subscriber_exists_mmo(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_mmo(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_mmo(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")

	if message.text == "Отписаться от Мморпг":
		if(not db.subscriber_exists_mmo(message.from_user.id)):
			db.add_subscriber_mmo(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_mmo(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя новость Мморпг":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = mmo.mmo_info()

		await bot.send_photo(
			message.chat.id,
			open(mmo.download_image_mmo(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)

	if message.text == "Подписаться на зарубежные игровые новости":
		markup_inline = types.InlineKeyboardMarkup()
		if(not db.subscriber_exists_eng(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_eng(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_eng(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")


	if message.text == "Отписаться от зарубежных игровых новостей":
		if(not db.subscriber_exists_eng(message.from_user.id)):
			db.add_subscriber_eng(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_eng(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя зарубежная новость":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = engame.daily_info()
		markup_inline = types.InlineKeyboardMarkup()
		item_newsg = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'google_ru')
		item_newsy = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'yandex_ru')
		item_cancelr = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'cancel_ru')
		markup_inline.add(item_newsg,item_newsy,item_cancelr)
		await bot.send_photo(
			message.chat.id,
			open(engame.download_image_eng(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
			disable_notification = True
		)
		await message.edit_reply_markup(reply_markup=None)

	if message.text == "Подписаться на Аниме":
		if(not db.subscriber_exists_anime(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_anime(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_anime(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")

	if message.text == "Отписаться от Аниме":
		if(not db.subscriber_exists_anime(message.from_user.id)):
			db.add_subscriber_anime(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_anime(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя Аниме новость":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = anime.anime_info()

		await bot.send_photo(
			message.chat.id,
			open(anime.download_image_anime(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)

	if message.text == "Подписаться на Спорт":
		if(not db.subscriber_exists_sport(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_sport(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_sport(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")

	if message.text == "Отписаться от Спорт":
		if(not db.subscriber_exists_sport(message.from_user.id)):
			db.add_subscriber_sport(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_sport(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя Спортивная новость":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = sport.sport_info()

		await bot.send_photo(
			message.chat.id,
			open(sport.download_image_sport(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)

	if message.text == "Подписаться на Кино":
		if(not db.subscriber_exists_kino(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_kino(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_kino(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")

	if message.text == "Отписаться от Кино":
		if(not db.subscriber_exists_kino(message.from_user.id)):
			db.add_subscriber_kino(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_kino(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя Кино-новость":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# парсим инфу о новой игре
		nfo = kino.kino_info()

		await bot.send_photo(
			message.chat.id,
			open(kino.download_image_kino(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],
			disable_notification = True
		)

	if message.text == "Подписаться на Космос":
		markup_inline = types.InlineKeyboardMarkup()
		if(not db.subscriber_exists_space(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_space(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_space(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")


	if message.text == "Отписаться от Космоса":
		if(not db.subscriber_exists_space(message.from_user.id)):
			db.add_subscriber_space(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_space(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя новость Космоса":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = space.space_info()
		markup_inline = types.InlineKeyboardMarkup()
		item_newsg = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'sgoogle_ru')
		item_newsy = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'syandex_ru')
		item_cancelr = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'scancel_ru')
		markup_inline.add(item_newsg,item_newsy,item_cancelr)
		await bot.send_photo(
			message.chat.id,
			open(space.download_image_space(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
			disable_notification = True
		)
		await message.edit_reply_markup(reply_markup=None)

	if message.text == "Подписаться на Гаджеты":
		if(not db.subscriber_exists_tech(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_tech(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_tech(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")

	if message.text == "Отписаться от Гаджетов":
		if(not db.subscriber_exists_tech(message.from_user.id)):
			db.add_subscriber_tech(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_tech(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя новость Гаджетов":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		markup_inline = types.InlineKeyboardMarkup()
		item_newsgt = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'tgoogle_ru')
		item_newsyt = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'tyandex_ru')
		item_cancelrt = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'tcancel_ru')
		markup_inline.add(item_newsgt,item_newsyt,item_cancelrt)
		nfo = tech.tech_info()

		await bot.send_photo(
			message.chat.id,
			open(tech.download_image_tech(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'],reply_markup = markup_inline,
			disable_notification = True
		)

	if message.text == "Подписаться на Музыку":
		markup_inline = types.InlineKeyboardMarkup()
		if(not db.subscriber_exists_mus(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber_mus(message.from_user.id)
		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription_mus(message.from_user.id, True)
		await message.answer("Вы успешно подписались на рассылку!")


	if message.text == "Отписаться от Музыки":
		if(not db.subscriber_exists_mus(message.from_user.id)):
			db.add_subscriber_mus(message.from_user.id, False)
			await message.answer("Вы итак не подписаны.")
		else:
			db.update_subscription_mus(message.from_user.id, False)
			await message.answer("Вы успешно отписаны от рассылки.")

	if message.text == "Последняя новость Музыки":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = mus.mus_info()
		markup_inline = types.InlineKeyboardMarkup()
		item_newsg = types.InlineKeyboardButton(text = 'Google_translate',callback_data = 'mgoogle_ru')
		item_newsy = types.InlineKeyboardButton(text = 'Yandex_translate',callback_data = 'myandex_ru')
		item_cancelr = types.InlineKeyboardButton(text = 'Мне не нужен перевод!',callback_data = 'mcancel_ru')
		markup_inline.add(item_newsg,item_newsy,item_cancelr)
		await bot.send_photo(
			message.chat.id,
			open(mus.download_image_mus(nfo['image']), 'rb'),
			caption = nfo['title'] + "\n\n" + nfo['text'] + "\n\n" + nfo['link'], reply_markup = markup_inline,
			disable_notification = True
		)
		await message.edit_reply_markup(reply_markup=None)

	if message.text == "Получить события за сегодня":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		nfo = cd.calend_info()

		for i in range(len(nfo["title"])):
			await bot.send_photo(
				message.chat.id,
				open(cd.download_image_cal(nfo['image'][i].find('a').find('img').get('src')), 'rb'),
				caption = nfo['title'][i].find('a').get_text()+ " " + nfo['year'][i].get_text() + " год",
				disable_notification = True
			)
		await message.edit_reply_markup(reply_markup=None)

	if message.text == "Выход":
		reply_markup = types.ReplyKeyboardRemove()
		await bot.send_message(message.from_user.id,'По команде /menu вы можете вернуться в начальное окно',reply_markup=reply_markup)

	if message.text == "Меню":
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item1 = types.KeyboardButton('Игры')
		item2 = types.KeyboardButton('Аниме')
		item3 = types.KeyboardButton('Спорт')
		item4 = types.KeyboardButton('Кино')
		item5 = types.KeyboardButton('Космос')
		item6 = types.KeyboardButton('Гаджеты')
		item7 = types.KeyboardButton('Музыка')
		item8 = types.KeyboardButton('Календарь')
		item9 = types.KeyboardButton('Выход')
		markup_reply.add(item1,item2,item3,item4,item5,item6,item7,item8,item9)
		await bot.send_message(message.from_user.id,"Выберите интересующую вас тему", reply_markup = markup_reply)

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
	loop.create_task(scheduled_space(10))
	loop.create_task(scheduled_mmo(10))
	loop.create_task(scheduled_mob(10))
	executor.start_polling(dp, skip_updates=True)