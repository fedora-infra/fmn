from wtforms import Form, TextField, IntegerField, validators


class FilterForm(Form):
    filter_id = IntegerField('filter_id')
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
    toggle_triggered_by = TextField('toggle_triggered_by')
    toggle_shorten = TextField('toggle_shorten')
    toggle_markup = TextField('toggle_markup')
    toggle_verbose = TextField('toggle_verbose')

    next_url = TextField('next_url')

    reset_to_defaults = TextField('reset_to_defaults')
    delete_all_filters = TextField('delete_all_filters')


class RuleForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    filter_id = IntegerField('filter_id', [validators.Required()])
    rule_name = TextField('rule_name', [validators.Required()])
    method = TextField('method')


class ArgumentForm(Form):
    openid = TextField('openid', [validators.Required()])
    context = TextField('context', [validators.Required()])
    filter_id = IntegerField('filter_id', [validators.Required()])
    rule_name = TextField('rule_name', [validators.Required()])
    key = TextField('key', [validators.Required()])
    value = TextField('value', [validators.Required()])
