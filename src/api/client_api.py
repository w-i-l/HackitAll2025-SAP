import urllib.request
import urllib.error
import json
import traceback

from api.errors import *
from server_api_models.penalty import Penalty
from server_api_models.flight_update import FlightUpdate
from server_api_models.state_update import StateUpdate
from server_api_models.round_update import RoundUpdate


class ClientAPI:
    def __init__(self, api_key: str) -> Exception | dict:
        self.base_url = "http://localhost:8080/api/"
        self.api_key = api_key
        self.session_id = None

    def start_session(self) -> Exception | str:
        endpoint = "v1/session/start"
        url = self.base_url + endpoint

        headers = {"API-KEY": self.api_key, "Content-Type": "application/json"}

        try:
            req = urllib.request.Request(url, headers=headers, method="POST")
            with urllib.request.urlopen(req) as response:
                session_id = response.read().decode("utf-8")
                self.session_id = session_id
                return session_id

        except urllib.error.HTTPError as e:
            if e.code == 409:
                return SessionAlreadyStartedError()

            return APIError(e.code, e.read().decode("utf-8"))

        except Exception as e:
            traceback.print_exc()
            return APIError(-1, str(e))

    def stop_session(self) -> Exception | StateUpdate:
        endpoint = "v1/session/end"
        url = self.base_url + endpoint

        headers = {"API-KEY": self.api_key, "Content-Type": "application/json"}

        try:
            req = urllib.request.Request(url, headers=headers, method="POST")
            with urllib.request.urlopen(req) as response:
                result = response.read().decode("utf-8")
                result = json.loads(result)

                day = result.get("day", 0) or 0
                hour = result.get("hour", 0) or 0

                penalties = result.get("penalties", []) or []
                penalties = [Penalty.from_dict(penalty) for penalty in penalties]

                flight_updates = result.get("flightUpdates", []) or []
                flight_updates = [
                    FlightUpdate.from_dict(update) for update in flight_updates
                ]

                total_cost = result.get("totalCost", 0.0) or 0.0

                state_update = StateUpdate(
                    day=day,
                    hour=hour,
                    penalties=penalties,
                    flight_updates=flight_updates,
                    total_cost=total_cost,
                )

                return state_update

        except urllib.error.HTTPError as e:
            if e.code == 404:
                return NoActiveSessionError()

            return APIError(e.code, e.read().decode("utf-8"))

        except Exception as e:
            traceback.print_exc()
            return APIError(-1, str(e))

    def play_round(self, update: RoundUpdate) -> Exception | StateUpdate:
        endpoint = "v1/play/round"
        url = self.base_url + endpoint

        if self.session_id is None:
            return NoActiveSessionError()

        headers = {
            "API-KEY": self.api_key,
            "SESSION-ID": self.session_id,
            "Content-Type": "application/json",
        }

        try:
            data = json.dumps(update.to_dict()).encode("utf-8")
            print(data)
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(req) as response:
                result = response.read().decode("utf-8")
                result = json.loads(result)

                day = result.get("day", 0) or 0
                hour = result.get("hour", 0) or 0

                penalties = result.get("penalties", []) or []
                penalties = [Penalty.from_dict(penalty) for penalty in penalties]

                flight_updates = result.get("flightUpdates", []) or []
                flight_updates = [
                    FlightUpdate.from_dict(update) for update in flight_updates
                ]

                total_cost = result.get("totalCost", 0.0) or 0.0

                state_update = StateUpdate(
                    day=day,
                    hour=hour,
                    penalties=penalties,
                    flight_updates=flight_updates,
                    total_cost=total_cost,
                )

                return state_update

        except urllib.error.HTTPError as e:
            if e.code == 400:
                return SessionAlreadyEndedError()

            return APIError(e.code, e.read().decode("utf-8"))

        except Exception as e:
            traceback.print_exc()
            return APIError(-1, str(e))
