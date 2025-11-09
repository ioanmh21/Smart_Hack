import json
from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .models import Obiect, Rezervare, User

beers = [
  "beer1",
  "beer2",
  "beer4",
  "beer5",
  "beer6",
  "beer7",
  "beer8",
  "beer9",
  "beer10",
  "beer11"
]
chairs = [
  "path20-40-4-9-08-41",
  "path20-40-4-9-08-1",
  "path20-40-4-9-08-78",
  "path20-40-4-9-08-23",
  "path20-40-4-9-08-4",
  "path20-40-4-9-08-26",
  "path20-40-4-9-08-3",
  "path20-40-4-9-08-2",
  "path20-40-4-9-08-7",
  "path20-40-4-9-08-9",
  "path20-51-0-8-78",
  "path20-40-68-3-37",
  "path20-84-1-9-1",
  "path20-51-7-3-0",
  "path20-40-4-9-08",
  "path20-84-3-6-3",
  "path20-51-99-7-45",
  "path20-40-2-99-0",
  "path20-84-5-7-1",
  "path20-51-9-69-45",
  "path20-40-6-3-62",
  "path20-84-8-5-03",
  "path20-51-0-8-3",
  "path20-40-68-3-00",
  "path20-84-1-9-48",
  "path20-51-7-3-30",
  "path20-40-4-9-129",
  "path20-84-3-6-03",
  "path20-51-99-7-8",
  "path20-40-2-99-8",
  "path20-84-5-7-57",
  "path20-51-9-69-7",
  "path20-40-6-3-0",
  "path20-84-8-5-89",
  "path20-51-0-8-98",
  "path20-40-68-3-302",
  "path20-84-1-9-2",
  "path20-51-7-3-3",
  "path20-40-4-9-6",
  "path20-84-3-6-7",
  "path20-51-99-7-1",
  "path20-40-2-99-5",
  "path20-84-5-7-5",
  "path20-51-9-69-40",
  "path20-40-6-3-260",
  "path20-84-8-5-6",
  "path20-51-0-8-92",
  "path20-40-68-3-0",
  "path20-84-1-9-70",
  "path20-51-7-3-6",
  "path20-40-4-9-07",
  "path20-84-3-6-0",
  "path20-51-99-7-5",
  "path20-40-2-99-67",
  "path20-84-5-7-38",
  "path20-51-9-69-49",
  "path20-40-6-3-26",
  "path20-84-8-5-57",
  "path20-51-0-8-0",
  "path20-40-68-3-6",
  "path20-84-1-9-7",
  "path20-51-7-3-50",
  "path20-40-4-9-04",
  "path20-84-3-6-54",
  "path20-51-99-7-95",
  "path20-40-2-99-64",
  "path20-84-5-7-8",
  "path20-51-9-69-21",
  "path20-40-6-3-6",
  "path20-84-8-5-83",
  "path20-51-0-8-11",
  "path20-40-68-3-32",
  "path20-84-1-9-53",
  "path20-51-7-3-5",
  "path20-40-4-9-12",
  "path20-84-3-6-22",
  "path20-51-99-7-6",
  "path20-40-2-99-40",
  "path20-84-5-7-70",
  "path20-51-9-69-3",
  "path20-40-6-3-4",
  "path20-84-8-5-0",
  "path20-51-0-8-7",
  "path20-40-68-3-30",
  "path20-84-1-9-3",
  "path20-51-7-3-8",
  "path20-40-4-9-25",
  "path20-84-3-6-2",
  "path20-51-99-7-0",
  "path20-40-2-99-3",
  "path20-84-5-7-7",
  "path20-51-9-69-29",
  "path20-40-6-3-7",
  "path20-84-8-5-5",
  "path20-51-0-8-1",
  "path20-40-68-3-2",
  "path20-84-1-9-5",
  "path20-51-7-3-7",
  "path20-40-4-9-4",
  "path20-84-3-6-4",
  "path20-51-99-7-4",
  "path20-40-2-99-4",
  "path20-84-5-7-4",
  "path20-51-9-69-2",
  "path20-40-6-3-9",
  "path20-84-8-5-3",
  "path20-40-4-9-3",
  "path20-40-4-9-2",
  "path20-40-4-9-86",
  "path20-40-4-9-1",
  "path20-51-0-8",
  "path20-40-68-3",
  "path20-84-1-9",
  "path20-51-7-3",
  "path20-40-4-9",
  "path20-40-4-9-8",
  "path20-84-3-6",
  "path20-51-99-7",
  "path20-40-2-99",
  "path20-84-5-7",
  "path20-51-9-69",
  "path20-40-6-3",
  "path20-84-8-5",
  "path20-51-0-8-9",
  "path20-40-68-3-3",
  "path20-84-1-9-4",
  "path20-51-7-3-4",
  "path20-40-4-9-0",
  "path20-84-3-6-5",
  "path20-51-99-7-9",
  "path20-40-2-99-6",
  "path20-84-5-7-3",
  "path20-51-9-69-4",
  "path20-40-6-3-2",
  "path20-84-8-5-8",
  "path20-51-0-67",
  "path20-40-68-7",
  "path20-84-1-2",
  "path20-51-7-29",
  "path20-40-4-4",
  "path20-84-3-1",
  "path20-51-99-96",
  "path20-40-2-9",
  "path20-84-5-82",
  "path20-51-9-5",
  "path20-40-6-54",
  "path20-84-8-9",
  "path20-51-0",
  "path20-40-68",
  "path20-84-1",
  "path20-51-7",
  "path20-40-4",
  "path20-84-3",
  "path20-51-99",
  "path20-40-2",
  "path20-84-5",
  "path20-51-9",
  "path20-40-6",
  "path20-84-8",
  "path20-51-0-2",
  "path20-40-68-2",
  "path20-84-1-8",
  "path20-51-7-2",
  "path20-40-4-8",
  "path20-84-3-9",
  "path20-51-99-0",
  "path20-40-2-7",
  "path20-84-5-8",
  "path20-51-9-1",
  "path20-40-6-5",
  "path20-84-8-8",
  "path20-51-0-25",
  "path20-40-68-8",
  "path20-84-1-6",
  "path20-51-7-26",
  "path20-40-4-5",
  "path20-84-3-3",
  "path20-51-99-9",
  "path20-40-2-2",
  "path20-84-5-4",
  "path20-51-9-6",
  "path20-40-6-1",
  "path20-84-8-82",
  "path20-51-0-6",
  "path20-40-68-29",
  "path20-84-1-5",
  "path20-51-7-20",
  "path20-40-4-0",
  "path20-84-3-39",
  "path20-51-99-1",
  "path20-40-2-8",
  "path20-84-5-1",
  "path20-51-9-9",
  "path20-40-6-53",
  "path20-84-8-2",
  "path20-51-4",
  "path20-40-9",
  "path20-84-6",
  "path20-51-3",
  "path20-40-83",
  "path20-84-7",
  "path20-51-8",
  "path20-40-8",
  "path20-84-0",
  "path20-51",
  "path20-40",
  "path20-84",
  "path20-9",
  "path20-80",
  "path20-182",
  "path20-733",
  "path20-16",
  "path20-73",
  "path20-15",
  "path20-0",
  "path20-3",
  "path20-78",
  "path20-18",
  "path20-44",
  "path20-61",
  "path20-65",
  "path20-86",
  "path20-8",
  "path20-77",
  "path20-13",
  "path20-12",
  "path20-7",
  "path20-6",
  "path20-1",
  "path20-4",
  "path20-5",
  "path20",
  "path20-07",
  "path20-40-4-9-82"
]

