[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matthieu-bernard/gee-processing/blob/main/chirps_processing_colab.ipynb)

# Google Earth Engine processing

Some bits of code and own experiments with Google Earth Engine.
More like a collection of scripts that might move to a proper package as it grows.


## Features

 - Retreive data from the Google Earth Engine.
 - Map data from Google earth engine.


## javacript one

```javascript
var precip =ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").select('precipitation');
var masked_precip = precip.map(function (img) {return img.gt(0)});

var aoi = ee.FeatureCollection('users/matthieu_bernard/aoi').geometry();

var months = ee.List.sequence(1, 12)
var years = ee.List.sequence(2013, 2017)

var byMonthYear = ee.ImageCollection.fromImages(
  years.map(function (y){
    return months.map(function (m) {
        return precip
        .filter(ee.Filter.calendarRange(y, y, 'year'))
        .filter(ee.Filter.calendarRange(m, m, 'month'))
        .sum()
        .set('month', m).set('year', y);
  });
}).flatten());
print(byMonthYear);

var byMonth = ee.ImageCollection.fromImages(
  months.map(function (m) {
        return byMonthYear
        .filterMetadata('month', 'equals', m)
        .mean()
        .clip(aoi)
        .set('month', m);
  }));

print(byMonth);

Map.addLayer(byMonth);
```


