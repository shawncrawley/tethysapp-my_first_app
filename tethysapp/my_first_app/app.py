from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.stores import PersistentStore


class MyFirstApp(TethysAppBase):
    """
    Tethys App Class for My First App.
    """

    name = 'My First App'
    index = 'my_first_app:home'
    icon = 'my_first_app/images/icon.gif'
    package = 'my_first_app'
    root_url = 'my-first-app'
    color = '#3498db'

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='my-first-app',
                           controller='my_first_app.controllers.home'
                           ),
                    UrlMap(name='map',
                           url='my-first-app/map',
                           controller='my_first_app.controllers.map'),
                    UrlMap(name='map_single',
                           url='my-first-app/map/{id}',
                           controller='my_first_app.controllers.map_single'),
                    UrlMap(name='echo_name',
                           url='my-first-app/echo-name',
                           controller='my_first_app.controllers.echo_name'),
                    )

        return url_maps

    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='stream_gage_db',
                                  initializer='my_first_app.init_stores.init_stream_gage_db',
                                  spatial=True
                                  ),
                  )

        return stores