from enum import Enum


class Choices(Enum):
    """Class for creating enumerated choices."""

    def __str__(self):
        return str(self.value)


class IntChoices(int, Choices):
    """Class for creating enumerated int choices"""


class StrChoices(str, Choices):
    """Class for creating enumerated string choices.

    StrChoices class allows for simpler string comparisons. Here are some examples of
    use cases that make StrChoices better than a regular Enum:

    # Enum comparison to string fails
    >>> from enum import Enum
    >>> class TestEnum(Enum):
    ...     ABC = 'abc'
    ...
    >>> TestEnum.ABC == 'abc'
    False

    # StrChoice comparison to string succeeds
    >>> from enso_utils.enums.choices import StrChoices
    >>> class TestStrChoices(StrChoices):
    ...     ABC = 'abc'
    ...
    >>> TestStrChoices.ABC == 'abc'
    True

    # using Enum as dict key doesn't work as expected
    >>> EnumDict = {TestEnum.ABC: 'blah'}
    >>> EnumDict['abc']
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    KeyError: 'abc'
    >>> EnumDict[TestEnum.ABC]
    'blah'

    # using StrChoices as dict key works as expected
    >>> StrChoiceDict = {TestStrChoices.ABC: 'boom'}
    >>> StrChoiceDict['abc']
    'boom'
    >>> StrChoiceDict[TestStrChoices.ABC]
    'boom'
    """
