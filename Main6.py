def new_decorator(func):

    def wrap_func():
        print("CODE here before executing func")
        func()
        print("FUNC() has been called")

    return wrap_func


# def func_needs_decorator():
#     print("This function is in need of decorator")
#
#
# func_needs_decorator1 = new_decorator(func_needs_decorator)
# func_needs_decorator1()

# @new_decorator
# def func_needs_decorator():
#     print("This function is in need of decorator")
#
#
# func_needs_decorator()