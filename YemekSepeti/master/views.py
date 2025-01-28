from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm
from .models import Store, MenuItem, Order


def index(request):
	stores = Store.objects.all()
	return render(request, 'index.html', {'stores': stores})

@login_required
def profile(request):
	user = request.user
	orders = Order.objects.filter(user=user).prefetch_related('order_items__customizations', 'order_items__menu_item', 'order_items__customizations__ingredient')
	
	return render(request, 'profile.html', context={'orders': orders})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.register()
			auth_login(request, user)
			return redirect('master:index')
		else:
			print(form.errors)
	return render(request, 'register.html')

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid() and form.login(request):
			return redirect('master:index')
	return render(request, 'login.html')

@login_required
def logout(request):
	auth_logout(request)
	return redirect('master:index')

def store(request, store_id):
	context = {}
	store = Store.objects.get(id=store_id)
	menus = MenuItem.objects.filter(store=store)
	context['store'] = store
	context['menus'] = menus

	# If the user has an active cart, get it from the session
	order = request.session.get('order', None)

	# If no order exists, initialize it
	if order is None:
		order = {
			"order_items": []
		}
		request.session['order'] = order
	context['order'] = order

	return render(request, 'store.html', context=context)

def order_add_item(request):
	menu_id = request.POST.get('menu_id')
	quantity = int(request.POST.get('quantity'))
	menu_item = MenuItem.objects.get(MenuItem, id=menu_id)

	# Get customizations from the form
	customizations = []
	for ingredient in menu_item.ingredients.all():
		customization_action = bool(request.POST.get(f'customizations_{ingredient.id}', False))
		customizations.append({
			"ingredient_id": ingredient.id,
			"action": customization_action
		})

	# Retrieve or initialize the order in session
	order = request.session.get('order', {"order_items": []})

	# Add the menu item with customizations to the order
	order['order_items'].append({
		"menu_id": menu_item.id,
		"quantity": quantity,
		"customizations": customizations
	})

	# Save the updated order back to the session
	request.session['order'] = order

	# Redirect back to the same store page
	return HttpResponseRedirect(f'/store/{store.id}/')

@login_required
def manager_dashboard(request):
	# You can add your logic here to display the manager's dashboard
	return render(request, 'manager_dashboard.html')

@login_required
def manager_add_item(request):
	# You can add your logic here to add a new item to the store's menu
	return render(request, 'manager_add_item.html')

@login_required
def manager_edit_item(request, item_id):
	# You can add your logic here to edit an existing item in the store's menu
	return render(request, 'manager_edit_item.html', {'item_id': item_id})

@login_required
def manager_delete_item(request, item_id):
	# You can add your logic here to delete an item from the store's menu
	return render(request, 'manager_delete_item.html', {'item_id': item_id})

@login_required
def order_summary(request):
	# Order page with pseudo payment
	# You can add your logic here to display the order summary
	return render(request, 'order_summary.html')

@login_required
def order_success(request):
	# Successful order page
	# You can add your logic here to display the order success page
	return render(request, 'order_success.html')