from wtforms import Form, TextField, IntegerField, validators


class ChainForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    chain_name = TextField('chain_name', [validators.Required()])
    method = TextField('method')


class DetailsForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    detail_value = TextField('detail_value', [validators.Required()])
    batch_delta = IntegerField('batch_delta')
    batch_count = IntegerField('batch_delta')


class FilterForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    chain_name = TextField('chain_name', [validators.Required()])
    filter_name = TextField('filter_name', [validators.Required()])
    method = TextField('method')
