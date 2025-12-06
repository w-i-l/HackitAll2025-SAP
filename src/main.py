from api.client_api import ClientAPI
from server_api_models.round_update import RoundUpdate
from server_api_models.kit_purchasing_order import KitPurchasingOrder
from api.errors import *


if __name__ == "__main__":
    API_KEY = "7bcd6334-bc2e-4cbf-b9d4-61cb9e868869"
    wrapper = ClientAPI(api_key=API_KEY)

    session_id = wrapper.start_session()
    print(session_id)

    DAYS = 30
    HOURS = 24

    state_updates = None

    for day in range(DAYS):
        for hour in range(HOURS):
            print(f"Playing round for day {day}, hour {hour}...")

            round_updates = RoundUpdate(
                day=day,
                hour=hour,
                flight_loads=[],
                kit_purchasing_order=KitPurchasingOrder(
                    first_class=1000,
                    business_class=1000,
                    premium_economy_class=1000,
                    economy_class=1000,
                ),
            )

            result = wrapper.play_round(round_updates)
            print(f"RESULT: {result}")
            state_updates = (
                result if not isinstance(result, Exception) else state_updates
            )

    print("Stopping session...")
    print(state_updates)

    try:
        final_state = wrapper.stop_session()
        print(final_state)
    except NoActiveSessionError:
        print("No active session to stop.")
