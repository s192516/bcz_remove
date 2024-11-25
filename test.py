



def print_function_name(func):
    def wrapper(*args, **kwargs):
        print(f"Function name: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class SomeClass:
    def __init__(self, *args, **kwargs):
        print(f"Class name: {self.__class__.__name__}")
        # 其他初始化代码

@print_function_name
def example_function():
    print("This is an example function.")

class ExampleClass:
    def __init__(self):
        print(f"Class name: {self.__class__.__name__}")

    @print_function_name
    def example_method(self):
        print("This is an example method.")

# 测试
example_function()

example_instance = ExampleClass()
example_instance.example_method()