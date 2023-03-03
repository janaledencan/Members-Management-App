from django.contrib import admin
from .models import Owner, Group, Member, MembersInGroup

# Register your models here.
admin.site.register(Owner)
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(MembersInGroup)
