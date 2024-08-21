from flask import render_template, request, redirect, jsonify, url_for
from app import app, db, models
from .forms import SignupForm, LoginForm, AddressForm, ChangePass,\
                   SearchProductsForm
from flask_login import login_user, login_required, logout_user, current_user
import datetime
import math


def getNumBasketItems():
    numBasketItems = 0
    # if the current user is logged in
    if (current_user.is_authenticated):
        # get the number of basket items to dispay next to basket
        basketItems = current_user.accountbasket.all()
        for i in basketItems:
            numBasketItems += i.quantity
    else:
        numBasketItems = 0

    return numBasketItems


@app.route('/', methods=['GET', 'POST'])
def home():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()

    # render page
    return render_template('home.html', title='Home',
                           numBasketItems=numBasketItems)


# gets all the info to loop over products the correct amount
def getProducts(products):
    # if there is products
    if products:
        productsRows = [0]
        productsLength = len(products)
        numOfRows = math.ceil(productsLength / 3)
        # add to array so can loop between for different rows
        for i in range(1, numOfRows):
            productsRows.append(i*3)

        # if rows isnt multiple of 3 then add it onto the array so
        # can loop over the odd number
        if (productsLength % 3) > 0:
            productsRows.append(productsRows[-1] + productsLength % 3)

    return numOfRows, productsRows


