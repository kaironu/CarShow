from .static_data import BRANDS, CATEGORIES, SERVICES
from django.conf import settings


def brands_processor(request):
    return {
        'brands': BRANDS,
        'grouped_services': {
            category: [service for service in SERVICES if service.category == category]
            for category in CATEGORIES
        },
        'categories': CATEGORIES,
    }


def admin_sidebar_counts(request):
    return {
        "new_booking_count": 0,
        "new_payment_count": 0,
        "total_trash": 0,
        "unread_notifications_count": 0,
        "booked_spare_parts_count": 0,
        "refund_count": 0,
        "subscribers_count": 0,
    }


def subscription_status(request):
    """
    Returns whether the logged-in user is subscribed.
    Available in all templates.
    """
    return {"is_subscribed": False}



def social_links(request):
    return {
        "social_links": getattr(settings, "SOCIAL_LINKS", {})
    }
