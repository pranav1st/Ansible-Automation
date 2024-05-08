import os

content = "Hello World"
file_path = "/home/Ubuntu/Desktop/hello.txt"

try:
    with open(file_path, 'w') as file:
        file.write(content)
    print("File 'hello.txt' created successfully at /home/Ubuntu/Desktop.")
except FileNotFoundError:
    print("Error: The specified directory '/home/Ubuntu/Desktop' does not exist.")
except PermissionError:
    print("Error: Permission denied to write to '/home/Ubuntu/Desktop'.")
except Exception as e:
    print("An error occurred:", e)
