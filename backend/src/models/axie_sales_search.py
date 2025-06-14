from pydantic import BaseModel, Field, field_validator
from typing import Literal, List, Dict, Annotated, Optional

Axie_Classes = Literal[
    "beast",
    "aquatic",
    "plant",
    "bug",
    "bird",
    "reptile",
    "mech",
    "dawn",
    "dusk"
]


def validate_two_number_range(
    v: List[int], 
    min_allowed: int, 
    max_allowed: int, 
    field_name: str = "value"
) -> List[int]:
    if len(v) != 2:
        raise ValueError(f"{field_name} must contain exactly two integers.")
    low, high = v
    if not (min_allowed <= low <= max_allowed and min_allowed <= high <= max_allowed):
        raise ValueError(f"Each element in {field_name} must be between {min_allowed} and {max_allowed}.")
    if low > high:
        raise ValueError(f"The first element in {field_name} must be less than or equal to the second element.")
    return v


class CollectionDetail(BaseModel):
    numParts: Optional[List[int]] = None

    @field_validator("numParts")
    @classmethod
    def validate_num_parts(cls, v):
        return validate_two_number_range(v, 1, 6, "numParts") if v else v


class CollectionWrapper(BaseModel):
    __root__: Dict[str, CollectionDetail]

    @field_validator("__root__")
    @classmethod
    def one_key_only(cls, v):
        if len(v) != 1:
            raise ValueError("Each collection item must have exactly one key.")
        return v


class AxieSalesSearch(BaseModel):
    time_unit: Literal["days", "hours"] = "days"
    time_num: Annotated[int, Field(default=30, gt=0, lt=366)]
    include_parts: Annotated[List[str], Field(default_factory=list)]
    exclude_parts: Annotated[List[str], Field(default_factory=list)]
    axie_class: Annotated[List[Axie_Classes], Field(default_factory=list)]
    level: Annotated[List[int], Field(default_factory=lambda: [1, 60])]
    breed_count: Annotated[List[int], Field(default_factory=lambda: [0, 7])]
    evolved_parts_count: Annotated[List[int], Field(default_factory=lambda: [0, 6])]
    collections: Annotated[List[CollectionWrapper], Field(default_factory=list)]

    @field_validator("level")
    @classmethod
    def validate_level(cls, v):
        return validate_two_number_range(v, 1, 60, "level")
    
    @field_validator("breed_count")
    @classmethod
    def validate_breed_count(cls, v):
        return validate_two_number_range(v, 0, 7, "breed_count")
    
    @field_validator("evolved_parts_count")
    @classmethod
    def validate_evolved_parts_count(cls, v):
        return validate_two_number_range(v, 0, 6, "evolved_parts_count")
