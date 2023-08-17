# Utils

## Description

The **`utils`** module is a comprehensive utility extension tailored for projects leveraging FastAPI and SQLAlchemy. Recognizing the recurring challenges in modern web applications, this module aims to simplify and streamline operations by offering a robust suite of utilities.


> If 'something' is able to run in any other different project, then here is the place
> * Example: if you copy paste from here to a different project and you do not need anything else than that


### **Key Features:**

1. **Databases (SQLAlchemy Integration)**:
    - Streamline database interactions and operations.
    - Enhance connection management and query execution.
2. **Schemas (Pydantic Integration)**:
    - Offers tools for schema validation and serialization.
    - Facilitates smoother data transformation and validation.
3. **Authentication**:
    - Secure hashing utilities to fortify user data and credentials based on `passlib` and `CryptContext`.
4. **Date and Time Utilities**:
    - Simplify date-time operations, parsing, and formatting.
    - Enhanced tools for timezone-aware operations.
5. **Exception Handlers**:
    - Gracefully manage and respond to application exceptions.
6. **Custom Exception Classes**:
    - Predefined error classes to handle various application-specific scenarios.
7. **Services**:
    - Follows the route-service-repository architecture for clear code organization.
    - Separate the business logic from route handling for improved maintainability.
8. **Filters**:
    - Comprehensive filtering utilities designed for SQLAlchemy queries.
    - Facilitate operations like filtering, ordering, and pagination with ease.


## Filters

Filters should be defined as `fastapi.Query` and set its **default** as `None`

### Example

```python
class MyAddressFilterSchema(FilterSchema):
    street__ieq: str = Query(None)
    num__gt: int = Query(None)
    num__gte: int = Query(None)
    num__lt: int = Query(None)
    num__lte: int = Query(None)
    num__eq: int = Query(None)
    postal_code__eq: str = Query(None)
    references__contains: str = Query(None)
    references__icontains: str = Query(None)
    city__in: List[int] = Query(None)  # `__in` lookup still in progress
```

* **default**: This is the only mandatory field. Provides a default value. This will be displayed in the OpenAPI documentation and also used if the client doesn't provide the value.
* **alias**: You can provide an alias for the field which will be used in the OpenAPI schema instead of the field name.
* **title**: A short description or title for the field.
* **description**: A longer description of the field. This will be displayed in the OpenAPI documentation.
* **gt**, **ge**, **lt**, **le**: These are validation constraints that mean greater than, greater than or equal, less than, and less than or equal, respectively. They can be used for numeric fields and will be reflected in the OpenAPI documentation.
* **min_length**, max_length: For string fields, these determine the minimum and maximum length of the string.
* **regex**: A regular expression pattern that the string field should match. It's used for validation and will be reflected in the OpenAPI documentation.
* **deprecated**: If set to True, this will mark the field as deprecated in the OpenAPI documentation.
* **embed**: By default, when you declare a body, FastAPI creates a new model and uses it as a sub-model in the body. If you want to use a single model without an enclosing sub-model, set this parameter to True.
* **example**: You can provide an example for the field which will be displayed in the OpenAPI documentation.
* **examples**: This parameter allows you to provide multiple examples for the field.



## Examples

### `utils.services.BaseService`

```python
class MyService(BaseService):
    pass

@router.get("/{id}")
async def get_item(id: int, my_service: Annotated[MyService, Depends(get_my_service)]):
    return my_service.get_by_id(id=id)
```


### `utils.database.BaseRepository`

```python
from app.models import MyModel  # SQLAlchemy mapper class

class MyModelRepository(BaseRepository):
    model = MyModel

my_repository = MyModelRepository()
my_repository.get_by_id(id=id)
```
