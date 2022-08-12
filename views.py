from django.shortcuts import render, redirect
from django.contrib import messages

import bcrypt


from .models import User, Category, Show

def login_reg_page(request):
    return render(request, 'index.html')

def create_user(request):
    potential_users = User.objects.filter(email = request.POST['email'])

    if len(potential_users) != 0:
        messages.error(request, "User with that email already exists!")
        return redirect('/')

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw,
    )

    request.session['user_id'] = new_user.id

    return redirect('/dashboard')

def login(request):
    potential_users = User.objects.filter(email = request.POST['email'])

    if len(potential_users) == 0:
        messages.error(request, "Please check your email and password.")
        return redirect('/')

    user = potential_users[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please check your email and password.")
        return redirect('/')

    request.session['user_id'] = user.id

    return redirect('/dashboard')

def logout(request):
    if 'user_id' not in request.session:
        messages.error(request, "You are not logged in!")
        return redirect('/')

    request.session.clear()

    return redirect('/')

def dashboard_page(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')
        
    current_user = User.objects.get(id=request.session['user_id'])
    current_user_added_shows = current_user.added_shows.all()
    all_shows = Show.objects.exclude(id__in=current_user_added_shows)

    context = {
        'current_user': current_user,
        'all_shows': all_shows,
        'users_added_shows': current_user_added_shows,
    }

    return render(request, 'dashboard.html', context)

def add_show_page(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')
        
    current_user = User.objects.get(id=request.session['user_id'])
    category_options = Category.objects.all().order_by('-created_at')

    context = {
        'current_user': current_user,
        'category_options': category_options
    }

    return render(request, 'showcreation.html', context)

def create_show(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])

    show_errors = Show.objects.basic_validator(request.POST)

    if len(Category.objects.filter(category = request.POST['category_text'])) != 0:
        messages.error(request, "The category you typed already exists. Please use that.")
        return redirect('/shows/add')

    if len(show_errors) > 0:
        for key, val in show_errors.items():
            messages.error(request, val)
        return redirect('/shows/add')

    new_show = Show.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        created_by_user = current_user,
    )

    if request.POST['category_text'] != "":
        new_category = Category.objects.create(category = request.POST['category_text'])
        new_show.categories.add(new_category)

    if request.POST.getlist('category') != []:
        for category_id in request.POST.getlist('category'):
            category = Category.objects.get(id = category_id)
            category.shows.add(new_show)

    return redirect('/dashboard')

def edit_show_page(request, show_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id = show_id)
    all_categories = Category.objects.all()

    if current_show.created_by_user != current_user:
        messages.error(request, "This is not your show silly goose. So you can't edit it")
        return redirect('/dashboard')

    context = {
        "current_user": current_user,
        "current_show": current_show,
        "all_categories": all_categories,
    }

    return render(request, 'editshow.html', context)

def update_show(request, show_id):
    if 'user_id' not in request.session:
        messages.error(request, "Log in Please!")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id = show_id)

    if len(Category.objects.filter(category = request.POST['category_text'])) != 0:
        messages.error(request, "This category alredy exist!.")
        return redirect(f'/shows/{show_id}/edit')

    if current_show.created_by_user != current_user:
        messages.error(request, "This show doesn't belong to you, Honey. You can't edit it!")
        return redirect('/dashboard')

    show_errors = Show.objects.basic_validator(request.POST)

    if len(show_errors) > 0:
        for key, val in show_errors.items():
            messages.error(request, val)
        return redirect(f'/shows/{show_id}/edit')

    for category in Category.objects.exclude(id__in = request.POST.getlist('category')):
        current_show.categories.remove(category)

    if request.POST['category_text'] != "":
        new_category = Category.objects.create(category = request.POST['category_text'])
        current_show.categories.add(new_category)

    for category_id in request.POST.getlist('category'):
        category = Category.objects.get(id = category_id)
        category.shows.add(current_show)

    

    current_show.title = request.POST['title']
    current_show.description = request.POST['description']
    current_show.save()

    return redirect('/dashboard')

def view_show_page(request, show_id):
    if 'user_id' not in request.session:
        messages.error(request, "You have to be logged in")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id = show_id)
    all_categories = Category.objects.all().order_by('category')

    current_user_added_shows = current_user.added_shows.all()
    all_shows = Show.objects.exclude(id__in=current_user_added_shows)

    category_empty = True

    if len(current_show.categories.all()) != 0:
        category_empty = False

    context = {
        'current_user': current_user,
        'all_shows': all_shows,
        'current_user_added_shows': current_user_added_shows,
        'current_show': current_show,
        'all_categories': all_categories,
        'category_empty': category_empty
    }

    return render(request, 'viewshow.html', context)

def delete_show(request, show_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please, login.")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id = show_id)

    if current_show.created_by_user != current_user:
        messages.error(request, "You can't remove it because this is not your TV Show")
        return redirect('/dashboard')

    current_show.delete()

    return redirect('/dashboard')

def add_show_to_user(request, show_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id = show_id)

    current_user.added_shows.add(current_show)

    return redirect('/dashboard')

def remove_show_from_user(request, show_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id = show_id)

    current_user.added_shows.remove(current_show)

    return redirect('/dashboard')

def done_show(request, show_id):
    if 'user_id' not in request.session:
        messages.error(request, "You have to be logged in!")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id = show_id)

    if current_user not in current_show.added_users.all():
        messages.error(request, "You can not add this TV Show, it belongs to someone else.")
        return redirect('/dashboard')

    current_show.delete()

    return redirect('/dashboard')