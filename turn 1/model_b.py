
from pydantic import BaseModel, validator

class LegalData(BaseModel):
    name: str
    age: int
    email: str
    country: str

    @validator('age')
    def age_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Age must be a positive integer.')
        return v

    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email format.')
        return v

    @validator('country')
    def country_must_be_uppercase(cls, v):
        return v.upper()

# Dummy data
data = [
    {'name': 'Alice', 'age': 25, 'email': 'alice@example.com', 'country': 'usa'},
    {'name': 'Bob', 'age': -3, 'email': 'bob@example.com', 'country': 'france'},
    {'name': 'Charlie', 'age': 30, 'email': 'charlie@example', 'country': 'canada'},
]

# Validation and error handling
for entry in data:
    try:
        legal_data = LegalData(**entry)
        print(f'Valid data: {legal_data}')
    except Exception as e:
        print(f'Error for {entry}: {e}')
