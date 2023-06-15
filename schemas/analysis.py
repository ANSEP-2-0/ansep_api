from pydantic import BaseModel

class Parameters(BaseModel):
    parameters_string: str
    sbml_model: str | None