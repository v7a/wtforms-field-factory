# wtforms field factory
Create fields on-the-fly at form construction time.

## Why?
In order to e.g. translate field labels depending on the request without relying on global state.
Additionally, you can conditionally exclude fields. This avoids dodgy workarounds needed when e.g.
having a form field that is not relevant or feasible to pass during unit testing.

## How?
Let's look at a use case where a field label must change depending on the locale(s) of the request:
```python
from gettext import translation
from typing import List
from wtforms_field_factory import field, Form, DefaultMeta
from wtforms import StringField

class MyMeta(DefaultMeta):
    def __init__(self, ordered_locales: List[str]):
        self.ordered_locales = ordered_locales

    @property
    def locales(self):
        # translate messages within wtforms depending on the request's locale(s)
        return self.ordered_locales

class MyBaseForm(Form):
    def __init__(self, ordered_locales: List[str], **kwargs):
        self.ordered_locales = ordered_locales
        super().__init__(meta=MyMeta(ordered_locales), **kwargs)

    @field(name="name")
    def name_field(self):
        _ = translation("default", languages=self.ordered_locales)
        return StringField(label=_("Name"))
```
The example above will not only translate the name field's label but also internal wtforms messages
such as field errors.

In cases where an external function is responsible for creating the field (useful for reusing field
factories) or if you want to precompute certain objects (e.g. the GNUTranslations object), the
following can be done:

```python
@field(name="name")
def name_field(_cls, _):  # since the associated attribute is bound, we need the class type as first arg
    return StringField(label=_("Name"))

class MyBaseForm(Form):
    some_class_attribute = name_field # to make Form actually discover this factory

    def __init__(self, ordered_locales: List[str], **kwargs):
        self.set_factory_args(translation("default", languages=self.ordered_locales))
        super().__init__(meta=MyMeta(ordered_locales), **kwargs)
```
Just use whatever method you find best. There is not "one" correct way of achieving your goal here.
The important part is that you now have an explicit contract and do not rely on global state.


## Contributing
Before comitting, run the following and check if it succeeds:
```sh
pip install --user -r requirements-dev.txt && \
black wtforms_field_factory.py && \
pylint wtforms_field_factory.py && \
pytest && \
coverage report --fail-under=100
```
