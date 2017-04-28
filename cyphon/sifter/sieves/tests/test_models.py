# -*- coding: utf-8 -*-
# Copyright 2017 Dunbar Security Solutions, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
"""
Tests the Rules and RuleSet classes.
"""

# standard library
import logging
from unittest import TestCase

# third party
from django.core.exceptions import ValidationError

# local
from sifter.sieves.models import FieldRule


class FieldRuleTestCase(TestCase):
    """
    Tests the FieldRule class.
    """

    def setUp(self):
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_contains(self):
        """
        Tests the is_match method for a 'contains' regex pattern.
        """
        true_rule = FieldRule(
            field_name='subject',
            operator='CharField:x',
            value='critical'
        )
        false_rule = FieldRule(
            field_name='subject',
            operator='CharField:x',
            value='urgent'
        )
        data = {'subject': 'this is a critical alert'}
        self.assertTrue(true_rule.is_match(data))
        self.assertFalse(false_rule.is_match(data))

    def test_does_not_contain(self):
        """
        Tests the is_match method for a 'does not contain' regex pattern.
        """
        true_rule = FieldRule(
            field_name='subject',
            operator='CharField:^((?!x).)*$',
            value='critical'
        )
        false_rule = FieldRule(
            field_name='subject',
            operator='CharField:^((?!x).)*$',
            value='urgent'
        )
        data = {'subject': 'this is an urgent alert'}
        self.assertTrue(true_rule.is_match(data))
        self.assertFalse(false_rule.is_match(data))

    def test_begins_with(self):
        """
        Tests the is_match method for a 'begins with' regex pattern.
        """
        true_rule = FieldRule(
            field_name='subject',
            operator='CharField:^x',
            value='this'
        )
        false_rule = FieldRule(
            field_name='subject',
            operator='CharField:^x',
            value='critical'
        )
        data = {'subject': 'this is a critical alert'}
        self.assertTrue(true_rule.is_match(data))
        self.assertFalse(false_rule.is_match(data))

    def test_ends_with(self):
        """
        Tests the is_match method for an 'ends with' regex pattern.
        """
        true_rule = FieldRule(
            field_name='subject',
            operator='CharField:x$',
            value='alert'
        )
        false_rule = FieldRule(
            field_name='subject',
            operator='CharField:x$',
            value='critical'
        )
        data = {'subject': 'this is a critical alert'}
        self.assertTrue(true_rule.is_match(data))
        self.assertFalse(false_rule.is_match(data))

    def test_equals(self):
        """
        Tests the is_match method for an 'equals' regex pattern.
        """
        true_rule = FieldRule(
            field_name='subject',
            operator='CharField:^x$',
            value='this is a critical alert'
        )
        false_rule = FieldRule(
            field_name='subject',
            operator='CharField:^x$',
            value='critical'
        )
        data = {'subject': 'this is a critical alert'}
        self.assertTrue(true_rule.is_match(data))
        self.assertFalse(false_rule.is_match(data))

    def test_special_characters(self):
        """
        Tests the is_match method for a string that contains special characters.
        """
        true_rule = FieldRule(
            field_name='subject',
            operator='CharField:x$',
            value='.* [CRIT]'
        )
        false_rule = FieldRule(
            field_name='subject',
            operator='CharField:x',
            value='.*[CRIT]',
        )
        data = {'subject': '*this is a critical alert.* [CRIT]'}
        self.assertTrue(true_rule.is_match(data))
        self.assertFalse(false_rule.is_match(data))

    def test_is_null(self):
        """
        Tests the is_match method for 'is null'.
        """
        rule = FieldRule(
            field_name='subject',
            operator='EmptyField',
        )
        data = {'subject': 'this is a critical alert'}
        self.assertFalse(rule.is_match(data))

        data = {'subject': None}
        self.assertTrue(rule.is_match(data))

    def test_invalid_regex(self):
        """
        Tests the is_match method when the value is not a valid regex.
        """
        valid_rule = FieldRule(
            field_name='subject',
            operator='CharField:x$',
            is_regex=False,
            value='[CRIT-999]'
        )
        invalid_rule = FieldRule(
            field_name='subject',
            operator='CharField:x$',
            is_regex=True,
            value='[CRIT-999]'
        )
        try:
            valid_rule.clean()
        except ValidationError:
            self.fail('Rule raised ValidationError unexpectedly')
        with self.assertRaises(ValidationError):
            self.assertFalse(invalid_rule.clean())
