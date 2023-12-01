from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import DroneForm, IceCreamForm, ConeForm, ToppingForm, UserForm, ProfileForm, MarkupForm
from.decorators import admin_required
# noinspection PyUnresolvedReferences
from DroneCustomer.models import Drone, IceCream, Cone, Topping, Order, IceCreamCone, Markup
# noinspection PyUnresolvedReferences
from Account.models import Profile

@admin_required
def index(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "DroneAdmin/order_history.html", {'orders': orders})

@admin_required
def user_management(request):
    user_list = User.objects.all()
    return render(request, 'DroneAdmin/user_management.html', {'user_list': user_list})

@admin_required
def edit_user(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        profile = get_object_or_404(Profile, pk=user_id)
    else:
        user = None
        profile = None
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_management')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'DroneAdmin/edit_user.html', {'user_form': user_form, 'profile_form': profile_form})


# noinspection PyUnboundLocalVariable
@admin_required
def delete_user(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        profile = get_object_or_404(Profile, pk=user_id)
    else:
        user = None
    if request.method == 'POST':
        profile.delete()
        user.delete()
        return redirect('user_management')
    return render(request, 'DroneAdmin/delete_user.html', {'user': user, 'profile': profile})

@admin_required
def drone_management(request):
    drones = Drone.objects.all()
    for drone in drones:
        droneOrders = Order.objects.filter(drone=drone)
        total_drone_minutes_worked = 0
        for order in droneOrders:
            total_drone_minutes_worked += 10
        drone.hours_worked = round(total_drone_minutes_worked / 60, 2)

    return render(
        request,
        "DroneAdmin/drone_management.html",
        {'drones': drones}
    )

@admin_required
def add_drone(request, item_id=None):
    if item_id:
        drone = get_object_or_404(Drone, pk=item_id)
        action_title = "Edit"
    else:
        drone = None
        action_title = "Add"
    if request.method == 'POST':
        form = DroneForm(request.POST, instance=drone)
        if form.is_valid():
            form.save()
            return redirect('drone_management')
    else:
        form = DroneForm(instance=drone)
    return render(request, 'DroneAdmin/add_drone.html', {'form': form, 'action_title': action_title})

@admin_required
def delete_drone(request, item_id=None):
    if item_id:
        drone = get_object_or_404(Drone, pk=item_id)
    else:
        drone = None
    if request.method == 'POST':
        drone.delete()
        return redirect('drone_management')
    return render(request, 'DroneAdmin/delete_drone.html', {'drone': drone})

@admin_required
def inventory(request):
    ice_creams = IceCream.objects.all()
    cones = Cone.objects.all()
    toppings = Topping.objects.all()

    return render(request, "DroneAdmin/inventory.html",
        {
            'ice_creams': ice_creams,
            'cones': cones,
            'toppings': toppings
        })

@admin_required
def add_ice_cream(request, item_id=None):
    if item_id:
        ice_cream = get_object_or_404(IceCream, pk=item_id)
        action_title = "Edit"
    else:
        ice_cream = None
        action_title = "Add"
    if request.method == 'POST':
        form = IceCreamForm(request.POST, instance=ice_cream)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = IceCreamForm(instance=ice_cream)
    return render(request, 'DroneAdmin/add_ice_cream.html', {'form': form, 'action_title': action_title})

@admin_required
def delete_ice_cream(request, item_id=None):
    if item_id:
        ice_cream = get_object_or_404(IceCream, pk=item_id)
    else:
        ice_cream = None
    if request.method == 'POST':
        ice_cream.delete()
        return redirect('inventory')
    return render(request, 'DroneAdmin/delete_ice_cream.html', {'ice_cream': ice_cream})

@admin_required
def add_cone(request, item_id=None):
    if item_id:
        cone = get_object_or_404(Cone, pk=item_id)
        action_title = "Edit"
    else:
        cone = None
        action_title = "Add"
    if request.method == 'POST':
        form = ConeForm(request.POST, instance=cone)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ConeForm(instance=cone)
    return render(request, 'DroneAdmin/add_cone.html', {'form': form, 'action_title': action_title})

@admin_required
def delete_cone(request, item_id=None):
    if item_id:
        cone = get_object_or_404(Cone, pk=item_id)
    else:
        cone = None
    if request.method == 'POST':
        cone.delete()
        return redirect('inventory')
    return render(request, 'DroneAdmin/delete_cone.html', {'cone': cone})

@admin_required
def add_topping(request, item_id=None):
    if item_id:
        topping = get_object_or_404(Topping, pk=item_id)
        action_title = "Edit"
    else:
        topping = None
        action_title = "Add"
    if request.method == 'POST':
        form = ToppingForm(request.POST, instance=topping)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ToppingForm(instance=topping)
    return render(request, 'DroneAdmin/add_topping.html',
                  {'form': form, 'action_title': action_title, 'topping': topping})

@admin_required
def delete_topping(request, item_id=None):
    if item_id:
        topping = get_object_or_404(Topping, pk=item_id)
    else:
        topping = None
    if request.method == 'POST':
        topping.delete()
        return redirect('inventory')
    return render(request, 'DroneAdmin/delete_topping.html', {'topping': topping})

@admin_required
def edit_markup(request):
    markup_instance = Markup.get_instance()

    if request.method == 'POST':
        form = MarkupForm(request.POST, instance=markup_instance)
        if form.is_valid():
            form.save()
            return redirect('sales')
    else:
        form = MarkupForm(instance=markup_instance)

    return render(request, 'DroneAdmin/edit_markup.html', {'form': form})

@admin_required
def sales(request):
    markup = Markup.get_instance()
    orders = Order.objects.all()
    total_revenue = 0
    ice_cream_sales = defaultdict(dict)
    cone_sales = defaultdict(dict)
    topping_sales = defaultdict(dict)

    for order in orders:
        total_revenue += order.get_order_total()
        json_data = order.get_cone_info()

        try:
            for item in json_data:
                flavor = item['flavor']['flavor']
                cone_name = item['cone']['name']
                toppings = [topping['name'] for topping in item['toppings']]
                quantity_sold = 1  # TO BE CHANGED

                flavor_price = float(item['flavor']['price'])
                flavor_revenue = flavor_price * quantity_sold

                cone_price = float(item['cone']['price'])
                cone_revenue = cone_price * quantity_sold

                topping_price = float(item['toppings'][0]['price']) if item['toppings'] else 0
                topping_revenue = topping_price * quantity_sold

                if flavor not in ice_cream_sales:
                    ice_cream_sales[flavor] = {'qty_sold': 0, 'total_revenue': 0, 'price_per_unit': 0}
                ice_cream_sales[flavor]['qty_sold'] += quantity_sold
                ice_cream_sales[flavor]['total_revenue'] += flavor_revenue
                ice_cream_sales[flavor]['price_per_unit'] = flavor_price

                if cone_name not in cone_sales:
                    cone_sales[cone_name] = {'qty_sold': 0, 'total_revenue': 0, 'price_per_unit': 0}
                cone_sales[cone_name]['qty_sold'] += quantity_sold
                cone_sales[cone_name]['total_revenue'] += cone_revenue
                cone_sales[cone_name]['price_per_unit'] = cone_price

                for topping in toppings:
                    if topping not in topping_sales:
                        topping_sales[topping] = {'qty_sold': 0, 'total_revenue': 0, 'price_per_unit': 0}
                    topping_sales[topping]['qty_sold'] += quantity_sold
                    topping_sales[topping]['total_revenue'] += topping_revenue
                    topping_sales[topping]['price_per_unit'] = topping_price

        except (KeyError, TypeError) as e:
            print(f"Error processing order {order.id}: {e}")

    ice_cream_sales = dict(ice_cream_sales)
    cone_sales = dict(cone_sales)
    topping_sales = dict(topping_sales)

    context = {
        'ice_cream_sales': ice_cream_sales,
        'cone_sales': cone_sales,
        'topping_sales': topping_sales,
        'total_revenue': total_revenue,
        'markup': markup.markup_percentage
    }

    return render(request, "DroneAdmin/sales.html", context)