
- Error Handlers [On Hold]
  - When raising custom `httpexceptions` intended to be handled by the httpexception handlers in `fastapi.ExceptionMiddleware` class. When adding the custom middleware to the app using `app.add_middleware(MyCustomMiddleware)` it gets added between `ExceptionMiddleware` class and `ServerErrorMiddleware` class. The `ServerErrorMiddleware` class is executed on top, then the `user_middleware` (a variable where mine is stored) and then `ExceptionMiddleware` below the custom custom class. Because of that, when custom exceptions are raised in `routes`, the exceptions do not get handled by `ExceptionMiddleware`, when re-raising the new custom `HTTPException`s it goes to `ServerErrorMiddleware` class and that middleware does not handle these exceptions.


- Pagination

- Documentation [In Progress]

- Authentication
