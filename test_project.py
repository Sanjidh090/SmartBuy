import pytest
from project import calculate_total, validate_item_number, validate_stock

# Sample data for testing
test_prices = [0.50,0.30,0.80,1.20, 1.00]
test_in_stock = [100, 150, 80, 50, 60]

def test_calculate_total():
    assert calculate_total(0.50, 5) == 2.50
    assert calculate_total(0.30, 10) == 3.00
    assert calculate_total(0.80, 2) == 1.60
    assert calculate_total(1.20, 4) == 4.80
    assert calculate_total(1.00, 0) == 0.00

def test_validate_item_number():
    assert validate_item_number(1) == True
    assert validate_item_number(5) == True
    assert validate_item_number(0) == False
    assert validate_item_number(6) == False
    assert validate_item_number(-1) == False

def test_validate_stock(monkeypatch):
    # Mocking_the in_stock list
    monkeypatch.setattr('project.in_stock', test_in_stock)

    assert validate_stock(1, 50) == True    # 100 >= 50
    assert validate_stock(2, 150) == True
    assert validate_stock(3, 80) == True    # 80 >= 80
    assert validate_stock(4, 51) == False
    assert validate_stock(5, 60) == True    # 60 >= 60
    assert validate_stock(5, 61) == False
