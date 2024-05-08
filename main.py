import os

content = "Hello World"
file_path = "/home/ubuntu/Desktop/hello.txt"

try:
    with open(file_path, 'w') as file:
        file.write(content)
    print("File 'hello.txt' created successfully at /home/ubuntu/Desktop.")
except FileNotFoundError:
    print("Error: The specified directory '/home/ubuntu/Desktop' does not exist.")
except PermissionError:
    print("Error: Permission denied to write to '/home/ubuntu/Desktop'.")
except Exception as e:
    print("An error occurred:", e)

