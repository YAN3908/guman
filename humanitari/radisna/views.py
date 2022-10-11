# import datetime
from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, TextInput, EmailInput, Select  # mast hewe
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError

from .models import User, Streets, Helps


class DateInput(forms.DateInput):
    input_type = 'date'


class NumberInput(forms.NumberInput):
    input_type = "number"


class RForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = (
            'username', 'password', 'last_name', 'first_name', 'patronymic', 'street', 'home', 'home_index',
            'apartment', 'apartment_index',
            'date_birth', 'pension',
            'invalid', 'many_children', 'email')
        datelimit = datetime.now() - timedelta(days=5111)
        widgets = {
            'date_birth': DateInput(
                attrs={'class': 'form-control', 'required': 'true', 'max': datelimit.strftime("%Y-%m-%d")}),
            # 'date_birth': DateInput(attrs={'class': 'form-control', 'required': 'true', 'max': '1979-12-31'}),
            'username': NumberInput(attrs={'class': 'form-control'}),
            'password': NumberInput(attrs={'class': 'form-control', 'min_length': 10}),
            'first_name': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'patronymic': TextInput(attrs={'class': 'form-control'}),
            'street': Select(attrs={'class': 'form-control'}),
            'home': NumberInput(attrs={'class': 'form-control'}),
            'apartment': NumberInput(attrs={'class': 'form-control'}),
            'invalid': TextInput(attrs={'class': 'form-control'}),
            'pension': TextInput(attrs={'class': 'form-control'}),
            'many_children': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'home_index': Select(attrs={'class': 'form-control'}),
            'apartment_index': Select(attrs={'class': 'form-control'})
        }
        # widgets = {
        #     'password': forms.NumberInput(attrs={'class': 'form-control'}),
        # }
        labels = {
            'username': ('РНОКПП'),
            'password': ('№ телефону'),
            'invalid': ('№ посв. інваліда'),
            'many_children': ('№ посв. багатодітної особи'),
            'patronymic': ('По-батькові'),
            'home': ('№ дому'),
            'apartment': ('Квартира'),
            'date_birth': ('Дата народження'),
            'street': ('Вулиця'),
            'pension': ('пенсійне')
        }

        # def clean(self):
        #     cleaned_data = super(RForm, self).clean()
        #     apartment = cleaned_data.get('apartment')
        #
        #
        #     if apartment:
        #         if apartment > 30:
        #             # count_text = len(title)
        #             raise ValidationError("Title is too short")


def register(request):
    # return HttpResponse(request.user)

    if request.method == "POST":
        form = RForm(request.POST)

        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        patronymic = request.POST["patronymic"]
        home = request.POST["home"]
        home_index=request.POST["home_index"]
        apartment = request.POST["apartment"]
        if apartment == '':
            apartment = 0
        apartment_index = request.POST["apartment_index"]
        date_birth = request.POST["date_birth"]
        invalid = request.POST["invalid"]
        many_children = request.POST["many_children"]
        street = request.POST['street']
        pension = request.POST['pension']
        if len(username) != 10:
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "Не вірний РОНКПП"})
        if all([password[:3] != "039",
                password[:3] != "051",
                password[:3] != "050",
                password[:3] != "063",
                password[:3] != "066",
                password[:3] != "067",
                password[:3] != "068",
                password[:3] != "073",
                password[:3] != "091",
                password[:3] != "092",
                password[:3] != "093",
                password[:3] != "094",
                password[:3] != "095",
                password[:3] != "096",
                password[:3] != "097",
                password[:3] != "098",
                password[:3] != "099",
                ]):
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "Не вірний номер телефону"
                                                             })
        if len(password) != 10:
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "Не вірний номер телефону"
                                                             })

        if not first_name.isalpha():
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "У вашому імені не повино бути цифр"
                                                             })
        if not last_name.isalpha():
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "У вашому прізвищі не повино бути цифр"
                                                             })
        if not patronymic.isalpha():
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "По-батькові не може містити цифр"
                                                             })
        if not invalid and not many_children and not pension:
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "Ви повині ввести хочаб один льготний документ"
                                                             })

        datelimit = datetime.now() - timedelta(days=21914)
        if not invalid and not many_children:
            if date_birth > datelimit.strftime("%Y-%m-%d"):
                return render(request, "radisna/register.html", {'form': form,
                                                                 "message": "Ваш вік повинен бути не меньшим за 60 років"
                                                                 })
        print(username)
        # Attempt to create new user
        # print(date_birth)

        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name,
                                            home=home, home_index=home_index,
                                            apartment=apartment, apartment_index=apartment_index, date_birth=date_birth, patronymic=patronymic,
                                            phone=password, pension=pension, invalid=invalid, many_children=many_children,
                                            street=Streets.objects.get(pk=street), )
            user.save()
        except IntegrityError:
            return render(request, "radisna/register.html", {'form': form,
                                                             "message": "Цей громадянин вже зареестрований"

                                                             })
        login(request, user)
        # return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("helpme"))

    else:
        return render(request, "radisna/register.html", {'form': RForm})


def login_view(request):  # not used
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "radisna/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "radisna/login.html")


class IGree(forms.ModelForm):
    i_gree = forms.BooleanField()


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, "radisna/listing.html", {"users": User.objects.filter(helps__Check=True)})

        else:
            return HttpResponseRedirect(reverse("helpme"))
    else:
        if request.method == "POST":
            if request.POST["I_gree"]:
                return HttpResponseRedirect(reverse("register"))
        else:
            return render(request, "radisna/index.html")
        # return HttpResponseRedirect(reverse("register"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def helpme(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=int(request.user.id))
        print(user)
        print("qwertyuiop")
        if request.method == "POST":
            if request.POST['helpme']:
                help = Helps(Check=True)
                help.save()
                user.helps.add(help)
                # lot.starting_price = form.cleaned_data["starting_price"]
                # lot.save()
                return HttpResponseRedirect(reverse("helpme"))
            else:
                return render(request, "radisna/helpme.html")

        else:
            print(request.user.id)
            # user = User.objects.get(pk=int(request.user.id))
            # print(user.helps.all().last().Check)
            if user.helps.all():
                if user.helps.all().last().Check == True:
                    return render(request, "radisna/helpme.html",
                                  {"message1": f"Ви зареєстровані як {user.first_name} "
                                               f"{user.patronymic}, ми вже готуємо вашу допомогу, чекайте будь ласка."})
                else:
                    return render(request, "radisna/helpme.html",
                                  {"message": f"Ви зареєстровані як {user.first_name} "
                                              f"{user.patronymic}, зробіть наступну заявку ."})
            else:
                return render(request, "radisna/helpme.html",
                              {"message": f"Ви зареєстровані як {user.first_name} {user.patronymic} "
                                          f"зробіть заявку на допомогу натиснувши кнопку нижче"})


def check(request):
    if request.method == "POST":
        if request.POST['check']:
            print(request.POST['check'])
            check = Helps.objects.get(pk=int(request.POST['check']))
            print(check)
            check.Check = False
            check.help = datetime.now()
            check.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
