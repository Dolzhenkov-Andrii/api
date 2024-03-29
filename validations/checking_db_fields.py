''' User date chek
'''
from dateutil import parser
from email_validator import validate_email
from validations.string_valid import valid_string_size_and_characters, valid_string_size
from exceptions.validate import (
    InvalidString,
    InvalidEmail,
    InvalidDate,
    ParserError,
    EmailNotValidError,
    InvalidType,
    InvalidKey
    )
from config.config import (
    VALID_MAX_SIZE_PASSWORD,
    VALID_MAX_SIZE_PHONE,
    VALID_MAX_SIZE_SURNAME,
    VALID_MIN_SIZE_PASSWORD,
    VALID_MIN_SIZE_PHONE,
    VALID_MIN_SIZE_SURNAME,
    VALID_MIN_SIZE_USERNAME,
    VALID_MAX_SIZE_USERNAME,
    VALID_MIN_SIZE_NAME,
    VALID_MAX_SIZE_NAME,
    VALID_PHONE_CHARACTERS,
    VALID_SURNAME_CHARACTERS,
    VALID_USERNAME_CHARACTERS,
    VALID_NAME_CHARACTERS,
)


def valid_username_field(username):
    '''
        Checking the username for correctness
        username: str
        valid_username: str
        Return verified valid_username
        Otherwise it will return an error
    '''

    try:
        valid_username = valid_string_size_and_characters(
            string=username,
            min_size=VALID_MIN_SIZE_USERNAME,
            max_size=VALID_MAX_SIZE_USERNAME,
            characters=VALID_USERNAME_CHARACTERS
        )
    except InvalidString as error:
        error.message = f'Error from username ({error.message})'
        raise error

    return valid_username


def valid_name_field(name):
    '''
        Checking the name for correctness
        name: str
        valid_name: str
        Return verified valid_name
        Otherwise it will return an error
    '''

    try:
        valid_name = valid_string_size_and_characters(
            string=name,
            min_size=VALID_MIN_SIZE_NAME,
            max_size=VALID_MAX_SIZE_NAME,
            characters=VALID_NAME_CHARACTERS
        )
    except InvalidString as error:
        error.message = f'Error from name ({error.message})'
        raise error

    return valid_name


def valid_surname_field(surname):
    '''
        Checking the surname for correctness
        surname: str
        valid_surname: str
        Return verified valid_surname
        Otherwise it will return an error
    '''

    try:
        valid_surname = valid_string_size_and_characters(
            string=surname,
            min_size=VALID_MIN_SIZE_SURNAME,
            max_size=VALID_MAX_SIZE_SURNAME,
            characters=VALID_SURNAME_CHARACTERS
        )
    except InvalidString as error:
        error.message = f'Error from surname ({error.message})'
        raise error

    return valid_surname


def valid_pasword_field(pasword):
    '''
        Checking the pasword for correctness
        pasword: str
        valid_pasword: str
        Return verified valid_pasword
        Otherwise it will return an error
    '''

    try:
        valid_pasword = valid_string_size(
            string=pasword,
            min_size=VALID_MIN_SIZE_PASSWORD,
            max_size=VALID_MAX_SIZE_PASSWORD,
        )
    except InvalidString as error:
        error.message = f'Error from password ({error.message})'
        raise error

    return valid_pasword


def valid_phone_field(phone):
    '''
        Checking the phone for correctness
        phone: str
        valid_phone: str
        Return verified valid_phone
        Otherwise it will return an error
    '''

    try:
        valid_phone = valid_string_size_and_characters(
            string=phone[1:],
            min_size=VALID_MIN_SIZE_PHONE,
            max_size=VALID_MAX_SIZE_PHONE,
            characters=VALID_PHONE_CHARACTERS,
        )
    except InvalidString as error:
        error.message = f'Error from phone ({error.message})'
        raise error

    return f'+{valid_phone}'


def valid_email_field(email):
    '''
        Checking the email for correctness
        email: str
        valid_email: str
        Return verified valid_email
        Otherwise it will return an error
    '''
    if isinstance(email, str) is False:
        raise InvalidType

    try:
        valid_email = validate_email(email).email
    except EmailNotValidError as error:
        InvalidEmail.message = error.args[0]
        raise InvalidEmail from error

    return valid_email


def valid_birthday_field(birthday):
    '''
        Checking the name for correctness
        birthday: str
        valid_birthday: dtae
        Return verified valid_birthday
        Otherwise it will return an error
    '''
    if isinstance(birthday, str) is False:
        raise InvalidType

    try:
        valid_birthday = parser.parse(birthday)
    except ParserError as error:
        raise InvalidDate from error

    return valid_birthday


def valid_field(data, key):
    """validate data from key"""

    if key == 'name':
        return valid_name_field(data)
    elif key == 'surname':
        return valid_surname_field(data)
    elif key == 'birthday':
        return valid_birthday_field(data)
    elif key == 'phone':
        return valid_phone_field(data)
    else:
        raise InvalidKey
