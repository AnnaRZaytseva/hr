from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

giga = GigaChat(
    credentials="M2Y3YmE2NTEtMTg1Zi00ZjY4LWEwOGMtYjE0ZjlhMDQ2OTYwOmE2ZDU2NmNkLTNmMTgtNDJmYi05NGU0LTc1ZDRjYjBkMmNkZg==",
    verify_ssl_certs=False,
)

with open('systemprompt.txt', 'r', encoding='utf-8') as f:
    system_message = f.read()

with open('info.txt', 'r', encoding='utf-8') as f:
    vacancy_info = f.read()

with open('info.txt', 'r', encoding='utf-8') as f:
    resume = f.read()

messages = [
        SystemMessage(content=system_message)
]

## Функция проведения собеседования
def begin(vacancy_info, resume):
    global messages

    user_answers = {}

    messages.append(HumanMessage(content=vacancy_info))
    messages.append(HumanMessage(content=resume))

    res = giga.invoke(messages)
    messages.append(res)
    print('HR: ' + res.content)
    user_ans = input('Human: ')
    while 'конец' not in user_ans:
        messages.append(HumanMessage(content=user_ans))

        res = giga.invoke(messages)
        print('HR: ' + res.content)
        messages.append(res)
        user_answers[res.content] = user_ans
        user_ans = input('Human: ')

    rating(user_answers, messages)


##запрос на анализ полученных данных от соискателя
def rating(user_answers, messages):
    messages.append(HumanMessage(content='Оцени кандидата в соответствии с его ответами на вопросы, резюме и требованиями вакансии. '
                                         'Напиши, насколько в процентах он подходит для вакансии и кратко аргументируй позицию'))
    res = giga.invoke(messages)

    print(res.content)
    print(user_answers)

begin(vacancy_info, resume)