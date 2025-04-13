import tkinter as tk
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("C:\\Users\\sivar\\Downloads\\kec-dc76f-firebase-adminsdk-fbsvc-f301eed158.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://kec-dc76f-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def validate_login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "user" and password == "password123":
        root.withdraw()
        open_user_form()
    else:
        error_label.config(text="Invalid username or password.")

def open_user_form():
    user_form = tk.Toplevel()
    user_form.title("User Information Form")
    user_form.geometry("300x300")
    
    label_user_id = tk.Label(user_form, text="User ID")
    label_user_id.pack(pady=10)
    entry_user_id = tk.Entry(user_form)
    entry_user_id.pack(pady=5)
    
    label_location = tk.Label(user_form, text="Location")
    label_location.pack(pady=10)
    location_options = ["Chennai", "Kanchipuram", "Chengalpattu", "Erode", "Dindukal"]
    location_var = tk.StringVar(user_form)
    location_var.set(location_options[0])
    location_dropdown = tk.OptionMenu(user_form, location_var, *location_options)
    location_dropdown.pack(pady=5)
    
    label_weight = tk.Label(user_form, text="Weight (in kgs)")
    label_weight.pack(pady=10)
    entry_weight = tk.Entry(user_form)
    entry_weight.pack(pady=5)

    def submit_form():
        user_id = entry_user_id.get()
        location = location_var.get()
        weight = float(entry_weight.get())
        
        print(f"User ID: {user_id}, Location: {location}, Weight: {weight} kgs")
        
        users_ref = db.reference('users')
        user_ref = users_ref.order_by_child('user_id').equal_to(user_id).get()

        if user_ref:
            user_key = list(user_ref.keys())[0]
            existing_weight = user_ref[user_key].get('weight', 0)
            new_weight = existing_weight + weight
            users_ref.child(user_key).update({'weight': new_weight})
            print(f'Updated weight for user {user_id} to {new_weight} kgs.')
        else:
            users_ref.push({'user_id': user_id, 'location': location, 'weight': weight})
            print(f'User {user_id} created successfully with weight {weight} kgs.')

        location_ref = db.reference(f'locations/{location}')
        location_data = location_ref.get()

        if location_data:
            new_total_weight = location_data.get('total_weight', 0) + weight
            location_ref.update({'total_weight': new_total_weight})
            print(f'Updated total weight for {location} to {new_total_weight} kgs.')
        else:
            location_ref.set({'total_weight': weight})
            print(f'Created location {location} with total weight {weight} kgs.')

        user_form.destroy()
        open_login_page()

    submit_button = tk.Button(user_form, text="Submit", command=submit_form)
    submit_button.pack(pady=20)

def open_login_page():
    global root
    root.deiconify()
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

root = tk.Tk()
root.title("Login Page")
root.geometry("300x200")

label_username = tk.Label(root, text="Username")
label_username.pack(pady=10)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Password")
label_password.pack(pady=10)

entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

error_label = tk.Label(root, text="", fg="red")
error_label.pack(pady=5)

login_button = tk.Button(root, text="Login", command=validate_login)
login_button.pack(pady=20)

root.mainloop()
