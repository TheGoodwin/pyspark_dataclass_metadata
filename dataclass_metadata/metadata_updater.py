from pyspark.sql import DataFrame
from typing import Type, TypeVar
from dataset_schema import DatasetSchema
from dataclasses import fields

T = TypeVar("T", bound=DatasetSchema)


class MetadataUpdater:
    """Class aiming at updating metadata of a DataFrame object from a dataclass with metadata"""

    def __init__(self):
        pass

    def update_dataset_metadata(
        dataframe: DataFrame, dataset_schema_class: Type[T]
    ) -> DataFrame:
        dataset_schema_fields: tuple = fields(dataset_schema_class)

        for field in dataset_schema_fields:
            field_name: str = field.name
            metadata: dict = field.metadata

            dataframe.withMetadata(field_name, metadata)
