from pydantic import BaseModel


class LufthansaQueryInput(BaseModel):
    text: str

# Can be represented by: {"text": q}


class LufthansaQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]