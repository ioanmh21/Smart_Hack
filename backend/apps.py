from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        """On app startup, print available Gemini models to the console.
        Uses HARDCODED_GOOGLE_API_KEY or GOOGLE_API_KEY env var. Safe no-op if missing.
        """
        try:
            # Avoid double-print during autoreload in DEBUG
            import os
            from django.conf import settings

            if settings.DEBUG and os.environ.get("RUN_MAIN") != "true":
                return

            api_key = getattr(settings, "HARDCODED_GOOGLE_API_KEY", None) or os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                print("[Gemini] GOOGLE_API_KEY not configured; skipping model listing.")
                return

            try:
                import google.generativeai as genai
            except Exception as imp_err:
                print(f"[Gemini] google-generativeai not installed: {imp_err}")
                return

            try:
                genai.configure(api_key=api_key)
                models = [
                    m for m in genai.list_models()
                    if "generateContent" in getattr(m, "supported_generation_methods", [])
                ]
                names = [getattr(m, "name", str(m)) for m in models]
                print("[Gemini] Available models:", ", ".join(names) if names else "(none)")
            except Exception as e:
                print(f"[Gemini] Failed to list models: {e}")
        except Exception:
            # Never block app startup due to logging
            pass
