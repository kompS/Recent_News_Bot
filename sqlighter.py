import sqlite3

class SQLighter:

    def __init__(self, database):
        # Подключаемся к БД и сохраняем курсор соединения
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # db sub games

    def get_subscriptions(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))



    # db sub eng


    def get_subscriptions_eng(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_eng` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_eng(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_eng` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_eng(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_eng` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_eng(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_eng` SET `status` = ? WHERE `user_id` = ?", (status, user_id))


    # db sub anime

    def get_subscriptions_anime(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_anime` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_anime(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_anime` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_anime(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_anime` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_anime(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_anime` SET `status` = ? WHERE `user_id` = ?", (status, user_id))



    # db sub tech

    def get_subscriptions_tech(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_tech` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_tech(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_tech` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_tech(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_tech` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_tech(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_tech` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    # db sub sale

    def get_subscriptions_sale(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_sale` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_sale(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_sale` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_sale(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_sale` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_sale(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_sale` SET `status` = ? WHERE `user_id` = ?", (status, user_id))


    # db sub sport

    def get_subscriptions_sport(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_sport` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_sport(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_sport` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_sport(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_sport` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_sport(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_sport` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    # db sub kino

    def get_subscriptions_kino(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_kino` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_kino(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_kino` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_kino(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_kino` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_kino(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_kino` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    # db sub mus

    def get_subscriptions_mus(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_mus` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_mus(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_mus` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_mus(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_mus` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_mus(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_mus` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
    # Закрываем соединение с БД
        self.connection.close()

    # db sub spc

    def get_subscriptions_space(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_space` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_space(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_space` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_space(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_space` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_space(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_space` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
    # Закрываем соединение с БД
        self.connection.close()


    # db sub mmo
    def get_subscriptions_mmo(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_mmo` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_mmo(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_mmo` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_mmo(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_mmo` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_mmo(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_mmo` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
    # Закрываем соединение с БД
        self.connection.close()

    # db sub mob
    def get_subscriptions_mob(self, status = True):
        # Получаем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_mob` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists_mob(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions_mob` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber_mob(self, user_id, status = True):
        # Добавляем нового подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions_mob` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription_mob(self, user_id, status):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions_mob` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
    # Закрываем соединение с БД
        self.connection.close()