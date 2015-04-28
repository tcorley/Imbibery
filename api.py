from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import urllib.request as r

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str)
parser.add_argument('restaurant', type=str)

class Review(Resource):
    def post(self):
        args = parser.parse_args()
        user_id = args['user_id']
        today = datetime.now()
        biz = args['restaurant']

        # logic
        url = 'http://www.yelp.com/user_details?userid={}'.format(user_id)
        page = r.urlopen(url)
        soup = bs(page.read())

        reviews = soup.find('ul', 'reviews')

        if reviews:
            reviews_stripped = [reviews.contents[i] for i in range(1,len(reviews.contents)-1, 2)]

            for review in reviews_stripped:
                # Get the business
                key = review.find_all('a', href=True)[0]['href'][5:]
                if key == biz:
                    print(key, biz)
                    # Get the date
                    date = review.find_all('span','rating-qualifier')[0].contents[0].strip()
                    print(datetime.now(), datetime.strptime(date, '%m/%d/%Y'))
                    print((datetime.now() - datetime.strptime(date, '%m/%d/%Y')),timedelta(1))
                    # if (datetime.now() - datetime.strptime(date, '%m/%d/%Y')) < timedelta(1):
                    if True:
                        print('got in')
                        result = dict()
                        # Get the user's rating
                        result['rating'] = review.find_all('i')[0]['class'][1][-1]
                        # Finally get the review
                        result['review'] = "".join(str(i) for i in review.find_all('p')[0].contents).replace("<br>","").replace("</br>","")
                        return result, 200

        return {'result':'review not found'}, 200

class User(Resource):
    def get(self, user_id):
        url = 'http://www.yelp.com/user_details?userid={}'.format(user_id)
        page = r.urlopen(url)
        soup = bs(page.read())

        result = dict()
        result["imageURL"] = soup.findAll(id="main_user_photo_in_about_user_column")[0]['src'].replace('ms.jpg','o.jpg')
        result["name"] = soup.h1.contents[0].strip().replace("'s Profile", "")
        result["userid"] = user_id
        return result, 200



api.add_resource(Review, '/reviewcheck')
api.add_resource(User, '/user/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)