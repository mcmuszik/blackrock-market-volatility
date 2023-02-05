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
            if val is None:
                self.__setattr__(key, contents.get(key))

    def to_dict(self) -> dict:
        self.__dict__
        return {'id': self.__dict__.get('id'),
                'first_name': self.__dict__.get('first_name'),
                'last_name': self.__dict__.get('last_name'),
                'birth_date': self.__dict__.get('birth_date'),
                'stock_transactions': [t.to_dict() for t in self.stock_transactions]
                }

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

    def get_transactions_df(self):
        return pd.DataFrame(self.stock_transactions)

    
    # @property
    # def portfolio_value(self):

if __name__ == "__main__":
    ID = '1b57fe1d-5fd5-4a13-b8e3-82bfbb1e8c42'
    user = User(ID)

    stock_prices = pd.read_gbq(f'select * from {DATASET}.prices')
    
    transactions_df = pd.DataFrame(user.stock_transactions)
    transactions_df = pd.concat([
        transactions_df,
        pd.DataFrame(Transaction('DG', 50, 'sell', dt.datetime(2023, 1, 1)).to_dict(), index=[0])
    ], axis=0)
    transactions_df= pd.concat([
        transactions_df,
        pd.DataFrame(Transaction('DG', 50, 'sell', dt.datetime(2023, 2, 1)).to_dict(), index=[0])
    ], axis=0)

    transactions_df.sort_values('ticker', 'datetime')
    holding_windows = transactions_df.groupby('ticker')





    purchases = transactions_df.query('is_purchase == "buy"')

    purchases.assign(
        Date=purchases.datetime.dt.strftime('%Y-%m-%d')
        ).merge(
            transactions_df
        )

    def delete_all_users():
        """
        WARNING: DO NOT CALL THIS IN PRODUCTION. DEV FUNCTION ONLY.
        """
        users_collection = db.collection('users').stream()
        for user in users_collection:
            user_document = db.collection('users').document(user.id)
            user_document.delete()


    ## Create New User
    stock_transactions = [
        Transaction('AAPL', 10, 'buy', dt.datetime(2022, 1, 1)),
        Transaction('FB', 20, 'buy', dt.datetime(2021, 6, 30)),
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
    new_user.id

