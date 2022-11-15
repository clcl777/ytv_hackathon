from pykintone import model
from setting import answer_app

# from answer import get_answers


def get_answer_rate(question_id):
    answer_number1 = answer_app.select(
        "question_id = {0} and content = 1".format(question_id)
    )
    answer_number2 = answer_app.select(
        "question_id = {0} and content = 2".format(question_id)
    )
    answer_number3 = answer_app.select(
        "question_id = {0} and content = 3".format(question_id)
    )
    answer_number4 = answer_app.select(
        "question_id = {0} and content = 4".format(question_id)
    )
    answer_number = answer_app.select()

    records1 = answer_number1.records
    records2 = answer_number2.records
    records3 = answer_number3.records
    records4 = answer_number4.records
    records = answer_number.records

    len_records = len(records)

    rate_records1 = len(records1) / len_records * 100
    rate_records2 = len(records2) / len_records * 100
    rate_records3 = len(records3) / len_records * 100
    rate_records4 = len(records4) / len_records * 100

    answer_rate_text = "1:{0}% 2:{1}% 3:{2}% 4:{3}%".format(
        int(rate_records1), int(rate_records2), int(rate_records3), int(rate_records4)
    )

    print(answer_rate_text)

    return answer_rate_text


get_answer_rate(1)
