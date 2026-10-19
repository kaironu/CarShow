from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .static_data import (
    BRANDS,
    CARS,
    CATEGORIES,
    SERVICES,
    SPARE_PARTS,
    get_car,
    get_part,
    get_service,
)

STATIC_USERNAME = "sang"
STATIC_PASSWORD = "123"


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        is_static_login = username == STATIC_USERNAME and password == STATIC_PASSWORD
        is_local_login = request.POST.get("local_account") == "1" and username
        if is_static_login or is_local_login:
            request.session["static_user"] = username
            request.session["static_email"] = request.POST.get("email", "")
            messages.success(request, "Đăng nhập thành công. Chào mừng bạn đến Prestige Lane.")
            return redirect("home")
        messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    return render(request, "accounts/login.html")


def logout_view(request):
    request.session.pop("static_user", None)
    request.session.pop("static_email", None)
    messages.info(request, "Bạn đã đăng xuất thành công.")
    return redirect("home")


def password_reset(request):
    return render(request, "password_reset.html")


def profile(request):
    username = request.session.get("static_user")
    if not username:
        return redirect("login")
    return render(request, "accounts/static_profile.html", {
        "profile_username": username,
        "profile_email": request.session.get("static_email", ""),
    })


def home(request):
    return render(request, "accounts/home.html", {
        "brands": BRANDS,
        "featured_cars": [car for car in CARS if car.featured],
        "cars": CARS,
        "is_subscribed": False,
    })


def car_list(request):
    query = request.GET.get("q", "").strip().lower()
    cars = [
        car for car in CARS
        if not query
        or query in car.name.lower()
        or query in car.brand.lower()
        or query in car.category.lower()
    ]
    return render(request, "accounts/car_list.html", {
        "cars": cars,
        "query": query,
        "user_wishlist": [],
        "no_results": not cars,
    })


def car_brand_list(request, brand_name):
    cars = [car for car in CARS if car.brand.lower() == brand_name.lower()]
    return render(request, "accounts/car_list.html", {
        "cars": cars,
        "brand_name": brand_name,
        "user_wishlist": [],
        "no_results": not cars,
    })


def car_details(request, car_id):
    car = get_car(car_id)
    if car is None:
        return render(request, "404.html", status=404)
    similar_cars = [
        item for item in CARS
        if item.category == car.category and item.id != car.id
    ][:4]
    return render(request, "accounts/car_details.html", {
        "car": car,
        "extra_images": car.extra_images,
        "user_wishlist": [],
        "similar_cars": similar_cars,
    })


def cart(request):
    return render(request, "accounts/cart.html")


def toggle_wishlist(request, car_id):
    if get_car(car_id) is None:
        return JsonResponse({"status": "error", "message": "Car not found"}, status=404)
    return JsonResponse({"status": "added"})


def autocomplete_search(request):
    query = request.GET.get("q", "").strip().lower()
    results = [
        {
            "type": "Car",
            "id": car.id,
            "label": f"{car.brand} {car.name}",
            "value": car.name,
        }
        for car in CARS
        if query and (query in car.name.lower() or query in car.brand.lower())
    ][:5]
    return JsonResponse(results, safe=False)


def about(request):
    return render(request, "accounts/about.html", {"approved_reviews": []})


def contact(request):
    if request.method == "POST":
        required_fields = ("name", "email", "phone", "message")
        if any(not request.POST.get(field, "").strip() for field in required_fields):
            messages.error(request, "Vui lòng điền đầy đủ thông tin trước khi gửi.")
            return render(request, "accounts/contact.html")
        messages.success(request, "Gửi tin nhắn thành công. Chúng tôi sẽ liên hệ với bạn sớm.")
        return redirect("contact")
    return render(request, "accounts/contact.html")


def services_list(request):
    grouped_services = {
        category: [service for service in SERVICES if service.category == category]
        for category in CATEGORIES
    }
    return render(request, "services/services_list.html", {
        "grouped_services": grouped_services
    })


def services_by_category(request, category_name):
    grouped_services = {
        category_name: [
            service for service in SERVICES
            if service.category.lower() == category_name.lower()
        ]
    }
    return render(request, "services/services_list.html", {
        "grouped_services": grouped_services
    })


def service_detail(request, service_id):
    service = get_service(service_id)
    if service is None:
        return render(request, "404.html", status=404)
    return render(request, "services/service_detail.html", {"service": service})


def spare_parts_list(request):
    query = request.GET.get("search", "").strip().lower()
    parts = [
        part for part in SPARE_PARTS
        if not query or query in part.name.lower()
    ]
    return render(request, "accounts/spare_parts_list.html", {
        "parts": parts,
        "search_query": query,
    })


def _booking_request(request, item, booking_type, back_url):
    if item is None:
        return render(request, "404.html", status=404)
    if request.method == "POST":
        required_fields = ("name", "email", "phone")
        if any(not request.POST.get(field, "").strip() for field in required_fields):
            messages.error(request, "Vui lòng điền đầy đủ họ tên, email và số điện thoại.")
            return render(request, "accounts/static_booking.html", {
                "item": item,
                "booking_type": booking_type,
                "back_url": back_url,
            })
        messages.success(request, "Gửi yêu cầu thành công. Nhân viên sẽ liên hệ với bạn sớm.")
        return redirect(back_url)
    return render(request, "accounts/static_booking.html", {
        "item": item,
        "booking_type": booking_type,
        "back_url": back_url,
    })


def book_car_action(request, car_id, booking_type):
    car = get_car(car_id)
    return _booking_request(
        request,
        car,
        booking_type.replace("_", " ").title(),
        reverse("car_details", args=[car_id]),
    )


def book_service(request, service_id):
    return _booking_request(
        request,
        get_service(service_id),
        "Service Request",
        reverse("service_detail", args=[service_id]),
    )


def book_part(request, part_id):
    return _booking_request(
        request,
        get_part(part_id),
        "Spare Part Request",
        reverse("spare_parts_list"),
    )
