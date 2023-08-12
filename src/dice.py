import random
import re

class Dice:
    def __init__(self, sides=20, quantity=1):
        if sides < 1:
            raise ValueError("Number of sides must be positive")
        if quantity == 0:
            raise ValueError("Quantity of dice must non-zero")
        self.sides = sides
        self.quantity = abs(quantity)
        self.sign = -1 if quantity < 0 else 1
        self.values = [1 * self.sign for _ in range(self.quantity)]
        self.total = self.quantity * self.sign

    def roll(self):
        self.values = [random.randint(1, self.sides) * self.sign for _ in range(self.quantity)]
        self.total = sum(self.values)
    
    def reroll(self, func: callable):
        for i in range(self.quantity):
            if func(self.values[i]):
                self.values[i] = random.randint(1, self.sides) * self.sign
        self.total = sum(self.values)
        

    def __str__(self):
        return f'{self.sign*self.quantity}d{abs(self.sides)}'

    def __repr__(self) -> str:
        return f'Dice(sides={self.sides}, quantity={self.quantity})'
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Dice):
            return self.sides == o.sides and self.quantity == o.quantity
        return False
    
    def __hash__(self) -> int:
        return hash((self.sides, self.quantity))
    
    
    def __add__(self, o: object):
        # allow adding dice like integers using the current total
        if isinstance(o, int):
            return self.total + o
        elif isinstance(o, Dice):
            return self.total + o.total
    
    def __radd__(self, o: object):
        return self.__add__(o)
    
    def __sub__(self, o: object):
        # allow subtracting dice like integers using the current total
        if isinstance(o, int):
            return self.total - o
        elif isinstance(o, Dice):
            return self.total - o.total
        
    def __rsub__(self, o: object):
        return self.__sub__(o)
    
    def __mul__(self, o: object):
        # allow multiplying dice like integers using the current total
        if isinstance(o, int):
            return self.total * o
        elif isinstance(o, Dice):
            return self.total * o.total
        
    def __rmul__(self, o: object):
        return self.__mul__(o)
    
    def __truediv__(self, o: object):
        # allow dividing dice like integers using the current total
        if isinstance(o, int):
            return self.total / o
        elif isinstance(o, Dice):
            return self.total / o.total
        
    def __rtruediv__(self, o: object):
        return self.__truediv__(o)
    
    def __floordiv__(self, o: object):
        # allow floor dividing dice like integers using the current total
        if isinstance(o, int):
            return self.total // o
        elif isinstance(o, Dice):
            return self.total // o.total
    
    def __rfloordiv__(self, o: object):
        return self.__floordiv__(o)
    

class DicePool:
    def __init__(self, dice_string=None):
        self.dice_constants = []
        self.total = 0

        if dice_string:
            self.add_dice_string(dice_string)


    def add_dice_string(self, dice_string):
            dice_constant_pattern = re.compile(r'(-?\d*)[dD](-?\d+)|(-?\d+)')

            dice_string = dice_string.replace(" ", "")  # removing spaces
            parts = dice_constant_pattern.findall(dice_string)
            
            for part in parts:
                if part[0] or part[1]:  # if first or second part exists, it's a dice set
                    # number of dice. if not specified, default is 1
                    num_dice = int(part[0]) if part[0] else 1
                    # create a dice object and add it to the pool
                    self.dice_constants.append(Dice(int(part[1]), num_dice))
                else:  # if no first or second part, it's a constant
                    self.dice_constants.append(int(part[2]))
            
            self.total = sum(self.dice_constants)

    def roll(self):
        for item in self.dice_constants:
            if isinstance(item, Dice):
                item.roll()
    
    def reroll(self, func: callable):
        for item in self.dice_constants:
            if isinstance(item, Dice):
                item.reroll(func)

    def look(self):
        return [{'sides': item.sides, 'quantity': item.quantity, 'values':item.values, 'total':item.total} if isinstance(item, Dice) else item for item in self.dice_constants]

    def __str__(self):
        return ' + '.join(str(item) for item in self.dice_constants)


# Testing the function
dice_string = "d20 + d6 - 3d4 + 5 - 2"
dice_pool = DicePool(dice_string)
print(dice_pool)  # should print: d20 + d6 + -3d4 + 5 + -2
print(dice_pool.total)
temp = dice_pool.look()
print(temp)
dice_pool.roll()
print(dice_pool)  # should print a list of numbers
print(temp)
print(dice_pool.look()) # should print a list of numbers

