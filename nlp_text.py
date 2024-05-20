#starter vars
file_path = "essays/[Tam] TR Arg #3 Highlights.txt"
content = ""
phrases = "important"

#open file & read
with open(file_path, "r") as file:
    content = file.read()

print(content)