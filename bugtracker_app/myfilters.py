from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addattrs')
def addattrs(value, args):
    if args is None:
        return value.as_widget()
    arg_list = [arg.strip() for arg in args.split(',')]
    attrs = {arg.split('=')[0]:arg.split('=')[1] for arg in arg_list}   
    return value.as_widget(attrs=attrs)

@register.filter(name='css_by_issue_status')
def css_by_issue_status(issue_status):
    css_class = 'default'
    if issue_status == 'отклонена':
        css_class = 'danger'
    elif issue_status == 'в работе':
        css_class = 'warning'
    elif issue_status == 'новая':
        css_class = 'info'
    elif issue_status == 'решена':
        css_class = 'success'
    return css_class
