from pykintone import model
from setting import answer_app
from correct_answer import get_question_correct_answers


class Answer(model.kintoneModel):
    def __init__(self):
        super(Answer, self).__init__()
        self.id = ""
        self.content = ""
        self.user_id = ""
        self.question_id = ""
        self.created_at = ""
        self.updated_at = ""


class AnswerPost(model.kintoneModel):
    def __init__(self):
        super(AnswerPost, self).__init__()
        self.content = ""
        self.user_id = ""
        self.question_id = ""


def get_answers():
    answers = answer_app.select().models(Answer)

    print(vars(answers[0]))

    return answers


# get_answers()

# 回答時間を取得する関数
def get_answer_times(question_id):
    select = "question_id = {0}".format(question_id)
    answer_times = answer_app.select(select)

    records = answer_times.records

    print(records)

    for record in records:
        print(record["created_at"]["value"])

    return answer_times


def post_answer(question_id, content, user_id):
    answer = AnswerPost()

    answer.question_id = question_id
    answer.content = content
    answer.user_id = user_id

    created_id = answer_app.create(answer).record_id

    print(vars(answer))
    print(created_id)


def obtain_ranking(question_id):
    correct_answer = get_question_correct_answers(question_id)

    db_data = answer_app.select(
        "question_id = {0} and content = {1} order by updated_at asc".format(
            question_id, correct_answer
        )
    ).models(Answer)

    ranking = []

    for i, data in enumerate(db_data):
        ranking.append(
            {
                "num": i + 1,
                "user_id": data.user_id,
                "time": data.updated_at.strftime("%Y/%m/%d %H:%M"),
            }
        )

    print(ranking)

    return ranking


obtain_ranking(1)