@app.route('/products', methods=['GET', 'POST'])
def products():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()
    # get all products
    # used to display the products on the page

    # search form
    searchProductsForm = SearchProductsForm()

    # if search form is valid and submit button is pressed
    if (searchProductsForm.submitSearch.data and
            searchProductsForm.validate_on_submit()):

        # if nothing is entered, then show all the products
        if searchProductsForm.productTag.data == "":
            products = models.Products.query.all()
            # get required data
            numOfRows, productsRows = getProducts(products)

        # otherwise get all the products with the tag entered, relationally
        else:
            products = models.Products.query.join(models.Products.tags, aliased=True).filter_by(tagName=searchProductsForm.productTag.data).all()
            # get required data
            numOfRows, productsRows = getProducts(products)

    # if form hasnt been submitted then we just want to show all the products
    else:
        products = models.Products.query.all()
        # get required data
        numOfRows, productsRows = getProducts(products)

    # render page
    return render_template('products.html', title='Products',
                           numBasketItems=numBasketItems, products=products,
                           searchProductsForm=searchProductsForm,
                           numOfRows=numOfRows, productsRows=productsRows)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()
    # form for signing up
    signupForm = SignupForm()

    # validating if submit button has been pressed and if data is valid
    if (signupForm.createAccount.data and
            signupForm.validate_on_submit()):
        # signup checking is done in forms
        # creating an account model using the from data
        account = models.Accounts(firstName=signupForm.firstName.data,
                                  lastName=signupForm.lastName.data,
                                  email=signupForm.email.data,
                                  password=signupForm.password.data)
        # add to database
        db.session.add(account)
        db.session.commit()
        # show login page
        return redirect(url_for('login'))

    # render page
    return render_template('signup.html', title='Signup',
                           numBasketItems=numBasketItems,
                           signupForm=signupForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()
    # form for logging in up
    loginForm = LoginForm()

    # validating if submit button has been pressed and if data is valid
    if (loginForm.submitLogin.data and
            loginForm.validate_on_submit()):
        # login checking is done in forms
        # get account object using email inputted
        user = models.Accounts.query.filter_by(
            email=loginForm.email.data).first()
        # login user
        if user:
            login_user(user)
            # show home page
            return redirect(url_for('home'))

    # render page
    return render_template('login.html', title='Login',
                           numBasketItems=numBasketItems, loginForm=loginForm)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # logout user
    logout_user()
    return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()

    # render page
    return render_template('account.html', title='Your Account',
                           numBasketItems=numBasketItems)


@app.route('/addresses', methods=['GET', 'POST'])
@login_required
def addresses():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()
    addressForm = AddressForm()

    # get users addresses
    addresses = current_user.address.all()

    if (addressForm.submitAddress.data and
            addressForm.validate_on_submit()):
        # create address object
        addressNew = models.Addresses(houseNumName=addressForm.
                                      houseNumName.data,
                                      street=addressForm.street.data,
                                      town=addressForm.town.data,
                                      postcode=addressForm.postcode.data)

        # add to database relating to current user account
        # many to many
        current_user.address.append(addressNew)
        db.session.add(current_user)
        db.session.add(addressNew)
        db.session.commit()

        # refresh page to show change
        return redirect(url_for("addresses"))

    # render page
    return render_template('addresses.html', title='Addresses',
                           numBasketItems=numBasketItems,
                           addressForm=addressForm,
                           addresses=addresses)


@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()

    # all basket items
    basket = current_user.accountbasket.all()

    costPerItem = []
    totalCost = 0
    totalNumOfRows = 0
    # loops through all the basket items and gets the total cost and the cost
    # per individal item
    for i in basket:
        costPerItem.append(format(i.quantity * i.cost, ".2f"))
        totalCost += i.quantity * i.cost
        totalNumOfRows += 1

    # format total cost so only 2dp
    totalCost = format(totalCost, ".2f")

    # render page
    return render_template('basket.html', title='Basket',
                           numBasketItems=numBasketItems,
                           basket=basket, totalNumOfRows=totalNumOfRows,
                           costPerItem=costPerItem, totalCost=totalCost)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()
    # all user addresses
    addresses = current_user.address.all()
    # so inform user to add an address to checkout if not atleast one added
    numAddresses = len(addresses)

    # render page
    return render_template('checkout.html', title='Orders',
                           numBasketItems=numBasketItems, addresses=addresses,
                           numAddresses=numAddresses)


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()

    # all orders
    orders = current_user.accountorders.order_by(models.Orders.orderID.desc()
                                                 ).all()

    totalNumOrders = 0
    totalOrderCost = 0
    orderRow = 0
    # total cost per order
    totalOrderCosts = []
    # the limits to loop between
    orderRows = []
    # each order address
    orderAddresses = []
    # if theres atleast 1 order add to the arrays
    if orders:
        orderRows.append(0)
        currentOrderID = orders[0].orderID
        orderAddress = models.Addresses.query.filter_by(id=orders[0].addressID
                                                        ).first()
        orderAddresses.append([orderAddress.houseNumName, orderAddress.street])

    # loop through all orders
    for i in orders:
        # then for each order num change add to the arrays again
        if currentOrderID != i.orderID:
            orderAddress = models.Addresses.query.filter_by(id=i.addressID
                                                            ).first()
            orderAddresses.append([orderAddress.houseNumName,
                                   orderAddress.street])
            currentOrderID = i.orderID
            totalNumOrders += 1
            orderRows.append(orderRow)
            totalOrderCost = format(totalOrderCost, ".2f")
            totalOrderCosts.append(totalOrderCost)
            totalOrderCost = 0

        orderRow += 1
        totalOrderCost += i.quantity * i.cost

    """ need to do 1 final time as last order hasnt had a change in order num
        to add to the arrays

        so done here but only if there is orders so errors arent caused when
        there are no errors """
    if orders:
        currentOrderID = i.orderID
        totalNumOrders += 1
        orderRows.append(orderRow)
        totalOrderCosts.append(totalOrderCost)

    # render page
    return render_template('orders.html', title='Orders',
                           numBasketItems=numBasketItems,
                           orders=orders, totalNumOrders=totalNumOrders,
                           orderRows=orderRows,
                           totalOrderCosts=totalOrderCosts,
                           orderAddresses=orderAddresses)


@app.route('/changepass', methods=['GET', 'POST'])
@login_required
def changepass():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()
    # form for chaning password
    changePassForm = ChangePass()

    # validating if submit button has been pressed and if data is valid
    if (changePassForm.submitPass.data and
            changePassForm.validate_on_submit()):
        # validation checking the password is correct is done in the forms
        # change the password
        current_user.password = changePassForm.newPassword.data
        db.session.add(current_user)
        db.session.commit()
        # go back to account page
        return redirect(url_for('account'))

    # render page
    return render_template('changepass.html', title='Change Password',
                           numBasketItems=numBasketItems,
                           changePassForm=changePassForm)


@app.route('/userOnly', methods=['GET', 'POST'])
def userOnly():
    # get number of basket items to display next to basket
    numBasketItems = getNumBasketItems()

    # render page
    return render_template('userOnly.html', numBasketItems=numBasketItems)


# for products search
@app.route('/tags')
def tagsDic():
    allTags = models.Tags.query.all()
    listTags = [i.as_dict() for i in allTags]
    return jsonify(listTags)


# AJAX stuff


@app.route('/addressDelete', methods=['POST'])
def addressDelete():
    # retrieve the data sent from JavaScript
    data = request.get_json()
    # delete the row with the id
    db.session.delete(models.Addresses.query.filter_by(id=data).first())
    db.session.commit()

    return jsonify(data=data)


@app.route('/addToBasket', methods=['POST'])
def addToBasket():
    # if the user is logged in then they can use the basket
    if (current_user.is_authenticated):
        # get data from JavaScript
        data = request.get_json()

        # see if the item is already in the basket
        basketItem = current_user.accountbasket.filter_by(
            productID=data["itemID"]).first()

        # if the item isnt already in the basket
        if (basketItem is None):
            # create a new basket object and add to database
            basketNew = models.Basket(productID=data["itemID"],
                                      quantity=data["itemQuantity"],
                                      name=data["itemName"],
                                      cost=data["itemCost"])

            # add to database relation to account
            # many to many
            current_user.accountbasket.append(basketNew)
            db.session.add(current_user)
            db.session.add(basketNew)
            db.session.commit()

        # if it is, just edit the quantity
        else:
            basketItem.quantity = basketItem.quantity + data["itemQuantity"]
            db.session.commit()

        # return a message to JavaSript to alert to user
        return("Added to basket")

    # if not logged in return alert saying to login
    else:
        return("Login to use the basket function")


@app.route('/basketDelete', methods=['POST'])
def basketDelete():
    # retrieve the data sent from JavaScript
    data = request.get_json()
    # delete the row with the id
    db.session.delete(models.Basket.query.filter_by(id=data).first())
    db.session.commit()

    return jsonify(data=data)


@app.route('/checkoutFinalised', methods=['POST'])
def checkoutFinalised():
    # retrieve the data sent from JavaScript
    data = request.get_json()
    # get all the items in the basket
    basket = current_user.accountbasket.all()

    # add up the total cost so can add to order
    totalCost = 0
    for i in basket:
        totalCost += i.quantity * i.cost

    # get order id
    lastOrder = models.Orders.query.order_by(models.Orders.orderID.desc()
                                             ).first()

    # if there isnt any orders in database then order id is 0
    if lastOrder is None:
        newOrderID = 0
    # otherwise add one for new order id
    else:
        newOrderID = lastOrder.orderID + 1
    for i in basket:
        # for each basket item create an order model
        basketItem = models.Orders(orderID=newOrderID, addressID=data,
                                   orderDate=datetime.datetime.utcnow(),
                                   productID=i.productID,
                                   quantity=i.quantity,
                                   name=i.name,
                                   cost=i.cost,
                                   totalOrderCost=totalCost)

        # add relationally to current user
        current_user.accountorders.append(basketItem)
        db.session.add(current_user)
        db.session.add(basketItem)

        # remove from stock count
        productQuantity = models.Products.query.filter_by(id=i.productID
                                                          ).first().quantity
        productQuantity -= i.quantity
        models.Products.query.filter_by(id=i.productID).first(
            ).quantity = productQuantity

        # delete item from basket
        db.session.delete(models.Basket.query.filter_by(id=i.id).first())
    db.session.commit()

    return jsonify(data=data)
