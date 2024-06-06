import json

with open("pickle-test/error_dict.txt", "r") as f:
    error_dict = json.load(f)

for error in error_dict:
    print(error)
    for vs in error_dict[error]:
        print(f"  {vs}")