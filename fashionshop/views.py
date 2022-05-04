
from multiprocessing import context
import re
from django.shortcuts import render
from django.contrib.auth.models import User
from fashionshop.forms import RegisterForm, LoginForm, ReviewForm, AddressForm
from fashionshop.models import Profile, Item, Item_picture, Review, Order, OrderItem, Address
from django.db.models import Q, Count, Sum, Avg
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from webapps.settings import GOOGLE_API_KEY


import json
# Create your views here.

cupone_map = {'WebApp_Team4': 0.8}


def get_all_review_ajax(request, id):
    response_json = get_review_ajax(Review.objects.all().filter(item_id=id))
    return HttpResponse(response_json, content_type='application/json')


def get_highest_rating_ajax(request, id):
    response_json = get_review_ajax(
        Review.objects.all().filter(item_id=id).order_by('-rating'))
    return HttpResponse(response_json, content_type='application/json')


def get_lowest_rating_ajax(request, id):
    response_json = get_review_ajax(
        Review.objects.all().filter(item_id=id).order_by('rating'))
    return HttpResponse(response_json, content_type='application/json')


def get_star_rating_ajax(request, id, rating_num):
    q1 = Review.objects.all().filter(item_id=id)
    response_json = get_review_ajax(q1.filter(rating=rating_num))
    return HttpResponse(response_json, content_type='application/json')


def get_picture_ajax(request, id):
    q1 = Review.objects.all().filter(item_id=id)
    response_json = get_review_ajax(q1.exclude(review_picture=''))
    return HttpResponse(response_json, content_type='application/json')


def get_review_ajax(query):
    response_data = []
    for review in query:
        time_str = review.creation_time.strftime("%Y-%m-%d %H:%M:%S")

        my_review = {
            'id': review.id,
            'nickname': review.nickname,
            'review_title': review.review_title,
            'review': str(review.review),
            'rating': review.get_rating_display(),
            'time': time_str,
            'review_picture': (review.review_picture.url) if review.review_picture else ''
        }
        if review.review_picture:
            print(review.review_picture.url)
        response_data.append(my_review)

    response_json = json.dumps(response_data)
    return response_json

@login_required(login_url='/login')
def item_action(request, id):
    print("item_action")
    context = update_cart_icon(request)

    item = Item.objects.get(item_id=id)
    item.pictures = Item_picture.objects.all().filter(item_id=id)
    item.reviews = Review.objects.all().filter(item_id=id)
    css_picture = ["First slide", "Second slide", "Third slide"]
    context['id'] = id
    context['item'] = item
    context['item_short_name'] = item.item_name.split(" ")[-1]
    context['num_review'] = Review.objects.all().count()
    context['quantity'] = 1
    context['zip_pic'] = zip(item.pictures, css_picture)
    if request.method == 'GET':
        context['form'] = ReviewForm()
        context['quantity'] = 1
        context['current_size'] = '40'
        return render(request, 'fashionshop/item_page.html', context)

    new_review = Review(item=Item.objects.get(
        item_id=id), creation_time=datetime.now())
    form = ReviewForm(request.POST, request.FILES, instance=new_review)

    if not form.is_valid():
        print("form is not valid")
        item.reviews = Review.objects.all().filter(item_id=id)
        context['item'] = item
        context['form'] = ReviewForm()
        return render(request, 'fashionshop/item_page.html', context)

    # At this point, the form data is valid.
    pic = form.cleaned_data['review_picture']
    print('__________________________')
    print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
    print('__________________________')
    if form.cleaned_data['review_picture']:
        new_review.review_picture = form.cleaned_data['review_picture']
        new_review.content_type = form.cleaned_data['review_picture'].content_type

    form.save()
    context['form'] = ReviewForm(request.GET)
    context['size'] = '40'
    return render(request, 'fashionshop/item_page.html', context)

