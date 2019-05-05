"""
Custom widgets for forms.

"""

from django.forms import DateTimeInput


class BootstrapDateTimePickerInput(DateTimeInput):
    """
    A custom widget to support a JS datetime picker.
    Based on `this example`_.

    .. _this example: https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    
    """

    template_name = "widgets/bootstrap_datetimepicker.html"

    def get_context(self, name, value, attrs):
        datetimepicker_id = "datetimepicker_{name}".format(name=name)
        if attrs is None:
            attrs = dict()
        attrs["data-target"] = "#{id}".format(id=datetimepicker_id)
        attrs["class"] = "form-control datetimepicker-input"
        context = super().get_context(name, value, attrs)
        context["widget"]["datetimepicker_id"] = datetimepicker_id
        return context
