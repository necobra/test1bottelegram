import sqlite3


class BotDB:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_topics(self, subject_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `topics` WHERE `subject_id` = ?",
                                         (subject_id,))
            return result.fetchall()

    def get_topic(self, topic, subject_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `topics` WHERE `name` = ? AND `subject_id` = ?",
                                         (topic, subject_id))
            return result.fetchall()

    def get_topic_by_id(self, topic_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `topics` WHERE `name` = ?",
                                         (topic_id,))
            return result.fetchall()

    def get_pers(self, topic):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `pers` WHERE `topic_id` = ?",
                                         (topic,))
            return result.fetchall()

    def get_photos(self, topic):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `photos` WHERE `topic_id` = ?",
                                         (topic,))
            return result.fetchall()

    def get_dates(self, topic):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `dates` WHERE `topic_id` = ?",
                                         (topic,))
            return result.fetchall()

    def get_answer(self, q_type, q_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `{q_type}` WHERE `id` = ?",
                                         (q_id,))
            return result.fetchall()

    def add_topic(self, name, subject_id, priot):
        with self.connection:
            return self.cursor.execute("INSERT INTO `topics` (`name`, `subject_id`, `priority`) "
                                       "VALUES(?,?,?)", (name, subject_id, priot))

    def update_topic_priot(self, topic_id, new_priot):
        with self.connection:
            return self.cursor.execute("UPDATE `topics` SET `priority` = ? WHERE `id` = ?",
                                       (new_priot, topic_id))

    def add_pers(self, name, descrp, topic_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `pers` (`ans`, `q`, `topic_id`) "
                                       "VALUES(?,?,?)", (name, descrp, topic_id))

    def add_photo(self, name, url, topic_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `photos` (`ans`, `q`, `topic_id`) "
                                       "VALUES(?,?,?)", (name, url, topic_id))

    def add_date(self, name, date, topic_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `dates` (`q`, `ans`, `topic_id`) "
                                       "VALUES(?,?,?)", (name, date, topic_id))

    def update_q_topic(self, t, q_id, new_topic):
        with self.connection:
            return self.cursor.execute(f"UPDATE `{t}` SET `topic_id` = ? WHERE `id` = ?",
                                       (new_topic, q_id))

    def update_q_q(self, t, q_id, new_q):
        with self.connection:
            return self.cursor.execute(f"UPDATE `{t}` SET `q` = ? WHERE `id` = ?",
                                       (new_q, q_id))

    def update_q_ans(self, t, q_id, new_ans):
        with self.connection:
            return self.cursor.execute(f"UPDATE `{t}` SET `ans` = ? WHERE `id` = ?",
                                       (new_ans, q_id))

    def get_questions(self, topic):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `questions` WHERE `topic_id` = ?",
                                         (topic,))
            return result.fetchall()

    def add_question(self, ans, q, topic_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `questions` (`ans`, `q`, `topic_id`) "
                                       "VALUES(?,?,?)", (ans, q, topic_id))

    def get_all_questions(self, t):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `{t}`",
                                         ())
            return result.fetchall()

    def close(self):
        self.connection.close()
