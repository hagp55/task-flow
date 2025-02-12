import logging
from sqlite3 import Connection, Cursor

from fastapi import APIRouter, Response, status

from src.apps.tasks.schemas import TaskIn, TaskOut
from src.core.db import get_connection

__all__ = ("router",)


router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(payload: TaskIn) -> TaskOut:
    connection: Connection = get_connection()
    cursor: Cursor = connection.cursor()
    tasks = cursor.execute(
        """
        INSERT INTO tasks (id, name, pomodoro_count, category_id) VALUES(?,?,?,?)
        """,
        (payload.id, payload.name, payload.pomodoro_count, payload.category_id),
    )
    connection.commit()
    connection.close()
    return TaskOut(**payload.model_dump())


@router.get(
    "",
    response_model=list[TaskOut],
    status_code=status.HTTP_200_OK,
)
async def get_tasks() -> list[TaskOut]:
    connection: Connection = get_connection()
    cursor: Cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM tasks").fetchall()
    tasks: list[TaskOut] = [
        TaskOut.model_validate(
            {
                "id": task[0],
                "name": task[1],
                "pomodoro_count": task[2],
                "category_id": task[3],
            }
        )
        for task in result
    ]
    connection.close()
    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
async def get_task(task_id: int) -> TaskOut:
    connection: Connection = get_connection()
    cursor = connection.cursor()
    result = cursor.execute(
        "SELECT * FROM tasks WHERE id =?",
        (task_id,),
    ).fetchone()
    connection.close()
    task: TaskOut = TaskOut.model_validate(
        {
            "id": result[0],
            "name": result[1],
            "pomodoro_count": result[2],
            "category_id": result[3],
        }
    )
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
async def partial_task(task_id: int, name: str) -> TaskOut:
    connection: Connection = get_connection()
    cursor = connection.cursor()
    tasks = cursor.execute(
        "UPDATE tasks SET name=? WHERE id =?",
        (name, task_id),
    )
    connection.commit()
    result = cursor.execute(
        "SELECT * FROM tasks WHERE id =?",
        (task_id,),
    ).fetchone()
    task: TaskOut = TaskOut.model_validate(
        {
            "id": result[0],
            "name": result[1],
            "pomodoro_count": result[2],
            "category_id": result[3],
        }
    )
    return task


@router.delete(
    "/{task_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(task_id: int) -> None:
    connection: Connection = get_connection()
    cursor = connection.cursor()
    connection.commit()
    result = cursor.execute(
        "SELECT * FROM tasks WHERE id =?",
        (task_id,),
    ).fetchone()
    if result:
        cursor.execute(
            "DELETE FROM tasks WHERE id =?",
            (task_id,),
        )
        connection.commit()
        connection.close()
