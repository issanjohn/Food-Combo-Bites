
from pyscript import document, when

# ==========================================
# FOOD COMBO BITES - MAIN.PY
# ==========================================

PRODUCTS = [
    {
        "name": "Cheese Bites",
        "price": 59,
        "icon": "🧀",
        "description": "Crispy, cheesy bites."
    },
    {
        "name": "Burger Combo",
        "price": 99,
        "icon": "🍔",
        "description": "A delicious burger snack combo."
    },
    {
        "name": "Fries Combo",
        "price": 69,
        "icon": "🍟",
        "description": "Golden and crispy fries."
    },
    {
        "name": "Chicken Bites",
        "price": 89,
        "icon": "🍗",
        "description": "Crunchy chicken pieces."
    },
    {
        "name": "Snack Combo",
        "price": 79,
        "icon": "🍱",
        "description": "A satisfying snack combination."
    },
    {
        "name": "Iced Drink",
        "price": 39,
        "icon": "🥤",
        "description": "A refreshing cold drink."
    }
]

cart = []
current_page = "home-page"


# ==========================================
# HELPERS
# ==========================================

def money(amount):
    return f"₱{amount:.2f}"


def show_message(message):
    toast = document.getElementById("toast")

    if toast:
        toast.textContent = message
        toast.hidden = False


def clear_order_message():
    message = document.getElementById("order-message")

    if message:
        message.textContent = ""


# ==========================================
# PRODUCT CARDS
# ==========================================

def make_product_card(product):
    card = document.createElement("article")
    card.className = "product-card"

    icon = document.createElement("div")
    icon.className = "product-icon"
    icon.textContent = product["icon"]

    title = document.createElement("h3")
    title.textContent = product["name"]

    description = document.createElement("p")
    description.textContent = product["description"]

    price = document.createElement("div")
    price.className = "product-price"
    price.textContent = money(product["price"])

    button = document.createElement("button")
    button.className = "add-btn"
    button.type = "button"
    button.textContent = "Add to Cart"

    # Store the product name on the button.
    button.setAttribute("data-product", product["name"])

    card.appendChild(icon)
    card.appendChild(title)
    card.appendChild(description)
    card.appendChild(price)
    card.appendChild(button)

    return card


def render_products():
    menu = document.getElementById("menu-list")
    bestsellers = document.getElementById("bestseller-list")

    if menu:
        menu.innerHTML = ""

        for product in PRODUCTS:
            menu.appendChild(make_product_card(product))

    if bestsellers:
        bestsellers.innerHTML = ""

        for product in PRODUCTS[:3]:
            bestsellers.appendChild(make_product_card(product))


# ==========================================
# NAVIGATION
# ==========================================

def navigate(page_id):
    global current_page

    page_ids = [
        "home-page",
        "bestsellers-page",
        "menu-page",
        "order-page",
        "settings-page"
    ]

    if page_id not in page_ids:
        return

    current_page = page_id

    for page_id_item in page_ids:
        page = document.getElementById(page_id_item)

        if page:
            page.hidden = page_id_item != page_id

    buttons = document.querySelectorAll(".nav-btn")

    for button in buttons:
        active = button.getAttribute("data-page") == page_id
        button.classList.toggle("active", active)

    if page_id == "order-page":
        render_cart()


@when("click", "#enter-btn")
def enter_website(event):
    welcome = document.getElementById("welcome-page")
    main = document.getElementById("main-site")

    if welcome:
        welcome.hidden = True

    if main:
        main.hidden = False

    navigate("home-page")


@when("click", ".nav-btn")
def navigation_clicked(event):
    target = event.target

    while target and not target.classList.contains("nav-btn"):
        target = target.parentElement

    if target:
        page_id = target.getAttribute("data-page")

        if page_id:
            navigate(page_id)


@when("click", "[data-page].primary-btn")
def home_navigation_clicked(event):
    target = event.target

    while target and not target.hasAttribute("data-page"):
        target = target.parentElement

    if target:
        page_id = target.getAttribute("data-page")

        if page_id:
            navigate(page_id)