def update_orderitem_in_page(request):
    context = update_cart_icon(request)
    context['quantity'] = 1
    context['current_size'] = '40'
    if request.method == "GET":
        return render(request, 'fashionshop/item_page.html', context)

    form_context = request.POST
    print("post=====")
    print(form_context)
    customer = request.user
    item_id = int(form_context['addtocart'])
    quantity = int(form_context['quantity'])
    size_str = form_context['current_size']
    
    
    
    item = Item.objects.get(item_id=item_id)
    
    item.pictures = Item_picture.objects.all().filter(item_id=item_id)
    item.reviews = Review.objects.all().filter(item_id=item_id)
    css_picture = ["First slide", "Second slide", "Third slide"]
    context['item_short_name'] = item.item_name.split(" ")[-1]
    context['num_review'] = Review.objects.all().count()
    context['item'] = item
    
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item, selected_size=size_str)
    print("previouse size:", order_item.selected_size)
    print("cur size:", size_str)
    if (not order_item.selected_size) or (order_item.selected_size == size_str):
        order_item.quantity += quantity
        order_item.selected_size = size_str
        order_item.save()
        if order_item.quantity <= 0:
            order_item.delete()
    else:
        created_item = OrderItem.objects.create(order=order, item=item)
        created_item.quantity = quantity
        created_item.selected_size = size_str
        created_item.save()
        if created_item.quantity <= 0:
            created_item.delete()
    context = update_cart_icon(request)
    context['quantity'] = quantity
    context['current_size'] = size_str
    context['item'] = item

    return render(request, 'fashionshop/item_page.html', context)

@login_required(login_url='/login')
def all_items_action(request, gender="", genre=""):
    if request.method != "GET":
        query_price = request.POST['price-slider']
        keyword = request.POST['search_text']
        sort_order = request.POST['sort_order']

    gender = str.lower(gender)
    genre = str.lower(genre)
    if gender in ('women', 'men'):
        items = Item.objects.all().filter(category_gender=gender)
        if genre in ('top', 'bottom', 'dress', 'shoes', 'accessories'):
            items = items.filter(category_genre=genre)
    else:
        items = Item.objects.all()

    if request.method != "GET":
        keyword = request.POST['search_text']
        items = items.filter(price__lt=query_price)
        keyword = str.lower(keyword)
        items = items.filter(Q(item_name__icontains=keyword)
                             | Q(description__icontains=keyword))
        if(sort_order == 'price_low'):
            items = items.order_by('price')
        elif(sort_order == 'price_high'):
            items = items.order_by('-price')
        elif(sort_order == 'best'):
            queryset = Item.objects.annotate(
                total_sell=Sum('orderitem__quantity'))
            items = queryset.order_by('-total_sell')
        elif(sort_order == 'rating_high'):
            queryset = Item.objects.annotate(
                total_rating=Avg('review__rating'))
            items = queryset.order_by('-total_rating')
            # print(items[0].total_rating)
    for item in items:
        item.pictures = Item_picture.objects.all().filter(item_id=item.item_id).first()
        # print(item.pictures.item_picture);
    context = update_cart_icon(request)
    context['items'] = items
    return render(request, 'fashionshop/all_items.html', context)


def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'fashionshop/login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'fashionshop/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('all_items'))


@login_required
def logout(request):
    django_logout(request)
    return redirect(reverse('login'))

def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect(reverse('login'))
        else:
            messages.success(
                request, 'Your password was successfully updated!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'fashionshop/reset_pw.html', {
        'form': form
    })


def register_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'fashionshop/register.html', context)
    form = RegisterForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'fashionshop/register.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    profile = Profile(user=new_user)
    profile.save()
    return redirect(reverse('all_items'))


