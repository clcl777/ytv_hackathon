from pykintone import model
from setting import question_app


class Question(model.kintoneModel):
    def __init__(self):
        super(Question, self).__init__()
        self.id = ""
        self.question = ""
        self.type = ""
        self.publish_date = ""


def get_questions():
    questions = question_app.select().models(Question)

    print(vars(questions[0]))

    return questions


# get_questions()


def get_question_text(id):
    select = "id = {0}".format(id)

    question_text = question_app.select(select)

    records = question_text.records

    # print(records)

    # for record in records:
    #     print(record['question']['value'])

    # print(question_text)

    # string型に変換
    question_text = question_text.records[0]["question"]["value"]

    return question_text


# get_question_text(1)

print(get_question_text(1))


def get_question_type(id):
    select = "id = {0}".format(id)

    question_type = question_app.select(select)

    records = question_type.records

    # print(records)

    # for record in records:
    #     print(record['type']['value'])

    # print(question_type)

    # string型に変換
    question_type = question_type.records[0]["type"]["value"]

    return question_type


# get_question_text(1)

print(get_question_type(1))
