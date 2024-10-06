import re
import random
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from config import Resources
from crud.crud_base import crud_project

from contants.constants import STOP_WORDS


async def get_projects_by_similar_tags(
    db: AsyncSession, user_query: str
) -> List[dict]:

    words = re.findall(r'\w+', user_query.lower())
    keywords = [
        Resources.morph.normal_forms(word)[0]
        for word in words if word not in STOP_WORDS
    ]

    projects = await crud_project.get_all_projects(db=db)

    project_scores = []

    for project in projects:
        project_tags = [
            Resources.morph.normal_forms(tag.lower())[0]
            for tag in project.tags
        ]
        project_title = ' '.join(
            [
                Resources.morph.normal_forms(word)[0]
                for word in re.findall(r'\w+', project.title.lower())
            ]
        )
        project_company = ' '.join(
            [
                Resources.morph.normal_forms(word)[0]
                for word in re.findall(r'\w+', project.company.lower())
            ]
        )

        searchable_fields = project_tags + [project_title, project_company]

        match_count = 0
        for keyword in keywords:
            for field in searchable_fields:
                if keyword in field:
                    match_count += 1
                    break

        if match_count > 0:
            project_scores.append({
                "project": {
                    "title": project.title,
                    "url": project.url,
                    "company": project.company,
                    "problem": project.problem,
                    "solution": project.solution,
                    "tags": project.tags
                },
                "score": match_count
            })

    project_scores.sort(key=lambda x: x['score'], reverse=True)

    grouped_projects = {}
    for item in project_scores:
        score = item['score']
        if score not in grouped_projects:
            grouped_projects[score] = []
        grouped_projects[score].append(item['project'])
    
    for score in grouped_projects:
        random.shuffle(grouped_projects[score])
    
    matching_projects = []
    for score in sorted(grouped_projects.keys(), reverse=True):
        matching_projects.extend(grouped_projects[score])

    return matching_projects