def backend_add_item():
    new_entry = Item(item_name='1461 Smooth Leather Platform Shoes',
                     description='Material: A twist on the classic Dr. Martens leather: durable, with a smooth and polished finish.',
                     category_gender='women', category_genre='shoes', price='130')
    new_entry.save()
    new_entry_pic1_1 = Item_picture(
        item_id=1, item_picture='/static/images/boots1.jpg')
    new_entry_pic1_2 = Item_picture(
        item_id=1, item_picture='/static/images/boots2.jpg')
    new_entry_pic1_3 = Item_picture(
        item_id=1, item_picture='/static/images/boots3.jpg')
    new_entry_pic1_1.save()
    new_entry_pic1_2.save()
    new_entry_pic1_3.save()

    new_entry2 = Item(item_name='Grey De-Velop-FS Denim Jacket',
                      description='Padded and quilted stretch denim jacket.',
                      category_gender='women', category_genre='top', price='200')
    new_entry2.save()
    new_entry_pic2 = Item_picture(
        item_id=2, item_picture='\static\images\clothes_diesel1.jpg')
    new_entry_pic2.save()
    new_entry3 = Item(item_name='Blue De-Ron-FS1 Mini Skirt',
                      description='Padded and quilted stretch denim skirt. Supplier color: Blue',
                      category_gender='women', category_genre='bottom', price='90')
    new_entry3.save()
    new_entry_pic3 = Item_picture(
        item_id=3, item_picture='\static\images\\bottom_diesel1.jpg')
    new_entry_pic3.save()
    new_entry4 = Item(item_name='Denim Couture Short-Sleeved Belted Jacket',
                      description='Deep Blue Lightweight Cotton Denim',
                      category_gender='women', category_genre='top', price='235')
    new_entry4.save()
    new_entry_pic4 = Item_picture(
        item_id=4, item_picture='\static\images\\top_dior1.jpg')
    new_entry_pic4.save()
    new_entry5 = Item(item_name='T-Shirt',
                      description='White Cotton Jersey with Fluorescent Blue D-Jungle Pop Motif',
                      category_gender='women', category_genre='top', price='110')
    new_entry5.save()
    new_entry_pic5 = Item_picture(
        item_id=5, item_picture='\static\images\\top_dior2.jpg')
    new_entry_pic5.save()
    new_entry6 = Item(item_name='Short-Sleeved Blouse',
                      description='Beige Stretch Cotton Gabardine',
                      category_gender='women', category_genre='top', price='145')
    new_entry6.save()
    new_entry_pic6 = Item_picture(
        item_id=6, item_picture='\static\images\\top_dior3.jpg')
    new_entry_pic6.save()


def base_action(request):
    context = update_cart_icon(request)
    return render(request, 'fashionshop/base.html', context)


def update_cart_icon(request):
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    if request.user.is_authenticated:

        items_in_order = order.orderitem_set.all()
        cart_item_num = order.get_total_num
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_num': 0}
        cart_item_num = order['get_total_num']

    items_in_order = order.orderitem_set.all()
    for item in items_in_order:
        item.pictures = Item_picture.objects.all().filter(item_id=item.item_id).first()

    total_price = order.get_total_price
    context = {'items_in_order': items_in_order,
               'cart_item_num': cart_item_num, 'total_price': total_price}
    return context


def cart_action(request):
    context = update_cart_icon(request)
    customer = request.user
    context['applied'] = 'No'
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    if request.method == "POST":
        form_context = request.POST
        input_cupone = form_context['search']
        print(input_cupone)
        if input_cupone in cupone_map:
            order.cupone = cupone_map.get(input_cupone)
            order.save()
            context['applied'] = 'YES'
        else:
            order.cupone = 1
            order.save()
    # items_in_order = order.orderitem_set.all()
    # for item in items_in_order:
    #     item.pictures =Item_picture.objects.all().filter(item_id = item.item_id).first()
    context['order'] = order
    return render(request, 'fashionshop/cart.html', context)


def profile_action(request):
    context = update_cart_icon(request)
    return render(request, 'fashionshop/my_profile.html', context)


def order(request):
    context = update_cart_icon(request)
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    context['order'] = order
    return render(request, 'fashionshop/order.html', context)


def detail(request):
    context = update_cart_icon(request)
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    context['order'] = order
    return render(request, 'fashionshop/detail.html', context)


def address(request):
    context = {}
    if request.method == 'GET':
        address = Address.objects.get_or_create()
        context['address'] = address
        return render(request, 'fashionshop/address.html', context)
    new_address = Address.objects.get_or_create(customer=request.user)
    print('new_address')
    new_address.fname = request.POST['fname']
    new_address.lname = request.POST['lname']
    new_address.country = request.POST['country']
    new_address.email = request.POST['email']
    new_address.city = request.POST['city']
    new_address.state = request.POST['state']
    new_address.phone_number = request.POST['phone_number']
    new_address.postcode = request.POST['postcode']
    new_address.street_address = request.POST['street_address']
    new_address.save()
    context['address'] = new_address

    return render(request, 'fashionshop/address.html', context)


