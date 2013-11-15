from wtforms import Form, TextField, validators


class NewChainForm(Form):
    username = TextField('username', [validators.Required()])
    context = TextField('context', [validators.Required()])
    chain_name = TextField('chain_name', [validators.Required()])


class DetailsForm(Form):
    username = TextField('username', [validators.Required()])
    context = TextField('context', [validators.Required()])
    detail_value = TextField('detail_value', [validators.Required()])


class NewFilterForm(Form):
    username = TextField('username', [validators.Required()])
    context = TextField('context', [validators.Required()])
    chain_name = TextField('chain_name', [validators.Required()])
    filter_name = TextField('filter_name', [validators.Required()])
    method = TextField('method')
