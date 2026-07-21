from hashlib import sha256

from sqlalchemy.orm import Session
from backend.models.user import User


def get_or_create_guest_user(db: Session, anonymous_user_id: str) -> User:
    user = db.query(User).filter(User.auth0_subject == f"guest:{anonymous_user_id}").first()
    if user is not None:
        return user

    user = User(
        auth0_subject=f"guest:{anonymous_user_id}",
        name="Guest user",
        email=f"guest-{anonymous_user_id[:24]}@guest.local",
        password_hash=None,
        is_guest=True,
        guest_chat_count=0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_guest_user_by_anonymous_id(db: Session, anonymous_user_id: str) -> User | None:
    return (
        db.query(User)
        .filter(
            User.auth0_subject == f"guest:{anonymous_user_id}",
            User.is_guest.is_(True),
        )
        .first()
    )


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def _fallback_email(subject: str) -> str:
    digest = sha256(subject.encode("utf-8")).hexdigest()[:24]
    return f"auth0-{digest}@auth0.local"


def _claim_value(claims: dict, field: str):
    if field in claims:
        return claims[field]

    suffix = f"/{field}"
    for key, value in claims.items():
        if isinstance(key, str) and key.endswith(suffix):
            return value

    return None


def _clean_text(value, max_length: int):
    if value is None:
        return None

    cleaned = str(value).strip()
    return cleaned[:max_length] if cleaned else None


def _clean_age(value):
    if value in {None, ""}:
        return None

    try:
        age = int(value)
    except (TypeError, ValueError):
        return None

    return age if 0 <= age <= 150 else None


def _apply_profile(db: Session, user: User, profile: dict) -> bool:
    changed = False

    updates = {
        "name": _clean_text(profile.get("name") or profile.get("nickname"), 100),
        "email": _clean_text(profile.get("email"), 100),
        "phone": _clean_text(
            profile.get("phone") or profile.get("phone_number"),
            20,
        ),
        "age": _clean_age(profile.get("age")),
    }

    for field, value in updates.items():
        if field == "email" and value is not None:
            existing_user = db.query(User).filter(User.email == value, User.id != user.id).first()
            if existing_user is not None:
                continue

        if value is not None and getattr(user, field) != value:
            setattr(user, field, value)
            changed = True

    return changed


def get_or_create_auth0_user(db: Session, subject: str, claims: dict) -> User:
    user = db.query(User).filter(User.auth0_subject == subject).first()
    if user is not None:
        if _apply_profile(db, user, claims):
            db.commit()
            db.refresh(user)
        return user

    email = _clean_text(_claim_value(claims, "email"), 100) or _fallback_email(subject)
    user = db.query(User).filter(User.email == email).first()
    if user is not None:
        user.auth0_subject = subject
        user.is_guest = False
        _apply_profile(db, user, claims)
        db.commit()
        db.refresh(user)
        return user

    user = User(
        auth0_subject=subject,
        name=_clean_text(_claim_value(claims, "name") or _claim_value(claims, "nickname"), 100)
        or "Navikenz user",
        email=email,
        phone=_clean_text(_claim_value(claims, "phone") or _claim_value(claims, "phone_number"), 20),
        age=_clean_age(_claim_value(claims, "age")),
        password_hash=None,
        is_guest=False,
        guest_chat_count=0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
