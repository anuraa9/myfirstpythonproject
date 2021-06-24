class Animal:
    def __init__(self):
        print("Animal Created")

    def whoami(self):
        print("Animal")

    def eat(self):
        print("Eating")


class Dog(Animal):
    def __init__(self):
        Animal.__init__(self)
        print("Dog Created")

    def bark(self):
        print("Woof")

    def eat(self):
        print("Dog Eating")


mydog = Dog()
mydog.whoami()
mydog.eat()
mydog.bark()