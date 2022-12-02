from pandas import DataFrame, read_csv, Index
from dataclasses import dataclass

@dataclass
class EqualityCondition:
    """# `EqualityCondition`
    A class that represents a single equality condition. Similiar to a term in a SQL `WHERE` clause:

    This class'
    ```Python
    EqualityCondition(col1, [val1, val2, ...])
    ```

    is roughly equivalent to SQL's:

    ```SQL
    WHERE col1 IN (val1, val2, ...)
    ```
    
    A list of `EqualityCondition` is equivalent to having `AND` between each SQL-statement
    """
    column: str
    values: list[str]

class Querier:
    """# `Querier`
    A class that takes a .csv file path to open it and and stores it as a dataframe to do SQL-inspired queries upon 
    using the `Querier.query(list[str], list[EqualityCondition])` function.
    """
    def __init__(self, csv_file: str):
        """ # `Querier`
        Initialise the `Querier` class.

        ## Args:
            - `csv_file (str)`: A path to a .csv file.
        """
        self.dataframe = read_csv(csv_file)
        self.projections = []
        self.conditions = []

        # Cache columns and unique values in each column

        self.__columns = self.dataframe.columns.to_list()

        self.__uniques = dict()
        for column in self.__columns:
            self.__uniques[column] = self.dataframe[column].unique()

    def columns(self) -> list[str]:
        """# `columns`
        Returns the names of the columns in the data frame as a list of strings

        ## Returns:
            list[str]: A list of strings of the columns in the data frame
        """
        return self.__columns

    def uniques(self, column: str, string = True) -> list:
        """# `uniques`
        Given a column name, return the unique values in that column

        ## Args:
            column (str): A name of a column in the data frame

        ## Returns:
            list[str]: A list of unique values in the given column
        """

        if not column:
            return []

        if string:
            return [str(x) for x in self.__uniques[column]]
        
        return self.__uniques[column]

    def query(self, projections: list[str] = [], conditions: list[EqualityCondition] = []) -> DataFrame:
        """# `query` 
        Given the list projections (read as 'SELECT col1, col2, ...') and conditions (as 'WHERE col1 IN (val1, val2, ...) AND col2 IN ...'), returns the stored 
        dataframe modified by the query options.

        ## Args:
            - `projections (list[str], optional)`: A list of the columns to project. Defaults to `[]`.
            - `conditions (list[EqualityCondition], optional)`: A list of conditions to apply to each tuple in the dataframe. Defaults to `[]`.
        """

        conditions_query = self.__condition_merger(conditions)
        result = self.dataframe.query(conditions_query)[projections]

        return result

    def __condition_merger(conditions: list[EqualityCondition] = []) -> str:
        """# `__condition_merger`
        Converts a list of conditions to a single query string

        ## Args:
            - `conditions (list[EqualityCondition], optional)`: A list of conditions to convert to a query string. Defaults to [].

        Returns:
            str: A string that can be used to in the Pandas' `DataFrame.query` function.
        """

        stringified_conditions = []
        for condition in conditions:
            stringified_conditions.append(f"{condition.column} in ({condition.values})")

        return " and ".join(stringified_conditions)