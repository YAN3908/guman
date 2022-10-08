# import datetime
from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, TextInput, EmailInput  # mast hewe
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError

from .models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class NumberInput(forms.NumberInput):
    input_type = "number"


class RForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = (
            'username', 'password', 'first_name', 'last_name', 'patronymic', 'home', 'apartment', 'date_birth',
            'invalid', 'many_children', 'email',)
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
            'home': NumberInput(attrs={'class': 'form-control'}),
            'apartment': NumberInput(attrs={'class': 'form-control'}),
            'invalid': TextInput(attrs={'class': 'form-control'}),
            'many_children': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }
        # widgets = {
        #     'password': forms.NumberInput(attrs={'class': 'form-control'}),
        # }
        labels = {
            'username': ('РНОКПП'),
            'password': ('№ телефону'),
            'invalid': ('№ посвідчення інваліда'),
            'many_children': ('№ посвідчення багатодітної особи'),
            'patronymic': ('По-батькові'),
            'home': ('№ дому'),
            'apartment': ('Квартира'),
            'date_birth': ('Дата народження')
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


def index(request):
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
        apartment = request.POST["apartment"]
        date_birth = request.POST["date_birth"]
        invalid = request.POST["invalid"]
        many_children = request.POST["many_children"]
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

        datelimit = datetime.now() - timedelta(days=21914)
        if not invalid and not many_children:
            if date_birth > datelimit.strftime("%Y-%m-%d"):
                return render(request, "radisna/register.html", {'form': form,
                                                              "message": "Ваш вік повинен бути не меньшим за 60 років"
                                                              })
        # print(email)
        # Attempt to create new user
        # print(date_birth)
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name,
                                            home=home,
                                            apartment=apartment, date_birth=date_birth, patronymic=patronymic,
                                            phone=password, invalid=invalid, many_children=many_children)
            user.save()
        except IntegrityError:
            return render(request, "radisna/register.html", {'form': form,
                                                          "message": "Цей громадянин вже зареестрований"
                                                          })
        login(request, user)
        # return HttpResponseRedirect(reverse("index"))
        return HttpResponse(request.user)

    else:
        return render(request, "radisna/register.html", {'form': RForm})