managers = [
  "mg1",
  "mg2",
  "mg3"
]

confs = [
  "conf1",
  "conf2"
]
pools = [
  "pool1",
  "pool2"
]
massages = ["masaj"] 
parties = ["party"]

OBJECT_GROUPS = {
    "beers": beers,
    "chairs": chairs,
    "managers": managers,
    "confs": confs,
    "pools": pools,
    "massages": massages,
    "parties": parties,
}


TIME_SLOTS = [time(hour=h) for h in range(8, 20)]



@require_GET
def landing(request):

    context = _build_user_context(request)
    return render(request, "backend/index.html", context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    context = {
        "login_initial": "",
        "register_initial": "",
        "message": "",
        "message_type": "",
    }

    if request.method == "POST":
        action = request.POST.get("action")
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        if action == "login":
            context["login_initial"] = email
            login_result = _handle_login(email, password)
            context.update(login_result)
            if login_result.get("message_type") == "success" and login_result.get("user_email"):
                request.session["user_email"] = login_result["user_email"]
                return redirect("backend:landing")
        elif action == "register":
            context["register_initial"] = email
            context.update(_handle_registration(email, password))
        else:
            context.update(
                {
                    "message": "Operatiune necunoscuta.",
                    "message_type": "error",
                }
            )

    return render(request, "backend/login.html", context)


@require_POST
def logout_view(request):
    request.session.pop("user_email", None)
    return redirect("backend:landing")


@require_GET
def profile_view(request):
    user = _get_authenticated_user(request)
    if not user:
        messages.info(request, "Autentifica-te pentru a-ti vedea rezervarile.")
        return redirect("backend:login")

    reservations = (
        user.rezervari.select_related("obiect")
        .order_by("data", "data_si_ora")
    )
    reservation_cards = []
    for reservation in reservations:
        localized_dt = timezone.localtime(reservation.data_si_ora)
        reservation_cards.append(
            {
                "reservation": reservation,
                "display_date": reservation.data.strftime("%A, %d %b"),
                "display_time": localized_dt.strftime("%H:%M"),
            }
        )
    context = {
        **_build_user_context(request),
        "reservation_cards": reservation_cards,
    }
    return render(request, "backend/profile.html", context)


@require_POST
def cancel_booking_view(request):
    user = _get_authenticated_user(request)
    if not user:
        messages.error(request, "Autentifica-te pentru a modifica rezervarile.")
        return redirect("backend:login")

    rez_id = request.POST.get("reservation_id")
    reservation = Rezervare.objects.filter(id_rez=rez_id, user=user).first()
    if reservation:
        reservation.delete()
        messages.success(request, "Rezervarea a fost anulata.")
    else:
        messages.error(request, "Rezervarea nu a fost gasita.")
    return redirect("backend:profile")


@require_GET
def availability_view(request, css_id: str):

    obiect = Obiect.objects.filter(id_css=css_id).first()
    if not obiect:
        return JsonResponse({"error": "Obiectul solicitat nu exista."}, status=404)

    target_date = _resolve_date(request.GET.get("date"))
    current_user_email = request.session.get("user_email")
    slots = _build_slot_payload(obiect, target_date, current_user_email)

    return JsonResponse(
        {
            "object": {
                "id": obiect.id_obiect,
                "css_id": obiect.id_css,
                "tip_obiect": obiect.tip_obiect,
            },
            "date": target_date.isoformat(),
            "slots": slots,
            "is_authenticated": bool(current_user_email),
            "login_url": reverse("backend:login"),
        }
    )


@require_POST
def book_slot_view(request):


    user_email = request.session.get("user_email")
    if not user_email:
        return JsonResponse({"error": "Trebuie sa fii autentificat pentru a rezerva."}, status=401)

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return JsonResponse({"error": "Contul asociat nu mai exista."}, status=401)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Format JSON invalid."}, status=400)

    css_id = (payload.get("css_id") or "").strip()
    slot_time = (payload.get("time") or "").strip()
    date_str = (payload.get("date") or "").strip()

    if not css_id or not slot_time:
        return JsonResponse({"error": "Ai nevoie de un obiect si o ora pentru rezervare."}, status=400)

    obiect = Obiect.objects.filter(id_css=css_id).first()
    if not obiect:
        return JsonResponse({"error": "Nu am gasit obiectul selectat."}, status=404)

    if slot_time not in {slot.strftime("%H:%M") for slot in TIME_SLOTS}:
        return JsonResponse({"error": "Ora selectata nu poate fi rezervata."}, status=400)

    target_date = _resolve_date(date_str)

    try:
        slot_datetime = _combine_date_and_time(target_date, slot_time)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    try:
        rezervare, created = Rezervare.objects.get_or_create(
            obiect=obiect,
            data=target_date,
            data_si_ora=slot_datetime,
            defaults={"user": user},
        )
    except IntegrityError:
        return JsonResponse({"error": "Slot-ul tocmai a fost rezervat. Incearca alt interval."}, status=409)

    if not created and rezervare.user_id != user.id_user:
        return JsonResponse({"error": "Acest slot este deja rezervat de alt coleg."}, status=409)

    if not created and rezervare.user_id == user.id_user:
        return JsonResponse(
            {
                "message": "Ai deja o rezervare pentru acest interval.",
                "already_reserved": True,
            },
            status=200,
        )

    return JsonResponse(
        {
            "message": "Rezervarea a fost confirmata!",
            "slot": {"time": slot_time, "date": target_date.isoformat()},
        },
        status=201,
    )


def _handle_login(email: str, password: str) -> dict:
    if not email or not password:
        return {"message": "Completeaza emailul si parola pentru login.", "message_type": "error"}

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return {"message": "Nu exista niciun cont cu acest email.", "message_type": "error"}

    if check_password(password, user.parola) or user.parola == password:
        return {
            "message": "Autentificare reusita. Bine ai revenit!",
            "message_type": "success",
            "user_email": user.email,
        }

    return {"message": "Parola introdusa nu este corecta.", "message_type": "error"}


def _handle_registration(email: str, password: str) -> dict:
    if not email or not password:
        return {"message": "Completeaza emailul si parola pentru inregistrare.", "message_type": "error"}

    if User.objects.filter(email__iexact=email).exists():
        return {"message": "Exista deja un utilizator cu acest email.", "message_type": "error"}

    User.objects.create(email=email, parola=make_password(password))
    return {"message": "Cont creat cu succes. Te poti autentifica acum!", "message_type": "success"}


def _get_authenticated_user(request):
    email = request.session.get("user_email")
    if not email:
        return None
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        request.session.pop("user_email", None)
        return None


def _build_user_context(request):
    email = request.session.get("user_email")
    if not email:
        return {}

    local_part = email.split("@")[0]
    tokens = [token for token in local_part.replace("-", " ").replace("_", " ").split() if token]
    initials = "".join(token[0] for token in tokens) or email[:2]

    return {
        "user_name": local_part.title(),
        "user_initials": initials[:2].upper(),
        "user_email": email,
    }


def _resolve_date(date_str: str | None):
    if not date_str:
        return timezone.localdate()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return timezone.localdate()


def _combine_date_and_time(target_date, time_str: str):
    try:
        hour, minute = (int(part) for part in time_str.split(":", 1))
    except ValueError as exc:
        raise ValueError("Formatul pentru ora este invalid. Foloseste HH:MM.") from exc

    slot_time = time(hour=hour, minute=minute)
    naive_dt = datetime.combine(target_date, slot_time)
    tz = timezone.get_current_timezone()
    return timezone.make_aware(naive_dt, tz)


def _format_slot_key(slot_datetime):
    dt = slot_datetime
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return timezone.localtime(dt).strftime("%H:%M")


def _build_slot_payload(obiect, target_date, current_user_email: str | None):
    reservations = Rezervare.objects.filter(obiect=obiect, data=target_date).select_related("user")
    reserved = {_format_slot_key(rez.data_si_ora): rez for rez in reservations}

    slots = []
    for slot_time in TIME_SLOTS:
        label = slot_time.strftime("%H:%M")
        reservation = reserved.get(label)
        slots.append(
            {
                "time": label,
                "available": reservation is None,
                "owned": bool(reservation and reservation.user.email == current_user_email),
                "booked_by": reservation.user.email if reservation else None,
            }
        )
    return slots
