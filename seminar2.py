#from dis import print_instructions


def create_city(city_name:str, city_pop:int, city_county:str) ->list:
    # city represented as a pyhton dictionary
    # "city" -> key, city_name-> value,(actual city name as str)

    # city as dict
    # return {"city": city_name, "population": city_pop, "county": city_county}

    # city as list
    return [city_name, city_pop, city_county]

def get_city_name(city: list) -> str:
    # return city["city"]
    return city[0]

def get_city_pop(city: list) -> int:
    # return city["population"]
    return city[1]

def get_city_county(city: list) -> str:
    # return city["county"]
    return city[2]

# we don't print - we return the str
def to_str(city: list) -> str:
    # return str of a city
    return "City name - " + get_city_name(city) + ", population - " + str(get_city_pop(city)) +", county - " + get_city_county(city)

def display_cities(city_list: list) -> None:
    for city in city_list:
        print(to_str(city))

def print_menu() -> None:
    print("1. Sort the cities")
    print("2. Display the list of cities")
    print("3. Search for a city (using partial, case-insensitve str matching)")
    print("4. Add a city from the console")
    print("5. Add a number of random cities to the list (the number is read from the console)")
    print("6. Quit")

def start():
    # let's hard code a few cities
    city_list = [create_city("Vatra Dornei",10_000,"Suceava"),
                 create_city("Deva",89_000,"Hunedoara"),
                 create_city("Piatra Neamt", 51_000,"Neamt")]
    print(city_list)
    while True:
        print_menu()

        option = int(input("Enter your choice: "))
        if option == 1:
            continue
        elif option == 2:
            display_cities(city_list)

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


