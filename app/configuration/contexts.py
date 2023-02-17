class GenericContextBase:
    def __init__(self, **kwargs):
        self.set_context(**kwargs)

    def set_context(self, **attrs):
        """Set attribute values in context.

        Args:
            attrs: dict of attribute names and values.
        """
        for name, value in attrs.items():
            setattr(self, name, value)
