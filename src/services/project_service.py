import time
import numpy as np
from typing import Dict, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sentence_transformers import util

from config import Resources
from contants.constants import MIN_SIMILARITY_THRESHOLD
from crud.project import crud_project
from utils.utils import preprocess_text


async def get_projects_by_similar_tags(
    db: AsyncSession, 
    user_query: str
) -> Tuple[List[Dict], float]:
    """
    Поиск проектов на основе запроса пользователя.

    1. Предобрабатывает текст запроса.
    2. Выполняет поиск в следующем порядке:
       a) По тегам
       b) По компании
       c) Fallback-поиск по всем полям
    """
    processed_query = preprocess_text(user_query)
    start_time = time.time()
    query_embedding = Resources.model.encode([processed_query])[0]
    projects = await crud_project.get_all_projects_with_embeddings(db=db)

    matching_projects = search_by_tags(
        projects=projects, 
        processed_query=processed_query, 
        query_embedding=query_embedding
    )
    if matching_projects:
        return matching_projects, time.time() - start_time

    matching_projects = search_by_company(
        projects=projects, 
        processed_query=processed_query, 
        query_embedding=query_embedding
    )
    if matching_projects:
        return matching_projects, time.time() - start_time

    matching_projects = search_by_project_embeddings_fallback(
        projects=projects, 
        query_embedding=query_embedding
    )
    return matching_projects, time.time() - start_time


def search_by_tags(
    projects: List[Dict], 
    processed_query: str, 
    query_embedding: np.ndarray
) -> List[Dict]:
    """
    Поиск по тегам
    """
    matching_projects = []
    query_words = set(processed_query.split())
    for project in projects:
        project_tags = set(tag.lower() for tag in project['tags'])
        if query_words.intersection(project_tags):
            similarity_score = util.pytorch_cos_sim(query_embedding, project['embedding']).item()
            if similarity_score > MIN_SIMILARITY_THRESHOLD:
                matching_projects.append({
                    "id": project["id"],
                    "title": project['title'],
                    "url": project['url'],
                    "company": project['company'],
                    "tags": project['tags'],
                    "problem": project['problem'],
                    "solution": project['solution'],
                    "similarity_score": similarity_score
                })
    matching_projects.sort(key=lambda x: x['similarity_score'], reverse=True)
    return matching_projects[:3]


def search_by_company(
    projects: List[Dict], 
    processed_query: str, 
    query_embedding: np.ndarray
) -> List[Dict]:
    """
    Поиск по компаниям
    """
    matching_projects = []
    query_words = set(processed_query.split())
    for project in projects:
        company_words = set(preprocess_text(project['company']).split())
        if query_words.intersection(company_words):
            similarity_score = util.pytorch_cos_sim(query_embedding, project['embedding']).item()
            if similarity_score > MIN_SIMILARITY_THRESHOLD:
                matching_projects.append({
                    "id": project["id"],
                    "title": project['title'],
                    "url": project['url'],
                    "company": project['company'],
                    "tags": project['tags'],
                    "problem": project['problem'],
                    "solution": project['solution'],
                    "similarity_score": similarity_score
                })
    matching_projects.sort(key=lambda x: x['similarity_score'], reverse=True)
    return matching_projects[:3]


def search_by_project_embeddings_fallback(
    projects: List[Dict], 
    query_embedding: np.ndarray
) -> List[Dict]:
    """
    Запасной поиск по проектам.
    """
    matching_projects = [
        {
            "id": project["id"],
            "title": project['title'],
            "url": project['url'],
            "company": project['company'],
            "tags": project['tags'],
            "problem": project['problem'],
            "solution": project['solution'],
            "similarity_score": util.pytorch_cos_sim(query_embedding, project['embedding']).item()
        } for project in projects
    ]
    
    matching_projects.sort(key=lambda x: x['similarity_score'], reverse=True)
    return matching_projects[:3]
