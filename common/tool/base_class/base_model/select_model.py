from .model import BaseModel


class SelectModel(BaseModel):
    model: "SelectModel"

    def set_options(self, *args, **kw):
        self.options: dict = {a: a for a in args}
        self.options.update(kw)
        return self

    def to_json(self):
        return dict(
            type="select",
            key=self.key,
            childs=[dict(title=o, value=o) for o in self.options],
        )

    def get_data(self):
        return self.model.options[self.get_value()]
