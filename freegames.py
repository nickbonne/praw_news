
import re
import sqlite3

from datetime import datetime
from nltk import word_tokenize


class Script():


    def  __init__(self, reddit):

        self.reddit = reddit
        self.conn = sqlite3.connect('bot_database.db')
        self.c = self.conn.cursor()


    def get_submissions(self):

        submissions = []

        for submission in self.reddit.subreddit('gamedeals').new(limit=50):

            submissions.append([submission.title,
                                submission.created_utc,
                                submission.permalink,
                                submission.id,
                                submission.score,
                                submission.url,
                                str(submission.link_flair_text)])

        return submissions


    def check_db(self, submissions):

        self.c.execute('SELECT submission_id from gamesBOT')
        id_list = str(self.c.fetchall())

        return [x for x in submissions if x[3] not in id_list]


    def add_db(self, submissions):

        for submission in submissions:

            t_stmp = datetime.fromtimestamp(submission[1]).strftime('%Y-%m-%d %H:%M:%S')

            self.c.execute('''INSERT INTO gamesBot(post_title,
                                                   time_stamp,
                                                   permalink,
                                                   submission_id,
                                                   upvotes)
                               VALUES (?,?,?,?,?)''',
                           (submission[0],
                            t_stmp,
                            submission[2],
                            submission[3],
                            submission[4]))

        self.conn.commit()
        self.conn.close()


    # Returns submissions with 'free' anywhere in the title
    def free_title(submissions):

        return [x for x in submissions if re.findall(r'\bfree\b', x[0].lower())]

    # Returns submissions without flair 'console'
    def no_peasntry(submissions):

        peasntry = ['xbox', 'xb1', 'psn', 'ps+', 'ps4', 'ps pro',
                    'nintendo', 'xbl', 'wii', 'wiiu']

        submissions = [x for x in submissions if x[6].lower() != 'console']

        return [x for x in submissions if not
                any(i in x[0].lower() for i in peasntry)]

    # Returns submissions without flair 'physical'
    def not_physical(submissions):

        return [x for x in submissions if x[6].lower() != 'physical']

    # if symbol of currency is in the title, make sure it's cost is 0.00
    def currency_title(submissions):

        money = ['$', '£', '€']
        passing = []
        
        for i, submission in enumerate(submissions):

            if any(symbol in submission[0] for symbol in money):

                hits = re.search(r'(?<=[\$\£\€])([0-9]+(\.[0-9]{0,2})?)', submission[0])

                if hits:

                    if float(hits.group(1)) > 0:

                        pass

            else:

                passing.append(submission)

        return passing

    # removes submissions with 'buy' or 'purchase' in title
    def no_buy(submissions):

        return [x for x in submissions if not
                any(i in x[0].lower() for i in ['buy', 'purchase'])]

    # DRM-free removed
    def drm_free(submissions):

        return [x for x in submissions if not re.findall('drm free', x[0].lower())]

    # removes submissions with percentage not equal to 100%
    def not_100(submissions):

        return [x for x in submissions if not re.findall(r'\b\d{1,2}%', x[0])]
