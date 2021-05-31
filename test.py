maze = []
with open("maze.txt", "r") as mazeFile:
    row: int = 0
    for line in mazeFile:
        l = []
        for col in range(len(line)):
            letter: str = line[col]
            l.append(letter)
        maze.append(l)
        row+=1
