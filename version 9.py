import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from tkinter import Listbox
from tkinter import *
import re
import pygame
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import math
import random
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib









conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='project'  # Use the 'project' database
)

# Create a cursor object
cursor = conn.cursor()

# Create the 'items' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        itemno INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255),
        quantity INT,
        unit_price FLOAT,
        expiry_date DATE,
        sale_price FLOAT,
        gst FLOAT,
        net_price FLOAT
    )
''')

root = tk.Tk()
root.title("Grocery Store Management")
root.geometry("1024x1024")



# Load a background image (you should replace 'xyz.png' with your actual image path)
bg_image = tk.PhotoImage(file=r"F:\Users\babu\Desktop\project\intro 1.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
pygame.init()

# Load the music file
pygame.mixer.music.load(r"F:\Users\babu\Desktop\project\welcome.mp3")
# Play the music
pygame.mixer.music.play()



# Define a common style for widgets
common_style = {"font": ("Arial", 25), "bg": "black","fg":"white", "padx": 10, "pady": 10}

frames = []

# Function to log in as an administrator
def login_administrator():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin":
        messagebox.showinfo("Success", "Administrator logged in successfully.")
        show_admin_menu()
    else:
        messagebox.showinfo("Error", "Invalid username or password.")
username_entry=None
password_entry=None



# Function to log in as a customer
customer_username_entry = None
customer_password_entry = None
customer_email_entry = None
security_question_entry = None

    # Add logic to authenticate customers here

# Function to sign up as a customer
def sign_up_customer():
    customer_username_entry
    customer_username = customer_username_entry.get()

    customer_password = customer_password_entry.get()
    customer_email = customer_email_entry.get()
    sec_question = security_question_entry.get()

    # Check if the username meets the conditions
    if not re.search(r'[A-Z]', customer_username):
        messagebox.showinfo("Error", "Username must contain at least one capital letter.")
        return

    # Check if the password meets the conditions
    if not (re.search(r'[A-Z]', customer_password) and re.search(r'[!@#$%^&*?<>/.,=+_-]', customer_password) and len(customer_password) >= 8):
        messagebox.showinfo("Error", "Password must have at least one capital letter, one special character, and be at least 8 characters long.")
        return

    # Check if the email is not empty
    if not customer_email:
        messagebox.showinfo("Error", "Please fill in the email field.")
        return
    if not sec_question:
        messagebox.showinfo("Error", "Please fill in the security question field.")
        return
    


    # Check if the username is unique
    cursor.execute("SELECT * FROM credentials WHERE USERNAME = %s", (customer_username,))
    existing_user = cursor.fetchone()
    if existing_user:
        messagebox.showinfo("Error", "Username already exists. Please choose a different username.")
        return
    cursor.execute("SELECT * FROM CREDENTIALS WHERE EMAIL=%s",(customer_email,))
    existing_email = cursor.fetchone()
    
    if existing_email:
        messagebox.showinfo("Error", "Email already exists. Please choose a different email.")
        return
    

    # If all conditions are met, insert customer data into the database
    cursor.execute("INSERT INTO credentials (USERNAME, PASSWORD, EMAIL,security_question) VALUES (%s, %s, %s,%s)",
                   (customer_username, customer_password, customer_email,sec_question))
    conn.commit()

    messagebox.showinfo("Success", "Account created successfully. You can now log in as a customer.")
    sender_email = 'groceryshop06@gmail.com'  # Replace with your sender email
    sender_password = 'einldaxynzpoapjb'  # Replace with your sender email password
    receiver_email = customer_email

    # Compose the email
    def compose_email(sender_email, receiver_email):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = 'THANK YOU FOR SIGNING UP IN OUR APP'

        body = 'THANK YOU FOR SIGNING UP. YOUR ACCOUNT HAS BEEN CREATED SUCCESSFULLY. YOU CAN NOW LOGIN AS CUSTOMER.'
        msg.attach(MIMEText(body, 'plain'))

        return msg

    # Send the email
    def send_email(sender_email, sender_password, receiver_email, msg):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            messagebox.showinfo("Success", "Confirmation email sent successfully.")
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to send email. Error: {str(e)}")

    email_msg = compose_email(sender_email, receiver_email)
    send_email(sender_email, sender_password, receiver_email, email_msg)
def login_customer():
    global customer_username
    global customer_password
    customer_username = customer_username_entry.get()
    customer_password = customer_password_entry.get()

    # Check the credentials against the SQL database
    cursor.execute("SELECT * FROM credentials WHERE USERNAME = %s AND PASSWORD = %s", (customer_username, customer_password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Customer logged in successfully.")
        show_customer_menu()
    else:
        messagebox.showinfo("Error", "Invalid username or password.")
email_entry=None
new_password_entry=None



security1_question_entry=None 
def generate_otp(length=6):
    """Generate a random OTP."""
    otp = ''.join([str(random.randint(0, 9)) for i in range(length)])
    return otp

def compose_email(sender, receiver, otp):
    """Compose an email with OTP."""
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Your OTP Code'

    body = f'Your OTP code is {otp}'
    msg.attach(MIMEText(body, 'plain'))

    return msg

def send_email(sender, password, receiver, msg):
    """Send an email with the OTP."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def forgot_password():
    def reset():
        customer_username = customer_username_entry.get()
        customer_password = new_password_entry.get()
        entered_otp = otp_entry.get()

        cursor.execute("SELECT username, email FROM credentials WHERE username = %s", (customer_username,))
        result = cursor.fetchone()

        if result:
            username, email = result
            if otp_verified and otp_verified[username] == entered_otp:
                if len(customer_password) < 8 or not any(char.isupper() for char in customer_password) or not any(char.isdigit() for char in customer_password) or not any(char in '!@#$%^&*()_+' for char in customer_password):
                    messagebox.showinfo("Error", "Invalid password format. Password must have at least 8 characters with at least one uppercase letter, one digit, and one special character.")
                else:
                    cursor.execute("UPDATE credentials SET password = %s WHERE username = %s", (customer_password, customer_username))
                    conn.commit()
                    messagebox.showinfo("Success", "Password reset success. You can now log in as a customer.")
                    root2.destroy()
            else:
                messagebox.showinfo("Error", "Invalid OTP.")
        else:
            messagebox.showinfo("Error", "Invalid username.")

    def send_otp():
        nonlocal otp_verified
        customer_username = customer_username_entry.get()

        cursor.execute("SELECT username, email FROM credentials WHERE username = %s", (customer_username,))
        result = cursor.fetchone()

        if result:
            username, email = result
            otp = generate_otp()
            otp_verified[username] = otp

            sender_email = 'groceryshop06@gmail.com'  # Replace with your sender email
            sender_password = 'einldaxynzpoapjb'  # Replace with your sender email password
            receiver_email = email

            email_msg = compose_email(sender_email, receiver_email, otp)
            send_email(sender_email, sender_password, receiver_email, email_msg)
            messagebox.showinfo("Success", "OTP has been sent to your registered email.")
        else:
            messagebox.showinfo("Error", "Invalid username.")

    otp_verified = {}

    # GUI setup
    root2 = tk.Tk()
    root2.title("Password Reset")

    username_label = tk.Label(root2, text="Username")
    username_label.grid(row=0, column=0)
    customer_username_entry = tk.Entry(root2)
    customer_username_entry.grid(row=0, column=1)

    otp_label = tk.Label(root2, text="OTP")
    otp_label.grid(row=1, column=0)
    otp_entry = tk.Entry(root2)
    otp_entry.grid(row=1, column=1)

    new_password_label = tk.Label(root2, text="New Password")
    new_password_label.grid(row=2, column=0)
    new_password_entry = tk.Entry(root2)
    new_password_entry.grid(row=2, column=1)

    send_otp_button = tk.Button(root2, text="Send OTP", command=send_otp)
    send_otp_button.grid(row=3, column=0, columnspan=2)

    reset_button = tk.Button(root2, text="Reset Password", command=reset)
    reset_button.grid(row=4, column=0, columnspan=2)

    


# You may want to start the Tkinter main loop




# You may want to start the Tkinter main loop


    
    
  
                                


# 



        
        



admin_login_frame=None
def admin_login():
    global username_entry
    global password_entry
    admin_login_frame = tk.Frame(root, bg="white", bd=5)
    admin_login_frame.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.2, anchor=tk.CENTER)
    

    username_label = tk.Label(admin_login_frame, text="Username:", bg="white")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(admin_login_frame)
    username_entry.grid(row=0, column=1)

    password_label = tk.Label(admin_login_frame, text="Password:", bg="white")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(admin_login_frame, show="*")
    password_entry.grid(row=1, column=1)


    login_button = tk.Button(admin_login_frame, text="Login as Admin", command=login_administrator)
    login_button.grid(row=2, columnspan=2)



# Create widgets for logging in as a customer
customer_login_frame=None
def customer_signin():
    global customer_login_frame, customer_username_entry, customer_password_entry  # Updated variable names
    customer_login_frame = tk.Frame(root, bg="blue", bd=10)
    customer_login_frame.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.2, anchor="n")

    # Create the entry widgets
    customer_username_entry = tk.Entry(customer_login_frame)
    customer_username_entry.grid(row=0, column=1)

    customer_password_entry = tk.Entry(customer_login_frame, show="*")
    customer_password_entry.grid(row=1, column=1)

    customer_login_button = tk.Button(customer_login_frame, text="Login as Customer", command=login_customer)
    customer_login_button.grid(row=2, columnspan=2)

    customer_username_label = tk.Label(customer_login_frame, text="Username:", bg="white")
    customer_username_label.grid(row=0, column=0)

    customer_password_label = tk.Label(customer_login_frame, text="Password:", bg="white")
    customer_password_label.grid(row=1, column=0)

    forgot_pswd = tk.Button(customer_login_frame, text="forgot password", command=forgot_password)
    forgot_pswd.grid(row=3, columnspan=2)



# Define global variables for customer entry fields
new_gst_entry=None
def customer_signup():
    global customer_username_entry, customer_password_entry, customer_email_entry, security_question_entry  # Updated variable names
    customer_sign_up_frame = tk.Frame(root, bg="white", bd=5)
    customer_sign_up_frame.place(relx=0.5, rely=0.8, relwidth=0.4, relheight=0.2, anchor="n")

    customer_signup_username_label = tk.Label(customer_sign_up_frame, text="Username:", bg="white")
    customer_signup_username_label.grid(row=0, column=0)
    customer_username_entry = tk.Entry(customer_sign_up_frame)
    customer_username_entry.grid(row=0, column=1)

    customer_signup_password_label = tk.Label(customer_sign_up_frame, text="Password:", bg="white")
    customer_signup_password_label.grid(row=1, column=0)
    customer_password_entry = tk.Entry(customer_sign_up_frame, show="*")
    customer_password_entry.grid(row=1, column=1)

    customer_email_label = tk.Label(customer_sign_up_frame, text="Email:", bg="white")
    customer_email_label.grid(row=2, column=0)
    customer_email_entry = tk.Entry(customer_sign_up_frame)
    customer_email_entry.grid(row=2, column=1)

    security_question_label = tk.Label(customer_sign_up_frame, text="enter your school studied or enter your favourite fruit", bg="white")
    security_question_label.grid(row=3, column=0)
    security_question_entry = tk.Entry(customer_sign_up_frame)
    security_question_entry.grid(row=3, column=1)

    sign_up_button = tk.Button(customer_sign_up_frame, text="Sign Up as Customer", command=sign_up_customer)
    sign_up_button.grid(row=4, columnspan=2)

    sign_up_button = tk.Button(customer_sign_up_frame, text="Sign Up as Customer", command=sign_up_customer)
    sign_up_button.grid(row=4, columnspan=2)



login_frame = ttk.Frame(root)
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

b1 = tk.Button(login_frame, text="Administrator Login", command=admin_login, **common_style)
b2 = tk.Button(login_frame, text="Customer Login", command=customer_signin, **common_style)
b3 = tk.Button(login_frame, text="Customer Signup", command=customer_signup, **common_style)

b1.pack(pady=60)
b2.pack(pady=60)
b3.pack(pady=60)

gst_entry=None
# Create widgets for the administrator's menu





def show_admin_menu():
   


   # Initialize pygame 
    pygame.init()

   # Load the music file
    pygame.mixer.music.load(r"F:\Users\babu\Desktop\project\success.mp3")

   # Play the music
    pygame.mixer.music.play()
    
    global admin_login_frame
    if admin_login_frame is not None:
        admin_login_frame.destroy()

    login_frame.destroy() # Destroy the login frame
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand='yes')
    # Instantiate the DateTimeApp class
  
     

    # Create widgets for adding items
    def add_item():
        
        item_name = item_name_entry.get()
        quantity = quantity_entry.get()
        unit_price = unit_price_entry.get()
        item_no = item_no_entry.get()
        exp_date = exp_date_entry.get()
        sale_price = sale_price_entry.get()
        gst=gst_entry.get()

        query = "INSERT INTO items (itemno, item_name, quantity, unit_price, expiry_date, sale_price, gst) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (item_no, item_name, quantity, unit_price, exp_date, sale_price,gst)

        try:
            print("Query:", query)
            print("Values:", values)
            cursor.execute(query, values)
            conn.commit()
            cursor.execute("update items SET net_price=sale_price+sale_price*gst/100")
            conn.commit()
            messagebox.showinfo("Success", "Item added successfully.")
        except mysql.connector.IntegrityError:
            messagebox.showinfo("Warning", "Item already exists. ")
           

    add_item_frame = ttk.Frame(root)
    notebook.add(add_item_frame, text='Add Item')
    
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\add entry.png")

# Add a label to display the image
    image_label = ttk.Label(add_item_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image 

# Create a custom style for labels, entry widgets, and the button
    custom_style = ttk.Style()
    custom_style.configure("Custom.TLabel", font=("Bernard MT condensed", 30))
    custom_style.configure("Custom.TEntry", font=("Bernard MT condensed", 30))
    custom_style.configure("Custom.TButton", font=("Bernard MT condensed", 30), background="black",foreground="green")

# Create labels with the custom style
    item_name_label = ttk.Label(add_item_frame, text="Product Name:", style="Custom.TLabel")
    item_name_label.grid(row=0, column=0, padx=10, pady=5)
    item_name_entry = ttk.Entry(add_item_frame, style="Custom.TEntry", width=30)  # Increase entry width
    item_name_entry.grid(row=0, column=1, padx=10, pady=5)

    quantity_label = ttk.Label(add_item_frame, text="Quantity:", style="Custom.TLabel")
    quantity_label.grid(row=1, column=0, padx=10, pady=5)
    quantity_entry = ttk.Entry(add_item_frame, style="Custom.TEntry", width=30)  # Increase entry width
    quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    unit_price_label = ttk.Label(add_item_frame, text="Unit Price:", style="Custom.TLabel")
    unit_price_label.grid(row=2, column=0, padx=10, pady=5)
    unit_price_entry = ttk.Entry(add_item_frame, style="Custom.TEntry", width=30)  # Increase entry width
    unit_price_entry.grid(row=2, column=1, padx=10, pady=5)

    item_no_label = ttk.Label(add_item_frame, text="Item No:", style="Custom.TLabel")
    item_no_label.grid(row=3, column=0, padx=10, pady=5)
    item_no_entry = ttk.Entry(add_item_frame, style="Custom.TEntry", width=30)  # Increase entry width
    item_no_entry.grid(row=3, column=1, padx=10, pady=5)

    exp_date_label = ttk.Label(add_item_frame, text="Expiry Date (yy/mm/dd):", style="Custom.TLabel")
    exp_date_label.grid(row=4, column=0, padx=10, pady=5)
    exp_date_entry = ttk.Entry(add_item_frame, style="Custom.TEntry", width=30)  # Increase entry width
    exp_date_entry.grid(row=4, column=1, padx=10, pady=5)

    sale_price_label = ttk.Label(add_item_frame, text="Sale Price:", style="Custom.TLabel")
    sale_price_label.grid(row=5, column=0, padx=10, pady=5)
    sale_price_entry = ttk.Entry(add_item_frame, style="Custom.TEntry", width=30)  # Increase entry width
    sale_price_entry.grid(row=5, column=1, padx=10, pady=5)

    gst_label = ttk.Label(add_item_frame, text="GST:", style="Custom.TLabel")
    gst_label.grid(row=6, column=0, padx=10, pady=5)
    gst_entry = ttk.Entry(add_item_frame, style="Custom.TEntry", width=30)  # Increase entry width
    gst_entry.grid(row=6, column=1, padx=10, pady=5)


# Create and configure the "Add Item" button
    add_button = ttk.Button(add_item_frame, text="Add Item", command=add_item, style="Custom.TButton")
    add_button.grid(row=7, columnspan=2, pady=10)

    # Create widgets for showing stock
    stock_treeview = ttk.Treeview(notebook, columns=("itemno", "item_name", "quantity", "unit_price", "expiry_date", "sale_price","gst","net_price"))
    notebook.add(stock_treeview, text='Show Stock')
    button_frame = ttk.Frame(stock_treeview)
    button_frame.grid(row=0, column=0, pady=10)


    # Define columns for the table
    stock_treeview.heading("#1", text="Item No")
    stock_treeview.heading("#2", text="Item Name")
    stock_treeview.heading("#3", text="Quantity")
    stock_treeview.heading("#4", text="Unit Price")
    stock_treeview.heading("#5", text="Expiry Date")
    stock_treeview.heading("#6", text="Sale Price")
    stock_treeview.heading("#7", text="gst")
    stock_treeview.heading("#8", text="net_Price")
    

    # Set column widths
    stock_treeview.column("#1", width=80)
    stock_treeview.column("#2", width=100)
    stock_treeview.column("#3", width=100)
    stock_treeview.column("#4", width=100)
    stock_treeview.column("#5", width=50)
    stock_treeview.column("#6", width=50)
    stock_treeview.column("#7", width=100)
    stock_treeview.column("#8", width=100)

    # Function to populate the table with stock data
    def show_stock():

        stock_treeview.delete(*stock_treeview.get_children())  # Clear the table
        cursor.execute("SELECT * FROM items")
        result = cursor.fetchall()
        for row in result:
            stock_treeview.insert("", "end", values=row)



    show_stock_button = ttk.Button(button_frame, text="Show Stock", command=show_stock)
    show_stock_button.grid(row=0, column=0, pady=10)
 
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 6))  # Increase the font size (12) as needed

# Increase the font size for cell values
      # Increase the font size (10) as needed

# Set the background color for the Treeview
    style.configure("Treeview", background="#D9E4FF")  # Change the color code to the color you want

    


    
    billed_items_frame = ttk.Frame(notebook)
    notebook.add(billed_items_frame, text='Show Billed Items')

    # Create and configure the Treeview for billed items
    bill_treeview = ttk.Treeview(billed_items_frame, columns=("bill_id", "customer_name", "mode_of_payment", "item_no", "item_name", "unit_price", "quantity", "sale_price", "phone_number", "address", "purchase_price", "gst", "net_price", "delivery_status"), show="headings")
    h_scrollbar = ttk.Scrollbar(billed_items_frame, orient="horizontal", command=bill_treeview.xview)
    bill_treeview.configure(xscrollcommand=h_scrollbar.set)
    h_scrollbar.pack(side="bottom", fill="x")

    bill_treeview.pack(fill='both', expand=True, padx=10, pady=10)

    # Define columns and headings for the Treeview
    billed_columns = [
        ("bill_id", "Bill No"),
        ("customer_name", "Customer Name"),
        ("mode_of_payment", "Mode of Payment"),
        ("item_no", "Item No"),
        ("item_name", "Item Name"),
        ("unit_price", "Unit Price"),
        ("quantity", "Quantity"),
        ("sale_price", "Sale Price"),
        ("phone_number", "Phone Number"),
        ("address", "Address"),
        ("purchase_price", "Purchase Price"),
        ("gst", "GST"),
        ("net_price", "Net Price"),
        ("delivery_status", "Delivery Status")
    ]
    
    for col, text in billed_columns:
        bill_treeview.heading(col, text=text)
        bill_treeview.column(col, width=100)

    # Create and pack the button frame for billed items
    billed_button_frame = ttk.Frame(billed_items_frame)
    billed_button_frame.pack(fill='x', pady=10)

    # Function to populate the Treeview with billed items data
    def show_bills():
        bill_treeview.delete(*bill_treeview.get_children())  # Clear the table
        cursor.execute("SELECT * FROM bills WHERE delivery_status = 'undelivered'")
        result = cursor.fetchall()
        for row in result:
            bill_treeview.insert("", "end", iid=row[0], values=row)

    # Function to update delivery status
    def update_delivery_status(item_id, new_status):
        query = "UPDATE bills SET delivery_status = %s WHERE bill_id = %s"
        values = (new_status, item_id)
        try:
            cursor.execute(query, values)
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    # Function to handle double-click events for editing
    def on_double_click(event):
        item = bill_treeview.selection()[0]
        current_value = bill_treeview.item(item, 'values')[13]  # 13 is the index for delivery_status
        new_value = simpledialog.askstring("Edit Delivery Status", "Enter new delivery status:", initialvalue=current_value)
        if new_value:
            update_delivery_status(item, new_value)
            show_bills()  # Refresh the display

    # Add Show Billed Items button
    show_billed_items_button = ttk.Button(billed_button_frame, text="Show Billed Items", command=show_bills)
    show_billed_items_button.pack()

    # Bind double-click event for editing
    bill_treeview.bind("<Double-1>", on_double_click)

    # Configure Treeview style
    style = ttk.Style()
    style.configure("Treeview", background="#D9E4FF")
    style.configure("Treeview.Heading", font=("Helvetica", 10)) 

    delivered_items_frame = ttk.Frame(notebook)
    notebook.add(delivered_items_frame, text='Show Delivered Items')

    # Create and configure the Treeview for delivered items
    delivered_treeview = ttk.Treeview(delivered_items_frame, columns=("bill_id", "customer_name", "mode_of_payment", "item_no", "item_name", "unit_price", "quantity", "sale_price", "phone_number", "address", "purchase_price", "gst", "net_price", "delivery_status"), show="headings")
    h_scrollbar_delivered = ttk.Scrollbar(delivered_items_frame, orient="horizontal", command=delivered_treeview.xview)
    delivered_treeview.configure(xscrollcommand=h_scrollbar_delivered.set)
    h_scrollbar_delivered.pack(side="bottom", fill="x")
    delivered_treeview.pack(fill='both', expand=True, padx=10, pady=10)

    # Define columns and headings for the Treeview
    for col, text in billed_columns:
        delivered_treeview.heading(col, text=text)
        delivered_treeview.column(col, width=100)

    # Function to populate the Treeview with delivered items data
    def show_delivered_items():
        delivered_treeview.delete(*delivered_treeview.get_children())  # Clear the table
        cursor.execute("SELECT * FROM bills WHERE delivery_status = 'delivered'")
        result = cursor.fetchall()
        for row in result:
            delivered_treeview.insert("", "end", iid=row[0], values=row)

    # Add Show Delivered Items button
    show_delivered_items_button = ttk.Button(delivered_items_frame, text="Show Delivered Items", command=show_delivered_items, style="Custom.TButton")
    show_delivered_items_button.pack(pady=10)

    # Configure Treeview style
    style = ttk.Style()
    style.configure("Treeview", background="#D9E4FF")
    style.configure("Treeview.Heading", font=("Helvetica", 10)) 
    

    def remove_item():
        

        item_no = int(item_no_remove_entry.get())
        qty = int(quantity_remove_entry.get())

        cursor.execute("SELECT quantity FROM items WHERE itemno = %s", (item_no,))
        current_qty = cursor.fetchone()

        if current_qty and current_qty[0] >= qty:
            cursor.execute("UPDATE items SET quantity = quantity - %s WHERE itemno = %s", (qty, item_no))
            conn.commit()
            messagebox.showinfo("Success", "Item removed successfully.")
        else:
            messagebox.showinfo("Warning", "Item does not exist or quantity is insufficient.")

    remove_item_frame = ttk.Frame(root)
    notebook.add(remove_item_frame, text='Remove Item')
    
    
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\remove.png")

# Add a label to display the image
    image_label = ttk.Label(remove_item_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image

    item_no_remove_label = ttk.Label(remove_item_frame, text="Item No to Remove")
    item_no_remove_label.grid(row=0, column=0, padx=10, pady=5)
    item_no_remove_entry = ttk.Entry(remove_item_frame)
    item_no_remove_entry.grid(row=0, column=1, padx=10, pady=5)

    quantity_remove_label = ttk.Label(remove_item_frame, text="Quantity to Remove")
    quantity_remove_label.grid(row=1, column=0, padx=10, pady=5)
    quantity_remove_entry = ttk.Entry(remove_item_frame)
    quantity_remove_entry.grid(row=1, column=1, padx=10, pady=5)

    remove_button = ttk.Button(remove_item_frame, text="Remove Item", command=remove_item, style="Custom.TButton")
    remove_button.grid(row=2, columnspan=2, pady=10)
    # Load the image
    
    def modify_item():
        item_no = item_no_modify_entry.get()
        new_quantity = new_quantity_entry.get()
        new_unit_price = new_unit_price_entry.get()
        new_exp_date = new_exp_date_entry.get()
        new_sale_price = new_sale_price_entry.get()
        new_gst=new_gst_entry.get()
        try:
            new_sale_price = float(new_sale_price)
            new_gst = float(new_gst)
        except ValueError:
            messagebox.showerror("Input Error", "Sale Price and GST must be numeric.")
            return
    
    # Perform the calculation
        new_netprice = new_sale_price + (new_sale_price * new_gst / 100)

        query = "UPDATE items SET quantity = %s, unit_price = %s, expiry_date = %s, sale_price=%s,gst=%s,net_price=%s WHERE itemno = %s"
        values = (new_quantity, new_unit_price, new_exp_date, new_sale_price,new_gst, new_netprice, item_no)

        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", f"Item {item_no} modified successfully.")

# Create widgets for modifying items
    modify_item_frame = ttk.Frame(root)
    notebook.add(modify_item_frame, text='Modify Item')
    xyz = ttk.Style()
    xyz.configure("custom.TLabel", font=("Bernard MT condensed", 30))
    xyz.configure("custom.TEntry", font=("Bernard MT condensed", 30))
    xyz.configure("custom.TButton", font=("Bernard MT condensed", 30), background="black",foreground="blue")
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\modify.png")

# Add a label to display the image
    image_label = ttk.Label(modify_item_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image 

    item_no_modify_label = ttk.Label(modify_item_frame, text="Item No to Modify:",style="Custom.TLabel")
    item_no_modify_label.grid(row=0, column=0, padx=10, pady=5)
    item_no_modify_entry = ttk.Entry(modify_item_frame,style="custom.TEntry")
    item_no_modify_entry.grid(row=0, column=1, padx=10, pady=5)

    new_quantity_label = ttk.Label(modify_item_frame, text="New Quantity:",style="Custom.TLabel")
    new_quantity_label.grid(row=1, column=0, padx=10, pady=5)
    new_quantity_entry = ttk.Entry(modify_item_frame,style="custom.TEntry")
    new_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    new_unit_price_label = ttk.Label(modify_item_frame, text="New Unit Price:",style="Custom.TLabel")
    new_unit_price_label.grid(row=2, column=0, padx=10, pady=5)
    new_unit_price_entry = ttk.Entry(modify_item_frame,style="custom.TEntry")
    new_unit_price_entry.grid(row=2, column=1, padx=10, pady=5)

    new_exp_date_label = ttk.Label(modify_item_frame, text="New Expiry Date (yy/mm/dd):",style="Custom.TLabel")
    new_exp_date_label.grid(row=3, column=0, padx=10, pady=5)
    new_exp_date_entry = ttk.Entry(modify_item_frame,style="custom.TEntry")
    new_exp_date_entry.grid(row=3, column=1, padx=10, pady=5)

    new_sale_price_label = ttk.Label(modify_item_frame, text="New Sale Price:",style="Custom.TLabel")
    new_sale_price_label.grid(row=4, column=0, padx=10, pady=5)
    new_sale_price_entry = ttk.Entry(modify_item_frame,style="custom.TEntry")
    new_sale_price_entry.grid(row=4, column=1, padx=10, pady=5)

    new_gst_label = ttk.Label(modify_item_frame, text="New gst:",style="Custom.TLabel")
    new_gst_label.grid(row=5, column=0, padx=10, pady=5)
    new_gst_entry = ttk.Entry(modify_item_frame,style="custom.TEntry")
    new_gst_entry.grid(row=5, column=1, padx=10, pady=5)

    modify_button = ttk.Button(modify_item_frame, text="Modify Item", command=modify_item,style="custom.TButton")
    modify_button.grid(row=7, columnspan=2, pady=10)



        # Create widgets for graphing data
 
    def profit_earned():
        cursor
        cursor.execute("select sum(total_price)-sum(purchase_price*quantity) from bills")
        result = cursor.fetchall()
        k=result[0][0]
        cursor.execute("select sum(unit_price*quantity )from items where expiry_date<=curdate() ")
        result1 = cursor.fetchall()
        if result1 and result1[0][0] is not None:
            l = result1[0][0]
        else:
            l = 0


        profit=k-l
        profit_display=ttk.Label(profit_frame,text=profit,style="custom.TLabel")
        profit_display.grid(row=4, column=0, padx=100, pady=100)

        

    profit_frame=ttk.Frame(root)
    notebook.add(profit_frame, text='profit earned')
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\profit.png")

# Add a label to display the image
    image_label = ttk.Label(profit_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image
    ss=ttk.Button(profit_frame,text="show profit",command=profit_earned,style="custom.TButton")
    ss.grid(row=5,pady=10,columnspan=2)
  
       
    xyz = ttk.Style()
    xyz.configure("custom.TLabel", font=("Bernard MT condensed", 30))
    xyz.configure("custom.TEntry", font=("Bernard MT condensed", 30))
        
    xyz.configure("custom.TButton", font=("Bernard MT condensed", 30), background="black",)
    cursor.execute("SELECT SUM(quantity),item_name FROM bills GROUP BY item_name ORDER BY item_name")
    result7 = cursor.fetchall()
    cursor.execute("SELECT DISTINCT item_name FROM bills ORDER BY item_name")
    result8 = cursor.fetchall()
    sales = [item[0] for item in result7]
    items = [item[0] for item in result8]
    def graphs1():
        fig = plt.figure(figsize = (7,5))
        axes = fig.add_subplot(1,1,1)
        axes.set_ylim(0, 300)
        palette = ['blue', 'red', 'green', 
           'darkorange', 'maroon', 'black']
        
        plt.bar(items,sales,width=0.3,color=palette)
        plt.title('Profit Earned')

        plt.xlabel("ITEMS")
        plt.ylabel("SALES")
        
       
        

        

        plt.show()

        
        
    def graphs2():
        plt.plot(items,sales)
        
        plt.xlabel("ITEMS")
        plt.ylabel("SALES")
        plt.show()
    def graphs3():
        plt.pie(sales, labels=items)
        plt.title('Sales')
       
        plt.show()

        
    graph_frame = ttk.Frame(root)
    notebook.add(graph_frame, text='Graph Data')
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\graph.png")

# Add a label to display the image
    image_label = ttk.Label(graph_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image
    
    graph_button1=ttk.Button(graph_frame,text="Generate bargraph",command=graphs1,style="custom.TButton")
    graph_button1.grid(row=0, columnspan=1, padx=150, pady=10)
    graph_button2=ttk.Button(graph_frame,text="Generate linechart",command=graphs2,style="custom.TButton")
    graph_button2.grid(row=4,columnspan=2,padx=150,pady=70)
    graph_button3=ttk.Button(graph_frame,text="Generate piechart",command=graphs3,style="custom.TButton")
    graph_button3.grid(row=8,columnspan=3,padx=150,pady=90)


    
    user_treeview = ttk.Treeview(notebook, columns=("username", "password","email", "security question"))
    notebook.add(user_treeview, text='Show users')
    user_treeview.heading("#1", text="username")
    user_treeview.heading("#2", text="password")
    user_treeview.heading("#3", text="email")
    user_treeview.heading("#4", text="security_question")

    # Set column widths
    user_treeview.column("#1", width=80)
    user_treeview.column("#2", width=200)
    user_treeview.column("#3", width=100)
    user_treeview.column("#4", width=100)
    

    # Function to populate the table with stock data
    def show_users():
        user_treeview.delete(*user_treeview.get_children())  # Clear the table
        cursor.execute("SELECT * FROM credentials")
        result = cursor.fetchall()
        for row in result:
            user_treeview.insert("", "end", values=row)

    user_frame = ttk.Frame(user_treeview)
    user_frame.grid(row=0, column=0, pady=10)
    show_user_button = ttk.Button(user_frame, text="Show users", command=show_users)
    show_user_button.grid(row=1, column=0, pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 18)) 
    # Increase the font size for cell values
    # Increase the font size (10) as needed

    # Set the background color for the Treeview
    style.configure("Treeview", background="#D9E4FF")  # Change the color code to the color you want

    delete_username_entry = None

    del_frame = ttk.Frame(root)
    notebook.add(del_frame, text='delete Users')
    xyzp= ttk.Style()
    xyzp.configure("custom.TLabel", font=("Bernard MT condensed", 30))
    xyzp.configure("custom.TEntry", font=("Bernard MT condensed", 30))
        
    xyzp.configure("custom.TButton", font=("Bernard MT condensed", 30), background="black",)
    

    def del1():
        delete_username = delete_username_entry.get()
        
        cursor.execute("DELETE FROM credentials WHERE username=%s", (delete_username,))
        conn.commit()
        messagebox.showinfo("deleted successfully")
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\users.png")

# Add a label to display the image
    image_label = ttk.Label(del_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image

    delete_label = ttk.Label(del_frame, text="enter userid to be deleted", style="custom.TLabel")
    delete_username_entry = ttk.Entry(del_frame, style="custom.TEntry")
    delete_button = ttk.Button(del_frame, text="delete", command=del1, style="custom.TButton")
    delete_label.grid(row=1, column=1,padx=150,pady=50)
    delete_username_entry.grid(row=4, column=1,pady=100,padx=100)
    delete_button.grid(row=5, column=1,pady=150,padx=150)
                                                


    

    

    
    

    



    frames.append(admin_login_frame)
      # Add the admin menu frame to the frames list

# Create widgets for the customer portal
customer_menu_frame = None
login_entry = None
customer_phone_number_entry=None
customer_address_entry=None



def show_customer_menu():
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
        bill_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(255),
        mode_of_payment VARCHAR(255),
        item_no INT,
        item_name VARCHAR(255),
        unit_price FLOAT,
        quantity INT,
        total_price FLOAT,
        phone_number varchar(10),
        address varchar(800),
        purchase_price int,
        gst int,
        net_price int,
        delivery_status varchar(20) DEFAULT 'undelivered'
    )
''')
        
  
    current_bill = []
    global customer_login_frame, frames, login_entry
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand='yes')
   


    
    if customer_login_frame is not None:
        customer_login_frame.destroy()
    login_frame.destroy()  # Destroy the login frame
 
    customer_cart = {}
    def order_groceries():
            current_bill = []

