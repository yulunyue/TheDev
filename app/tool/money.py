from common.tool.export import (
    TableConfig,
    StrModel,
    NumberModel,
    TableBase,
    FrontTable,
    DateModel,
)
from common.util.export import Node, enum_cls, time


class MoneyConfig(TableConfig):
    date = DateModel()
    money = NumberModel()
    user = StrModel()
    detail = StrModel()
    check = StrModel()


R: TableBase[MoneyConfig] = None


def get_r():
    global R
    if R is None:
        R = TableBase[MoneyConfig]().set_resource("money")
    return R


class Money:
    API_ROUTE = "/app/money"

    def add_record(
        self,
        date: str,
        money: str,
        user: enum_cls("yly", "xx", "yx"),
        detail: enum_cls("吃饭", "交通", "衣服", "其它"),
        check: str,
        **kw,
    ):
        db = get_r()
        r = db.insert()
        r.update(
            date=date,
            money=money,
            user=user["value"],
            detail=detail["value"],
            check=check,
        )
        db.save()
        return FrontTable().load_from_table(db)

    def query(self, **kw):
        return FrontTable().load_from_table(get_r())
