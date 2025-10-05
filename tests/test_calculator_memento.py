import datetime
from decimal import Decimal
import pytest
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_creation():
    """Test the basic creation of a CalculatorMemento object."""
    calc1 = Calculation(operation="Addition", operand1=Decimal("1"), operand2=Decimal("2"))
    history = [calc1]
    memento = CalculatorMemento(history=history)

    assert memento.history == history
    assert isinstance(memento.timestamp, datetime.datetime)


def test_memento_to_dict():
    """Test the serialization of a CalculatorMemento to a dictionary."""
    # Arrange: Create a memento with a populated history
    calc1 = Calculation(operation="Addition", operand1=Decimal("10"), operand2=Decimal("5"))
    calc2 = Calculation(operation="Subtraction", operand1=Decimal("20"), operand2=Decimal("3"))
    history = [calc1, calc2]
    memento = CalculatorMemento(history=history)

    # Act: Serialize the memento to a dictionary
    memento_dict = memento.to_dict()

    # Assert: Check the structure and content of the dictionary
    expected_dict = {
        'history': [calc1.to_dict(), calc2.to_dict()],
        'timestamp': memento.timestamp.isoformat()
    }
    assert memento_dict == expected_dict


def test_memento_to_dict_empty_history():
    """Test serializing a memento with an empty history list."""
    # Arrange: Create a memento with an empty history
    memento = CalculatorMemento(history=[])

    # Act: Serialize the memento
    memento_dict = memento.to_dict()

    # Assert: The history list in the dictionary should be empty
    expected_dict = {
        'history': [],
        'timestamp': memento.timestamp.isoformat()
    }
    assert memento_dict == expected_dict


def test_memento_from_dict():
    """Test deserializing a dictionary back into a CalculatorMemento object."""
    # Arrange: Create a dictionary representing a serialized memento
    now = datetime.datetime.now()
    memento_data = {
        'history': [
            {'operation': 'Addition', 'operand1': '1', 'operand2': '2', 'result': '3', 'timestamp': now.isoformat()}
        ],
        'timestamp': now.isoformat()
    }

    # Act: Deserialize the dictionary
    memento = CalculatorMemento.from_dict(memento_data)

    # Assert: Check that the new memento object has the correct data
    assert isinstance(memento, CalculatorMemento)
    assert len(memento.history) == 1
    assert isinstance(memento.history[0], Calculation)
    assert memento.history[0].result == Decimal('3')
    assert memento.timestamp == now


def test_memento_from_dict_empty_history():
    """Test deserializing a memento with an empty history."""
    now = datetime.datetime.now()
    memento_data = {'history': [], 'timestamp': now.isoformat()}

    memento = CalculatorMemento.from_dict(memento_data)

    assert isinstance(memento, CalculatorMemento)
    assert memento.history == []
    assert memento.timestamp == now


def test_memento_from_dict_missing_key():
    """Test that deserializing with a missing key raises a KeyError."""
    memento_data = {'history': []}  # Missing 'timestamp' key
    with pytest.raises(KeyError):
        CalculatorMemento.from_dict(memento_data)
