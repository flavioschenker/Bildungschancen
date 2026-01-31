import ulid


def generate_id(prefix: str | None = None) -> str:
    uid = ulid.new().str.lower()
    if prefix:
        return f"{prefix}_{uid[:16]}"
    return uid
