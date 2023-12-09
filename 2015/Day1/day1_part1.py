import os

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        line = file.readline()
        up, down = line.count('('), line.count(')')
        print(up - down)