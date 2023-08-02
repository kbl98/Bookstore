from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser,Book
# Register your models here.

class CustomUserAdmin(UserAdmin):
    #add_form=CustomUserCreationForm
    #form=CustomUserChangeForm
    model=CustomUser
    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('author_pseudonym',)}),
)
    list_display=["email","username","author_pseudonym","id"]

class BookAdmin(admin.ModelAdmin):
     list_display=["title","description","author","id"]

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Book,BookAdmin)

