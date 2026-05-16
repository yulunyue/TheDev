from .model import BaseModel


class SelectModel(BaseModel):
    model: "SelectModel"

    def set_options(self, *args, **kw):
        self.options: dict = {a: a for a in args}
        self.options.update(kw)
        return self

    def to_json(self):
        return super().to_json(
            type="select",
            children=[dict(title=v, value=key) for key, v in self.options.items()],
        )

    def get_data(self):
        return self.model.options[self.get_value()]
