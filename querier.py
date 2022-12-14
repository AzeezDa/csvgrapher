from pandas import DataFrame, read_csv, Index
from dataclasses import dataclass
from numpy import int64
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
    values: list

    def __str__(self) -> str:
        return f"{self.column} in {self.values}"

class Querier:
    """# `Querier`
    A class that takes a .csv file path to open it and and stores it as a dataframe to do SQL-inspired queries upon 
    using the `Querier.query(list[str], list[EqualityCondition])` function.
    """
    def __init__(self, in_data: str | DataFrame):
        """ # `Querier`
        Initialise the `Querier` class.

        ## Args:
            - `csv_file (str)`: A path to a .csv file.
        """

        if isinstance(in_data, str):
            self.__dataframe = read_csv(in_data)
        elif isinstance(in_data, DataFrame):
            self.__dataframe = in_data
        else:
            return None

        # Cache columns and unique values in each column

        self.__columns = self.__dataframe.columns.to_list()

        self.__uniques = dict()
        for column in self.__columns:
            self.__uniques[column] = self.__dataframe[column].unique()

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

    def dataframe(self) -> DataFrame:
        """# `dataframe`

        Returns:
            `DataFrame`: The underlying pandas dataframe
        """
        return self.__dataframe

    def incorporate_dtype(self, column: str, values: list[str]) -> list:
        """# `incorporate_dtypes`
        Takes a list of strings and a column name then returns a list of the same values but convereted to datatype from the column they came from.
        This is used to transform strings on the Qt list widgets into data with the correct data types used in the plots or queries.
        ## Args:
            `column (str)`: The column from which the values come from
            `values (list[str])`: A list of values to change the data type of

        ## Returns:
            `list`: A list with values converted to their actual data type
        """
        converted_values = values
        try:
            if self.__dataframe.dtypes[column] == int64:
                converted_values = [int64(x) for x in values]
        except:
            return values

        return converted_values

    def query(self, projections: list[str] = [], conditions: list[EqualityCondition] = []) -> DataFrame:
        """# `query` 
        Given the list projections (read as 'SELECT col1, col2, ...') and conditions (as 'WHERE col1 IN (val1, val2, ...) AND col2 IN ...'), returns the stored 
        dataframe modified by the query options.

        ## Args:
            - `projections (list[str], optional)`: A list of the columns to project. Defaults to `[]`.
            - `conditions (list[EqualityCondition], optional)`: A list of conditions to apply to each tuple in the dataframe. Defaults to `[]`.
        """
        stringified_conditions = []
        for condition in conditions:
            stringified_conditions.append(str(condition))
        conditions_query = " & ".join(stringified_conditions)

        result = self.__dataframe.query(conditions_query)
        result = result[projections]

        return result