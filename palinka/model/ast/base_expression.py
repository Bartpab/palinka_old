class BaseExpression:
    def as_(self, type):
        try:
            return self.as_expression().as_child(type)
        except:
            raise Exception(f"Cannot cast from {self.__class__.__name__} to {type.__name__}.")