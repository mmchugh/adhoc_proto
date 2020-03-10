import parser

user_id_to_check = 2456938384156277127
transactions = parser.TransactionRecordsData('roster_proto/txnlog.dat')

total_credits = 0.0
total_debits = 0.0
total_autopays_started = 0
total_autopays_ended = 0
user_balance = 0.0


for record in transactions.records:
    if record.record_name == "Credit":
        total_credits += record.amount
        if record.user_id == user_id_to_check:
            user_balance += record.amount

    elif record.record_name == "Debit":
        total_debits += record.amount
        if record.user_id == user_id_to_check:
            user_balance -= record.amount

    elif record.record_name == "StartAutopay":
        total_autopays_started += 1

    elif record.record_name == "EndAutopay":
        total_autopays_ended += 1


print("total credit amount={:.2f}".format(total_credits))
print("total debit amount={:.2f}".format(total_debits))
print("autopays started={}".format(total_autopays_started))
print("autopays ended={}".format(total_autopays_ended))
print("balance for user {}={:.2f}".format(user_id_to_check, user_balance))
