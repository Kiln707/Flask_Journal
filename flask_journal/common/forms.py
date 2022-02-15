from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, SelectMultipleField


class BaseForm(FlaskForm):
    """Base form"""
    def __init__(self, *args, accept_charset=None, action=None, autocomplete=None,
                enctype=None, method=None, name=None, novalidate=None,
                rel=None, target=None, **kwargs ):
        super().__init__(*args, **kwargs)
        self.accept_charset = accept_charset
        self.action = action
        self.autocomplete = autocomplete
        self.enctype = enctype
        self.method = method
        self.name = name
        self.novalidate = novalidate
        self.rel = rel
        self.target = target


class EditCategoryForm(BaseForm):
    name = StringField("Category Name")
    description = StringField("Category Description")
    parent_id = SelectField("Parent Category", choices=[])
    submit = SubmitField("Submit")

    def __init__(self, category, categories, *args, method="POST", **kwargs):
        super(EditCategoryForm, self).__init__(*args, method=method, obj=category, **kwargs)
        parent_category_choices = [(None, "-----")]
        parent_category_choices.extend([(cat.id, cat.name) for cat in categories if cat.parent is None])


class PostEditorForm(BaseForm):
    title = StringField("Title:")
    summary = StringField("Summary:")
    categories = SelectMultipleField("Categories:")
    # content = WysiwygField("Content: ") TODO: Add the WYSIWYG Editor
    submit = SubmitField("Save")

    def __init__(self, post, categories, *args, method="POST", **kwargs):
        super().__init__(*args, method=method, obj=post, **kwargs)
        self.categories.choices = [(str(cat.id), cat.name) for cat in categories if cat.parent is not None]
        if 'categories' not in

    def populate_obj(self, post, datastore):
        for name, field in self._fields.items():
            if name == 'categories':
                new_categories = []
                for cat_id in field.data:
                    category = datastore.get_category(int(cat_id))
                    new_categories.append(category)
                post.categories = new_categories
            else:
                field.populate_obj(post, name)


class SeriesEditorForm(BaseForm):
    title = StringField("Title:")
    summary = StringField("Summary:")
    categories = SelectMultipleField("Categories: ", choices=self.get_categories())
    posts = SelectMultipleField("Posts: ", choices=self.get_posts(series))
    # content = WysiwygField("Content: ") # TODO Add WYSIWYG editor
    submit = SubmitField("Save")

    def __init__(self, *args, method="POST", **kwargs):
        super().__init__(*args, method=method, **kwargs)

    def populate_obj(self, series, datastore):
        for name, field in self._fields.items():
            if name == 'categories':
                new_categories = []
                for cat_id in field.data:
                    category = datastore.get_category(int(cat_id))
                    new_categories.append(category)
                series.categories = new_categories
            elif name == 'posts':
                posts = []
                for post_id in field.data:
                    post = datastore.get_post(int(post_id))
                    append = True
                    for sp in series.posts:
                        if sp.post is post:
                            append = False
                            break
                    if append:
                        datastore.add_post_to_series(series=series, post=post)
                    posts.append(post)
                for sp in series.posts:
                    if sp.post not in posts:
                        datastore.remove_post_from_series(sp)
            else:
                field.populate_obj(series, name)


