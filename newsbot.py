
import os
import re
import praw
import time
import sqlite3
import freegames

from datetime import datetime
from nltk import word_tokenize


def main():

    message = ''
    error_count = 0

    while message != 'sent':

        if error_count == 5:

            break

        try:

            reddit_id = os.environ['REDDIT_ID']
            reddit_secret = os.environ['REDDIT_SECRET']
            reddit_password = os.environ['REDDIT_KEY']
            user = 'nbonneBOT'
            user_agent = 'by u/prgrmr_noob'

            reddit = praw.Reddit(client_id=reddit_id,
                              client_secret=reddit_secret,
                              password=reddit_password,
                              user_agent=user_agent,
                              username=user)  

            usr_lst = ['nbonne', 'prgrmr_noob', 'B_ongfunk']

            news = Scripts.us_news(Scripts(reddit))
            world_news = Scripts.world_news(Scripts(reddit))
            politics = Scripts.politics(Scripts(reddit))
            games = Scripts.games(Scripts(reddit))

            if news != ValueError:

                message = message + '**US News Report**' + '\n\n\n\n' + \
                    str(news) + '\n\n\n\n'

            if world_news != ValueError:
                message = message + '**World News Report**' + '\n\n\n\n' + \
                    str(world_news)

            if politics != ValueError:

                message = message + "**Politics Report**" + '\n\n\n\n' + \
                    str(politics) + '\n\n\n\n'

            if games != ValueError:

                message = message + "**Free Game(s)!**" + '\n\n\n\n' + \
                    str(games) + '\n\n\n\n'

            if message != '':

                for usr in usr_lst:

                    reddit.redditor(usr).message('Report', message)

                message = 'sent'

            else:

                for usr in usr_lst:

                    reddit.redditor(usr).message('Report', '__No rising stories.__')
                    
                message = 'sent'

        except Exception as e:

            print('Error:' + '\n' + str(e) + '\n')
            error_count += 1

    return


