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
