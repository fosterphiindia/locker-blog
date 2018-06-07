from django.contrib import admin

# Register your models here.
from .models import Account

class AccountModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'email', 'token']
	list_display_links = ["id"]
	list_filter = ["id"]
	search_fields = ["id"]

	class Meta:
		model = Account

admin.site.register(Account, AccountModelAdmin)