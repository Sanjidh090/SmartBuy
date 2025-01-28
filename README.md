# SmartBuy
This is my project "Smartbuy", a product order management system.I have coded this in C &  python

# SmartBUY: A Product Order Management System

#### Video Demo: [https://youtu.be/QbBGb6yyDeE]

## **Description**

SmartBUY is a command-line based Product Order Management System built using Python. It allows users to:

- **Order Products**: Browse available products, place orders, and receive receipts.
- **Admin Panel**: View transaction logs and edit product details (price and stock).

## **Features**

1. **Order Products**:
    - Displays a list of available products with their prices and stock.
    - Allows users to add multiple products to their order.
    - Generates a textual receipt (`bill.txt`) and offers to create an elegant PDF receipt (`bill.pdf`).

2. **Admin Panel**:
    - **View Transactions**: Access a log of all past transactions (`transactions.log`).
    - **Edit Product**: Update the price and stock quantity of existing products.

## **Files**

1. **`project.py`**: Contains the main code for the SmartBUY application, including all core functions.
2. **`test_project.py`**: Contains unit tests for the core functions using `pytest`.
3. **`requirements.txt`**: Lists external libraries required for the project.
4. **`README.md`**: Provides an overview and instructions for the project.
5. **`products.txt`**: Stores product data in the format `ProductName,Price,InStock`.
6. **`transactions.log`**: Logs all transactions made through the system (generated at runtime).
7. **`bill.txt`**: Generates a textual receipt for each order (created at runtime).
8. **`bill.pdf`**: Generates a PDF version of the receipt upon user request (created at runtime).


1. **Main Menu**:

    ```
    Welcome to SmartBUY. How may I help you?
    1. Order Products
    2. Admin Panel
    3. Exit
    Enter your choice:
    ```

3. **Ordering Products**:

    - Select **Option 1**.
    - Browse the list of products.
    - Enter the item number and quantity for each product you wish to order.
    - Press **Enter** without typing an item number to finish ordering.
    - View your textual receipt.
    - Choose whether to generate a PDF receipt.

4. **Admin Panel**:

    - Select **Option 2**.
    - Enter the admin password (`1222`).
    - Choose to view transactions or edit product details.

5. **Exit**:

    - Select **Option 3** to exit the application.

## **Testing**

Ensure that `pytest` is installed. To run the tests:

```bash
pytest test_project.py

