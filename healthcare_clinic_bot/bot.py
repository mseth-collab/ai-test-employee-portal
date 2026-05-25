"""
Healthcare Clinic Bot - Core logic
Handles intents: greeting, hours, location, appointments, services, emergency, help.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

# Clinic info (customize for your clinic)
CLINIC_NAME = "Sunrise Family Health"
CLINIC_HOURS = "Monday–Friday 8:00 AM–6:00 PM, Saturday 9:00 AM–1:00 PM. Closed Sundays."
CLINIC_ADDRESS = "123 Wellness Way, Suite 100"
CLINIC_PHONE = "(555) 123-4567"
SERVICES = (
    "General checkups, vaccinations, minor procedures, lab work, "
    "chronic care management, and same-day sick visits."
)


@dataclass
class Session:
    """Per-user session state for multi-turn flows (e.g. booking)."""
    name: Optional[str] = None
    appointment_reason: Optional[str] = None
    preferred_day: Optional[str] = None
    step: str = "idle"  # idle | booking_name | booking_reason | booking_day | done


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _match_keywords(text: str, *keyword_lists: list[str]) -> bool:
    t = _normalize(text)
    for keywords in keyword_lists:
        if any(kw in t for kw in keywords):
            return True
    return False


def handle_message(message: str, session: Session) -> tuple[str, Session]:
    """
    Process one user message and return (reply, updated_session).
    """
    msg = _normalize(message)

    # Appointment booking flow (stateful)
    if session.step == "booking_name":
        session.name = message.strip() or "Patient"
        session.step = "booking_reason"
        return (
            f"Thanks, {session.name}. What would you like to see the doctor for? (e.g. checkup, sick visit)",
            session,
        )
    if session.step == "booking_reason":
        session.appointment_reason = message.strip() or "general visit"
        session.step = "booking_day"
        return (
            "Which day works best for you? (e.g. Monday, this week)",
            session,
        )
    if session.step == "booking_day":
        session.preferred_day = message.strip() or "soon"
        session.step = "idle"
        session.name = None
        session.appointment_reason = None
        session.preferred_day = None
        return (
            "Your appointment request has been noted. Our front desk will call you to confirm time and availability. "
            f"For immediate help, call us at {CLINIC_PHONE}.",
            session,
        )

    # Intents
    if _match_keywords(message, ["hi", "hello", "hey", "good morning", "good afternoon"]):
        return (
            f"Hello! Welcome to {CLINIC_NAME}. I can help with appointments, hours, location, and services. How can I help you today?",
            session,
        )

    if _match_keywords(message, ["hour", "open", "close", "when are you"]):
        return (
            f"Our hours are: {CLINIC_HOURS}.",
            session,
        )

    if _match_keywords(message, ["address", "location", "where", "directions"]):
        return (
            f"We're located at {CLINIC_ADDRESS}. Need directions or parking info?",
            session,
        )

    if _match_keywords(message, ["phone", "call", "number", "contact"]):
        return (
            f"You can reach us at {CLINIC_PHONE}.",
            session,
        )

    if _match_keywords(message, ["service", "offer", "do you do", "what kind", "treatment"]):
        return (
            f"We offer: {SERVICES}",
            session,
        )

    if _match_keywords(message, ["appointment", "book", "schedule", "see a doctor", "come in"]):
        session.step = "booking_name"
        return (
            "I can help you request an appointment. What's your name?",
            session,
        )

    if _match_keywords(message, ["cancel", "reschedule"]):
        return (
            f"To cancel or reschedule, please call us at {CLINIC_PHONE} and we’ll assist you.",
            session,
        )

    if _match_keywords(message, ["emergency", "urgent", "chest pain", "can't breathe", "severe"]):
        return (
            "If this is a medical emergency, please call 911 or go to your nearest emergency room. "
            f"For non-life-threatening urgent issues, call us at {CLINIC_PHONE}.",
            session,
        )

    if _match_keywords(message, ["help", "what can you", "options"]):
        return (
            "I can help you with: **appointments** (book or cancel), **hours**, **location**, **phone**, **services**, and **emergency** guidance. What do you need?",
            session,
        )

    # Default
    return (
        "I'm not sure I understood. You can ask about appointments, hours, location, phone, services, or say 'help' for options.",
        session,
    )
