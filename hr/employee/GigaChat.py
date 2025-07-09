# your_app/llm_service.py
from langchain_gigachat.chat_models import GigaChat

# Инициализация при импорте модуля
giga = GigaChat(
    credentials="M2Y3YmE2NTEtMTg1Zi00ZjY4LWEwOGMtYjE0ZjlhMDQ2OTYwOmE2ZDU2NmNkLTNmMTgtNDJmYi05NGU0LTc1ZDRjYjBkMmNkZg==",
    verify_ssl_certs=False,
    temperature=0.5
)