import json
import os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from pathlib import Path
from datetime import datetime, time

from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
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
            avatar_file = request.FILES.get("avatar")
            context.update(_handle_registration(email, password, avatar_file))
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


def _handle_registration(email: str, password: str, avatar_file=None) -> dict:
    if not email or not password:
        return {"message": "Completeaza emailul si parola pentru inregistrare.", "message_type": "error"}

    if User.objects.filter(email__iexact=email).exists():
        return {"message": "Exista deja un utilizator cu acest email.", "message_type": "error"}

    user = User(email=email, parola=make_password(password))
    if avatar_file:
        user.avatar = avatar_file
    user.save()
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
    user = _get_authenticated_user(request)
    if not user:
        return {}

    email = user.email
    local_part = email.split("@")[0]
    tokens = [token for token in local_part.replace("-", " ").replace("_", " ").split() if token]
    initials = "".join(token[0] for token in tokens) or email[:2]

    context = {
        "user_name": local_part.title(),
        "user_initials": initials[:2].upper(),
        "user_email": email,
    }
    if user.avatar:
        context["user_avatar_url"] = user.avatar.url
    return context


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


@csrf_exempt
@require_POST
def chat_sql_api(request):
    """
    POST /api/chat/sql/
    Body: { "question": "..." }

    - Reads GOOGLE_API_KEY and DATABASE_URL (or CHAT_DATABASE_URL) from environment
      (or uses hardcoded values from settings for local/testing).
    - Runs a LangChain Text-to-SQL agent against the configured database using Gemini.
    - Returns JSON: { "answer": "..." } or { "error": "..." }.
    """
    # Optional: require our session-auth user
    user = _get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    # Parse JSON body
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    question = (payload.get("question") or "").strip()
    if not question:
        return JsonResponse({"error": "Missing 'question' in request body"}, status=400)

    # Secrets from env / settings
    # Prefer hardcoded Google key from settings if provided (not recommended for production)
    google_api_key = getattr(settings, "HARDCODED_GOOGLE_API_KEY", None)
    if not google_api_key:
        # fallback to env var
        google_api_key = os.environ.get("GOOGLE_API_KEY")
    db_url = (
        os.environ.get("CHAT_DATABASE_URL")
        or os.environ.get("DATABASE_URL")
        or getattr(settings, "DATABASE_URL", None)
    )

    if not google_api_key:
        return JsonResponse({"error": "GOOGLE_API_KEY not configured in environment"}, status=500)
    if not db_url:
        return JsonResponse({"error": "DATABASE_URL not configured in environment"}, status=500)

    # Build LLM (Gemini)
    try:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI  # preferred
        except Exception:
            # Legacy import path fallback is not common; keep single import.
            from langchain_google_genai import ChatGoogleGenerativeAI

        model_name = (
            getattr(settings, "GOOGLE_MODEL", None)
            or getattr(settings, "GENAI_MODEL", None)
            or os.environ.get("GOOGLE_MODEL")
            or os.environ.get("GENAI_MODEL")
            or "gemini-2.5-pro"
        )
        llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model=model_name, temperature=0)
    except Exception as e:
        return JsonResponse({"error": "Failed to initialize Gemini LLM", "details": str(e)}, status=500)

    # Build SQL database utility (normalize URL, add driver, strip problematic params)
    def _normalize_db_url(raw: str):
        if not raw:
            return raw, raw, {}
        parsed = urlparse(raw)
        scheme = parsed.scheme
        query_pairs = dict(parse_qsl(parsed.query))
        # Remove channel_binding which breaks many clients
        query_pairs.pop("channel_binding", None)
        # Ensure sslmode for remote DBs (keep if present)
        if parsed.hostname not in (None, "localhost", "127.0.0.1"):
            query_pairs.setdefault("sslmode", "require")
        # Prefer explicit psycopg2 driver for Postgres
        if scheme in ("postgres", "postgresql"):
            scheme = "postgresql+psycopg2"
        normalized = urlunparse(
            (
                scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                urlencode(query_pairs, doseq=True),
                parsed.fragment,
            )
        )
        # Mask password for logs/errors
        masked_netloc = parsed.netloc
        if "@" in parsed.netloc:
            creds, host = parsed.netloc.split("@", 1)
            if ":" in creds:
                user, _pwd = creds.split(":", 1)
                masked_netloc = f"{user}:***@{host}"
            else:
                masked_netloc = f"***@{host}"
        masked = urlunparse((scheme, masked_netloc, parsed.path, parsed.params, urlencode(query_pairs, doseq=True), parsed.fragment))
        # Engine args: pass sslmode via connect_args for psycopg2 if present
        engine_args = {}
        if scheme.startswith("postgresql+") and query_pairs.get("sslmode"):
            engine_args = {"connect_args": {"sslmode": query_pairs.get("sslmode")}}
        return normalized, masked, engine_args

    try:
        # Try multiple import paths for broad LangChain compatibility
        SQLDatabase = None
        import_err = None
        try:
            from langchain_community.utilities import SQLDatabase as _SQLDatabase  # preferred modern path
            SQLDatabase = _SQLDatabase
        except Exception as ie1:
            import_err = ie1
            try:
                from langchain_community.utilities.sql_database import SQLDatabase as _SQLDatabase  # alt path
                SQLDatabase = _SQLDatabase
            except Exception as ie2:
                import_err = ie2
                try:
                    from langchain.sql_database import SQLDatabase as _SQLDatabase  # older LC
                    SQLDatabase = _SQLDatabase
                except Exception as ie3:
                    import_err = ie3
                    try:
                        from langchain.utilities import SQLDatabase as _SQLDatabase  # legacy fallback
                        SQLDatabase = _SQLDatabase
                    except Exception as ie4:
                        import_err = ie4
        if SQLDatabase is None:
            raise import_err or ImportError("Unable to import SQLDatabase from LangChain.")

        normalized_url, masked_url, engine_args = _normalize_db_url(db_url)
        db = None
        try:
            db = SQLDatabase.from_uri(normalized_url, engine_args=engine_args)
        except Exception as inner:
            # Fallback to local sqlite if available
            sqlite_file = Path(settings.BASE_DIR) / "db.sqlite3"
            if sqlite_file.exists():
                sqlite_url = f"sqlite:///{sqlite_file.resolve().as_posix()}"
                db = SQLDatabase.from_uri(sqlite_url)
            else:
                raise inner
    except Exception as e:
        err = str(e)
        low = err.lower()
        hint = None
        if "no module named 'sqlalchemy'" in low or "no module named sqlalchemy" in low:
            hint = "Install SQLAlchemy: pip install sqlalchemy"
        elif "no module named 'langchain_community'" in low or "no module named langchain_community" in low:
            hint = "Install LangChain community: pip install langchain-community"
        elif "no module named 'langchain.utilities'" in low or "no module named langchain.utilities" in low:
            hint = "Install LangChain community: pip install langchain-community (newer LC split utilities to langchain-community)"
        elif "no module named 'langchain.sql_database'" in low or "no module named langchain.sql_database" in low:
            hint = "Upgrade/downgrade LangChain or install langchain-community: pip install -U langchain langchain-community"
        elif "no module named 'langchain'" in low:
            hint = "Install LangChain: pip install langchain"
        elif "psycopg2" in low:
            hint = "Install driver: pip install psycopg2-binary"
        return JsonResponse(
            {
                "error": "Failed to connect SQLDatabase",
                "details": err,
                "hint": hint,
                "db_url": masked_url if 'masked_url' in locals() else None,
            },
            status=500,
        )

    # Create an agent/chain able to generate SQL and query the DB
    chain = None
    agent_err = None
    try:
        try:
            from langchain_community.agent_toolkits import (
                SQLDatabaseToolkit,
                create_sql_agent,
            )
        except Exception:
            from langchain.agents.agent_toolkits import (
                SQLDatabaseToolkit,
                create_sql_agent,
            )

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        # Try agent creation without forcing an AgentType (more LLM-agnostic)
        try:
            chain = create_sql_agent(llm=llm, toolkit=toolkit, verbose=False)
        except Exception:
            # Fallback to an agent type compatible with non-OpenAI models
            try:
                from langchain.agents import AgentType
                try:
                    chain = create_sql_agent(
                        llm=llm,
                        toolkit=toolkit,
                        verbose=False,
                        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    )
                except Exception:
                    chain = create_sql_agent(
                        llm=llm,
                        toolkit=toolkit,
                        verbose=False,
                        agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                    )
            except Exception:
                chain = None
    except Exception as e:
        agent_err = e

    # Fallback to SQLDatabaseChain if agent creation failed
    if chain is None:
        try:
            try:
                from langchain_experimental.sql import SQLDatabaseChain
            except Exception:
                # Older import path
                from langchain.chains import SQLDatabaseChain
            chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)
        except Exception as e:
            return JsonResponse({
                "error": "Failed to initialize SQL agent/chain",
                "details": f"agent_error={agent_err}; chain_error={e}",
            }, status=500)

    # Execute the query through the chain/agent with 429-aware fallback
    def _invoke_chain(ch):
        if hasattr(ch, "run"):
            return ch.run(question)
        res = ch.invoke({"input": question})
        if isinstance(res, dict):
            return res.get("output") or res.get("result") or str(res)
        return str(res)

    try:
        answer = _invoke_chain(chain)
    except Exception as e:
        e_str = str(e)
        low = e_str.lower()
        # Detect rate limit / quota exceeded
        if "429" in low or "quota" in low or "rate" in low:
            # Try fallback model if defined and different
            primary_model = (
                getattr(settings, "GOOGLE_MODEL", None)
                or getattr(settings, "GENAI_MODEL", None)
                or os.environ.get("GOOGLE_MODEL")
                or os.environ.get("GENAI_MODEL")
                or "gemini-2.5-pro"
            )
            fallback_model = (
                getattr(settings, "GOOGLE_MODEL_FALLBACK", None)
                or os.environ.get("GOOGLE_MODEL_FALLBACK")
                or os.environ.get("GENAI_MODEL_FALLBACK")
                or "gemini-1.5-flash-latest"
            )
            retry_after = None
            # Attempt to parse suggested retry delay
            import re
            m = re.search(r"retry\s*in\s*([0-9]+(?:\.[0-9]+)?)s", e_str, re.IGNORECASE)
            if m:
                try:
                    retry_after = float(m.group(1))
                except Exception:
                    retry_after = None
            if fallback_model:
                try:
                    from langchain_google_genai import ChatGoogleGenerativeAI

                    def _try_model(model_name: str):
                        try:
                            llm_fb = ChatGoogleGenerativeAI(google_api_key=google_api_key, model=model_name, temperature=0)
                        except Exception:
                            return None
                        # Rebuild agent with fallback LLM
                        try:
                            try:
                                from langchain_community.agent_toolkits import (
                                    SQLDatabaseToolkit,
                                    create_sql_agent,
                                )
                            except Exception:
                                from langchain.agents.agent_toolkits import (
                                    SQLDatabaseToolkit,
                                    create_sql_agent,
                                )
                            toolkit_fb = SQLDatabaseToolkit(db=db, llm=llm_fb)
                            try:
                                chain_fb = create_sql_agent(llm=llm_fb, toolkit=toolkit_fb, verbose=False)
                            except Exception:
                                chain_fb = None
                            if chain_fb is None:
                                try:
                                    try:
                                        from langchain_experimental.sql import SQLDatabaseChain
                                    except Exception:
                                        from langchain.chains import SQLDatabaseChain
                                    chain_fb = SQLDatabaseChain.from_llm(llm_fb, db, verbose=False)
                                except Exception:
                                    chain_fb = None
                            if chain_fb is None:
                                return None
                            try:
                                ans = _invoke_chain(chain_fb)
                                return {"answer": str(ans).strip() or "", "model_used": model_name}
                            except Exception:
                                return None
                        except Exception:
                            return None

                    tried = set()
                    candidates = []
                    # Avoid retrying the same primary model; add fallback only if different
                    if fallback_model != primary_model:
                        candidates.append(fallback_model)
                    # Try a "-latest" variant too
                    if not fallback_model.endswith("-latest"):
                        candidates.append(fallback_model + "-latest")
                    # Add widely available stable models
                    candidates.extend(["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro", "gemini-1.5-pro-latest"])
                    for cand in candidates:
                        if cand in tried:
                            continue
                        tried.add(cand)
                        out = _try_model(cand)
                        if out is not None:
                            return JsonResponse(out, status=200)
                except Exception:
                    # ignore and fall through to 429
                    pass
            # If fallback not possible/successful, return 429 with retry info
            payload = {"error": "Agent execution failed: rate limit", "details": e_str}
            if retry_after is not None:
                payload["retry_after_seconds"] = retry_after
            return JsonResponse(payload, status=429)
        # Non-rate-limit error
        return JsonResponse({"error": "Agent execution failed", "details": e_str}, status=500)

    return JsonResponse({"answer": str(answer).strip() or ""}, status=200)
