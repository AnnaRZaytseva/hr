# your_app/llm_service.py
from langchain_gigachat.chat_models import GigaChat
from langchain_openai import ChatOpenAI
# Инициализация при импорте модуля
# giga = GigaChat(
#     credentials="M2Y3YmE2NTEtMTg1Zi00ZjY4LWEwOGMtYjE0ZjlhMDQ2OTYwOmE2ZDU2NmNkLTNmMTgtNDJmYi05NGU0LTc1ZDRjYjBkMmNkZg==",
#     verify_ssl_certs=False,
#     temperature=0.5
# )

giga = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="gemma-4-e2b-it-uncensored"
)