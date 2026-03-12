class CurrencyNotFoundError(Exception):
    def __init__(self, currency_id: int):
        self.currency_id = currency_id
        self.message = f"Currency with {currency_id} not found!"
        super().__init__(self.message)
        
class CurrencyAlreadyExistsError(Exception):
    pass
