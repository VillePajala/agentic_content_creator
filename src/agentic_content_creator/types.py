from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import List

class Report(BaseModel):
    title: str = Field(...,description="The title of the report")
    abstract: str = Field(...,description="The abstract for the report")
    content: str = Field(...,description="The actual deep content of the report")
    summarylist: str = Field(...,description="Bulleted list of the key points of the report")