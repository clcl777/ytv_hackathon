from pykintone import model
from setting import answer_app


class Answer(model.kintoneModel):
    def __init__(self):
        super(Answer, self).__init__()
        self.id = ""
        self.content = ""
        self.user_id = ""
        self.question_id = ""
        self.created_at = ""
        self.updated_at = ""


def get_answers():
    answers = answer_app.select().models(Answer)
    print(vars(answers[0]))
    return answers


get_answers()
