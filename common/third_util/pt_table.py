from prettytable import PrettyTable


class PtTable:
    def __init__(self):
        pass

    def load_form_dict(self):
        pass

    def load_from_matrix(self, matrix, titles=None):
        self.pr = PrettyTable(titles)
        for m in matrix:
            self.pr.add_row(m)
        return self

    def __str__(self):
        return f"-------\n{self.pr}\n"
