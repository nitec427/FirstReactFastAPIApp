import typing
from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry : typing.Dict = {}

@as_declarative(class_registry = class_registry)
class Base:
    id: typing.Any
    __name__:str
    
    # Generate __tablename__ automatically
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # In other codebases you may seen the line below
    
    # Base = declarative_base()
    
    # We were using RECIPES list toy data, now we're ready to define our recipe table. To do so, we define via ORM in models/recipe.py