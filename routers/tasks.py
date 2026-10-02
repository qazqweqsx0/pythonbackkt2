import strawberry
from typing import List
from models.task import Category
from models.task import Task
from strawberry.fastapi import GraphQLRouter

tasks_db = [
    Task(id=strawberry.ID("1"), title="Изучить GraphQL", description="...",
         is_completed=False, category=Category(name="Учёба", color="blue")),
]

@strawberry.type
class Query:
    @strawberry.field
    def all_tasks(self) -> List[Task]:
        return tasks_db

    @strawberry.field
    def task(self, id: strawberry.ID) -> Task | None:
        for task in tasks_db:
            if task.id == id:
                return task
        return None
    
@strawberry.input
class TaskInput:
    title: str
    description: str
    category_name: str = "Без категории"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(self, input: TaskInput) -> Task:
        new_task = Task(
            id=strawberry.ID(str(len(tasks_db) + 1)),
            title=input.title,
            description=input.description,
            is_completed=False,
            category=Category(name=input.category_name, color="gray")
        )
        tasks_db.append(new_task)
        return new_task

    @strawberry.mutation
    def complete_task(self, id: strawberry.ID) -> Task | None:
        for task in tasks_db:
            if task.id == id:
                task.is_completed = True
                return task
        return None

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)