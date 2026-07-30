from fastapi import APIRouter, HTTPException, Query

from app.services import kanban_store

router = APIRouter(prefix="/kanban", tags=["kanban"])


@router.get("/boards")
async def list_boards():
    return kanban_store.list_boards()


@router.post("/boards")
async def create_board(data: dict):
    name = data.get("name", "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="name requis")
    board = kanban_store.create_board(name)
    if data.get("tasks"):
        kanban_store.add_tasks_bulk(board["id"], data["tasks"])
        board = kanban_store.get_board(board["id"])
    return board


@router.get("/boards/{board_id}")
async def get_board(board_id: str):
    board = kanban_store.get_board(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Tableau introuvable")
    return board


@router.delete("/boards/{board_id}")
async def delete_board(board_id: str):
    if not kanban_store.delete_board(board_id):
        raise HTTPException(status_code=404, detail="Tableau introuvable")
    return {"ok": True}


@router.post("/boards/{board_id}/tasks")
async def add_task(board_id: str, data: dict):
    board = kanban_store.get_board(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Tableau introuvable")
    title = data.get("title", "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="title requis")
    return kanban_store.add_task(
        board_id=board_id,
        title=title,
        description=data.get("description", ""),
        column=data.get("column", "todo"),
        priority=data.get("priority", "medium"),
        position=data.get("position"),
    )


@router.put("/tasks/{task_id}")
async def update_task(task_id: str, data: dict):
    task = kanban_store.update_task(task_id, **data)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    if not kanban_store.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    return {"ok": True}
