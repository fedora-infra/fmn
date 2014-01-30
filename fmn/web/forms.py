from wtforms import Form, TextField, IntegerField, validators


class FilterForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    filter_name = TextField('filter_name', [validators.Required()])
    method = TextField('method')


class DetailsForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    detail_value = TextField('detail_value')

    # We really want these to be integers, but I don't know how to allow that
    # to also be "None"
    batch_delta = TextField('batch_delta')
    batch_count = TextField('batch_delta')

    # Did they press the button?
    toggle_enable = TextField('toggle_enable')

    next_url = TextField('next_url')


class RuleForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    filter_id = IntegerField('filter_id', [validators.Required()])
    rule_name = TextField('rule_name', [validators.Required()])
    method = TextField('method')
