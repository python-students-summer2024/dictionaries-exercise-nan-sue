"""
Functions necessary for running a virtual cookie shop.
See README.md for instructions.
Do not run this file directly.  Rather, run main.py instead.
"""
import csv

def bake_cookies(filepath):
    """
    Opens up the CSV data file from the path specified as an argument.
    - Each line in the file, except the first, is assumed to contain comma-separated information about one cookie.
    - Creates a dictionary with the data from each line.
    - Adds each dictionary to a list of all cookies that is returned.

    :param filepath: The path to the data file.
    :returns: A list of all cookie data, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    cookies = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cookie = {
                'id': int(row['id']),
                'title': row['title'],
                'description': row['description'],
                'price': float(row['price'].strip('$'))
            }
            cookies.append(cookie)
    return cookies


def welcome():
    """
    Prints a welcome message to the customer in the format:

      Welcome to the Python Cookie Shop!
      We feed each according to their need.

    """
    # write your code for this function below this line
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.\n")


def display_cookies(cookies):
    """
    Prints a list of all cookies in the shop to the user.
    - Sample output - we show only two cookies here, but imagine the output continues for all cookiese:
        Here are the cookies we have in the shop for you:

          #1 - Basboosa Semolina Cake
          This is a This is a traditional Middle Eastern dessert made with semolina and yogurt then soaked in a rose water syrup.
          Price: $3.99

          #2 - Vanilla Chai Cookie
          Crisp with a smooth inside. Rich vanilla pairs perfectly with its Chai partner a combination of cinnamon ands ginger and cloves. Can you think of a better way to have your coffee AND your Vanilla Chai in the morning?
          Price: $5.50

    - If doing the extra credit version, ask the user for their dietary restrictions first, and only print those cookies that are suitable for the customer.

    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below this line
    print("Here are the cookies we have in the shop for you:\n")

    for cookie in cookies:
        line1 = f"#{cookie['id']} - {cookie['title']}"
        line2 = cookie['description']
        line3 = f"Price: ${cookie['price']:.2f}"
        
        print(line1)
        print(line2)
        print(f"{line3}\n")


def get_cookie_from_dict(id, cookies):
    """
    Finds the cookie that matches the given id from the full list of cookies.

    :param id: the id of the cookie to look for
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: the matching cookie, as a dictionary
    """
    # write your code for this function below this line
    for cookie in cookies:
        if cookie['id'] == id:
            return cookie
    return None


def solicit_quantity(id, cookies):
    """
    Asks the user how many of the given cookie they would like to order.
    - Validates the response.
    - Uses the get_cookie_from_dict function to get the full information about the cookie whose id is passed as an argument, including its title and price.
    - Displays the subtotal for the given quantity of this cookie, formatted to two decimal places.
    - Follows the format (with sample responses from the user):

        My favorite! How many Animal Cupcakes would you like? 5
        Your subtotal for 5 Animal Cupcake is $4.95.

    :param id: the id of the cookie to ask about
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: The quantity the user entered, as an integer.
    """
    # write your code for this function below this line
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
    """
    Takes the complete order from the customer.
    - Asks over-and-over again for the user to enter the id of a cookie they want to order until they enter 'finished', 'done', 'quit', or 'exit'.
    - Validates the id the user enters.
    - For every id the user enters, determines the quantity they want by calling the solicit_quantity function.
    - Places the id and quantity of each cookie the user wants into a dictionary with the format
        {'id': 5, 'quantity': 10}
    - Returns a list of all sub-orders, in the format:
        [
          {'id': 5, 'quantity': 10},
          {'id': 1, 'quantity': 3}
        ]

    :returns: A list of the ids and quantities of each cookies the user wants to order.
    """
    # write your code for this function below this line
    orders = []

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
                orders.append({'id': cookie_id, 'quantity': cookie_num})
        else:
            print("Sorry, the ID you entered is not valid. Please enter a valid cookie ID.")

    return orders


def display_order_total(order, cookies):
    """
    Prints a summary of the user's complete order.
    - Includes a breakdown of the title and quantity of each cookie the user ordereed.
    - Includes the total cost of the complete order, formatted to two decimal places.
    - Follows the format:

        Thank you for your order. You have ordered:

        -8 Animal Cupcake
        -1 Basboosa Semolina Cake

        Your total is $11.91.
        Please pay with Bitcoin before picking-up.

        Thank you!
        -The Python Cookie Shop Robot.

    """
    # write your code for this function below this line
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
    """
    Executes the cookie shop program, following requirements in the README.md file.
    - This function definition is given to you.
    - Do not modify it!

    :param cookies: A list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    welcome()
    display_cookies(cookies)
    order = solicit_order(cookies)
    display_order_total(order, cookies)
