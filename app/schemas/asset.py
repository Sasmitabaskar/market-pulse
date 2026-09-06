from pydantic import BaseModel, ConfigDict, Field, field_validator

class AssetCreate(BaseModel):
    symbol: str = Field(
        min_length=1,
        max_length=20,
    )
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, value: str) -> str:
        value = value.strip().upper()

        if not value:
            raise ValueError("Symbol cannot be empty or whitespace")

        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty or whitespace")

        return value

class AssetResponse(BaseModel):
    id: int
    symbol: str
    name: str

    model_config = ConfigDict(from_attributes=True)

class AssetUpdate(BaseModel):
    symbol: str = Field(
        min_length=1,
        max_length=20,
    )
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, value: str) -> str:
        value = value.strip().upper()

        if not value:
            raise ValueError("Symbol cannot be empty or whitespace")

        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty or whitespace")

        return value