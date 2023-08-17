from jamdict import Jamdict

jam = Jamdict(memory_mode=True)
#jam = Jamdict(memory_mode=True) #Runs much faster after the first query that may take a minute!

def test_something() -> None:
    #print(jam.lookup("下さい"))
    #print(jam.lookup("くださる"))
    lookup = jam.lookup("ましょう")
    print(lookup)


def test_pos() -> None:
    for pos in jam.all_pos():
        print(pos)  # pos is a string

def test_name() -> None:
    for ne_type in jam.all_ne_type():
        print(ne_type)  # ne_type is a string