class Scripts():

    def __init__(self, reddit):

        self.reddit = reddit


    def us_news(self):

        conn = sqlite3.connect('bot_database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS
                     usNewsBot(post_title TEXT,
                              time_stamp INTEGER,
                              permalink TEXT,
                              submission_id TEXT,
                              upvotes INTEGER)''')

        article_list = []
        c.execute('SELECT submission_id FROM usNewsBot')
        id_list =[x[0] for x in c.fetchall()]

        for submission in self.reddit.subreddit('news').new(limit=100):

            post_title = submission.title
            t_stmp = submission.created_utc
            d_stmp = datetime.fromtimestamp(t_stmp).strftime('%Y-%m-%d %H:%M:%S')
            permalink = str(submission.permalink)
            submission_id = str(submission.id)
            upvotes = int(submission.score)

            if t_stmp > (time.time() - 10800):

              if submission.score > 300:

                  if submission.id not in id_list:

                      c.execute('''INSERT INTO usNewsBot(post_title,
                                                         time_stamp,
                                                         permalink,
                                                         submission_id,
                                                         upvotes)
                               VALUES (?,?,?,?,?)''',
                                (post_title, d_stmp,
                                 permalink, submission_id, upvotes))

                      article_message = ['[__' + str(upvotes) + '__] ' + '[' + submission.title + '] \
                                (' + permalink + ')' + '\n\n', upvotes]

                      article_list.append(article_message)

        conn.commit()

        if len(article_list) == 0:
            conn.close()
            return ValueError

        if len(article_list) > 0:

            conn.close()
            message = sorted(article_list, key=lambda x: x[1], reverse=True)

            return (' ').join([x[0] for x in message])

        else:
            conn.close()
            return


    def world_news(self):

        conn = sqlite3.connect('bot_database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS
                     worldNewsBot(post_title TEXT,
                              time_stamp INTEGER,
                              permalink TEXT,
                              submission_id TEXT,
                              upvotes INTEGER)''')

        article_list = []
        c.execute('SELECT submission_id FROM worldNewsBot')
        id_list = [x[0] for x in c.fetchall()]

        for submission in self.reddit.subreddit('worldnews').new(limit=100):

            post_title = submission.title
            post_title = submission.title
            t_stmp = submission.created_utc
            d_stmp = datetime.fromtimestamp(t_stmp).strftime('%Y-%m-%d %H:%M:%S')
            permalink = str(submission.permalink)
            submission_id = str(submission.id)
            upvotes = int(submission.score)

            if t_stmp > (time.time() - 10800):

              if submission.score > 300:

                  if submission.id not in id_list:

                      c.execute('''INSERT INTO worldNewsBot(post_title,
                                                            time_stamp,
                                                            permalink,
                                                            submission_id,
                                                            upvotes)
                                   VALUES (?,?,?,?,?)''',
                                (post_title, d_stmp,
                                 permalink, submission_id, upvotes))

                      article_message = ['[__' + str(upvotes) + '__] ' + '[' + submission.title + '] \
                                (' + permalink + ')' + '\n\n', upvotes]

                      article_list.append(article_message)

        conn.commit()

        if len(article_list) == 0:
            conn.close()
            return ValueError

        if len(article_list) > 0:

            conn.close()
            message = sorted(article_list, key=lambda x: x[1], reverse=True)

            return (' ').join([x[0] for x in message])

        else:

            conn.close()
            return

    
    def politics(self):

        conn = sqlite3.connect('bot_database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS
                     politicsBot(post_title TEXT,
                              time_stamp INTEGER,
                              permalink TEXT,
                              submission_id TEXT,
                              upvotes INTEGER)''')

        article_list = []
        c.execute('SELECT submission_id FROM politicsBot')
        id_list = str(c.fetchall())

        for submission in self.reddit.subreddit('politics').new(limit=100):

            post_title = submission.title
            t_stmp = submission.created_utc
            d_stmp = datetime.fromtimestamp(t_stmp).strftime('%Y-%m-%d %H:%M:%S')
            permalink = str(submission.permalink)
            submission_id = str(submission.id)
            upvotes = int(submission.score)

            if t_stmp > (time.time() - 10800):

              if submission.score > 600:

                  if submission.id not in id_list:

                      c.execute('''INSERT INTO politicsBot(post_title,
                                                            time_stamp,
                                                            permalink,
                                                            submission_id,
                                                            upvotes)
                                   VALUES (?,?,?,?,?)''',
                                (post_title, d_stmp,
                                 permalink, submission_id, upvotes))

                      article_message = ['[__' + str(upvotes) + '__] ' + '[' + submission.title + '] \
                                (' + permalink + ')' + '\n\n', upvotes]

                      article_list.append(article_message)

        conn.commit()

        if len(article_list) == 0:
            conn.close()
            return ValueError

        if len(article_list) > 0:

            conn.close()
            message = sorted(article_list, key=lambda x: x[1], reverse=True)

            return (' ').join([x[0] for x in message])

        else:
            conn.close()
            return       


    def games(self):

        message = []

        reddit = self.reddit
        games = freegames.Script(reddit).get_submissions()
        games = freegames.Script.free_title(games)
        games = freegames.Script.check_db(freegames.Script(reddit), games)
        games = freegames.Script.no_buy(games)
        games = freegames.Script.not_100(games)
        games = freegames.Script.no_peasntry(games)
        games = freegames.Script.not_physical(games)
        games = freegames.Script.currency_title(games)

        freegames.Script.add_db(freegames.Script(reddit), games)

        if len(games) == 0:

            return ValueError

        elif len(games) > 0:

            for game in games:

                game_str = ['[__' + str(game[4]) + '__] ' + '[' + game[0] + '] \
                                    (' + game[2] + ')' + '\n\n']

                message.append(game_str)

            message = (' ').join([str(x[0]) for x in message])

            return message


if __name__ == '__main__':

    main()
