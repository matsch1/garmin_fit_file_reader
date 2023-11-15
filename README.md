# garmin_fit_file_reader
classes to read garmin fit files for swimming, running and cycling to enable further analysis

## export fit file from garmin
Download fit file from garmin connect.

## swim fit file reader
Reads basic information from garmin fit file of a pool swim session.

``` py
swimReader = SwimFitReader('activity_garmin.fit')
test_lap = swimReader.get_lap(0)
print(test_lap)
```

return:

{'index': 0, <br>
'start_time': datetime.datetime(2023, 11, 13, 17, 22, 6), <br>
'stroke': 'Miscellaneous', <br>
'total_strokes': 62, <br>
'total_distance': 100.0, <br>
'number_of_lanes': 4, '<br>
avg_velocity_in_m_per_s': 0.656, <br>
'avg_pace_in_min_per_100m': 2.540650406504065, <br>
'avg_pace_in_min_per_100m_string': '2:32.4', <br>
'max_velocity_in_m_per_s': 0.676, <br>
'max_pace_in_min_per_100m': 2.465483234714004, <br>
'max_pace_in_min_per_100m_string': '2:27.9', <br>
'total_elapsed_time_in_min': 2.54165, <br>
'total_elapsed_time_in_min_string': '2:32.5', <br>
'lanes': <br>
  [{'index': 0, 'stroke': 'Freestyle', 'total_strokes': 16, 'velocity_in_m_per_s': 0.624, 'avg_pace_in_min_per_100m': 2.6709401709401708, 'avg_pace_in_min_per_100m_string': '2:40.3', 'total_elapsed_time_in_min': 0.6677, 'total_elapsed_time_in_min_string': '0:40.1'},<br>
  {'index': 1, 'stroke': 'Breaststroke', 'total_strokes': 16, 'velocity_in_m_per_s': 0.659, 'avg_pace_in_min_per_100m': 2.529084471421345, 'avg_pace_in_min_per_100m_string': '2:31.7', 'total_elapsed_time_in_min': 0.6322833333333333, 'total_elapsed_time_in_min_string': '0:37.9'},<br>
  {'index': 2, 'stroke': 'Breaststroke', 'total_strokes': 15, 'velocity_in_m_per_s': 0.667, 'avg_pace_in_min_per_100m': 2.498750624687656, 'avg_pace_in_min_per_100m_string': '2:29.9', 'total_elapsed_time_in_min': 0.625, 'total_elapsed_time_in_min_string': '0:37.5'},<br>
  {'index': 3, 'stroke': 'Breaststroke', 'total_strokes': 15, 'velocity_in_m_per_s': 0.676, 'avg_pace_in_min_per_100m': 2.465483234714004, 'avg_pace_in_min_per_100m_string': '2:27.9', 'total_elapsed_time_in_min': 0.6166666666666667, 'total_elapsed_time_in_min_string': '0:37.0'}]}

  view in garmin connect:
  ![image](https://github.com/matsch1/garmin_fit_file_reader/assets/95409477/4ee015d1-c89d-449c-81da-f7f43979e14b)
