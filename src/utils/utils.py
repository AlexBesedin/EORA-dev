import re

from config import Resources
from contants.constants import STOP_WORDS


def extract_company_from_query(user_query: str) -> str:
    """
    Определяем, упоминается ли конкретная компания в вопросе пользователя.
    Если да, возвращаем название компании.
    """
    user_query = user_query.lower()

    patterns = [
        r"для компании (\w+)",
        r"что вы делали для (\w+)",
        r"для (\w+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, user_query)
        if match:
            return match.group(1)

    return None



def preprocess_text(text: str) -> str:
    words = text.lower().split()
    lemmatized = [
        Resources.morph.parse(word)[0].normal_form
        for word in words if word not in STOP_WORDS
    ]
    return ' '.join(lemmatized)



def is_project_relevant(project: dict, user_query: str) -> bool:
    """
    Проверяет, содержит ли проект ключевые слова из запроса пользователя.
    Возвращает True, если проект релевантен запросу.
    """
    query_keywords = user_query.lower().split()
    project_text = (
        f"{project['title']} {project['company']} "
        f"{' '.join(project['tags'])} {project['problem']} "
        f"{project['solution']}".lower()
    )
    return any(keyword in project_text for keyword in query_keywords)