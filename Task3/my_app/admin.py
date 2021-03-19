from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Post, Comment


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'title', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description ')
    list_filter = ('user',)
    fields = ('title', 'description', 'photo', 'user')
    save_on_top = True

    def response_change(self, request, obj):
        if "_delete_comments" in request.POST:
            post = self.get_object(request=request, object_id=obj.id)
            Comment.objects.filter(post=post).delete()
            self.message_user(request, "Все комментарии удалены")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
AdminSite.site_header = 'Редактирование постов'
AdminSite.site_title = 'Редактирование постов'
