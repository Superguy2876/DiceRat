### Dice Class

This class represents a single type of dice, with a specified number of sides and a quantity of that dice type.

#### Constructor: `__init__(self, sides=20, quantity=1)`

Parameters:
- `sides` (default=20): The number of sides on the dice.
- `quantity` (default=1): The number of dice of this type. Use a negative value for negative dice (e.g., `-3` would mean subtracting the total of 3 dice).

Raises:
- `ValueError`: If the number of sides is less than 1 or the quantity is 0.

#### Methods:

- `roll()`: Rolls all the dice of this type and updates the values and total.
- `reroll(func: callable)`: Re-rolls the dice values that satisfy the provided function `func`. `func` should take a single integer argument (the dice value) and return a boolean.
- Arithmetic methods (`__add__`, `__sub__`, etc.): Allows dice objects to be used in arithmetic operations.

#### Example Usage:

```python
    dice = Dice(sides=6, quantity=3)
    dice.roll()
    print(dice.values)  # returns values of each individual dice
    print(dice.total)   # returns the total of all dice values
```

### DicePool Class

This class represents a collection (pool) of different dice types, and constants.

#### Constructor: `__init__(self, dice_string=None)`

Parameters:
- `dice_string`: A string representation of the dice pool, e.g., "d20 + d6 - 3d4 + 5 - 2".

#### Methods:

- `add_dice_string(dice_string)`: Adds more dice and constants to the pool based on the provided string.
- `roll()`: Rolls all the dice in the pool and updates their values and the total of the pool.
- `reroll(func: callable)`: Re-rolls the dice in the pool whose values satisfy the provided function `func`. `func` should take a single integer argument (the dice value) and return a boolean.
- `look()`: Returns a list of dictionaries (for dice) and integers (for constants). Each dictionary contains information about the dice type, such as sides, quantity, values, and total.

#### Example Usage:

```python
    dice_string = "d20 + d6 - 3d4 + 5 - 2"
    dice_pool = DicePool(dice_string)
    print(dice_pool)  # prints: d20 + d6 + -3d4 + 5 + -2

    dice_pool.roll()
    print(dice_pool.look())  # displays values of all dice and constants
```

Notes:
- The DicePool class can handle both dice and constants. For instance, "d20 + 5" represents a d20 dice and a constant of 5.
- When adding dice to the pool, the order matters. "d20 + d6" will add a d20 and a d6 dice, while "d6 + d20" will add a d6 followed by a d20.
- The look method in the DicePool class provides a detailed view of each dice type and their current values in the pool.