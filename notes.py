# object oriented programming

# (define-struct dog [fur_color name age favorite_food])

class Dog:
    def __init__(self, fur_color, name, age, favorite_food):
        self.fur_color = fur_color
        self.name = name
        self.age = age
        self.favorite_food = favorite_food

    def __str__(self):
        return f"{self.name} is a {self.fur_color} dog, \n{self.age} years old, and loves {self.favorite_food}."

    def __add__(self, other):
        if isinstance(other, Dog):
            return Dog(
                fur_color=f"{self.fur_color} and {other.fur_color}",
                name=f"{self.name} and {other.name}",
                age=max(self.age, other.age),
                favorite_food=f"{self.favorite_food} and {other.favorite_food}"
            )
        return NotImplemented

    def bark(self):
        return "Woof!"

    def eat(self):
        return f"{self.name} is eating {self.favorite_food}."

    def birthday(self):
        self.age += 1
        return f"Happy Birthday {self.name}! You are now {self.age} years old."

logan = Dog("black", "Logan", 10, "salmon")
print(logan.bark())
print(logan.eat())
print(logan.birthday())

pepper = Dog("black and brown", "Pepper", 12, "kibble")
print(pepper.bark())
print(pepper.eat())
print(pepper.birthday())
print(pepper)

roman = Dog("black", "Roman", 2, "lamb")
print(roman)

twoDogs = logan + pepper
print(twoDogs)