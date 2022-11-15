from pykintone import model
from setting import correct_answer_app


class CorrectAnswer(model.kintoneModel):
    def __init__(self):
        super(CorrectAnswer, self).__init__()
        self.question_id = ""
        self.answer = ""


def get_correct_answers():
    correct_answers = correct_answer_app.select().models(CorrectAnswer)

    print(vars(correct_answers[0]))

    return correct_answers


# 正解の解答の番号を取得する関数
def get_question_correct_answers(question_id):
    select = "question_id = {0}".format(question_id)

    question_correct_answers = correct_answer_app.select(select)

    records = question_correct_answers.records

    # print(records)

    # for record in records:
    #     print(record['answer']['value'])

    # print(type(question_correct_answers))

    # string型に変換
    question_correct_answers = question_correct_answers.records[0]["answer"]["value"]

    return question_correct_answers


get_question_correct_answers(1)
