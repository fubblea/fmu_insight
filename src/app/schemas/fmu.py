from dataclasses import dataclass
from typing import Self

from fmpy.model_description import ScalarVariable


@dataclass
class FmuParameter:
    _raw: ScalarVariable
    name: str
    unit: str
    type: str
    default_value: str | float

    @classmethod
    def from_scalar_variable(cls, v: ScalarVariable) -> Self:
        try:
            default = float(v.start)
        except (TypeError, ValueError):
            default = v.start

        return cls(
            _raw=v,
            name=v.name,
            unit=v.unit,
            type=v.type,
            default_value=default,
        )


@dataclass
class FmuInput:
    _raw: ScalarVariable
    name: str
    unit: str
    type: str

    @classmethod
    def from_scalar_variable(cls, v: ScalarVariable) -> Self:
        return cls(
            _raw=v,
            name=v.name,
            unit=v.unit,
            type=v.type,
        )


@dataclass
class FmuOutput:
    _raw: ScalarVariable
    name: str
    unit: str
    type: str

    @classmethod
    def from_scalar_variable(cls, v: ScalarVariable) -> Self:
        return cls(
            _raw=v,
            name=v.name,
            unit=v.unit,
            type=v.type,
        )
