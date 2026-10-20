from __future__ import annotations

from typing import Any


def identity_normalization_prompt(context: dict[str, Any]) -> str:
    return f"""
You normalize people identities for a meeting. Return ONLY a JSON object with this exact shape:
{{"items": [{{"action": "merge_alias", "target_email": "...", "alias": "...", "confidence": 0.95, "reason": "..."}}]}}
Never return a bare array. The top-level value must be an object with key "items".

Rules:
- Merge likely aliases aggressively when evidence supports same human.
- Email local-part is strong evidence. Ignore dots, hyphens, underscores, and numeric suffixes.
- Abbreviated local-parts count: janedoe2323 can mean t + addison and should merge with Jane Doe when meeting context supports it; jdoe can match John Doe.
- Transcript speaker names, Fireflies participants/host/organizer emails, existing aliases, and unknown task owners are all identity evidence.
- Prefer real emails over anonymous emails. If a real email appears later for an anonymous person, merge anonymous into real.
- Prefer @example.com emails as the primary owner email/name when the same human also has a non-Four-Reasons email.
- If a non-@example.com email matches the same human as a @example.com email, return email_alias with target_email=<@example.com email> and alias_email=<non-Four-Reasons email>. Do not make the external email primary.
- Fireflies emails are immutable identities: do not mutate their email string. Use alias/email-alias actions.
- Role labels are NOT people. Reject labels like listing owner, reporting owner, dashboard owner, reviewer access decision owner, account owner.
- If there is no real email but the text is a human name, create/keep an anonymous identity.
- Be high confidence (>=0.9) for clear initial+surname, first-name+domain/local-part, or repeated same-speaker evidence.

Allowed actions:
- merge_alias: target_email + alias
- email_alias: target_email + alias_email
- merge_anonymous_into_real: from_email + to_email
- create_anonymous: alias
- reject_role_label: alias
- review_required: alias

Context JSON:
{context}
""".strip()
