from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
import json
import os

giga = GigaChat(
    credentials="M2Y3YmE2NTEtMTg1Zi00ZjY4LWEwOGMtYjE0ZjlhMDQ2OTYwOmE2ZDU2NmNkLTNmMTgtNDJmYi05NGU0LTc1ZDRjYjBkMmNkZg==",
    verify_ssl_certs=False,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir)


with open(file_path + '/systemprompt.txt', 'r', encoding='utf-8') as f:
    system_message = f.read()

with open(file_path + '/info.txt', 'r', encoding='utf-8') as f:
    vacancy_info = f.read()

with open(file_path + '/resume.txt', 'r', encoding='utf-8') as f:
    resume = f.read()

def get_q(messages):

    answer = messages['all'][-1]
    question = messages['all'][-2]

    res = giga.invoke(messages['all'])
    messages['all'].append(res.content)
    messages[question] = answer


    return messages

## Функция проведения собеседования
def begin():
    messages = {
        'all': [SystemMessage(content=system_message), ]
    }

    messages['all'].append(HumanMessage(content=vacancy_info))

    res = giga.invoke(messages['all'])
    messages['all'].append(res.content)

    return messages


##запрос на анализ полученных данных от соискателя
def rating(user_answers, messages):
    messages.append(HumanMessage(content='Оцени кандидата в соответствии с его ответами на вопросы, резюме и требованиями вакансии. '
                                         'Напиши, насколько в процентах он подходит для вакансии и кратко аргументируй позицию'))
    res = giga.invoke(messages)

    print(res.content)
    print(user_answers)