from pyspark.sql import DataFrame
from typing import Type, TypeVar
from pyspark_dataclass_metadata.dataset_schema import DatasetSchema
from dataclasses import fields

T = TypeVar("T", bound=DatasetSchema)


class MetadataUpdater:
    """Class aiming at updating metadata of a DataFrame object from a dataclass with metadata"""

    def __init__(self):
        pass

    def update_dataset_metadata(
        self, dataframe: DataFrame, dataset_schema_class: Type[T]
    ) -> DataFrame:
        # Check for subclass
        if not issubclass(dataset_schema_class, DatasetSchema):
            raise TypeError(
                f"{dataset_schema_class.__name__} is not a subclass of DatasetSchema"
            )

        result_dataframe: DataFrame = dataframe

        dataset_schema_fields: tuple = fields(dataset_schema_class)

        for field in dataset_schema_fields:
            field_name: str = field.name
            metadata: dict = dict(field.metadata)

            result_dataframe = result_dataframe.withMetadata(field_name, metadata)
        return result_dataframe
