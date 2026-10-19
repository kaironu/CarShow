from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class StaticImage:
    url: str


@dataclass(frozen=True)
class StaticCar:
    id: int
    name: str
    brand: str
    category: str
    price: Decimal
    image: StaticImage
    model_year: int
    engine_type: str
    transmission: str
    fuel_type: str
    mileage: str
    seats: int
    description: str
    featured: bool = False
    extra_images: tuple = field(default_factory=tuple)


@dataclass(frozen=True)
class StaticService:
    id: int
    name: str
    category: str
    description: str
    duration: str
    price: Decimal
    price_min: Decimal
    price_max: Decimal
    image: StaticImage
    process_steps: tuple


@dataclass(frozen=True)
class StaticPart:
    id: int
    name: str
    category: str
    price: Decimal
    stock: int


LOCAL_CAR_IMAGES = (
    "car-images/audi-images/a7/a71.jpeg",
    "car-images/audi-images/r8/r81.jpeg",
    "car-images/bmw-images/bmw-m4-image/m4-1.jpeg",
    "car-images/bmw-images/m8/m8_1.jpeg",
    "car-images/lexus-images/ic-images/ic-1.jpeg",
    "car-images/lexus-images/lc-black-images/icblack-1.jpeg",
    "car-images/porsche-images/911/911_1.jpeg",
    "car-images/porsche-images/988/988_1.jpeg",
    "car-images/mclaren-images/720s/720_1.jpeg",
    "car-images/mclaren-images/765lt/765_1.jpeg",
)


def _car_image(seed):
    image_path = LOCAL_CAR_IMAGES[sum(ord(char) for char in seed) % len(LOCAL_CAR_IMAGES)]
    return StaticImage(f"/static/{image_path}")


def _service_image(filename):
    return StaticImage(f"/static/service-images/{filename}")


CAR_DATA = (
    ("Toyota", "Camry", "premium", "2519000", "photo-1621007947382-bb3c3994e3fb"),
    ("Toyota", "Fortuner", "luxury", "3269000", "photo-1553440569-b7ba18a444e0"),
    ("Honda", "City", "basic", "1249000", "photo-1606664515524-ed2f786a0bd6"),
    ("Honda", "CR-V", "premium", "2899000", "photo-1549317661-bd32c8ce0db2"),
    ("Hyundai", "Creta", "premium", "1899000", "photo-1606664515524-ed2f786a0bd6"),
    ("Hyundai", "Ioniq 5", "luxury", "4499000", "photo-1619767886558-efdc259cde1a"),
    ("Kia", "Seltos", "premium", "1799000", "photo-1542362567-b07e54358753"),
    ("Kia", "EV6", "luxury", "4999000", "photo-1593941707882-a5bba14938c7"),
    ("Ford", "Mustang", "luxury", "7499000", "photo-1584345604476-8ec5e12e42dd"),
    ("Ford", "Endeavour", "premium", "3599000", "photo-1533473359331-0135ef1b58bf"),
    ("BMW", "3 Series", "luxury", "5999000", "photo-1555215695-3004980ad54e"),
    ("BMW", "X5", "luxury", "9899000", "photo-1551830820-330a71b99659"),
    ("Mercedes-Benz", "C-Class", "luxury", "6999000", "photo-1563720223185-11003d516935"),
    ("Mercedes-Benz", "GLC", "luxury", "8999000", "photo-1618843479313-40f8afb4b4d8"),
    ("Audi", "A4", "luxury", "5799000", "photo-1606664515524-ed2f786a0bd6"),
    ("Audi", "Q5", "luxury", "7299000", "photo-1606664515524-ed2f786a0bd6"),
    ("Lexus", "ES", "luxury", "6399000", "photo-1616422285623-13ff0162193c"),
    ("Lexus", "RX", "luxury", "9499000", "photo-1542362567-b07e54358753"),
    ("Toyota", "Innova Hycross", "premium", "2599000", "photo-1544829099-b9a0c07fad1a"),
    ("Honda", "Elevate", "premium", "1699000", "photo-1503376780353-7e6692767b70"),
)


CARS = tuple(
    StaticCar(
        id=index,
        name=model,
        brand=brand,
        category=category,
        price=Decimal(price),
        image=_car_image(image_seed),
        model_year=2025,
        engine_type="2.0L Turbo",
        transmission="Automatic",
        fuel_type="Petrol / Hybrid",
        mileage="14 km/l",
        seats=5,
        description=f"{brand} {model} combines refined comfort, modern technology and confident performance.",
        featured=index <= 5,
    )
    for index, (brand, model, category, price, image_seed) in enumerate(CAR_DATA, 1)
)


SERVICES = (
    StaticService(1, "Premium Periodic Service", "maintenance", "Complete inspection and maintenance for a smooth, reliable drive.", "2 hrs", Decimal("2499"), Decimal("2499"), Decimal("4999"), _service_image("full_service.jpg"), ("Inspection", "Fluid replacement", "Final quality check")),
    StaticService(2, "Luxury Detailing", "detailing", "Deep exterior and interior detailing with premium protective finish.", "4 hrs", Decimal("4999"), Decimal("4999"), Decimal("8999"), _service_image("ceramic.jpg"), ("Foam wash", "Interior treatment", "Paint protection")),
    StaticService(3, "Brake & Safety Check", "repair", "Safety-first brake, tyre and suspension diagnosis by trained technicians.", "90 mins", Decimal("1499"), Decimal("1499"), Decimal("2999"), _service_image("car_brake.jpg"), ("Diagnostics", "Brake inspection", "Road test")),
    StaticService(4, "Ceramic Protection", "premium", "Long-lasting ceramic coating that keeps your vehicle showroom ready.", "1 day", Decimal("12999"), Decimal("12999"), Decimal("19999"), _service_image("ceramic.jpg"), ("Paint correction", "Coating application", "Curing and delivery")),
)


SPARE_PARTS = (
    StaticPart(1, "Premium Brake Pad Set", "brakes", Decimal("3499"), 18),
    StaticPart(2, "Engine Air Filter", "engine", Decimal("899"), 32),
    StaticPart(3, "All-Weather Floor Mat", "wheels", Decimal("2499"), 24),
    StaticPart(4, "LED Headlight Pair", "electrical", Decimal("5999"), 10),
    StaticPart(5, "Transmission Fluid Kit", "transmission", Decimal("1899"), 15),
    StaticPart(6, "Radiator Coolant", "cooling", Decimal("699"), 40),
)


BRANDS = tuple(dict.fromkeys(car.brand for car in CARS))
CATEGORIES = tuple(dict.fromkeys(service.category for service in SERVICES))


def get_car(car_id):
    return next((car for car in CARS if car.id == int(car_id)), None)


def get_service(service_id):
    return next((service for service in SERVICES if service.id == int(service_id)), None)


def get_part(part_id):
    return next((part for part in SPARE_PARTS if part.id == int(part_id)), None)
