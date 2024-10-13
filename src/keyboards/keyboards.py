from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_rating_keyboard(project_id: int, similarity: float, response_time: float) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с оценками от 1 до 5 для оценки точности ответа.
    Передает project_id, similarity и response_time в callback_data.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1", callback_data=f"rate_1_{project_id}_{similarity}_{response_time}"),
                InlineKeyboardButton(text="2", callback_data=f"rate_2_{project_id}_{similarity}_{response_time}"),
                InlineKeyboardButton(text="3", callback_data=f"rate_3_{project_id}_{similarity}_{response_time}"),
                InlineKeyboardButton(text="4", callback_data=f"rate_4_{project_id}_{similarity}_{response_time}"),
                InlineKeyboardButton(text="5", callback_data=f"rate_5_{project_id}_{similarity}_{response_time}")
            ]
        ]
    )
    return keyboard


