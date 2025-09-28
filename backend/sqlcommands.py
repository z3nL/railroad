#  assume plaintext passwords (test-only) and no RLS.
# If you enable RLS later, use a service role key here (server-only).

import os
import uuid
import shutil
from typing import Optional, TypedDict, Tuple, Dict, Any, List
from supabase import create_client, Client
from dotenv import load_dotenv

# ---------- Load .env ----------
load_dotenv(dotenv_path=".env")  # loads variables from .env into os.environ

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")
BUCKET_NAME = "aiImages"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(BASE_DIR, "generated_images")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE in .env")

# ---------- Supabase client ----------
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# ---------- Types ----------
class AppUser(TypedDict):
    id: str
    email: str
    name: Optional[str]
    role: int

# ---------- Users ----------
def verify_user(email: str, password: str) -> Optional[AppUser]:
    """Lookup a user by email, plaintext password (test), and role."""
    res = (
        supabase.table("users")
        .select("id,email,name,role")
        .match({"email": email, "password": password})
        .limit(1)
        .execute()
    )
    rows = res.data or []
    return rows[0] if rows else None  # type: ignore

def create_account(email: str, password: str, name: str, role: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Insert a new user. Returns (user_dict, error)."""
    exists = supabase.table("users").select("id").eq("email", email).limit(1).execute()
    if exists.data:
        return None, "Email already registered"

    result = (
        supabase.table("users")
        .insert({"email": email, "password": password, "name": name, "role": role})
        .execute()
    )
    if not result.data:
        return None, "Failed to create user"
    # Fetch the newly created user by email
    user = (
        supabase.table("users")
        .select("id,email,name,role,created_at")
        .eq("email", email)
        .limit(1)
        .execute()
    )
    if not user.data:
        return None, "Failed to fetch created user"
    return user.data[0], None

# ---------- Lessons ----------
def get_lessons(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    q = supabase.table("lessons").select(
        "lesson_id,created_at,lesson_name,lesson_descriptions,lesson_level"
    )
    # if user_id: q = q.eq("owner_id", user_id)
    return q.order("created_at", desc=True).execute().data or []

def get_steps(lesson_id: int) -> List[Dict[str, Any]]:
    res = (
        supabase.table("steps")
        .select("lessons_id,step_number,step_image,step_description")
        .eq("lessons_id", lesson_id)
        .order("step_number", desc=False)
        .execute()
    )
    return res.data or []

def add_lesson(
    lesson_name: str,
    lesson_description: str,
    lesson_level: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    insert_lesson = (
        supabase.table("lessons")
        .insert({
            "lesson_name": lesson_name,
            "lesson_descriptions": lesson_description,
            "lesson_level": lesson_level,
        })
        .execute()
    )
    if not insert_lesson.data:
        return None, "Failed to create lesson"
    # Fetch the newly created lesson by its id
    lesson_id = insert_lesson.data[0]["lesson_id"]
    lesson = (
        supabase.table("lessons")
        .select("lesson_id,created_at,lesson_name,lesson_descriptions,lesson_level")
        .eq("lesson_id", lesson_id)
        .limit(1)
        .execute()
    )
    if not lesson.data:
        return None, "Failed to fetch created lesson"
    
    return lesson.data[0], None

# ---------- Steps ----------
def add_steps(
    lesson_id: int,
    steps: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    if not steps:
        return [], None

    payload: List[Dict[str, Any]] = []
    for s in steps:
        payload.append({
            "lessons_id": lesson_id,
            "step_number": int(s["step_number"]),
            "step_description": s["step_description"],
            "step_image": s.get("step_image"),
        })

    res = (
        supabase.table("steps")
        .insert(payload)
        .execute()
    )
    if getattr(res, "error", None) or not res.data:
        error_message = getattr(res, "message", "Failed to insert steps")
        return [], error_message

    return sorted(res.data, key=lambda x: x["step_number"]), None

def add_step(
    lesson_id: int,
    step_number: int,
    step_description: str,
    step_image: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    res = (
        supabase.table("steps")
        .insert({
            "lessons_id": lesson_id,
            "step_number": int(step_number),
            "step_description": step_description,
            "image_bucket": "aiImages",
            "image_path": step_image,
        })
        .execute()
    )
    if not res.data:
        error_message = getattr(res, "message", "Failed to insert step")
        return None, error_message
    rows = res.data or []
    return (rows[0] if rows else None), None

def upload_directory():
    uploaded_files = []

    if not os.path.exists(GENERATED_DIR):
        print(f"⚠️ Directory not found: {GENERATED_DIR}")
        return uploaded_files

    for filename in os.listdir(GENERATED_DIR):
        filepath = os.path.join(GENERATED_DIR, filename)

        # Skip non-files
        if not os.path.isfile(filepath):
            continue

        # Restrict to common image extensions
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            continue

        # Generate unique filename to avoid collisions
        ext = filename.split(".")[-1]
        unique_name = f"{uuid.uuid4()}.{ext}"

        try:
            with open(filepath, "rb") as f:
                supabase.storage.from_(BUCKET_NAME).upload(unique_name, f)
            
            # Get public URL
            public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_name)
            uploaded_files.append({"file": filename, "url": public_url})
            print(f"✅ Uploaded {filename} → {public_url}")

        except Exception as e:
            print(f"❌ Failed to upload {filename}: {e}")

    return uploaded_files


def clear_generated_images():
    """
    Recursively deletes all files and folders inside generated_images.
    Keeps the generated_images folder itself.
    """
    if not os.path.exists(GENERATED_DIR):
        print(f"⚠️ Directory not found: {GENERATED_DIR}")
        return

    for item in os.listdir(GENERATED_DIR):
        path = os.path.join(GENERATED_DIR, item)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)  # remove file or symlink
            elif os.path.isdir(path):
                shutil.rmtree(path)  # remove folder and its contents
        except Exception as e:
            print(f"❌ Failed to delete {path}: {e}")

    print(f"✅ Cleared contents of {GENERATED_DIR}")
