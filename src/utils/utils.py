from contants.constants import STOP_WORDS


def preprocess_text(text: str) -> str:
    words = text.lower().split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    return ' '.join(filtered_words)


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