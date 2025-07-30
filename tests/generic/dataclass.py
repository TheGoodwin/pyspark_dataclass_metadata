from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from dataclass_metadata.dataset_schema import DatasetSchema


@dataclass
class GenericDatasetSchema(DatasetSchema):
    """A Generic DatasetSchema created as a DataClass"""

    column_1: str = field(
        metadata={
            "description": "This is the first column",
        }
    )

    column_2: str = field(
        metadata={
            "description": "This is the second column",
        }
    )
