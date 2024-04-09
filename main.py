import json
import os

# Function to load data from JSON file
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            data = json.load(file)
        return data
    else:
        return {'users': [], 'movies': []}

# Function to save data to JSON file
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

# Function to check if username is unique
def is_username_unique(username, data):
    for user in data['users']:
        if user['username'] == username:
            return False
    return True

# Function for user sign up
def sign_up(username, data):
    if is_username_unique(username, data):
        data['users'].append({'username': username, 'history': []})
        save_data(data)
        return True
    else:
        return False

# Function to log in
def log_in(username, data):
    for user in data['users']:
        if user['username'] == username:
            return user
    return None

# Function to book tickets
def book_tickets(user, movie_name, num_tickets, selected_seats, data):
    for movie in data['movies']:
        if movie['name'] == movie_name:
            for seat in selected_seats:
                if seat in movie['available_seats']:
                    movie['available_seats'].remove(seat)
                    user['history'].append({'movie': movie_name, 'seats': num_tickets})
            save_data(data)
            return True
    return False


# # Function to display available movies with their available seats
def display_movies(data):
    print("Available Movies:")
    for movie in data['movies']:
        print(f"Movie: {movie['name']}, Available Seats: {movie['available_seats']}")



# Function to add a new movie
def add_movie(data):
    movie_name = input("Enter the name of the new movie: ")
    available_seats = input("Enter available seats for the movie (comma-separated): ").split(",")
    data['movies'].append({'name': movie_name, 'available_seats': available_seats})
    save_data(data)
    print("Movie added successfully!")

# Function to display user history
def display_history(user):
    if user['history']:
        print("Your booking history:")
        for booking in user['history']:
            print(f"Movie: {booking['movie']}, Seats booked: {booking['seats']}")
    else:
        print("You haven't booked any tickets yet.")


def main():
    data = load_data()

    while True:
        print("\nWelcome to the Movie Ticketing System!")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Add Movie")
        print("4. Display Movies")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter a username: ")
            if sign_up(username, data):
                print("Sign up successful!")
            else:
                print("Username already exists. Please try again.")

        elif choice == '2':
            username = input("Enter your username: ")
            user = log_in(username, data)
            if user:
                while True:
                    print("\n1. Book Tickets")
                    print("2. View Booking History")
                    print("3. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        display_movies(data)
                        movie_name = input("Enter the name of the movie you want to book: ")
                        num_tickets = int(input("Enter the number of tickets you want to book: "))
                        selected_seats = []
                        for i in range(num_tickets):
                            seat = input(f"Enter seat number for ticket {i+1}: ")
                            selected_seats.append(seat)
                        if book_tickets(user, movie_name, num_tickets, selected_seats, data):
                            print("Tickets booked successfully!")
                        else:
                            print("Failed to book tickets. Please try again.")

                    elif user_choice == '2':
                        display_history(user)

                    elif user_choice == '3':
                        break

                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("User not found. Please sign up first.")

        elif choice == '3':
            add_movie(data)

        elif choice == '4':
            display_movies(data)

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
