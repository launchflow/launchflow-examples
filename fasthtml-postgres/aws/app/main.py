from contextlib import asynccontextmanager

import launchflow as lf
from app import crud
from app.infra import postgres
from fasthtml.common import *


@asynccontextmanager
async def lifespan(app):
    # Create the SQLAlchemy async engine during startup
    engine = await postgres.sqlalchemy_async_engine()

    # Create the database tables using the engine (but not when deployed)
    if not lf.is_deployment():
        await crud.create_tables(engine)

    # Configure the SQLAlchemy connection pool
    crud.setup_async_session(engine)

    print("Postgres database connected")
    yield
    # Everything run after the yield will be executed during shutdown
    print("Shutting down")


app, rt = fast_app(
    hdrs=[Style(":root { --pico-font-size: 100%; }")],
    done=bool,
    pk="id",
    lifespan=lifespan,
)

id_curr = "current-todo"


def tid(id):
    return f"todo-{id}"


@patch
def __ft__(self: crud.Todo):
    show = AX(self.title, f"/todos/{self.id}", id_curr)
    edit = AX("edit", f"/edit/{self.id}", id_curr)
    dt = " ✅" if self.done else ""
    return Li(show, dt, " | ", edit, id=tid(self.id))


def mk_input(**kw):
    return Input(id="new-title", name="title", placeholder="New Todo", **kw)


@rt("/")
async def get():
    add = Form(
        Group(mk_input(), Button("Add")),
        hx_post="/",
        target_id="todo-list",
        hx_swap="beforeend",
    )
    todos = await crud.list_todos()
    card = (Card(Ul(*todos, id="todo-list"), header=add, footer=Div(id=id_curr)),)
    title = "Todo list"
    return Title(title), Main(H1(title), card, cls="container")


@rt("/todos/{id}")
async def delete(id: int):
    await crud.delete_todo(id)
    return clear(id_curr)


@rt("/")
async def post(todo: crud.Todo):
    new_todo = await crud.insert_todo(todo)
    return new_todo, mk_input(hx_swap_oob="true")


@rt("/edit/{id}")
async def get(id: int):
    res = Form(
        Group(Input(id="title"), Button("Save")),
        Hidden(id="id"),
        Checkbox(id="done", label="Done"),
        hx_put="/",
        target_id=tid(id),
        id="edit",
    )
    todo = await crud.get_todo(id)
    return fill_form(res, todo)


@rt("/")
async def put(todo: crud.Todo):
    new_todo = await crud.update_todo(todo)
    return new_todo, clear(id_curr)


@rt("/todos/{id}")
async def get(id: int):
    todo = await crud.get_todo(id)
    btn = Button(
        "delete",
        hx_delete=f"/todos/{todo.id}",
        target_id=tid(todo.id),
        hx_swap="outerHTML",
    )
    return Div(Div(todo.title), btn)


serve()
