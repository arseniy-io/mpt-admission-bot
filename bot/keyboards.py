from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.services.content import ContentRepository, Section, Specialty


MAIN_MENU_ITEMS = [
    ("🎓 Поступить в МПТ", "admission"),
    ("📄 Документы", "documents"),
    ("🏫 Специальности", "specialties"),
    ("📝 Вступительные испытания", "exams"),
    ("💰 Обучение", "education"),
    ("📅 Сроки приема", "deadlines"),
    ("🏠 Общежитие", "dormitory"),
    ("📍 Контакты", "contacts"),
    ("❓ Частые вопросы", "faq"),
    ("🔗 Полезные ссылки", "links"),
    ("✍️ Задать вопрос", "ask_question"),
]


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for title, section_id in MAIN_MENU_ITEMS:
        callback_data = (
            f"section:{section_id}" if section_id != "ask_question" else "ask:start"
        )
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1)
    return builder.as_markup()


def section_keyboard(section: Section) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in section.items:
        builder.button(
            text=item.question,
            callback_data=f"answer:{section.id}:{item.id}",
        )
    builder.button(text="🏠 Главное меню", callback_data="nav:main")
    builder.adjust(1)
    return builder.as_markup()


def answer_keyboard(section_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data=f"section:{section_id}")
    builder.button(text="🏠 Главное меню", callback_data="nav:main")
    builder.adjust(1)
    return builder.as_markup()


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="nav:main")
    builder.button(text="🏠 Главное меню", callback_data="nav:main")
    builder.adjust(1)
    return builder.as_markup()


def specialties_keyboard(content: ContentRepository) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for specialty in content.specialties.values():
        builder.button(
            text=f"{specialty.code} {specialty.title}",
            callback_data=f"specialty:{specialty.id}",
        )
    builder.button(text="🏠 Главное меню", callback_data="nav:main")
    builder.adjust(1)
    return builder.as_markup()


def specialty_keyboard(specialty: Specialty) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подробнее",
        callback_data=f"specialty_details:{specialty.id}",
    )
    builder.button(text="⬅️ Назад", callback_data="section:specialties")
    builder.button(text="🏠 Главное меню", callback_data="nav:main")
    builder.adjust(1)
    return builder.as_markup()


def specialty_details_keyboard(specialty_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data=f"specialty:{specialty_id}")
    builder.button(text="🏠 Главное меню", callback_data="nav:main")
    builder.adjust(1)
    return builder.as_markup()


def links_keyboard(content: ContentRepository) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for link in content.links:
        rows.append([InlineKeyboardButton(text=link.title, url=link.url)])

    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="nav:main")])
    rows.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
