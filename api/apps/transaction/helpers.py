import re
from datetime import datetime

from rest_framework.exceptions import ValidationError


def process_transaction_file(ofx_data, account_map=None):
    parsed_data = []
    for account in ofx_data.accounts:
        transaction_list = account.statement.transactions
        account_data = {
            "id": account.account_id,
            "kind": account.account_type,
            "transactions": [],
        }

        for transaction in transaction_list:

            if not validate_amount_format(transaction.amount):
                raise ValueError("Invalid amount format")
            if not validate_payee_length(transaction.payee):
                raise ValueError("Description too long")
            if not validate_currency_length(account.statement.currency):
                raise ValueError("Currency code incorrect")

            transaction_data = {
                "date": datetime.date(transaction.date),
                "amount": transaction.amount,
                "description": transaction.payee,
                "currency_code": account.statement.currency,
            }
            if account_map:
                transaction_data["account"] = account_map[account.account_id]

            account_data["transactions"].append(transaction_data)
        parsed_data.append(account_data)

    return parsed_data


def validate_amount_format(amount):
    amount_regex = r"^-?\d+(\.\d{1,2})?$"
    return bool(re.match(amount_regex, str(amount)))


def validate_payee_length(payee):
    return len(payee) <= 255


def validate_currency_length(currency_code):
    return len(currency_code) == 3


def validate_ofx_file(fpath):
    first_line = fpath.readline().decode()
    if not first_line.startswith("OFXHEADER"):
        raise ValidationError("File must be OFX format")
