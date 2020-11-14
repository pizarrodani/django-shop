from django.shortcuts import render

from django.http import HttpResponseRedirect

from core.models import (
    Product,
    Order,
    Vehiculo
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.models import (
    User,
    Group
)

import stripe
stripe.api_key = 'sk_test_51HQlYBKVWRemJMNbYdPyEEGInMoFLN9MwF1UA0m6rxk8o97VVB4jS5B4LXBjNN8XGeVXWiBjcNTT1NqIin9I1HJj00LtxiIU4C'

def getIndex(request):
    items = None
    selectedItems = 0
    if request.session.get('ar'):
        items = request.session.get('ar')
        selectedItems = len(items)
    else:
        pass
    fetchAllProducts = Product.objects.all()[:4]
    data = {
        'products': fetchAllProducts,
        'items': selectedItems
    }
    return render(request, 'index.html', data)

def getAddProduct(request):
    return render(request, 'products/add-product.html')

def postAddToBag(request, id):
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html')
    else:
        productsCart = 0
        if request.session.get('ar'):
            items = request.session.get('ar')
            index = len(items)
            items.insert(index + 1, id)
            request.session['ar'] = items
            productsCart = index + 1
        else:
            ar = []
            ar.insert(0, id)
            request.session['ar'] = ar
            items = request.session.get('ar')
            productsCart = 1
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Views to login and authentication
def getLogIn(request):
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html')
    items = None
    selectedItems = 0
    if request.session.get('ar'):
        items = request.session.get('ar')
        selectedItems = len(items)
    else:
        pass
    fetchAllProducts = Product.objects.all()[:4]
    data = {
        'products': fetchAllProducts,
        'items': selectedItems
    }
    return render(request, 'index.html', data)

def getLogOut(request):
    logout(request)
    fetchAllProducts = Product.objects.all()[:4]
    data = {
        'products': fetchAllProducts
    }
    return render(request, 'index.html', data)

def postLogIn(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        data = {
            'check' : False
        }
        return render(request, 'auth/login.html', data)
    fetchAllProducts = Product.objects.all()[:4]
    data = {
        'products': fetchAllProducts
    }
    return render(request, 'index.html', data)

def getSignUp(request):
    if not request.user.is_authenticated:
        return render(request, 'auth/signup.html')
    fetchAllProducts = Product.objects.all()[:4]
    data = {
        'products': fetchAllProducts
    }
    return render(request, 'index.html', data)

def postSignUp(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username, email, password)
    user.save()
    user = authenticate(request, username=username, password=password)
    user_group = Group.objects.get(name='Clients')
    user.groups.add(user_group)
    login(request, user)
    return render(request, 'auth/signup.html')
# end

# Views to Stripe payments
def getCheckout(request):
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html')
    fetchAllItems = []
    if request.session.get('ar'):
        items = request.session.get('ar')
        product = None
        index = 0
        for i in items:
            product = Product.objects.get(pk=items[index])
            fetchAllItems.insert(index, product)
            index += 1
    else:
        print('No Hay sesiones!')

    data = {
        'orderItems': fetchAllItems,
        'items': len(fetchAllItems)
    }
    return render(request, 'shop/checkout.html', data)
    #product = Product.objects.get(productId=id)
    #checkout_session = stripe.checkout.Session.create(
    #    payment_method_types=['card'],
    #    line_items=[
    #        {
    #          'price_data': {
    #            'currency': 'clp',
    #            'unit_amount': product.price,
    #            'product_data': {
    #              'name': product.title,
    #             },
    #           },
    #             'quantity': 1,
    #         },
    #        ],
    #        mode='payment',
    #        success_url='http://localhost:8000/success/' + str(id),
    #        cancel_url='http://localhost:8000',
    #    )
    #return render(request, 'shop/checkout.html', {'id': checkout_session.id})

def getSuccessPay(request, id):
    fetchProduct = Product.objects.get(productId=id)
    current_user = request.user
    Order.objects.create(
        product = fetchProduct,
        total_price = fetchProduct.price,
        user = current_user
    )
    fetchAllProducts = Product.objects.all()[:4]
    data = {
        'products': fetchAllProducts
    }
    return render(request, 'index.html', data)
# end
