import random
import html
import logging
from openai import OpenAI
from config import Config
from contants.constants import (
    GPT_CONTEXT_INTRO, 
    GPT_SYSTEM_PROMPT, 
    MAX_TOKENS, 
    NO_PROJECTS_FOUND_MESSAGE, 
    TEMPERATURE
)

logger = logging.getLogger(__name__)

client = OpenAI(
        api_key=Config.OPENAI_TOKEN,
        base_url=Config.PROXYAPI_URL,
    )


def generate_response(user_query, matching_projects):
    if not matching_projects:
        return NO_PROJECTS_FOUND_MESSAGE
    
    if len(matching_projects) > 2:
        matching_projects = random.sample(matching_projects, 2)

    project_descriptions = [
        f"{project['title']} для {project['company']}. "
        f"Решение: {project['solution'][:100]}..."
        for project in matching_projects
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

        for i, project in enumerate(matching_projects, start=1):
            safe_title = html.escape(project['title'])
            safe_company = html.escape(project['company'])
            project_identifier = f"{safe_title} - ({safe_company})"
            final_response = final_response.replace(f"({i})", project_identifier)
            link = f'<a href="{html.escape(project["url"])}">[ссылка]</a>'
            final_response += f'\n{i}. {project_identifier}: {link}'

        return final_response

    except Exception as e:
        logger.error(f"Ошибка при взаимодействии с OpenAI: {e}")