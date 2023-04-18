class NumsysException(Exception):
    def __init__(self):
        super().__init__()

class FullResidueSystemException(NumsysException):
    def __init__(self, value):
        super().__init__()
        self.value = value


class ExpansivityException(NumsysException):
    def __init__(self, value):
        super().__init__()
        self.value = value


class UnitConditionException(NumsysException):
    def __init__(self, value):
        super().__init__()
        self.value = value


class RegularityException(NumsysException):
    def __init__(self, value):
        super().__init__()
        self.value = value


class OptimizationFailed(NumsysException):
    def __init__(self, value):
        super().__init__()
        self.value = value


class SmartDecideTimeout(NumsysException):
    def __init__(self, value):
        super().__init__()
        self.value = value