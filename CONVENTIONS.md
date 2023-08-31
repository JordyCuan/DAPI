# PROJECT STRUCTURE
* We follow `Domain Driven Design`:

> ```
> app/
> ├── auth
> │   ├── __init__.py
> │   ├── dependencies.py
> │   ├── router.py
> │   ├── schemas.py
> │   └── security.py
> ├── posts
> │   ├── __init__.py
> │   ├── dependencies.py
> │   ├── docs.py
> │   ├── filters.py
> │   ├── models.py
> │   ├── repository.py
> │   ├── router.py
> │   ├── schemas.py
> │   └── services.py
> └── users
>     ├── __init__.py
>     ├── models.py
>     ├── repository.py
>     ├── router.py
>     └── schemas.py
> ```



# MODELS AND DATABASE
* Table names should be CamelCase and plural UNLESS they are catalogs

> Example:
>
> ```python
>     Users, Addresses, Roles, Permissions
>
>     ProgramType, CountryState, WorkShift
> ```


# FRONTEND PAYLOAD (Pydantic)
* Make sure to excessively delegate incoming FrontEnd data validation to Pydantic




# DEPENDENCIES
* While Pydantic can validate the values from client input, Dependencies should be used to validate data against database constraints like **email already exists**, **user not found**, etc.
>
> ```python
> async def valid_post_id(id: int) -> PostModel:
>     post = await service.get_by_id(id)
>     if not post:
>         raise PostNotFound()
>
>     return post
> ```



# ROUTERS

* As naming convention, whenever we refer to basic http method operations, we refer to them as:
  * `retrieve..[GET]`
  * `list......[GET]`
  * `create....[POST]`
  * `update....[PUT]`
  * `destroy...[DELETE]`


> Example:
>
> ```python
> async def retrieve_user(...): ...
> async def retrieve_by_id(...): ...
> async def list_user(...): ...
> async def create_user(...): ...
> async def update_user(...): ...
> async def destroy_user(...): ...
> ```

* URL paths must be plural
> Example:
>
> ```python
> router = APIRouter(prefix="/users", tags=["users"])
> ```


* Endpoint function return annotations must be `Any` as FastAPI converts `ResponsePydanticObject` to `Dict` then to an instance of `ResponseModel` then to `Dict` then to `JSON`. Hence,
* `response_model` attribute must be set in routes

> Example:
>
> ```python
> @app.get("/", response_model=ProfileResponse)
> def retrieve_profile():
>     ...
> ```

## Filters
* Filter definitions are Pydantic schemas where the attribute name is the `field-lookup` and the value is the filtering criteria.
  * `fields` should be a valid model attribute (a.k.a. table's column)
  * `lookup` should be a valid lookup keyword. The current available lookups are:
    - `gt`: Greater than
    - `gte`: Greater than or equal to
    - `lt`: Less than
    - `lte`: Less than or equal to
    - `eq`: Equal to
    - `ieq`: Case insensitive equality (using `ILIKE`)
    - `contains`: Check if column contains the value
    - `icontains`: Case insensitive check if column contains the value
  * `field-lookups` are separated by `__` (double underscore)
> Example:
>
> ```python
> class PostFilterSchema(FilterSchema, extra="forbid"):
>     title__ieq: Optional[str] = Query(None)
>     description__gt: Optional[str] = Query(None)
>     author__icontains: Optional[str] = Query(None)
> ```



## OrderBy
* Sorting should ALWAYS be an outer dependency (never be within Pydantic objects) in order to make it work.
  * Notice how you explicitly define the `ordering` name
> Example:
>
> ```python
> def get_post_filter_manager(
>     filters: PostFilterSchema = Depends(),
>     ordering: Optional[list[str]] = Query(None),
> ) -> PostFilterManager:
>     return PostFilterManager(filters=filters, ordering=ordering)
> ```


## Pagination



# Server Responses
