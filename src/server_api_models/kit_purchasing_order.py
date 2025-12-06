class KitPurchasingOrder:
    def __init__(
        self,
        first_class: int,
        business_class: int,
        premium_economy_class: int,
        economy_class: int,
    ) -> None:
        self.first_class = first_class
        self.business_class = business_class
        self.premium_economy_class = premium_economy_class
        self.economy_class = economy_class

    @classmethod
    def empty(cls) -> "KitPurchasingOrder":
        return cls(
            first_class=0, business_class=0, premium_economy_class=0, economy_class=0
        )

    def to_dict(self) -> dict:
        return {
            "first": self.first_class,
            "business": self.business_class,
            "premiumEconomy": self.premium_economy_class,
            "economy": self.economy_class,
        }

    def __repr__(self):
        return f"KitPurchasingOrder(\n first_class={self.first_class},\n business_class={self.business_class},\n premium_economy_class={self.premium_economy_class},\n economy_class={self.economy_class}\n)"

    def __str__(self):
        return self.__repr__()
