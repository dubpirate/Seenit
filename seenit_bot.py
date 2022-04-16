import praw

from letterbot import LetterBot

class SeenitBot:

    ERR_MSG = "Sorry, I can't seem find that film on letterboxd. Please double check the share link and try again."
    COMMENT_RATING = "{subreddit}'s Rating of {name} is {stars} / 5 Stars (based on {total_reviews} reviews)."
    NO_REVIEWS = "No-one from {subreddit} has rated {name} yet."

    def __init__(self, bot_name, subreddit, bot_lid=None):
        self.bot_name = bot_name
        self.bot = praw.Reddit(bot_name)
        self.subreddit = subreddit
        if bot_lid is None:
            self.bot_lid = "IJkp"

        self.last_resolved = None

    def handle_mention(self, mention:praw.models.Comment) -> None:
        '''Prints an appropriate response to a mention.
        
        Parameters:
            mention (praw.models.Comment) The comment that mentions this bot.
        '''

        match_string = "boxd.it/"

        if match_string in mention.body:
            index = mention.body.index(match_string)
            film_url = mention.body[index:].split("]")[0].split(" ")[0]
            film_id = film_url.split('/')[-1]

            try:
                lba = LetterBot(self.bot_lid)
                score, total_reviews, film_name = lba.get_rating(
                    film_id=film_id
                )

                if total_reviews == 0:
                    mention.reply(self.NO_REVIEWS.format(
                        subreddit=self.subreddit,
                        name=film_name
                    ))

                else:
                    mention.reply(self.COMMENT_RATING.format(
                        subreddit=self.subreddit,
                        name=film_name,
                        stars=score, # maybe round this.
                        total_reviews=total_reviews,
                    ))

            except Exception:
                mention.reply(self.ERR_MSG)

    def scan_mentions(self) -> None:
        '''Scans most recent mentions of the given bot, replys to review
        requests.
        '''
        mentions = self.bot.inbox.mentions(limit=25)
        first = True
        for mention in mentions:
            if first:
                top_resolved = mention.id
                first = False

            if mention.id == self.last_resolved:
                break
            
            self.handle_mention(mention)

        self.last_resolved = top_resolved