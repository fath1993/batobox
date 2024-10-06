# Online Marketplace to Buy from Amazon and Shipping

This project is an online marketplace that allows users to browse products from Amazon, place orders, and arrange shipping through a simplified platform. The platform integrates with Amazon's product catalog and provides an easy checkout process with additional shipping options.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Browse products from Amazon with real-time data.
- Add items to a cart and proceed to checkout.
- Simplified checkout process with multiple payment options.
- Custom shipping options and tracking for orders.
- User profiles to manage previous orders and shipping addresses.
- Integration with Amazon's API for product details and pricing.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/online-marketplace-amazon.git
    ```

2. Navigate into the project directory:
    ```bash
    cd online-marketplace-amazon
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for the admin interface (optional):
    ```bash
    python manage.py createsuperuser
    ```

6. Set up the Amazon API integration by adding your credentials to the `.env` file:
    ```bash
    AMAZON_API_KEY=your_amazon_api_key
    ```

7. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

Once the server is running, visit `http://127.0.0.1:8000/` in your browser to start using the marketplace.

- **Browse products**: Search for products from Amazon by keyword or category.
- **Add to cart**: Add products to your cart for purchase.
- **Checkout**: Use the simple checkout process to confirm your order and choose shipping options.
- **Order tracking**: View the status of
