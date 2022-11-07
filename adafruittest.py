# Import Adafruit_IO library and create instance of REST client.

from Adafruit_IO import RequestError, Client, Feed

ADAFRUIT_IO_USERNAME = ''
ADAFRUIT_IO_KEY = ''

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try:
    test = aio.feeds('test')
except RequestError: # Doesn't exist, create new feed
    test_feed = Feed(name='test')
    test_feed = aio.create_feed(feed)

aio.send_data(test.key, 42)