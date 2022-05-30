from main.models.Adverts.adverts_model import AdvertCondition


def get_advert_condition_service():
    try:
        adverts_condition = AdvertCondition.query.all()
        return adverts_condition, 200
    except Exception as e:
        return {'message': 'Server Error' + str(e)}, 500
