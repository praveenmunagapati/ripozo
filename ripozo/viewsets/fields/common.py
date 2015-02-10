from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo.exceptions import ValidationException, TranslationException
from ripozo.viewsets.fields.base import BaseField

import six


class StringField(BaseField):
    """
    Used for casting and validating string fields.
    """
    field_type = six.string_types

    def __init__(self, name, max_length=None, min_length=None, regex=None, required=False):
        """
        A field class for validating string inputs.

        :param int max_length: The maximum length of the string
        :param int min_length: The minimum legnth of the string
        :param _sre.SRE_Pattern regex: A compiled regular expression that must
            match at least once.
        """
        super(StringField, self).__init__(name, required=required)
        self.max_length = max_length
        self.min_length = min_length
        self.regex = regex

    def translate(self, obj):
        """
        Attempts to convert the object to a string type

        :param object obj:
        :return: The object in its string representation
        :rtype: unicode
        :raises: TranslationsException
        """
        # A none input should be handled by the validator
        if obj is None:
            return obj

        obj = super(StringField, self).translate(obj)
        try:
            return six.text_type(obj)
        except ValueError:
            raise TranslationException('obj is not a valid unicode string: {0}'.format(obj))

    def validate(self, obj):
        """
        Validates the object.  It makes a call to super checking if the input
        can be None

        :param unicode obj:
        :return:
        :rtype: unicode
        :raises: ValidationException
        """
        obj = super(StringField, self).validate(obj)
        obj = self._validate_size(obj, len(obj))
        if not self.regex.match(obj):
            raise ValidationException('The input string did not match the'
                                      ' required regex: {0} != {1}'.format(obj, self.regex))

        # passed validation
        return obj


class IntegerField(BaseField):
    """
    A field used for translating and validating an integer input
    """
    field_type = int

    def translate(self, obj):
        # A none input should be handled by the validator
        if obj is None:
            return obj

        obj = super(IntegerField, self).translate(obj)
        try:
            return int(obj)
        except ValueError:
            raise TranslationException('Not a valid integer type: {0}'.format(obj))

    def validate(self, obj):
        obj = super(IntegerField, self).validate(obj)
        return self._validate_size(obj, obj)


class FloatField(IntegerField):
    """
    A field used for translating and validating a float input
    """

    def translate(self, obj):
        # A none input should be handled by the validator
        if obj is None:
            return obj

        obj = super(FloatField, self).translate(obj)
        try:
            return float(obj)
        except ValueError:
            raise TranslationException('obj is not castable to float: {0}'.format(obj))


class BooleanField(BaseField):
    """
    A field used for translating and validating a boolean input
    It can take either a boolean or a string.
    """

    def translate(self, obj):
        # A none input should be handled by the validator
        if obj is None:
            return obj

        if isinstance(obj, bool):
            return obj
        if isinstance(obj, six.string_types):
            if obj.lower() == 'false':
                return False
            elif obj.lower() == 'true':
                return True
        raise ValidationException('{0} is not a valid boolean.  Either'
                                  ' "true" or "false" is required (case insensitive)'.format(obj))