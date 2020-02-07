from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os
import base64

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'Login' page of the shopping site"""
    return redirect("/login")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons has to offer"""
    melons = model.get_melons()
    print(session,"########")
    if "user" in session and session["logged_in"] is True:
        customer = model.get_customer_by_email(str(session["user"]))
        flash("Welcome, %s %s" % (customer.givenname, customer.surname))

    else:
        flash("That is an invalid login.")
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""

    melon = model.get_melon_by_id(id)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added."""
    if "cart" not in session or len(session["cart"])== 0 :
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        if "user" in session and session["logged_in"] == True:
            customer = model.get_customer_by_email(str(session["user"]))
            flash("Welcome, %s %s" % (customer.givenname, customer.surname))
        else:
            flash("That is an invalid login.")


        items = session["cart"]
        dict_of_melons = {}

        total_price = 0
        for item in items:
            #print(item,"#############")
            melon = model.get_melon_by_id(item)
            total_price += melon.price
            if melon.id in dict_of_melons:
                dict_of_melons[melon.id]["qty"] += 1
            else:
                dict_of_melons[melon.id] = {"qty":1, "name": melon.common_name, "price":melon.price}
        print(dict_of_melons)
        return render_template("cart.html", display_cart = dict_of_melons, total = total_price)  
    

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    if "cart" not in session:
        session["cart"] = []

    session["cart"]
    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/cart")



@app.route("/del_to_cart/<int:id>")
def del_from_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is delete from a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully deleted from cart" """

    if "cart" not in session:
        session["cart"] = []

    print session["cart"]
    session["cart"].pop(session["cart"].index(id))

    flash("Successfully deleted from cart!")
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    session["logged_in"] = False
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    session["logged_in"] = False
    email = request.form.get("email")
    password = request.form.get("password")
    customer = model.get_customer_by_email(email)

    if customer.email == email and customer.password == base64.b64encode(password.encode("utf-8")) :
        #flash("Welcome, %s %s" % (customer.givenname, customer.surname))
        #user={"username":customer.givenname+" "+customer.surname}
        if "user" in session:
            session["logged_in"] = True
        else:
            session["user"] = email
            session["logged_in"] = True
        return redirect("/melons")
    else:
        flash("That is an invalid login.")
        session["logged_in"] = False
        return render_template("login.html")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented later .")
    return redirect("/melons")



@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect("/login")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)
