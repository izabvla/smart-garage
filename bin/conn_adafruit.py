# Boilerplate adafruit connection
# Import Adafruit_IO library and create instance of REST client.
from Adafruit_IO import RequestError, Client, Feed

# Adafruit username and key
ADAFRUIT_IO_USERNAME = 'compiotgroup3'
ADAFRUIT_IO_KEY = 'aio_gpXs67Bn7HYZmTFj0t1Zuisebnv5'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Try to assign test to existing feed 'test'
try:
    test = aio.feeds('test')
except RequestError: # Doesn't exist, create new feed
    test_feed = Feed(name='test')
    test_feed = aio.create_feed(test_feed)

aio.send_data(test.key, 32)
