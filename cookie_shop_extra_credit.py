import csv

def bake_cookies(filepath):
    cookies = []
    with open(filepath, 'r') as file:
        read_file = csv.DictReader(file)
        for row in read_file:
            cookie = {
                'id': int(row['id']),
                'title': row['title'],
                'description': row['description'],
                'price': float(row['price'].strip('$')),
                'sugar_free': row['sugar_free'].lower() == 'true',
                'gluten_free': row['gluten_free'].lower() == 'true',
                'contains_nuts': row['contains_nuts'].lower() == 'true'
            }
            cookies.append(cookie)
    return cookies

def welcome():
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.\n")
    allergies = {}
    nut_response = input("Are you allergic to nuts? (yes/no): ").strip().lower()
    gluten_response = input("Are you allergic to gluten? (yes/no): ").strip().lower()
    sugar_response = input("Do you suffer from diabetes? (yes/no): ").strip().lower()
    allergies['nuts'] = nut_response in ['yes', 'y']
    allergies['gluten'] = gluten_response in ['yes', 'y']
    allergies['sugar'] = sugar_response in ['yes', 'y']
    return allergies

def display_cookies(cookies, allergies):
    print("Here are the cookies we have in the shop for you:\n")    
    
    for cookie in cookies:
        if allergies['nuts'] and cookie['contains_nuts']:
            continue
        if allergies['gluten'] and not cookie['gluten_free']:
            continue
        if allergies['sugar'] and not cookie['sugar_free']:
            continue
        
        line1 = f"#{cookie['id']} - {cookie['title']}"
        line2 = cookie['description']
        line3 = f"Price: ${cookie['price']:.2f}"
        
        print(line1)
        print(line2)
        print(f"{line3}\n")

def get_cookie_from_dict(id, cookies):
    # write your code for this function below this line
    for cookie in cookies:
        if cookie['id'] == id:
            return cookie
    return None

def solicit_quantity(id, cookies):
    cookie = get_cookie_from_dict(id, cookies)
    if not cookie:
        print(f"Sorry, the cookie you ordered with id {id} not found here.")
        return 0

    quantity_int = False
    while not quantity_int:
        try:
            num_cookies = input(f"My favorite! How many {cookie['title']} would you like? ")
            int_num_cookies = int(num_cookies)
            if int_num_cookies <= 0:
                print("Sorry, the quantity is invalid. Please enter a positive quantity.")
            else:
                total_price = int_num_cookies * cookie['price']
                print(f"Your subtotal for {int_num_cookies} {cookie['title']}(s) is ${total_price:.2f}.")
                quantity_int = True
                return int_num_cookies
        except ValueError:
            print("Sorry, the quantity is invalid. Please enter a positive quantity.")


def solicit_order(cookies):
    user_orders = []

    while True:
        user_response = input("Please enter the number of any cookie you would like to purchase (or type 'finished', 'done', 'quit', or 'exit' to complete your order): ").lower()
        if user_response in ['finished', 'done', 'quit', 'exit']:
            break

        try:
            cookie_id = int(user_response)
        except ValueError:
            print("Sorry, the ID you entered is not valid. Please enter a valid cookie ID.")
            continue

        cookie = get_cookie_from_dict(cookie_id, cookies)
        if cookie:
            cookie_num = solicit_quantity(cookie_id, cookies)
            if cookie_num > 0:
                user_orders.append({'id': cookie_id, 'quantity': cookie_num})
        else:
            print("Sorry, the ID you entered is not valid. Please enter a valid cookie ID.")

    return user_orders


def display_order_total(order, cookies):
    print("\nThank you for your order. You have ordered:\n")

    sum_price = 0
    for thing in order:
        cookie = get_cookie_from_dict(thing['id'], cookies)
        if cookie:
            quantity = thing['quantity']
            title = cookie['title']
            print(f"- {quantity} {title}")
            price = cookie['price']
            total_price = quantity * price
            sum_price += total_price

    sum_price_output = f"\nYour total is ${sum_price:.2f}."
    payment_method = "Please pay with Bitcoin before picking-up."
    ending = "\nThank you!\n-The Python Cookie Shop Robot."
    print(sum_price_output)
    print(payment_method)
    print(ending)


def run_shop(cookies):
    allergies = welcome()
    display_cookies(cookies, allergies)
    order = solicit_order(cookies)
    display_order_total(order, cookies)



