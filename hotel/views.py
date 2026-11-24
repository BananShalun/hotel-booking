from django.shortcuts import render
from .models import Booking, RoomCategory

def booking_list(request):
    # ВНИМАНИЕ: Это "наивная" версия. Она специально сделана медленной!
    bookings = Booking.objects.all() 

    # Фильтры (пока простые)
    if request.GET.get("category"):
        bookings = bookings.filter(room_category_id=request.GET["category"])
    if request.GET.get("status"):
        bookings = bookings.filter(status=request.GET["status"])
    if request.GET.get("q"):
        bookings = bookings.filter(guest_name__icontains=request.GET["q"])
    
    # Грузим ВСЕ объекты в память, чтобы посчитать их (очень медленно на 100к записей)
    total = len(bookings) 
    
    # Берем только первые 25 для отображения
    bookings = bookings[:25] 
    
    categories = RoomCategory.objects.all()

    return render(request, "hotel/booking_list.html", {
        "bookings": bookings, 
        "total": total, 
        "categories": categories,
    })