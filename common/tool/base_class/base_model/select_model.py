from .model import BaseModel


class SelectModel(BaseModel):
    def set_options(self, *args):
        self.options = list(args)
        return self

    def to_json(self):
        return dict(
            type="select",
            key=self.key,
            childs=[dict(title=o, value=o) for o in self.options],
        )
