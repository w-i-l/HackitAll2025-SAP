class Penalty:
    def __init__(
        self,
        code: str,
        flight_id: str | None,
        flight_number: str | None,
        issued_day: int,
        issued_hour: int,
        penalty: float,
        reason: str,
    ) -> None:
        self.code = code
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.issued_day = issued_day
        self.issued_hour = issued_hour
        self.penalty = penalty
        self.reason = reason

    @classmethod
    def from_dict(cls, data: dict) -> "Penalty":
        return cls(
            code=data.get("code"),
            flight_id=data.get("flightId"),
            flight_number=data.get("flightNumber"),
            issued_day=data.get("issuedDay"),
            issued_hour=data.get("issuedHour"),
            penalty=data.get("penalty"),
            reason=data.get("reason"),
        )

    def __repr__(self):
        return f"Penalty(\n code={self.code},\n flight_id={self.flight_id},\n flight_number={self.flight_number},\n issued_day={self.issued_day},\n issued_hour={self.issued_hour},\n penalty={self.penalty},\n reason={self.reason}\n)"

    def __str__(self):
        return self.__repr__()
