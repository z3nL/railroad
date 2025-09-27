# db_api.py
# NOTE: these helpers assume plaintext passwords (test-only) and no RLS.
# If you enable RLS later, use a service role key here (server-only).

import os
from typing import Optional, TypedDict, Tuple, Dict, Any, List
from supabase import create_client, Client

# ---------- Supabase client ----------
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE = os.environ["SUPABASE_SERVICE_ROLE"]  # server-only secret
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# ---------- Types ----------
class AppUser(TypedDict):
    id: str
    email: str
    name: Optional[str]
    role: int

# ---------- Users ----------
def verify_user(email: str, password: str, role: int) -> Optional[AppUser]:
    """Lookup a user by email, plaintext password (test), and role."""
    res = (
        supabase.table("users")
        .select("id,email,name,role")
        .match({"email": email, "password": password, "role": role})
        .limit(1)
        .execute()
    )
    rows = res.data or []
    return rows[0] if rows else None

def create_account(email: str, password: str, name: str, role: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Insert a new user. Returns (user_dict, error)."""
    # Optional: uniqueness check (also add UNIQUE(email) in SQL)
    exists = supabase.table("users").select("id").eq("email", email).limit(1).execute()
    if exists.data:
        return None, "Email already registered"

    result = (
        supabase.table("users")
        .insert({"email": email, "password": password, "name": name, "role": role})
        .select("id,email,name,role,created_at")
        .execute()
    )
    if not result.data:
        return None, "Failed to create user"
    return result.data[0], None

# ---------- Lessons ----------
def get_lessons(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch lessons. If you later add owner scoping, filter with .eq('owner_id', user_id).
    """
    q = supabase.table("lessons").select(
        "lesson_id,created_at,lesson_name,lesson_descriptions,lesson_level"
    )
    # if user_id: q = q.eq("owner_id", user_id)
    return q.order("created_at", desc=True).execute().data or []

def get_steps(lesson_id: int) -> List[Dict[str, Any]]:
    """Fetch steps for a lesson, ordered by step_number ASC."""
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
    """
    Create ONLY the lesson row. Steps are added later by add_steps/add_step.
    Returns (lesson_dict, error).
    """
    insert_lesson = (
        supabase.table("lessons")
        .insert({
            "lesson_name": lesson_name,
            "lesson_descriptions": lesson_description,
            "lesson_level": lesson_level,
        })
        .select("lesson_id,created_at,lesson_name,lesson_descriptions,lesson_level")
        .execute()
    )
    if not insert_lesson.data:
        return None, "Failed to create lesson"
    return insert_lesson.data[0], None

# ---------- Steps (added after images are generated) ----------
def add_steps(
    lesson_id: int,
    steps: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Bulk-insert steps for an existing lesson.
    steps: [{ step_number:int, step_description:str, step_image?:str }]
    Returns (inserted_steps_sorted, error).
    """
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
        .select("lessons_id,step_number,step_image,step_description")
        .execute()
    )
    if getattr(res, "error", None):
        return [], res.error.message

    return sorted(res.data, key=lambda x: x["step_number"]), None

def add_step(
    lesson_id: int,
    step_number: int,
    step_description: str,
    step_image: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Insert a single step (useful as each image finishes).
    Returns (inserted_step, error).
    """
    res = (
        supabase.table("steps")
        .insert({
            "lessons_id": lesson_id,
            "step_number": int(step_number),
            "step_description": step_description,
            "step_image": step_image,
        })
        .select("lessons_id,step_number,step_image,step_description")
        .execute()
    )
    rows = res.data or []
    if getattr(res, "error", None):
        return None, res.error.message
    return (rows[0] if rows else None), None
