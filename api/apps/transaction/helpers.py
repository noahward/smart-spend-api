from datetime import datetime


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
