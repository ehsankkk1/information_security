
# import re

# class Unique(object):

#     def __init__(self, instance=None, field=None, message=None):
#         self.instance = instance
#         self.field = field
#         self.message = message

#     def __call__(self, form, field):
#         if self.instance.query.filter(self.field == field.data).first():
#             if not self.message:
#                 self.message = '{} already exists.'.format(field.name)
#             # raise ValidationError(self.message)


# class StrongNames(object):

#     def __init__(self, message=None):
#         self.message = message
#         if not self.message:
#             self.message = "Field contains only alphabet."

#     def __call__(self, form, field):
#         if not re.match("^[a-zA-Z]+$", field.data):
#             # raise ValidationError(self.message)

# class CorrectPhoneNumber(object):

#     def __init__(self, message=None):
#         self.message = message
#         if not self.message:
#             self.message = "Enter Valid Phone Number."

#     def __call__(self, form, field):
#         regex = "^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
#         if not re.match(regex, field.data):
#             # raise ValidationError(self.message)

# class StrongUsername(object):

#     def __init__(self, message=None):
#         self.message = message
#         if not self.message:
#             self.message = "Username contain only (A-Za-z0-9_-.) characters."

#     def __call__(self, form, field):
#         username = field.data
#         if not re.match("^[a-zA-Z0-9_.-]+$", username):
#             # raise ValidationError(self.message)


# class StrongPassword(object):

#     def __init__(self, message=None):
#         self.message = message
#         if not self.message:
#             self.message = "Please choose a strong password."

#     def __call__(self, form, field):
#         password = field.data
#         # if not re.match(r"(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", password):
#         #     raise ValidationError(self.message)