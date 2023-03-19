from datetime import datetime
from banking.models import *


def update_bank_balance():
    # Retrieve all users from the database
    # users = User.objects.all()
    account = CreditCardDetail.objects.get(AccountNumber='0000-0000-0000-0001')
    account.balance+=1
   