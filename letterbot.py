import letterboxd as lb
import json
import os


class LetterBot:
    def __init__(self, id:str):
        '''Creates a letterbot instance.
        :param id: Letterboxd account id to average followers reviews from.'''
        self.lbxd = self.init_letterboxd()
        self.id = id 

    def init_letterboxd(self) -> lb.Letterboxd:
        if os.getenv('LBXD_API_KEY') and not os.getenv('LBXD_API_SECRET'):
            return lb.new()

        try:
            with open('secrets.json') as secrets_json:
                secrets = json.load(secrets_json)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "secrets.json MUST be in same dir as this file!"
                + e.with_traceback()
            )

        if ('letterboxd' not in secrets
            or 'key' not in secrets['letterboxd']
            or 'secret' not in secrets['letterboxd']):

            raise KeyError(
                "secrets.json must have the fields letterboxd.key "
                "and letterboxd.secret. Or LBXD_API_KEY and " 
                "LBXD_API_SECRET env varaibles must be set"
            )

        lbxd = lb.new(
                api_base='https://api.letterboxd.com/api/v0',
                api_key=secrets['letterboxd']['key'],
                api_secret=secrets['letterboxd']['secret']
            )

        return lbxd
        

    def get_rating(self, film_id:str) -> tuple[float, int]:
        '''Returns the average review in float form of all users the current bot
        follows, and the total number of reviews averaged.'''
        if type(film_id) != str:
            raise TypeError("film_lid must be a string.")

        review_sum = 0.0
        total_reviews = 0
        cursor = None
        has_next = True

        film = self.lbxd.film(film_id=film_id)
        film_name = film.details()['name']

        while has_next:
            member_film_relationships_request = {
                "cursor": cursor,
                "perPage": 100,
                "member": self.id,
                "memberRelationship": "IsFollowing",
                "filmRelationship": "Rated",
            }

            member_film_relationships_response = film.members(
                member_film_relationships_request=member_film_relationships_request
            )


            for item in member_film_relationships_response['items']:
                if 'rating' in item['relationship']:
                    review_sum += float(item['relationship']['rating'])
                    total_reviews += 1

            if 'next' not in member_film_relationships_response:
                has_next = False
            else:
                cursor = member_film_relationships_request['next']

        # Avoid divide by 0 errors.
        if total_reviews == 0:
            return 0, 0, film_name

        rating = round((review_sum / total_reviews), 2)
        return rating, total_reviews, film_name