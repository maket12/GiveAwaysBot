from aiogram.fsm.state import State, StatesGroup


class NewGiveAway(StatesGroup):
    give_post_text = State()
    give_post_photo = State()
    give_post_prizes = State()
    give_amount_of_orders = State()
    give_post_finish_date = State()


class NewOrder(StatesGroup):
    give_customer = State()
    give_phone = State()
    give_fullname = State()
    give_amount = State()


class RejectingReason(StatesGroup):
    give_reason = State()


class DeleteCustomer(StatesGroup):
    give_phone = State()


class NewGiveawayDate(StatesGroup):
    give_new_date = State()
