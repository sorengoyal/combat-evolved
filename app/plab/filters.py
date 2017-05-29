# the geo json geometry object we got from geojson.io
geo_json_geometry = {
  "type": "Polygon",
       "coordinates": [
          [
            [
              -121.95789277553557,
              37.417830946910904
            ],
            [
              -121.95595085620879,
              37.416510162308874
            ],
            [
              -121.95349395275115,
              37.41863618802896
            ],
            [
              -121.95355296134949,
              37.41921561543447
            ],
            [
              -121.95466876029967,
              37.41922839687082
            ],
            [
              -121.95605278015137,
              37.4190111121562
            ],
            [
              -121.95626199245453,
              37.41891738130037
            ],
            [
              -121.95648729801177,
              37.41879382681114
            ],
            [
              -121.95731341838837,
              37.41809510103616
            ],
            [
              -121.95789277553557,
              37.417830946910904
            ]
        ]
    ]
}

# filter for items the overlap with our chosen geometry
geometry_filter = {
  "type": "GeometryFilter",
  "field_name": "geometry",
  "config": geo_json_geometry
}

# filter images acquired in a certain date range
date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "2017-04-01T00:00:00.000Z",
    "lte": "2018-08-01T00:00:00.000Z"
  }
}

# filter any images which are more than 50% clouds
cloud_cover_filter = {
  "type": "RangeFilter",
  "field_name": "cloud_cover",
  "config": {
    "lte": 0.05
  }
}

# create a filter that combines our geo and date filters
# could also use an "OrFilter"
my_filter = {
  "type": "AndFilter",
  "config": [geometry_filter, date_range_filter, cloud_cover_filter]
}