def checkout_action(request):
    context = update_cart_icon(request)
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    if request.method == 'GET':
        context['order'] = order
        return render(request, 'fashionshop/checkout.html', context)
    new_address = Address.objects.get()
    context['order'] = order
    new_address.customer = request.user
    new_address.fname = request.POST['fname']
    new_address.lname = request.POST['lname']
    new_address.country = request.POST['country']
    new_address.email = request.POST['email']
    new_address.city = request.POST['city']
    new_address.state = request.POST['state']
    new_address.phone_number = request.POST['phone_number']
    new_address.postcode = request.POST['postcode']
    new_address.street_address = request.POST['street_address']
    new_address.save()
    context['address'] = new_address
    return render(request, 'fashionshop/checkout.html', context)


def updateItem(request):

    data = json.loads(request.body)
    item_id = data['item_id']
    print(data)
    action = data['action']
    size = data['size']
    
    customer = request.user
    item = Item.objects.get(item_id=item_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item, selected_size =size)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)

def updateItemMain(request):

    data = json.loads(request.body)
    item_id = data['item_id']
    size_str = data['size']
    customer = request.user
    item = Item.objects.get(item_id=item_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item, selected_size=size_str)
    
    item = Item.objects.get(item_id=item_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item, selected_size=size_str)
    print("previouse size:", order_item.selected_size)
    print("cur size:", size_str)
    if (not order_item.selected_size) or (order_item.selected_size == size_str):
        order_item.quantity += 1
        order_item.selected_size = size_str
        order_item.save()
        if order_item.quantity <= 0:
            order_item.delete()
        
    else:
        created_item = OrderItem.objects.create(order=order, item=item)
        created_item.quantity = 1
        created_item.selected_size = size_str
        created_item.save()
        if order_item.quantity <= 0:
            order_item.delete()

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
        
        
    return JsonResponse('Item was added', safe=False)

def updateShip(request):
    data = json.loads(request.body)
    price = data['price']
    price = float(price)
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order.shipping_price = price
    order.save()
    return JsonResponse('ship price was selected', safe=False)


def updateItemSignle(request):

    data = json.loads(request.body)
    item_id = data['item_id']
    size_str = data['size']
    qty = int(data['qty'])
    customer = request.user
    item = Item.objects.get(item_id=item_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item, selected_size=size_str)
    
    item = Item.objects.get(item_id=item_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item, selected_size=size_str)
    print("previouse size:", order_item.selected_size)
    print("cur size:", size_str)
    if (not order_item.selected_size) or (order_item.selected_size == size_str):
        order_item.quantity += qty
        order_item.selected_size = size_str
        order_item.save()
        if order_item.quantity <= 0:
            order_item.delete()
        
    else:
        created_item = OrderItem.objects.create(order=order, item=item)
        created_item.quantity = qty
        created_item.selected_size = size_str
        created_item.save()
        if order_item.quantity <= 0:
            order_item.delete()

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()     
    return JsonResponse('Item was added', safe=False)

def updateShip(request):
    data = json.loads(request.body)
    price = data['price']
    price = float(price)
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order.shipping_price = price
    order.save()
    return JsonResponse('ship price was selected', safe=False)


def clearCart(request):
    data = json.loads(request.body)
    clear = data['clear']
    if clear:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items_in_order = order.orderitem_set.all()
        for item in items_in_order:
            item.delete()
        order.shipping_price = 0
        order.order_total = 0
        order.save()
    return JsonResponse('backend clear cart', safe=False)


def store_locator(request):
    print(GOOGLE_API_KEY)
    key = 'https://maps.googleapis.com/maps/api/js?key=' + GOOGLE_API_KEY + \
        '&callback=initMap&libraries=places,geometry&solution_channel=GMP_QB_locatorplus_v4_cABD'
    context=update_cart_icon(request)
    context['api_key'] = key
    print(key)
    return render(request, 'fashionshop/store_locator.html', context)

def payment_action(request, orderId):
    order = get_object_or_404(Order,pk=orderId)
    context=update_cart_icon(request)
    context['total'] = order.get_order_total
    return render(request, 'fashionshop/payment.html', context)
