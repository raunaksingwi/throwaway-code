from pydantic import BaseModel
from typing import Optional
from .enums import Language, Framework, DatabaseType, ORM



class LanguageFrameworkResult(BaseModel):
    language: Optional[Language] = None
    framework: Optional[Framework] = None
