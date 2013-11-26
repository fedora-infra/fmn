from wtforms import Form, TextField, IntegerField, validators


class ChainForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    filter_name = TextField('filter_name', [validators.Required()])
    method = TextField('method')


class DetailsForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    detail_value = TextField('detail_value', [validators.Required()])

    # We really want these to be integers, but I don't know how to allow that
    # to also be "None"
    batch_delta = TextField('batch_delta')
    batch_count = TextField('batch_delta')


class RuleForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    filter_name = TextField('filter_name', [validators.Required()])
    rule_name = TextField('rule_name', [validators.Required()])
    method = TextField('method')
