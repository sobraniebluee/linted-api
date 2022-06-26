from datetime import timedelta


class Config:
    SECRET = '5d724b35-2ea4-4a58-b741-9f2c3056311d'
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = '5fa7bc58-8a03-4d32-b083-6392a11ee8b3'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_COOKIE_SECURE = False


class ConfigAWS:
    AWS_ENDPOINT = 'https://linted-storage.s3.eu-west-2.amazonaws.com'
    AWS_DEFAULT_AVATAR_PATH = '/avatars/default/default_avatar.png'
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_KEY = ''
    REGION = 'eu-west-2'
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024


class Const:
    ROOT_API_PATH = '/api/v1'
    FOLLOW = 'follow'
    UNFOLLOW = 'unfollow'
    MAX_LENGTH_REVIEW = 128
    FOLLOWERS = 'followers'
    FOLlOWS = 'follows'
    MAX_MEMBER_PER_PAGE = 40
    PAGE_COUNT_ADVERT = 24
    MAX_COUNT_FILES_FOR_ADVERT = 8
    MAX_PRICE = 1000000
    OFFER_PRICE_PERCENT = 0.5
    MAX_COUNT_OFFERS_PER_DAY = 7
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'


DB = "mysql+pymysql://root@localhost/linted?charset=utf8mb4"
