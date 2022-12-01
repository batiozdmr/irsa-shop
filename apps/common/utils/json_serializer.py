from django.core.serializers.json import DjangoJSONEncoder
from prices import Money

MONEY_TYPE = "Money"


class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Money):
            return {"_type": MONEY_TYPE, "amount": obj.amount, "currency": obj.currency}
        return super().default(obj)
