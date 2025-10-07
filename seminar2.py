def create_city(city_name:str, city_pop:int, city_county:str) ->dict:
    # city represented as a pyhton dictionary
    # "city" -> key, city_name-> value,(actual city name as str)
    return {"city": city_name, "population": city_pop, "county": city_county}

def get_city_name(city: dict) -> str:
    return city["city"]

def get_city_pop(city: dict) -> int:
    return city["population"]

def get_city_county(city: dict) -> str:
    return city["county"]


def print_menu() -> None:
    print("1. Sort the cities")
    print("2. Display the list of cities")
    print("3. Search for a city (using partial, case-insensitve str matching)")
    print("4. Add a city from the console")
    print("5. Add a number of random cities to the list (the number is read from the console)")
    print("6. Quit")

def start():
    while True:
        print_menu()

        option = int(input("Enter your choice: "))
        if option == 1:
            continue
        elif option == 6:
            # exist the nearest running loop
            break
        else:
            print("Invalid choice")

# represent a city using a list
# What is a list?
# each element has a predecessor and a succesor
# elements can be accesed by their index (list is sorted)

#vatra_dornei = ["Vatra Dornei", 10000, "Suceava"]
#print("City name: " + vatra_dornei[0])

# represent the city using a dict
# what is a dict?
# pairs of keys/values elements where keys aree unique and (in python) immutable (numbers, str, tuples)
# there is no ordering, so no accesing elements using their index
"""""
suceava_as_list = ["Suceava", 100000, "Suceava"]
suceava_as_dict = {"city name": "Suceava", "city_population": 100000, "city_county": "Suceava"}
print("City name: " + suceava_as_dict["city name"])

x = create_city("Vatra Dornei", 10000, "Suceava")

print(type(x))
print(x)

print("City name: " + get_city_name(x))
"""""
start()


