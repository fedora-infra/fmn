from wtforms import Form, StringField, IntegerField, validators


class FilterForm(Form):
    filter_id = IntegerField('filter_id')
    openid = StringField('openid', [validators.InputRequired()])
    context = StringField('context', [validators.InputRequired()])
    filter_name = StringField('filter_name', [validators.InputRequired()])
    method = StringField('method')


class DetailsForm(Form):
    openid = StringField('openid', [validators.InputRequired()])
    context = StringField('context', [validators.InputRequired()])
    detail_value = StringField('detail_value')

    # We really want these to be integers, but I don't know how to allow that
    # to also be "None"
    batch_delta = StringField('batch_delta')
    batch_count = StringField('batch_delta')

    # Did they press the button?
    toggle_enable = StringField('toggle_enable')
    toggle_triggered_by = StringField('toggle_triggered_by')
    toggle_shorten = StringField('toggle_shorten')
    toggle_markup = StringField('toggle_markup')
    toggle_verbose = StringField('toggle_verbose')

    next_url = StringField('next_url')

    reset_to_defaults = StringField('reset_to_defaults')
    delete_all_filters = StringField('delete_all_filters')


class RuleForm(Form):
    openid = StringField('openid', [validators.InputRequired()])
    context = StringField('context', [validators.InputRequired()])
    filter_id = IntegerField('filter_id', [validators.InputRequired()])
    rule_name = StringField('rule_name', [validators.InputRequired()])
    rule_id = IntegerField('rule_id')
    method = StringField('method')


class ArgumentForm(Form):
    openid = StringField('openid', [validators.InputRequired()])
    context = StringField('context', [validators.InputRequired()])
    filter_id = IntegerField('filter_id', [validators.InputRequired()])
    rule_id = IntegerField('rule_id', [validators.InputRequired()])
    rule_name = StringField('rule_name', [validators.InputRequired()])
    key = StringField('key', [validators.InputRequired()])
    value = StringField('value', [validators.InputRequired()])
