import unittest
from pyspark.sql import DataFrame, SparkSession
from tests.generic.dataclass import GenericDatasetSchema
from dataclasses import asdict, dataclass, field
from pyspark_dataclass_metadata.metadata_updater import MetadataUpdater
from pyspark.sql.types import StructType, StructField


class TestStringMethods(unittest.TestCase):

    spark: SparkSession

    @classmethod
    def setUpClass(cls):
        cls.spark: SparkSession = (
            SparkSession.builder.master("local[*]")
            .config("spark.driver.bindAddress", "localhost")
            .config("spark.ui.port", "4050")
            .config("spark.driver.memory", "8g")
            .appName("dataclass-metadata")
            .getOrCreate()
        )

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_update_dataset_metadata(self):
        # GIVEN
        sample: list[GenericDatasetSchema] = [
            GenericDatasetSchema("value 1 of column 1", "value 1 of column 2"),
            GenericDatasetSchema("value 2 of column 1", "value 2 of column 2"),
        ]

        df: DataFrame = self.spark.createDataFrame([asdict(s) for s in sample])

        updater: MetadataUpdater = MetadataUpdater()

        # WHEN
        actualDf: DataFrame = updater.update_dataset_metadata(
            dataframe=df, dataset_schema_class=GenericDatasetSchema
        )

        # THEN

        # Get the fields of the updated DataFrame
        actualSchema: StructType = actualDf.schema
        field1: StructField = actualSchema.fields[0]
        field2: StructField = actualSchema.fields[1]

        # Check metadata exists
        self.assertTrue("description" in field1.metadata)
        self.assertTrue("description" in field2.metadata)

        # Check metadata is the one requested
        self.assertEquals(field1.metadata["description"], "This is the first column")
        self.assertEquals(field2.metadata["description"], "This is the second column")

    def test_update_dataset_metadata_not_subclass(self):
        # GIVEN
        @dataclass
        class GenericSchemaNotSubclass:
            """A Generic Schema created as a DataClass but not as a DatasetSchema"""

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

        sample: list[GenericSchemaNotSubclass] = [
            GenericSchemaNotSubclass("value 1 of column 1", "value 1 of column 2"),
            GenericSchemaNotSubclass("value 2 of column 1", "value 2 of column 2"),
        ]

        df: DataFrame = self.spark.createDataFrame([asdict(s) for s in sample])

        updater: MetadataUpdater = MetadataUpdater()

        # WHEN
        with self.assertRaises(TypeError) as context:
            updater.update_dataset_metadata(
                dataframe=df, dataset_schema_class=GenericSchemaNotSubclass
            )

        # THEN

        self.assertEquals(
            "GenericSchemaNotSubclass is not a subclass of DatasetSchema",
            str(context.exception),
        )
