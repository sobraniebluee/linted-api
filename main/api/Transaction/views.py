from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with
from main.service.transaction_service import create_transaction_service, complete_transaction_service
from main.schemas.transaction_schema import TransactionSchema, CreateTransactionSchema
from main import docs

transaction = Blueprint('transactions', __name__)


@transaction.route('/create', methods=['POST'])
@jwt_required()
@use_kwargs(CreateTransactionSchema)
@marshal_with(TransactionSchema)
def create_transaction_for_advert(**kwargs):
    identity = get_jwt_identity()
    return create_transaction_service(id_user=identity, **kwargs)


@transaction.route('/complete/<int:id_transaction>', methods=['PUT'])
@jwt_required()
def complete_transaction_for_advert(id_transaction):
    identity = get_jwt_identity()
    return complete_transaction_service(id_transaction=id_transaction, id_buyer=identity)


docs.register(create_transaction_for_advert, blueprint='transactions')
docs.register(complete_transaction_for_advert, blueprint='transactions')
