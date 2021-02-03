from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.messages import get_messages
from SkateSpotsApp.models import User, Message, Comment, Marker
from SkateSpotsApp.forms import MarkerForm
import bcrypt
# from datetime import date, datetime
# from geolocation.main import GoogleMaps
import json
import boto3
from django.views.generic import TemplateView

def index(request):
    return render(request, "index.html")


def login(request):
    valid_user = User.objects.filter(email=request.POST['email'])
    if valid_user:
        current_user = valid_user[0]

        pw_match = bcrypt.checkpw(
            request.POST['password'].encode(), current_user.password.encode())

        if pw_match:
            request.session['user_id'] = current_user.id
        else:
            messages.error(request, "Invalid credentials")
            return redirect("/")
    else:
        messages.error(request, "Invalid credentials")
        messages.error(request, "Please try again")
        return redirect("/")
    return redirect("/home")


def register(request):
    taken_user = User.objects.filter(email=request.POST['email'])
    if taken_user:
        messages.error(request, "Invalid credentials")
        return redirect("/")

    if not User.objects.is_reg_valid(request):
        return redirect("/")

    hashed = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                   email=request.POST['email'], password=hashed, birthday=request.POST['birthday'])
    request.session['user_id'] = new_user.id
    return redirect("/home")


def logout(request):
    request.session.clear()
    return redirect('/')


# class MarkerView(TemplateView):
#     template_name = 'home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['markers'] = Marker.objects.all()
#         return context


def home(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    user = User.objects.get(id=user_id)

    all_markers = Marker.objects.all()
    print(all_markers)

    context = {"user": user, "markers": all_markers}
    return render(request, "home.html", context)


def wall(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    user = User.objects.get(id=user_id)
    all_messages = Message.objects.all()
    all_comments = Comment.objects.all()

    context = {"user": user, "messages": all_messages,
               "comments": all_comments}
    return render(request, "messages.html", context)


def spot(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    context = {"user": user}
    return render(request, "spot.html", context)


def create(request):

    # Marker.objects.create(name=request.POST['name'], photo=request.POST['photo'],
    #                       lat=request.POST['lat'], long=request.POST['long'], kind=request.POST['kind'], desc=request.POST['desc'])

    # if request.method == 'POST':
    #     form = MarkerForm(request.POST, request.FILES)

    #     if form.is_valid():
    #         form.save()
    #         return redirect("/home")
    #     else:
    #         form = MarkerForm()
    #     return render(request, 'photo.html', {'form': form})

    if request.method == 'POST':
        form = MarkerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("/home")
        else:
            form = MarkerForm()
        return render(request, 'spot.html', {'form': form})


def remove(request, spot_id):
    spot = Marker.objects.get(id=spot_id)
    spot.delete()
    return redirect('/home')


def add_message(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    new_message = Message.objects.create(
        user=user, message=request.POST['message'], subject=request.POST['subject'])
    request.session['message_id'] = new_message.id
    return redirect("/wall")


def delete(request, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect('/wall')


def add_comment(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    message_id = request.POST['comment_id']
    message = Message.objects.get(id=message_id)

    Comment.objects.create(
        user=user, message=message, comment=request.POST['comment'])
    return redirect(f"/message/{message_id}")


def message(request, message_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    message = Message.objects.get(id=message_id)
    user = User.objects.get(id=user_id)
    all_comments = Comment.objects.all()

    context = {"user": user, "message": message, "comments": all_comments}
    return render(request, "message.html", context)


def profile(request, user_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    user = User.objects.get(id=user_id)

    context = {"user": user, }
    return render(request, "user.html", context)


def update(request, user_id):
    # taken_user = User.objects.filter(email=request.POST['email'])
    # if taken_user:
    #     messages.error(request, "Invalid credentials")
    #     return redirect("/")

    # if not User.objects.is_reg_valid(request):
    #     return redirect("/")

    # user_id = request.session.get('user_id')

    # if not user_id:
    #     return redirect("/")

    user = User.objects.get(id=user_id)

    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.password = hashed
    user.birthday = request.POST['birthday']
    # user.photo = request.POST['photo']
    user.save()

    return redirect("/home")


def edit(request, spot_id):
    spot = Marker.objects.get(id=spot_id)
    print(spot)
    context = {"spot": spot}
    return render(request, "edit.html", context)


def edit_spot(request, spot_id):

    this_spot = Marker.objects.get(id=spot_id)

    this_spot.name = request.POST['name']
    # this_spot.photo = request.POST['photo']
    this_spot.lat = request.POST['lat']
    this_spot.long = request.POST['long']
    this_spot.kind = request.POST['kind']
    this_spot.desc = request.POST['desc']
    this_spot.save()

    return redirect("/home")