# Initialize the Tkinter window

    billing_frame = ttk.Frame(root)
    notebook.add(billing_frame, text='Billing')
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\bill.PNG")

# Add a label to display the image
    image_label = ttk.Label(billing_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image 


   

# Function to display the current bill
    

# Function to update the displayed bill
    
    def display_customer_info():
        bill_text.config(state=tk.NORMAL)
        bill_text.delete("1.0", tk.END)
        bill_text.insert(tk.END, "*" * 100 + "\n")
        bill_text.insert(tk.END, "Customer Name: {}\tMode of Payment: {}\n".format(customer_name_entry.get(), mode_of_payment_entry.get()))
        bill_text.insert(tk.END, "*" * 100 + "\n")
        bill_text.config(state=tk.DISABLED)

# Function to display items in the bill
    def display_items():
        bill_text.config(state=tk.NORMAL)
        bill_text.insert(tk.END, "Item No\t\tItem Name\t\t\tUnit Price\t\tQuantity\t\tTotal Price\t\tgst\tnet_price\n")
        bill_text.insert(tk.END, "*" * 105 + "\n")
        for item in current_bill:
            item_no, item_name, unit_price, quantity, total_price,gst,net_price= item
            bill_text.insert(tk.END, f"{item_no}\t\t{item_name}\t\t\t{unit_price}\t\t{quantity}\t\t{total_price}\t\t{gst}\t{net_price}\n")
            bill_text.insert(tk.END, "*" * 105 + "\n")
        total_amount = sum(item[6] for item in current_bill)
        total_amount_label.config(text=f"Total Amount: {total_amount:.2f}")
        bill_text.config(state=tk.DISABLED)
        

# Function to update the displayed bill
    def update_bill():
        display_customer_info()
        display_items()

# Function to bill an item
  # Function to bill an item
    finalize_stock_update = False
    def bill_item():
        item_no = item_no_bill_entry.get()
        quantity = quantity_bill_entry.get()
        customer_name = customer_name_entry.get()
        mode_of_payment = mode_of_payment_entry.get()

        if not item_no or not quantity:
            messagebox.showinfo("Error", "Item No and Quantity are required.")
            return

        try:
            item_no = int(item_no)
            quantity = int(quantity)

            cursor.execute("SELECT item_name, sale_price, expiry_date, gst FROM items WHERE itemno = %s", (item_no,))
            result = cursor.fetchone()

            if result:
                item_name, unit_price, expiry_date, gst = result
                cursor.execute("SELECT quantity FROM items WHERE itemno = %s", (item_no,))
                current_stock = cursor.fetchone()

                if current_stock:
                    current_stock = current_stock[0]
                    total_quantity_in_bill = sum(item[3] for item in current_bill if item[0] == item_no)
                    if current_stock >= (quantity + total_quantity_in_bill):
                        if expiry_date > datetime.now().date():  # Check if the product is not expired
                            total_price = unit_price * quantity
                            net_price = total_price * gst / 100 + total_price
                            current_bill.append((item_no, item_name, unit_price, quantity, total_price, gst, net_price))
                            update_bill()
                        else:
                            messagebox.showerror('Expired', 'This product is Expired')
                    else:
                        messagebox.showinfo("Error", "Insufficient stock for this item.")
                else:
                    messagebox.showinfo("Error", "Item not found.")
            else:
                messagebox.showinfo("Error", "Item not found.")

        except ValueError:
            messagebox.showinfo("Error", "Invalid quantity. Please enter a valid number.")


# Function to finalize the bill
    def finalize_bill():
        global finalize_stock_update
        customer_name = customer_name_entry.get()
        mode_of_payment = mode_of_payment_entry.get()

        customer_phone_number = customer_phone_number_entry.get()
        customer_address = customer_address_entry.get()
        if not customer_phone_number or not customer_address:
            messagebox.showinfo("Error", "phone number address need to be filled .")
            
        else:

            pygame.init()

            # Load the music file
            pygame.mixer.music.load(r"F:\Users\babu\Desktop\project\confirm.mp3")

            # Play the music
            pygame.mixer.music.play()

            for item in current_bill:
                item_no, item_name, unit_price, quantity, total_price, gst, net_price = item
                cursor.execute("select unit_price from items where itemno=%s", (item_no,))
                price = cursor.fetchone()
                m = price[0]
                cursor.execute("select gst from items where itemno=%s", (item_no,))
                tax = cursor.fetchone()
                t = tax[0]
                np = total_price + (total_price * t / 100)

                pur_price = unit_price * quantity

                cursor.execute(
                "INSERT INTO bills (customer_name, mode_of_payment, item_no, item_name, unit_price, quantity, total_price,phone_number,address,purchase_price,gst,net_price) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)",
                (customer_name, mode_of_payment, item_no, item_name, unit_price, quantity, total_price,
                customer_phone_number, customer_address, m, t, np,))
                conn.commit()
                cursor.execute("update items set quantity = quantity - %s where itemno=%s", (quantity,item_no,))
                conn.commit()

           
            current_bill.clear()
            update_bill()
            finalize_stock_update = False
    xyz = ttk.Style()
    xyz.configure("custom.TLabel", font=("Bernard MT condensed", 15),foreground="red")
    xyz.configure("custom.TEntry", font=("Bernard MT condensed", 30))
    xyz.configure("custom.TButton", font=("Bernard MT condensed", 15), background="black",foreground="green")

# Create UI elements
 
    customer_name_label = ttk.Label(billing_frame, text="Customer Name:",style="custom.TLabel")
    customer_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    customer_name_entry = ttk.Entry(billing_frame,style="custom.TEntry")
    customer_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    mode_of_payment_label = ttk.Label(billing_frame, text="Mode of Payment:",style="custom.TLabel")
    mode_of_payment_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    mode_of_payment_entry = ttk.Entry(billing_frame,style="custom.TEntry")
    mode_of_payment_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    item_no_bill_label = ttk.Label(billing_frame, text="Item No:",style="custom.TLabel")
    item_no_bill_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    item_no_bill_entry = ttk.Entry(billing_frame)
    item_no_bill_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    quantity_bill_label = ttk.Label(billing_frame, text="Quantity:",style="custom.TLabel")
    quantity_bill_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    quantity_bill_entry = ttk.Entry(billing_frame)
    quantity_bill_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    bill_button = ttk.Button(billing_frame, text="Bill Item", command=bill_item,style="custom.TButton")
    bill_button.grid(row=4, columnspan=2, pady=10)

    bill_text = tk.Text(billing_frame, height=20, width=110)
    bill_text.grid(row=5, columnspan=2, pady=10,sticky="nsew")
    bill_text.config(state=tk.DISABLED)

    total_amount_label = ttk.Label(billing_frame, text="Total Amount: 0.00",style="custom.TLabel")
    total_amount_label.grid(row=6, columnspan=2, pady=5)

    finalize_button = ttk.Button(billing_frame, text="Finalize Bill", command=finalize_bill,style="custom.TButton")
    finalize_button.grid(row=8, columnspan=2, pady=10)

    customer_phone_number_label = ttk.Label(billing_frame, text="Phone Number:",style="custom.TLabel")
    customer_phone_number_label.grid(row=4, column=2, padx=40, pady=5)
    customer_phone_number_entry = ttk.Entry(billing_frame)
    customer_phone_number_entry.grid(row=4, column=3, padx=45, pady=5)

    customer_address_label = ttk.Label(billing_frame, text="Address:",style="custom.TLabel")
    customer_address_label.grid(row=5, column=2, padx=40, pady=5,)
    customer_address_entry = ttk.Entry(billing_frame)
    customer_address_entry.grid(row=5, column=3, padx=45, pady=5)

    stock_treeview = ttk.Treeview(notebook, columns=("itemno", "item_name", "quantity",  "expiry_date", "sale_price","gst","net_price"))
    notebook.add(stock_treeview, text='Show Stock')
    button_frame = ttk.Frame(stock_treeview)
    button_frame.grid(row=0, column=0, pady=10)


    # Define columns for the table
    stock_treeview.heading("#1", text="Item No")
    stock_treeview.heading("#2", text="Item Name")
    stock_treeview.heading("#3", text="Quantity")
    
    stock_treeview.heading("#4", text="Expiry Date")
    stock_treeview.heading("#5", text="Sale Price")
    stock_treeview.heading("#6", text="gst")
    stock_treeview.heading("#7", text="net price")


    # Set column widths
    stock_treeview.column("#1", width=100)
    stock_treeview.column("#2", width=200)
    stock_treeview.column("#3", width=100)
 
    stock_treeview.column("#4", width=150)
    stock_treeview.column("#5", width=100)
    stock_treeview.column("#6", width=100)
    stock_treeview.column("#7", width=100)




    # Function to populate the table with stock data
    def show_stock():

        stock_treeview.delete(*stock_treeview.get_children())  # Clear the table
        cursor.execute("SELECT itemno,item_name,quantity,expiry_date,sale_price,gst,net_price FROM items")
        result = cursor.fetchall()
        for row in result:
            stock_treeview.insert("", "end", values=row)
    

    show_stock_button = ttk.Button(button_frame, text="Show Stock", command=show_stock)
    show_stock_button.grid(row=0, column=0, pady=10)
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 18))  # Increase the font size (12) as needed

