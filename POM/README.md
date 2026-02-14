# 🚀 Selenium Automation Framework | Page Object Model (POM)

![Selenium](https://img.shields.io/badge/Selenium-Automation-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![PyTest](https://img.shields.io/badge/PyTest-TestRunner-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📌 About the Project
This repository contains a **real-world Selenium Automation Framework** designed using the **Page Object Model (POM)** pattern.

The framework demonstrates **industry-standard automation practices** including clean architecture, reusable components, and scalable test design — suitable for both **learning** and **professional portfolio showcasing**.

---

## 🎯 Why This Project?
✔ Demonstrates strong understanding of automation architecture  
✔ Follows best practices used in real-time projects  
✔ Clean separation of test logic and UI interactions  
✔ Ideal for interviews & GitHub portfolio review  

---

## 🛠️ Tech Stack
- **Programming Language:** Python  
- **Automation Tool:** Selenium WebDriver  
- **Test Framework:** PyTest  
- **Design Pattern:** Page Object Model (POM)  
- **Browser Support:** Chrome (extendable)

---

## 🌐 Application Under Test
**SauceDemo – Demo E-Commerce Application**  
🔗 https://www.saucedemo.com/

### Test Credentials
Username: standard_user
Password: secret_sauce


---

## 🧠 Framework Architecture (POM)
- Each web page is represented as a **separate class**
- Page classes handle:
  - Element locators
  - Page-level actions
- Test classes handle:
  - Test scenarios
  - Assertions
- Utilities manage:
  - WebDriver setup
  - Configuration
  - Common reusable methods

---

## 📂 Project Structure
POM_Automation_Project/
│
├── tests/ # Test cases
│ ├── test_login.py
│ ├── test_product.py
│ ├── test_cart.py
│ └── test_checkout.py
│
├── pages/ # Page Object classes
│ ├── login_page.py
│ ├── products_page.py
│ ├── cart_page.py
│ └── checkout_page.py
│
├── utilities/ # Framework utilities
│ ├── driver_setup.py
│ ├── config_reader.py
│ └── common_methods.py
│
├── testdata/ # Test data
│ └── test_data.py
│
├── reports/ # Test execution reports
│
├── screenshots/ # Failure screenshots
│
├── config/ # Configuration files
│ └── config.ini
│
├── requirements.txt
└── README.md



---

## ✅ Automated Test Scenarios
- Login with valid credentials
- Login with invalid credentials
- Add product to cart
- Verify cart items
- Complete checkout process
- Logout from application

---

## ▶️ How to Run the Tests

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
