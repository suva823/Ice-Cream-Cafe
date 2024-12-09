import sqlite3

def initialize_db():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS seasonal_flavors (
                        id INTEGER PRIMARY KEY,
                        flavor_name TEXT NOT NULL,
                        description TEXT,
                        availability TEXT NOT NULL)
                    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredient_inventory (
                        id INTEGER PRIMARY KEY,
                        ingredient_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL)
                    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS customer_suggestions (
                        id INTEGER PRIMARY KEY,
                        flavor_suggestion TEXT,
                        allergy_concern TEXT)
                    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS allergens (
                        id INTEGER PRIMARY KEY,
                        allergen_name TEXT UNIQUE NOT NULL)
                    ''')

    conn.commit()
    conn.close()

def add_seasonal_flavor(flavor_name, description, availability):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO seasonal_flavors (flavor_name, description, availability) VALUES (?, ?, ?)',
                   (flavor_name, description, availability))
    conn.commit()
    conn.close()

def search_flavors(keyword):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM seasonal_flavors WHERE flavor_name LIKE ?', (f'%{keyword}%',))
    results = cursor.fetchall()
    conn.close()
    return results

def add_allergen(allergen_name):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO allergens (allergen_name) VALUES (?)', (allergen_name,))
        conn.commit()
        print(f"Allergen '{allergen_name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Allergen '{allergen_name}' already exists.")
    conn.close()

def main():
    initialize_db()

    print("Welcome to the Ice Cream Parlor Cafe!")
    while True:
        print("\nOptions:")
        print("1. Add Seasonal Flavor")
        print("2. Search Flavors")
        print("3. Add Allergen")
        print("4. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            flavor_name = input("Enter flavor name: ")
            description = input("Enter flavor description: ")
            availability = input("Enter availability (e.g., Summer, Winter): ")
            add_seasonal_flavor(flavor_name, description, availability)
            print(f"Flavor '{flavor_name}' added successfully.")

        elif choice == '2':
            keyword = input("Enter a keyword to search flavors: ")
            results = search_flavors(keyword)
            if results:
                print("\nMatching Flavors:")
                for flavor in results:
                    print(f"- {flavor[1]} ({flavor[3]}) - {flavor[2]}")
            else:
                print("No matching flavors found.")

        elif choice == '3':
            allergen_name = input("Enter allergen name to add: ")
            add_allergen(allergen_name)

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()