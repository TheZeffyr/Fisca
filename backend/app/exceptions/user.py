class UserNotFoundError(Exception):
    def __init__(self, **kwargs):
        if not kwargs:
            raise ValueError("At least one search field required")
        
        field, value = next(iter(kwargs.items()))
        self.field = field
        self.value = value
        self.message = f"User with {field} '{value}' not found"
        super().__init__(self.message) 


class UserAlreadyExistsError(Exception):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.message = f"User with tg_id {tg_id} already exists"
        super().__init__(self.message)