# Increase the font size for cell values
      # Increase the font size (10) as needed

# Set the background color for the Treeview
    style.configure("Treeview", background="#D9E4FF")  # Change the color code to the color you want
    pygame.init()

# Load the music file
    pygame.mixer.music.load(r"F:\Users\babu\Desktop\project\success.mp3")

# Play the music
    pygame.mixer.music.play()
    customer_password_label=None

    def view_details():
        
        customer_username = customer_username_entry.get()
        cursor.execute("SELECT email, password FROM credentials where username=%s",(customer_username,) )
        results = cursor.fetchall()
        if results:
            email = results[0][0]
            password = results[0][1]
            customer_email_label.config(text=f"Email: {email}")
            customer_password_label.config(text=f"Password: {password}")
        else:
            customer_email_label.config(text="No details found")
            customer_password_label.config(text="No details found")
    
    view_details_frame = ttk.Frame(root)
    notebook.add(view_details_frame, text='view your details')
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\bill1.png")

# Add a label to display the image
    image_label = ttk.Label(view_details_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image 

# Create a custom style for labels, entry widgets, and the button
    custom_style = ttk.Style()
    custom_style.configure("Custom.TLabel", font=("Bernard MT condensed", 30))
    custom_style.configure("Custom.TEntry", font=("Bernard MT condensed", 30))
    custom_style.configure("Custom.TButton", font=("Bernard MT condensed", 30), background="black",foreground="green")

    customer_username_label= ttk.Label(view_details_frame, text="username ",style="Custom.TLabel")
    customer_username_label.grid(row=0, column=0, padx=10, pady=10)
    customer_username_entry = ttk.Entry(view_details_frame, width=30)
    customer_username_entry.grid(row=0, column=1, padx=10, pady=10)
    view_details_Button = ttk.Button(view_details_frame, text="view details", command=view_details , style="Custom.TButton")
    view_details_Button.grid(row=1, column=0, pady=10)
    customer_email_label = ttk.Label(view_details_frame, text="Email:",style="Custom.TLabel")
    customer_email_label.grid(row=2, column=0, padx=10, pady=5)

    customer_password_label = ttk.Label(view_details_frame, text="Password:",style="Custom.TLabel")
    customer_password_label.grid(row=3, column=0, padx=10, pady=5)
    
    notebook.add(billing_frame, text='Billing')
    otp_verified = {"status": False}
    edit_email_frame = ttk.Frame(root)
    notebook.add(edit_email_frame, text='Edit Email')
    image = PhotoImage(file=r"F:\users\babu\Desktop\project\add entry.png")

# Add a label to display the image
    image_label = ttk.Label(edit_email_frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image 

# Create a custom style for labels, entry widgets, and the button
    custom_style = ttk.Style()
    custom_style.configure("Custom.TLabel", font=("Bernard MT condensed", 30))
    custom_style.configure("Custom.TEntry", font=("Bernard MT condensed", 30))
    custom_style.configure("Custom.TButton", font=("Bernard MT condensed", 30), background="black",foreground="crimson")

    
    def generate_otp():
        return str(random.randint(1000, 9999))

    def send_otp():
        email = email_entry.get()
        cursor.execute("SELECT * FROM CREDENTIALS WHERE EMAIL=%s",(email, ))
        result=cursor.fetchone()
        if result:
        
    
            if email:
                global otp
                otp = generate_otp()

                # Email settings
                sender_email = "groceryshop06@gmail.com"  # Replace with your email
                sender_password = "einldaxynzpoapjb"  # Replace with your email password
                subject = "Your OTP Code"
                body = f"hi Your OTP code is: {otp}"

            # Create the email message
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                try:
                    # Connect to the SMTP server and send the email
                    server = smtplib.SMTP("smtp.gmail.com", 587)  # Replace with your SMTP server and port
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, email, msg.as_string())
                    server.quit()

                    otp_verified["status"] = True
                    messagebox.showinfo("OTP Sent", "An OTP has been sent to your email.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to send OTP: {e}")
            else:
                messagebox.showerror("Error", "Please enter an email address.")
        else:
            messagebox.showerror("Error", " email address  not found.")


    def edit_email():
        email = email_entry.get()
        cursor.execute("select * from credentials where email=%s",(email,))
        result=cursor.fetchone()
        if result:
        
            if otp_verified["status"]:
                entered_otp = entered_otp_entry.get()
            
        
                if otp == entered_otp:
                    new_email = new_email_entry.get()
                
            
                    cursor.execute("UPDATE credentials SET email = %s WHERE email = %s", (new_email, email))
                    conn.commit()
                    messagebox.showinfo("Success", "Email updated successfully.")
                    otp_verified["status"] = False
                else:
                    messagebox.showerror("Error", "Invalid OTP.")
            else:
                messagebox.showerror("Error, entered email does not exist/otp not entered.")
        else:
            messagebox.showerror("Error", "Email does not exist.")

# UI elements for the Edit Email frame
    email_label = ttk.Label(edit_email_frame, text="Enter your email address:",style="Custom.TLabel")
    email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    email_entry = ttk.Entry(edit_email_frame)
    email_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")


  

    entered_otp_label = ttk.Label(edit_email_frame, text="Enter OTP:",style="Custom.TLabel")
    entered_otp_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entered_otp_entry = ttk.Entry(edit_email_frame)
    entered_otp_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    new_email_label = ttk.Label(edit_email_frame, text="Enter new email:",style="Custom.TLabel")
    new_email_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    new_email_entry = ttk.Entry(edit_email_frame)
    new_email_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    send_otp_button = ttk.Button(edit_email_frame, text="Send OTP", command=send_otp,style="Custom.TButton")
    send_otp_button.grid(row=5, columnspan=2, pady=10)

    verify_otp_button = ttk.Button(edit_email_frame, text="Verify and Update Email", command=edit_email,style="Custom.TButton")
    verify_otp_button.grid(row=6, columnspan=2, pady=10)

    notebook.pack(fill='both', expand='yes')












root.mainloop()
    
 
    

       

    
    








    

    


