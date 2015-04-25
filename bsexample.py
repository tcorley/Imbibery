from bs4 import BeautifulSoup as bs
import urllib.request as r

url = "http://www.yelp.com/user_details?userid=wHvO5kK43yjqkcQ4HdtNAQ"
page = r.urlopen(url)
soup = bs(page.read())


reviews = soup.find('ul', 'reviews')

if reviews:
    reviews_stripped = [reviews.contents[i] for i in range(1,len(reviews.contents)-1, 2)]

    result = dict()

    for review in reviews_stripped:

        # Get the business
        key = review.find_all('a', href=True)[0]['href'][5:]
        result[key] = dict()

        # Get the user's rating
        result[key]['rating'] = review.find_all('i')[0]['class'][1][-1]

        # Get the date
        result[key]['date'] = review.find_all('span','rating-qualifier')[0].contents[0].strip()

        # Finally get the review
        result[key]['review'] = "".join(str(i) for i in re.find_all('p')[0].contents).replace("<br>","").replace("</br>","")

    print(result)

else:
    print('no reviews found')