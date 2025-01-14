import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

# Constants
NUM_ITEMS = 5
FILENAME = "products.txt"
ADMIN_PASSWORD = "1222"
LOGO_FILENAME = "logo.png"  # Replace with your logo file if available

# Global variables
in_stock = [0] * NUM_ITEMS
food_names = [""] * NUM_ITEMS
prices = [0.0] * NUM_ITEMS

def load_products():
    global food_names, prices, in_stock
    if not os.path.exists(FILENAME):
        print(f"Error: could not open {FILENAME}.")
        sys.exit(1)
    
    with open(FILENAME, 'r') as file:
        for i in range(NUM_ITEMS):
            line = file.readline()
            if not line:
                print(f"Error: insufficient data in {FILENAME}.")
                sys.exit(1)
            parts = line.strip().split(',')
            if len(parts) != 3:
                print(f"Error: invalid format in {FILENAME} on line {i+1}.")
                sys.exit(1)
            food_names[i] = parts[0]
            try:
                prices[i] = float(parts[1])
                in_stock[i] = int(parts[2])
            except ValueError:
                print(f"Error: invalid numerical data in {FILENAME} on line {i+1}.")
                sys.exit(1)

def save_products():
    with open(FILENAME, 'w') as file:
        for i in range(NUM_ITEMS):
            file.write(f"{food_names[i]},{prices[i]:.2f},{in_stock[i]}\n")

def print_food_table():
    print("______________________________________________________")
    print("|  Item No.  |  Item Name   |  Price    |  In Stock   |")
    print("------------------------------------------------------")
    for i in range(NUM_ITEMS):
        print(f"|    {i + 1:2d}      | {food_names[i]:<12} | {prices[i]:6.2f}    |     {in_stock[i]:3d}     |")
        if i != NUM_ITEMS - 1:
            print("+----------------------------------------------------+")
    print("+-----------------------------------------------------+")

def display_menu():
    print("\nWelcome to SmartBUY. How may I help you?")
    print("1. Order Products")
    print("2. Admin Panel")
    print("3. Exit")

def display_admin_menu():
    password = input("\nEnter admin password: ")
    if password == ADMIN_PASSWORD:
        while True:
            print("\nAdmin Panel:")
            print("1. View Transactions")
            print("2. Edit Product")
            print("3. Return to Main Menu")
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Error: invalid input.")
                continue

            if choice == 1:
                view_transactions()
            elif choice == 2:
                edit_product()
                save_products()
            elif choice == 3:
                break
            else:
                print("Error: invalid choice.")
    else:
        print("Error: incorrect password.")

def generate_pdf_receipt(pdf_filename, receipt_data):
    """
    Generates a PDF receipt using ReportLab's Platypus.
    """
    try:
        doc = SimpleDocTemplate(pdf_filename, pagesize=LETTER,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        elements = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=1))
        styles.add(ParagraphStyle(name='Left', alignment=0))
        
        # Header with logo and company name
        if os.path.exists(LOGO_FILENAME):
            im = Image(LOGO_FILENAME, 2*inch, 2*inch)
            im.hAlign = 'LEFT'
            elements.append(im)
        else:
            # Placeholder if logo not found
            elements.append(Paragraph("<b>SmartBUY</b>", styles['Title']))
        
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("<b>SmartBUY: A Product Order Management System</b>", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Date: {receipt_data['date']}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Table for items
        data = [['Item', 'Quantity', 'Price (USD)', 'Total (USD)']]
        for item, qty, price, total in zip(receipt_data['items'], receipt_data['quantities'], receipt_data['prices'], receipt_data['totals']):
            data.append([item, str(qty), f"${price:.2f}", f"${total:.2f}"])
        data.append(['', '', 'Total', f"${receipt_data['grand_total']:.2f}"])

        # Create table
        table = Table(data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 24))
        
        # Footer
        elements.append(Paragraph("Thank you for shopping with us!", styles['Center']))
        
        doc.build(elements)
        print(f"PDF receipt has been saved to {pdf_filename}")
    except Exception as e:
        print(f"Error creating PDF: {e}")

def print_receipt(num_items, f, q, total):
    try:
        with open("bill.txt", 'w') as bill_file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bill_file.write("------------------------------------------\n")
            bill_file.write("SmartBUY: A Product Order Management System\n")
            bill_file.write("------------------------------------------\n")
            bill_file.write(f"Date: {current_time}\n")
            bill_file.write("------------------------------------------\n")
            bill_file.write("{:<15} {:<10} {:<10} {:<10}\n".format("Item", "Quantity", "Price", "Total"))
            bill_file.write("------------------------------------------\n")
            for i in range(num_items):
                bill_file.write("{:<15} {:<10} ${:<9.2f} ${:<9.2f}\n".format(
                    food_names[f[i] - 1],
                    q[i],
                    prices[f[i] - 1],
                    prices[f[i] - 1] * q[i]
                ))
            bill_file.write("------------------------------------------\n")
            bill_file.write("{:<15} {:<10} {:<10} ${:<9.2f}\n".format("", "", "TOTAL", total))
            bill_file.write("------------------------------------------\n")
            bill_file.write(" Thank you for choosing SmartBUY!          \n")
            bill_file.write("------------------------------------------\n")
        print("Bill has been saved to bill.txt")
    except Exception as e:
        print(f"Error creating bill file: {e}")

