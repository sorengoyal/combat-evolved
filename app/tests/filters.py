# the geo json geometry object we got from geojson.io
coordinates = [
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
          -121.95789277553557,
          37.417830946910904
        ]
    ]
]

geo_json_geometry = {
  "type": "Polygon",
       "coordinates": coordinates
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

winter_date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "2016-12-01T00:00:00.000Z",
    "lte": "2017-03-31T00:00:00.000Z"
  }
}
spring_date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "2016-04-01T00:00:00.000Z",
    "lte": "2017-05-31T00:00:00.000Z"
  }
} 
summer_date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "2016-06-01T00:00:00.000Z",
    "lte": "2017-08-31T00:00:00.000Z"
  }
}  
fall_date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "2016-09-01T00:00:00.000Z",
    "lte": "2017-11-31T00:00:00.000Z"
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

cloud_cover_filter2 = {
  "type": "RangeFilter",
  "field_name": "cloud_cover",
  "config": {
    "gte": 100
  }
}
  
# create a filter that combines our geo and date filters
# could also use an "OrFilter"
negFilter = {
  "type": "AndFilter",
  "config": [geometry_filter, date_range_filter, cloud_cover_filter2]
}

posFilter = {
  "type": "AndFilter",
  "config": [geometry_filter, date_range_filter, cloud_cover_filter]
}

winterFilter = {
  "type": "AndFilter",
  "config": [geometry_filter, winter_date_range_filter, cloud_cover_filter]
}
springPosFilter = {
  "type": "AndFilter",
  "config": [geometry_filter, spring_date_range_filter, cloud_cover_filter]
}
summerFilter = {
  "type": "AndFilter",
  "config": [geometry_filter, summer_date_range_filter, cloud_cover_filter]
}
fallPosFilter = {
  "type": "AndFilter",
  "config": [geometry_filter, fall_date_range_filter, cloud_cover_filter]
}
