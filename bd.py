import sqlite3


class BotDB:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_reminder(self, name, desrp, portrait, topic, type):
        with self.connection:
            return self.cursor.execute("INSERT INTO `personality` (`name`, `desrp`, `portrait`, `topic`, `type`) "
                                       "VALUES(?,?,?,?,?)", (name, desrp, portrait, topic, type))

    def get_list(self, topic, type, photo):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `personality` WHERE `topic` = ? AND `type` = ? AND "
                                         "`portrait` != ?",
                                         (topic, type, photo))
            return result

    def get_list_all(self, photo):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `personality` WHERE `portrait` != ?",
                                         (photo,))
            return result

    def get_list_notype(self, topic, photo):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `personality` WHERE `topic` = ? AND `portrait` != ?",
                                         (topic, photo))
            return result

    def get_list_notopic(self, type, photo):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `personality` WHERE `type` = ? AND `portrait` != ?",
                                         (type, photo))
            return result

    def add_date(self, name, date, topic):
        with self.connection:
            return self.cursor.execute("INSERT INTO `dates` (`name`, `date`, `topic`) "
                                       "VALUES(?,?,?)", (name, date, topic))

    def get_dates(self, topic):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `dates` WHERE `topic` = ?",
                                         (topic,))
            return result

    def get_dates_all(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `dates`",
                                         ())
            return result

    def close(self):
        self.connection.close()
