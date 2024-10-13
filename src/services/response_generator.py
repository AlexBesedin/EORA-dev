import html
import logging
from openai import OpenAI
from config import Config
from contants.constants import (
    GPT_CONTEXT_INTRO, 
    GPT_SYSTEM_PROMPT, 
    MAX_TOKENS,
    MIN_SIMILARITY_THRESHOLD, 
    NO_PROJECTS_FOUND_MESSAGE, 
    TEMPERATURE
)
from utils.utils import is_project_relevant

logger = logging.getLogger(__name__)

client = OpenAI(
        api_key=Config.OPENAI_TOKEN,
        base_url=Config.PROXYAPI_URL,
    )


def generate_response(user_query: str, matching_projects: list[dict]) -> str:
    if not matching_projects:
        return NO_PROJECTS_FOUND_MESSAGE
    
    filtered_projects = [
        project for project in matching_projects
        if (project['similarity_score'] >= MIN_SIMILARITY_THRESHOLD and
            is_project_relevant(project, user_query))
    ]

    if not filtered_projects:
        return NO_PROJECTS_FOUND_MESSAGE

    filtered_projects = filtered_projects[:2]

    project_descriptions = [
        f"{project['title']} для {project['company']}. "
        f"Проблема: {project['problem']}... "
        f"Решение: {project['solution']}... "
        f"Теги: {', '.join(project['tags'])}"
        for project in filtered_projects
    ]

    context = GPT_CONTEXT_INTRO + "\n".join(project_descriptions)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": GPT_SYSTEM_PROMPT},
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": context}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        final_response = response.choices[0].message.content.strip()
        final_response += "\n"

        for i, project in enumerate(filtered_projects, start=1):
            safe_title = html.escape(project['title'])
            safe_company = html.escape(project['company'])
            project_identifier = f"{safe_title} - ({safe_company})"
            final_response = final_response.replace(f"({i})", project_identifier)
            link = f'<a href="{html.escape(project["url"])}">[ссылка]</a>'
            final_response += f'\n{i}. {project_identifier}: {link}, Сходство: {project["similarity_score"]:.2f}'
        return final_response

    except Exception as e:
        return f"Ошибка при взаимодействии с OpenAI: {e}"
