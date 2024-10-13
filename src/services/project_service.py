import time
import torch
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sentence_transformers import util

from config import Resources
from crud.project import crud_project
from utils.utils import extract_company_from_query, preprocess_text


async def get_projects_by_similar_tags(db: AsyncSession, user_query: str) -> List[Dict]:
    """
    Поиск проектов на основе запроса пользователя.

    1. Предобрабатывает текст запроса и преобразует его в эмбеддинг.
    2. Извлекает название компании из запроса (если есть) для фильтрации проектов по компании.
    3. Вычисляет косинусное сходство между эмбеддингом запроса и эмбеддингами проектов.
    4. Если достаточное количество проектов с высоким сходством не найдено, выполняет fallback-поиск.
    """
    processed_query = preprocess_text(user_query)
    start_time = time.time() 
    query_embedding = Resources.model.encode([processed_query])[0]
    company_name = extract_company_from_query(user_query)
    projects = await crud_project.get_all_projects_with_embeddings(db=db)

    project_scores = []

    for project in projects:
        if company_name and company_name not in project['company'].lower():
            continue
        project_embedding = project['embedding']
        similarity_score = util.pytorch_cos_sim(query_embedding, project_embedding).item()

        project_scores.append({
            "project": project,
            "score": similarity_score
        })

    project_scores.sort(key=lambda x: x['score'], reverse=True)

    end_time = time.time()  
    response_time = end_time - start_time

    if len(project_scores) == 0 or project_scores[0]['score'] < 0.5:
        matching_projects = search_by_project_embeddings_fallback(projects, query_embedding)
    else:
        matching_projects = [{
            "id": project['id'],
            "title": item['project']['title'],
            "url": item['project']['url'],
            "company": item['project']['company'],
            "tags": item['project']['tags'],
            "problem": item['project']['problem'],
            "solution": item['project']['solution'],
            "similarity_score": item['score']
        } for item in project_scores[:3]]

    return matching_projects, response_time




def search_by_project_embeddings_fallback(projects: List[Dict], query_embedding: torch.Tensor) -> List[Dict]:
    """
    Запасной поиск по проектам с использованием косинусного сходства между эмбеддингами.

    Используется, если основной поиск по компании и эмбеддингам не дал достаточных результатов. 
    Вычисляет косинусное сходство между эмбеддингом запроса и эмбеддингами всех проектов.
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