class FullResidueSystemException(Exception):
    def __init__(self, value):
        self.value = value


class ExpansivityException(Exception):
    def __init__(self, value):
        self.value = value


class UnitConditionException(Exception):
    def __init__(self, value):
        self.value = value


class RegularityException(Exception):
    def __init__(self, value):
        self.value = value


class OptimizationFailed(Exception):
    def __init__(self, value):
        self.value = value


class SmartDecideTimeout(Exception):
    def __init__(self, value):
        self.value = value