import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.config import Settings
from bot.keyboards import back_to_main_keyboard, main_menu_keyboard
from bot.messages import ASK_QUESTION_TEXT, QUESTION_NOT_SENT_TEXT, QUESTION_SENT_TEXT


router = Router()
logger = logging.getLogger(__name__)


class AskQuestion(StatesGroup):
    waiting_for_question = State()


@router.callback_query(F.data == "ask:start")
async def ask_question_start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(AskQuestion.waiting_for_question)

    if callback.message:
        await callback.message.edit_text(
            ASK_QUESTION_TEXT,
            reply_markup=back_to_main_keyboard(),
        )


@router.message(AskQuestion.waiting_for_question)
async def receive_question(
    message: Message,
    state: FSMContext,
    bot: Bot,
    settings: Settings,
) -> None:
    await state.clear()

    if settings.admin_ids:
        for admin_id in settings.admin_ids:
            await bot.send_message(
                admin_id,
                _format_admin_question(message),
            )
            await message.forward(admin_id)
        await message.answer(QUESTION_SENT_TEXT, reply_markup=main_menu_keyboard())
        return

    logger.warning("ADMIN_IDS не заданы. Вопрос пользователя не отправлен.")
    await message.answer(QUESTION_NOT_SENT_TEXT, reply_markup=main_menu_keyboard())


def _format_admin_question(message: Message) -> str:
    user = message.from_user
    if user is None:
        return "Новый вопрос от пользователя Telegram:"

    username = f"@{user.username}" if user.username else "username не указан"
    return (
        "Новый вопрос для приемной комиссии\n\n"
        f"Пользователь: {user.full_name}\n"
        f"Username: {username}\n"
        f"Telegram ID: {user.id}"
    )
