from django.urls import path

from core.views import (
    getIndex,
    getProducts,
    getAdminProducts,
    getAddProduct,
    getCart,
    postCartAddItem,
    postCartDeleteItem,
    getOrder,
    postOrder,
    getLogIn,
    postLogIn,
    getLogOut,
    getSignUp,
    postSignUp
)

urlpatterns = [
    path('', getIndex, name='getIndex'),
    path('products/', getProducts, name='getProducts'),
    path('admin-products/', getAdminProducts, name='getAdminProducts'),
    path('admin-products/add-product', getAddProduct, name='addProduct'),
    path('cart/', getCart, name='cart'),
    path('cart-add-item/<int:id>', postCartAddItem, name='postCartAddItem'),
    path('cart-delete-item/<int:id>', postCartDeleteItem, name='postCartDeleteItem'),
    path('create-order/', getOrder, name='getOrder'),
    path('checkout/<slug:id>', postOrder, name='postOrder'),
    path('login/', getLogIn, name='getLogIn'),
    path('login-auth/', postLogIn, name='postLogIn'),
    path('logout/', getLogOut, name='getLogOut'),
    path('signup/', getSignUp, name='getSignUp'),
    path('signup-auth/', postSignUp, name='postSignUp'),
]
