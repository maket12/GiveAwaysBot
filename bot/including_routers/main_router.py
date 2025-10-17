from aiogram import Dispatcher
from bot.handlers.messages.start import router as start_router
from bot.handlers.reply_keyboard.new_giveaway import router as new_giveaway_router
from bot.handlers.states.giveaways_states import router as giveaways_states_router
from bot.handlers.reply_keyboard.new_order import router as new_order_router
from bot.handlers.states.order_states import router as order_states_router
from bot.handlers.inline_keyboard.participating_answers.answers_handlers import router as participating_answers_router
from bot.handlers.states.rejecting_reason import router as rejecting_reason_router
from bot.handlers.reply_keyboard.main_admin_actions.delete_customer import router as delete_customer_router
from bot.handlers.states.delete_customer_state import router as delete_customer_state_router
from bot.handlers.reply_keyboard.main_admin_actions.change_giveaway_date import router as change_giveaway_date_router
from bot.handlers.states.new_giveaway_date_state import router as new_date_router
from bot.handlers.inline_keyboard.choose_giveaway import router as choose_giveaway_router


def include_all_routers(dp: Dispatcher):
    routers_list = [start_router, new_giveaway_router, giveaways_states_router,
                    new_order_router, order_states_router, participating_answers_router,
                    rejecting_reason_router, delete_customer_router, delete_customer_state_router,
                    change_giveaway_date_router, new_date_router, choose_giveaway_router]
    for router in routers_list:
        dp.include_router(router)
