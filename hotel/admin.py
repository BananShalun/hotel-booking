from django.contrib import admin
from .models import Booking, RoomCategory, Service

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "base_price", "capacity")
    list_filter = ("capacity",)
    search_fields = ("name",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    search_fields = ("name",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "guest_name", "room_category", "user", "status", "check_in", "check_out", "created_at")
    list_filter = ("status", "room_category", "services")
    search_fields = ("guest_name", "comment")
    list_select_related = ("room_category", "user")
    filter_horizontal = ("services",)
    date_hierarchy = "check_in"
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50