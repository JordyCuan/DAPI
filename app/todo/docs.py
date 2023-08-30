from utils.docs import FastAPIRouteParameters


class RetrieveTodoDocs(FastAPIRouteParameters):
    status_code: int = 200


class ListTodoDocs(FastAPIRouteParameters):
    status_code: int = 200


class CreateTodoDocs(FastAPIRouteParameters):
    status_code: int = 201


class UpdateTodoDocs(FastAPIRouteParameters):
    status_code: int = 200


class DestroyTodoDocs(FastAPIRouteParameters):
    status_code: int = 204


retrieve_todo_docs = RetrieveTodoDocs().model_dump()
list_todo_docs = ListTodoDocs().model_dump()
create_todo_docs = CreateTodoDocs().model_dump()
update_todo_docs = UpdateTodoDocs().model_dump()
destroy_todo_docs = DestroyTodoDocs().model_dump()
