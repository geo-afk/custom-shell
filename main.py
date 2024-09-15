from typing import Dict
from sys import platform
from subprocess import run

# print(platform.system())

file_operations = {

    "create": ["echo. >", "touch"],
    "delete": [],
    "rename": []

}

output = run(["powershell", "touch", "rand.txt"],
             capture_output=True, text=True)

print(output.stdout)

# user_input = input(">> ")

# input_list = user_input.split(" ")

# if file_operations[input_list[0]]:
#     commands = file_operations[input_list[0]][0] + " "+input_list[1]
#     print(commands)
#     output = run(["powershell", "echo. ", ">", "rand.txt"],
#                  capture_output=True, text=True)

#     if output.returncode == 0:
#         print(output.stdout)

#     print(output.args)
