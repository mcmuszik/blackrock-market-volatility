import uuid
import datetime as dt
import pandas as pd
from dataclasses import dataclass, field
from typing import List
from google.oauth2 import service_account
from google.cloud import firestore

CREDENTIALS = service_account.Credentials.from_service_account_file('uga-hacks-2023-mv-660b14c32eea.json')

db = firestore.Client(credentials=CREDENTIALS)


def uuid_str():
    return str(uuid.uuid4())


@dataclass
class Transaction:
    ticker: str
    quantity: int
    is_purchase: bool
    datetime: dt.datetime = field(default_factory=dt.datetime.now)
    id: str = field(default_factory=uuid_str)

    def to_dict(self):
        return self.__dict__


@dataclass
class User:
    id: str = field(default_factory=uuid_str)
    first_name: str = None
    last_name: str = None
    birth_date: str = None
    stock_transactions: List[Transaction] = None

    def __post_init__(self):
        self.document_ref = db.collection('users').document(self.id)
        if None not in self.__dict__.values():
            return
        #If any fields are empty, fill them with the saved data
        contents = self.document_ref.get()
        for key, val in self.__dict__.items():
            print(key)
            if val is None:
                self.__setattr__(key, contents.get(key))

    def create_user(self) -> str:
        self.document_ref.set(self.to_dict())
        return 'User created successfully'

    def update_transactions(self, transactions=List[Transaction]) -> str:
        transactions_dicts = [t.to_dict() for t in stock_transactions]
        self.document_ref.update(
            {'transactions': firestore.ArrayUnion(transactions_dicts)}
            )
        return 'Updated successfully'

    def delete_user(self) -> str:
        self.document_ref.delete()
        return 'Deleted successfully'

    def to_dict(self) -> dict:
        return {'id': self.__dict__.get('id'),
                'first_name': self.__dict__.get('first_name'),
                'last_name': self.__dict__.get('last_name'),
                'birth_date': self.__dict__.get('birth_date'),
                'stock_transactions': [t.to_dict() for t in self.stock_transactions]
                }

    # @property
    # def portfolio_value(self):

if __name__ == "__main__":
    ID = '6efcb234-fcb5-45fb-90e2-6136f46a86b4'

    ## Create New User
    stock_transactions = [
        Transaction('QQQ', 10, 'buy', dt.datetime(2022, 1, 1)),
        Transaction('SPY', 20, 'buy', dt.datetime(2021, 6, 30)),
        Transaction('AMZN', 1, 'buy', dt.datetime(2021, 12, 31))
    ]

    new_user = User(
        first_name='Marc',
        last_name='Muszik',
        birth_date=dt.datetime(1998, 5, 7),
        stock_transactions=stock_transactions
        )

    new_user.create_user()

    stock_transactions = [
        Transaction('DG', 100, 'buy', dt.datetime(2022, 1, 1)),
        Transaction('FHN', 30, 'buy', dt.datetime(2021, 6, 30)),
        Transaction('KR', 15, 'buy', dt.datetime(2021, 12, 31))
    ]

    new_user = User(
        first_name='Hunter',
        last_name='Black',
        birth_date=dt.datetime(1997, 7, 8),
        stock_transactions=stock_transactions
        )

    new_user.create_user()

