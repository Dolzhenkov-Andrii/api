'''Routs validations
'''


from exceptions.validate import ErrorForms
from validations.checking_db_fields import (
    valid_username_field,
    valid_pasword_field,
)


class Authorization:
    '''Authorization check
    '''
    validate_fields = {
        'username': str,
        'password': str,
        'remember_me': bool,
    }

    def __init__(self, **request_data):
        self.request_data = request_data


    def validate(self):
        '''Key verification
        '''
        for key in Authorization.validate_fields:  # pylint: disable=C0206
            if (key not in self.request_data
                    or isinstance(self.request_data[key],
                                  Authorization.validate_fields[key]) is False):
                raise ErrorForms
        try:
            validate_request_data = {
                'username': valid_username_field(self.request_data['username']),
                'password': valid_pasword_field(self.request_data['password']),
                'remember_me': self.request_data['remember_me']
            }
        except ErrorForms as error:
            raise error
        return validate_request_data
