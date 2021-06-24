def decorator(func):
    def return_decorator():
        print("Before calling func")
        func()
        print("After calling func")

    return return_decorator


def decorator_arg():
    print("decorator as argument")


dc = decorator(decorator_arg)
dc()
