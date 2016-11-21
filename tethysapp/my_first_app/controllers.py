from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .model import SessionMaker, StreamGage
from tethys_gizmos.gizmo_options import MapView, MVLayer, MVView
from tethys_gizmos.gizmo_options import TextInput


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'my_first_app/home.html', context)


def map(request):
    """
    Controller for map page.
    """
    # Create a session
    session = SessionMaker()

    # Query DB for gage objects
    gages = session.query(StreamGage).all()

    # Close the session (open connection to the database) sicne it will no longer be used
    session.close()

    # Transform into GeoJSON format
    features = []

    for gage in gages:
        gage_feature = {
          'type': 'Feature',
          'geometry': {
            'type': 'Point',
            'coordinates': [gage.longitude, gage.latitude]
          }
        }

        features.append(gage_feature)

    geojson_gages = {
      'type': 'FeatureCollection',
      'crs': {
        'type': 'name',
        'properties': {
          'name': 'EPSG:4326'
        }
      },
      'features': features
    }

    # Define layer for Map View
    geojson_layer = MVLayer(source='GeoJSON',
                            options=geojson_gages,
                            legend_title='Provo Stream Gages',
                            legend_extent=[-111.74, 40.22, -111.67, 40.25])

    # Define initial view for Map View
    view_options = MVView(
        projection='EPSG:4326',
        center=[-100, 40],
        zoom=3.5,
        maxZoom=18,
        minZoom=2
    )

    # Configure the map
    map_options = MapView(height='500px',
                          width='100%',
                          layers=[geojson_layer],
                          view=view_options,
                          basemap='OpenStreetMap',
                          legend=True)

    # Pass variables to the template via the context dictionary
    context = {'map_options': map_options}

    return render(request, 'my_first_app/map.html', context)


def map_single(request, id):
    """
    Controller for map page.
    """
    # Create a session
    session = SessionMaker()

    # Query DB for gage objects
    gage = session.query(StreamGage).filter(StreamGage.id==id).one()

    # Close the session
    session.close()

    # Transform into GeoJSON format
    gage_feature = {
      'type': 'Feature',
      'geometry': {
        'type': 'Point',
        'coordinates': [gage.longitude, gage.latitude]
      }
    }

    geojson_gages = {
      'type': 'FeatureCollection',
      'crs': {
        'type': 'name',
        'properties': {
          'name': 'EPSG:4326'
        }
      },
      'features': [gage_feature]
    }

    # Define layer for Map View
    geojson_layer = MVLayer(source='GeoJSON',
                            options=geojson_gages,
                            legend_title='Provo Stream Gages',
                            legend_extent=[-111.74, 40.22, -111.67, 40.25])

    # Define initial view for Map View
    view_options = MVView(
        projection='EPSG:4326',
        center=[-111.70, 40.24],
        zoom=13,
        maxZoom=18,
        minZoom=2
    )

    # Configure the map
    map_options = MapView(height='500px',
                          width='100%',
                          layers=[geojson_layer],
                          view=view_options,
                          basemap='OpenStreetMap',
                          legend=True)

    context = {'map_options': map_options,
               'gage_id': id}

    return render(request, 'my_first_app/map.html', context)


def echo_name(request):
    """
    Controller that will echo the name provided by the user via a form.
    """
    # Default value for name
    name = ''

    # Define Gizmo Options
    text_input_options = TextInput(display_text='Enter Name',
                                   name='name-input')

    # Check form data
    if request.POST and 'name-input' in request.POST:
        name = request.POST['name-input']

    # Create template context dictionary
    context = {'name': name,
               'text_input_options': text_input_options}

    return render(request, 'my_first_app/echo_name.html', context)