# ==========================================
# ADD TO CART
# ==========================================

def add_product(product_name):
    for product in PRODUCTS:
        if product["name"] == product_name:
            cart.append({
                "name": product["name"],
                "price": product["price"]
            })

            update_cart_count()
            render_cart()
            clear_order_message()

            show_message(
                product["name"] + " added to your cart!"
            )
            return

    show_message("Sorry, this product could not be found.")


def handle_add_click(event):
    target = event.target

    # Find the Add to Cart button that was clicked.
    while target and not target.classList.contains("add-btn"):
        target = target.parentElement

    if not target:
        return

    product_name = target.getAttribute("data-product")

    if product_name:
        add_product(product_name)


# These handlers are attached to existing parent containers.
# They also work for product cards created later by Python.

@when("click", "#menu-list")
def menu_add_clicked(event):
    handle_add_click(event)


@when("click", "#bestseller-list")
def bestseller_add_clicked(event):
    handle_add_click(event)


# ==========================================
# CART COUNT AND TOTAL
# ==========================================

def update_cart_count():
    counter = document.getElementById("cart-count")

    if counter:
        counter.textContent = str(len(cart))


def render_cart():
    container = document.getElementById("cart-items")
    total_element = document.getElementById("cart-total")

    if not container or not total_element:
        update_cart_count()
        return

    container.innerHTML = ""

    if not cart:
        empty = document.createElement("p")
        empty.textContent = "Your order is currently empty."
        container.appendChild(empty)

    for index, item in enumerate(cart):
        row = document.createElement("div")
        row.className = "cart-row"

        details = document.createElement("div")
        details.textContent = (
            f'{item["name"]} — {money(item["price"])}'
        )

        remove_button = document.createElement("button")
        remove_button.className = "remove-btn"
        remove_button.type = "button"
        remove_button.textContent = "Remove"
        remove_button.setAttribute(
            "data-remove-index", str(index)
        )

        row.appendChild(details)
        row.appendChild(remove_button)
        container.appendChild(row)

    total = sum(item["price"] for item in cart)

    total_element.textContent = money(total)
    update_cart_count()


# ==========================================
# REMOVE ITEM
# ==========================================

@when("click", "#cart-items")
def remove_cart_item(event):
    target = event.target

    while target and not target.classList.contains("remove-btn"):
        target = target.parentElement

    if not target:
        return

    try:
        index = int(target.getAttribute("data-remove-index"))

        if 0 <= index < len(cart):
            removed = cart.pop(index)

            render_cart()
            clear_order_message()

            show_message(
                removed["name"] + " removed from your cart."
            )

    except (ValueError, TypeError):
        show_message("Unable to remove this item.")


# ==========================================
# CLEAR CART
# ==========================================

@when("click", "#clear-cart")
def clear_cart_clicked(event):
    cart.clear()

    render_cart()
    clear_order_message()

    show_message("Your order has been cleared.")


# ==========================================
# ORDER NOW
# ==========================================

@when("click", "#order-now-btn")
def order_now_clicked(event):
    message = document.getElementById("order-message")

    if not message:
        return

    if not cart:
        message.textContent = (
            "Your order is empty. Please add items first."
        )
        return

    message.textContent = (
        "Order successful, delivery is on your way!"
    )

    # Demo confirmation: clear the cart after successful confirmation.
    cart.clear()
    render_cart()


# ==========================================
# SETTINGS
# ==========================================

@when("change", "#dark-mode")
def dark_mode_changed(event):
    checkbox = document.getElementById("dark-mode")

    if checkbox:
        document.body.classList.toggle(
            "dark-mode", checkbox.checked
        )


@when("change", "#large-text")
def large_text_changed(event):
    checkbox = document.getElementById("large-text")

    if checkbox:
        document.body.classList.toggle(
            "large-text", checkbox.checked
        )


# ==========================================
# INITIALIZE WEBSITE
# ==========================================

render_products()
update_cart_count()
