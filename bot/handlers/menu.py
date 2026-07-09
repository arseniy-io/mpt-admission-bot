from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import (
    answer_keyboard,
    back_to_main_keyboard,
    links_keyboard,
    main_menu_keyboard,
    section_keyboard,
    specialties_keyboard,
    specialty_details_keyboard,
    specialty_keyboard,
)
from bot.messages import DORMITORY_TEXT, LINKS_TEXT, NOT_FOUND_TEXT, WELCOME_TEXT
from bot.services.content import ContentRepository, Specialty


router = Router()


async def _edit_or_answer(
    callback: CallbackQuery,
    text: str,
    reply_markup=None,
) -> None:
    if callback.message is None:
        return

    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(text, reply_markup=reply_markup)
        except TelegramBadRequest as exc:
            if "message is not modified" in str(exc).lower():
                return
            await callback.message.answer(text, reply_markup=reply_markup)


def _specialty_card(specialty: Specialty) -> str:
    return (
        f"{specialty.code} {specialty.title}\n\n"
        f"Срок обучения: {specialty.study_period}\n"
        f"Форма обучения: {specialty.study_form}\n"
        f"Количество мест: {specialty.places}\n"
        f"Бюджет: {specialty.budget}\n"
        f"Вступительное испытание: {specialty.entrance_exam}"
    )


@router.callback_query(F.data == "nav:main")
async def show_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await _edit_or_answer(callback, WELCOME_TEXT, main_menu_keyboard())


@router.callback_query(F.data.startswith("section:"))
async def show_section(
    callback: CallbackQuery,
    content: ContentRepository,
    state: FSMContext,
) -> None:
    await callback.answer()
    await state.clear()
    section_id = callback.data.split(":", 1)[1] if callback.data else ""

    if section_id == "specialties":
        await _edit_or_answer(
            callback,
            "Выберите специальность:",
            specialties_keyboard(content),
        )
        return

    if section_id == "dormitory":
        await _edit_or_answer(callback, DORMITORY_TEXT, back_to_main_keyboard())
        return

    if section_id == "links":
        await _edit_or_answer(callback, LINKS_TEXT, links_keyboard(content))
        return

    section = content.get_section(section_id)
    if section is None:
        await _edit_or_answer(callback, NOT_FOUND_TEXT, main_menu_keyboard())
        return

    await _edit_or_answer(callback, section.title, section_keyboard(section))


@router.callback_query(F.data.startswith("answer:"))
async def show_answer(
    callback: CallbackQuery,
    content: ContentRepository,
) -> None:
    await callback.answer()

    if not callback.data:
        await _edit_or_answer(callback, NOT_FOUND_TEXT, main_menu_keyboard())
        return

    _, section_id, item_id = callback.data.split(":", 2)
    item = content.get_item(section_id, item_id)
    if item is None:
        await _edit_or_answer(callback, NOT_FOUND_TEXT, main_menu_keyboard())
        return

    text = f"{item.question}\n\n{item.answer}"
    await _edit_or_answer(callback, text, answer_keyboard(section_id))


@router.callback_query(F.data.startswith("specialty:"))
async def show_specialty(
    callback: CallbackQuery,
    content: ContentRepository,
) -> None:
    await callback.answer()

    specialty_id = callback.data.split(":", 1)[1] if callback.data else ""
    specialty = content.get_specialty(specialty_id)
    if specialty is None:
        await _edit_or_answer(callback, NOT_FOUND_TEXT, main_menu_keyboard())
        return

    await _edit_or_answer(
        callback,
        _specialty_card(specialty),
        specialty_keyboard(specialty),
    )


@router.callback_query(F.data.startswith("specialty_details:"))
async def show_specialty_details(
    callback: CallbackQuery,
    content: ContentRepository,
) -> None:
    await callback.answer()

    specialty_id = callback.data.split(":", 1)[1] if callback.data else ""
    specialty = content.get_specialty(specialty_id)
    if specialty is None:
        await _edit_or_answer(callback, NOT_FOUND_TEXT, main_menu_keyboard())
        return

    await _edit_or_answer(
        callback,
        specialty.details,
        specialty_details_keyboard(specialty.id),
    )


@router.message()
async def fallback_message(message: Message) -> None:
    await message.answer(
        "Я работаю через кнопки. Нажмите /start или выберите раздел в меню.",
        reply_markup=main_menu_keyboard(),
    )
