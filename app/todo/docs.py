from utils.schemas.docs import FastAPIRouteParameters


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


retrieve_todo_docs = RetrieveTodoDocs()
list_todo_docs = ListTodoDocs()
create_todo_docs = CreateTodoDocs()
update_todo_docs = UpdateTodoDocs()
destroy_todo_docs = DestroyTodoDocs()
