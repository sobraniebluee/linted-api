from datetime import timedelta


class Config:
    ROOT_API_PATH = '/api/v.1.0'
    JWT_SECRET_KEY = '5fa7bc58-8a03-4d32-b083-6392a11ee8b3'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    MAX_COUNT_FILES_FOR_ADVERT = 8
    ADVERT_IMAGE = 'advert_image'
    AVATAR_IMAGE = 'avatar_image'
    PAGE_COUNT_ADVERT = 24
    MAX_PRICE = 1000000
    OFFER_PRICE_PERCENT = 0.5
    MAX_COUNT_OFFERS_PER_DAY = 7


class ConfigAWS:
    AWS_ENDPOINT = 'https://linted-storage.s3.eu-west-2.amazonaws.com'
    AWS_DEFAULT_AVATAR_PATH = '/avatars/default/default_avatar.png'
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_KEY = ''
    REGION = 'eu-west-2'
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024


class Const:
    FOLLOW = 'follow'
    UNFOLLOW = 'unfollow'
    MAX_LENGTH_REVIEW = 128
    FOLLOWERS = 'followers'
    FOLlOWS = 'follows'


advert_condition_items = [
    {
        "id": 100,
        "name": "New with tags",
        "description": "A brand-new, unused item with tags attached or in the original packaging."
    },
    {
        "id": 200,
        "name": "New without tags",
        "description": "A brand-new, unused item without tags or original packaging."
    },
    {
        "id": 300,
        "name": "Very good",
        "description": "A lightly used item that may have slight imperfections, but still looks great. Include photos and descriptions of any flaws in your listing."
    },
    {
        "id": 400,
        "name": "Good",
        "description": "A used item that may show imperfections and signs of wear. Include photos and descriptions of flaws in your listing."
    },
    {
        "id": 500,
        "name": "Satisfactory",
        "description": "A frequently used item with imperfections and signs of wear. Include photos and descriptions of flaws in your listing."
    }
]

DB = "mysql+pymysql://root@localhost/linted?charset=utf8mb4"
