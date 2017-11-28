from wtforms.validators import ValidationError


def validate(data, rules=None):
    if rules is None:
        assert type(data) is dict

        error_messages = None
        for name, field in data.items():
            validation = validate(field['data'], field['rules'])
            if not validation.validated:
                if error_messages is None:
                    error_messages = {name: validation.error_message}
                else:
                    error_messages[name] = validation.error_message

        return error_messages

    return Validator(data, rules)


class Validator(object):

    validated = False
    error_message = ''

    def __init__(self, data, rules):
        self.data = data
        self.rules = rules

        try:
            for rule in iter(self.rules):
                rule(self.data)
        except ValidationError as e:
            self.error_message = str(e)
        else:
            self.validated = True


class Rules(object):
    """验证规则"""
    class Required(object):
        def __init__(self, message='', data=None):
            self.message = message
            self.data = data

        def __call__(self, data):
            if self.data is None:
                rule = data is not None and data != str() and data != list()
            else:
                if type(data) is list:
                    rule = set(self.data) - set(data) != set(self.data)
                else:
                    rule = data in self.data

            if not rule:
                raise ValidationError(self.message)

    class Unique(object):
        def __init__(self, model, field, message='该内容已存在'):
            self.model = model
            self.field = field
            self.message = message

        def __call__(self, form, field):
            check = self.model.query.filter(self.field == field.data).first()
            if check:
                raise ValidationError(self.message)
