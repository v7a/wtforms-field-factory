"""Test the form class."""

import pytest

from wtforms import StringField
from wtforms_field_factory import field, Form


def test_factory_collection():
    class TestForm(Form):
        @field(name="test")
        def test_field(self):
            return StringField(label="test")

        @field(name="test2")
        def test2_field(self):
            return StringField(label="test2")

    form = TestForm()
    assert form.test.label.text == "test"
    assert form.test2.label.text == "test2"


def test_factory_arguments():
    class TestForm(Form):
        def __init__(self, arg: str, **kwargs):
            self.set_factory_args(arg)
            super().__init__(**kwargs)

        @field(name="test")
        def test_field(self, arg: str):
            return StringField(label=arg)

    assert TestForm("test1").test.label.text == "test1"
    assert TestForm("test2").test.label.text == "test2"


def test_classmethod_argument():
    class TestForm(Form):
        @classmethod
        @field(name="test")
        def test_field(cls):
            return StringField(cls.__name__)

    assert TestForm().test.label.text == TestForm.__name__


def test_instancemethod_argument():
    class TestForm(Form):
        def __init__(self, **kwargs):
            self.arg = "test"
            super().__init__(**kwargs)

        @field(name="test")
        def test_field(self):
            return StringField(self.arg)

    assert TestForm().test.label.text == "test"


def test_disabled_field():
    class TestForm(Form):
        enabled = False

        def __init__(self, arg, **kwargs):
            self.arg = arg
            super().__init__(**kwargs)

        @field(name="test", enable_if=lambda self: self.arg)
        def test_field(self):
            return StringField()

        @classmethod
        @field(name="test2", enable_if=lambda cls: cls.enabled)
        def test2_field(cls):
            return StringField()

    with pytest.raises(AttributeError):
        TestForm(False).test

    with pytest.raises(AttributeError):
        TestForm(True).test2  # dependent on class attribute

    TestForm(True).test  # should not raise