def log_transaction(num_items, f, q, total):
    try:
        with open("transactions.log", 'a') as log_file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write("------------------------------------------\n")
            log_file.write(f"Date: {current_time}\n")
            log_file.write("------------------------------------------\n")
            log_file.write("{:<15} {:<10} {:<10} {:<10}\n".format("Item", "Qty", "Price", "Total"))
            log_file.write("------------------------------------------\n")
            for i in range(num_items):
                log_file.write("{:<15} {:<10} ${:<9.2f} ${:<9.2f}\n".format(
                    food_names[f[i] - 1],
                    q[i],
                    prices[f[i] - 1],
                    prices[f[i] - 1] * q[i]
                ))
            log_file.write("------------------------------------------\n")
            log_file.write("{:<15} {:<10} {:<10} ${:<9.2f}\n".format("", "", "TOTAL", total))
            log_file.write("------------------------------------------\n")
    except Exception as e:
        print(f"Error creating transaction log file: {e}")

def view_transactions():
    if not os.path.exists("transactions.log"):
        print("No transactions found.")
        return
    try:
        with open("transactions.log", 'r') as log_file:
            content = log_file.read()
            print("\n----- Transactions -----")
            print(content)
            print("------------------------\n")
    except Exception as e:
        print(f"Error opening transaction log file: {e}")

def edit_product():
    print_food_table()
    try:
        choice = int(input("Enter the product no. to edit: "))
        if choice < 1 or choice > NUM_ITEMS:
            print("Error: invalid Item number.")
            return
    except ValueError:
        print("Error: invalid input.")
        return

    try:
        new_price = float(input("Enter the new price (USD): "))
        if new_price < 0:
            print("Error: invalid price.")
            return
    except ValueError:
        print("Error: invalid price.")
        return

    try:
        new_stock = int(input("Enter the new stock quantity: "))
        if new_stock < 0:
            print("Error: invalid stock quantity.")
            return
    except ValueError:
        print("Error: invalid stock quantity.")
        return

    prices[choice - 1] = new_price
    in_stock[choice - 1] = new_stock
    print("Product updated successfully.")

def display_receipt():
    """Function to display the contents of bill.txt."""
    if not os.path.exists("bill.txt"):
        print("No receipt found.")
        return
    try:
        with open("bill.txt", 'r') as bill_file:
            receipt = bill_file.read()
            print("\n----- Receipt -----")
            print(receipt)
            print("-------------------\n")
    except Exception as e:
        print(f"Error reading bill file: {e}")

def main():
    load_products()
    
    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Error: invalid input.")
            continue

        if choice == 1:
            print("You have selected Order Products.")
            print_food_table()
            f = []  # List to store item numbers
            q = []  # List to store quantities
            total = 0.0

            while True:
                item_input = input("Enter the item no. to order (press Enter to finish): ").strip()
                if item_input == '':
                    break
                try:
                    item_no = int(item_input)
                    if item_no < 1 or item_no > NUM_ITEMS:
                        print("Error: invalid item number.")
                        continue
                except ValueError:
                    print("Error: please enter a valid item number or press Enter to finish.")
                    continue

                try:
                    quantity_input = input(f"Enter the quantity for {food_names[item_no - 1]}: ").strip()
                    quantity = int(quantity_input)
                    if quantity < 1:
                        print("Error: invalid quantity.")
                        continue
                except ValueError:
                    print("Error: please enter a valid quantity.")
                    continue

                if quantity > in_stock[item_no - 1]:
                    print(f"Error: insufficient stock for {food_names[item_no - 1]}. Available: {in_stock[item_no - 1]}")
                    continue

                # Update order lists and total
                f.append(item_no)
                q.append(quantity)
                total += prices[item_no - 1] * quantity
                in_stock[item_no - 1] -= quantity
                print(f"You have ordered {quantity} {food_names[item_no - 1]}. Total cost so far: ${total:.2f}")

            if not f:
                print("No items ordered.")
                continue

            # Generate and log the receipt
            print_receipt(len(f), f, q, total)
            log_transaction(len(f), f, q, total)
            save_products()

            # Display the saved receipt
            display_receipt()

            # Prompt for PDF receipt
            while True:
                receipt_choice = input("Do you want a PDF receipt? (1 = Yes, 2 = No): ").strip().lower()
                if receipt_choice in ['1', 'yes']:
                    # Prepare data for PDF
                    receipt_data = {
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'items': [food_names[item - 1] for item in f],
                        'quantities': q,
                        'prices': [prices[item - 1] for item in f],
                        'totals': [prices[item - 1] * qty for item, qty, qty in zip(f, q, q)],
                        'grand_total': total
                    }
                    generate_pdf_receipt("bill.pdf", receipt_data)
                    break
                elif receipt_choice in ['2', 'no', '']:
                    print("No PDF receipt will be created.")
                    break
                else:
                    print("Invalid input. Please enter 1 for Yes or 2 for No.")

        elif choice == 2:
            display_admin_menu()

        elif choice == 3:
            print("Thanks for visiting.")
            break

        else:
            print("Error: invalid choice.")

if __name__ == "__main__":
    main()
