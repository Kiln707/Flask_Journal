from flask import Blueprint, url_for


class BlogBlueprint(Blueprint):
    def __init__(self, app, datastore, blog_name, templates_folder='blog', name='Blog',
                 static_folder='static', url_prefix='/blog', use_blog_name_for_templates=False):
        self.app = app
        self.datastore = datastore
        self.blog_name = blog_name
        self.templates = blog_name if use_blog_name_for_templates else templates_folder
        self.admin_templates = self.templates + '/admin'
        super(BlogBlueprint, self).__init__(name=name,
                                            import_name=__name__,
                                            static_folder=static_folder,
                                            template_folder=self.templates,
                                            url_prefix=url_prefix,
                                            url_defaults={'url_for_blog': self.url_for_blog})
        self.add_app_template_global(self.datastore, name='datastore')

    def initialize(self):
        self.app.register_blueprint(self)

    def url_for_blog(self, endpoint, **values):
        return url_for("%s.%s" %(self.name, endpoint), **values)
