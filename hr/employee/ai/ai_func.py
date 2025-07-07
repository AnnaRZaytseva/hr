from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from langchain_openai import ChatOpenAI
import json
import os
import psycopg2
import sqlite3

# giga = GigaChat(
#     credentials="M2Y3YmE2NTEtMTg1Zi00ZjY4LWEwOGMtYjE0ZjlhMDQ2OTYwOmE2ZDU2NmNkLTNmMTgtNDJmYi05NGU0LTc1ZDRjYjBkMmNkZg==",
#     verify_ssl_certs=False,
# )

giga = ChatOpenAI(
    # model="deepseek/deepseek-r1-0528-qwen3-8b:free",
    # model="meta-llama/llama-4-maverick:free",
    model="deepseek/deepseek-chat:free",
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.2,
    openai_api_key="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"
)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir)


with open(file_path + '/systemprompt.txt', 'r', encoding='utf-8') as f:
    system_message = f.read()

# with open(file_path + '/info.txt', 'r', encoding='utf-8') as f:
#     vacancy_info = f.read()

with open(file_path + '/resume.txt', 'r', encoding='utf-8') as f:
    resume = f.read()
    


def get_vacancy_info(vacancy_id):
    """Получает данные вакансии из БД по ID"""
    try:
        # Подключение к БД (укажите свои параметры подключения)
        DB_NAME = "ai_hr_database"
        DB_HOST = "127.0.0.1"
        DB_USER = "postgres"
        DB_PASSWORD = "33772"
        DB_PORT = "5432"
        
        # conn = sqlite3.connect('db.sqlite3')
        
        conn = psycopg2.connect(dbname=DB_NAME,
                               host=DB_HOST,
                               user=DB_USER,
                               password=DB_PASSWORD,
                               port=DB_PORT)

        cursor = conn.cursor()
        
        # Выполнение запроса
        cursor.execute("""
            SELECT title, description, requirements, responsibilities, conditions
            FROM employee_vacancy 
            WHERE id = %s     
        """, (vacancy_id,))    # для postgre %s   |   для sqlite ?
        
        # Получение результатов
        result = cursor.fetchone()
        
        if not result:
            raise ValueError(f"Вакансия с ID {vacancy_id} не найдена")
        
        result = ("Описание вакансии: "+result[0]+
                  "\n\nТребования к кандидату: "+result[1]+
                  "\n\nОбязанности кандидата: "+result[2]+
                  "\n\nУсловия для кандидата: "+result[3])
        
        return result
        
        # return {
        #     'description': result[0],
        #     'requirements': result[1],
        #     'responsibilities': result[2],
        #     'conditions': result[3]
        # }
        
    except Exception as e:
        print(f"Ошибка при получении данных вакансии: {e}")
        raise
    finally:
        conn.close()
        
        



def get_q(messages):

    answer = messages['all'][-1]
    question = messages['all'][-2]
    # vacancy_info = get_vacancy_info(id)
    
    res = giga.invoke(messages['all'])
    messages['all'].append(res.content)
    messages[str(question)] = answer
    # print("###\n###\n###\n###")
    # print(messages)
    # print("###\n###\n###\n###")

    return messages

## Функция проведения собеседования
# vacancy_info = get_vacancy_info(16)
# print(vacancy_info)

def begin(vacancy_id):
    vacancy_info = get_vacancy_info(vacancy_id)
    
    messages = {
        'all': [SystemMessage(content=system_message), ]
        # 'all': [HumanMessage(content=system_message), ]
    }

    messages['all'].append(HumanMessage(content=vacancy_info))

    res = giga.invoke(messages['all'])
    # print(res.content)
    # print("TYPE:", type(res))
    messages['all'].append(res.content)

    return messages


##запрос на анализ полученных данных от соискателя
def rating(user_answers, messages):
    messages.append(HumanMessage(content='Оцени кандидата в соответствии с его ответами на вопросы, резюме и требованиями вакансии. '
                                         'Напиши, насколько в процентах он подходит для вакансии и кратко аргументируй позицию'))
    res = giga.invoke(messages)

    print(res.content)
    print(user_answers)