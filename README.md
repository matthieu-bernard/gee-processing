[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matthieu-bernard/gee-processing/blob/main/chirps_processing_colab.ipynb)

# Google Earth Engine processing

Some bits of code and own experiments with Google Earth Engine.
More like a collection of scripts that might move to a proper package as it grows.


## Features

 - Retreive data from the Google Earth Engine.
 - Map data from Google earth engine.


## Pipeline demo.


### Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matthieu-bernard/gee-processing/blob/main/chirps_processing_colab.ipynb)

The colab link will launch a notebook in Google Colab.
The notebook is self contained but will require you to have a Google Drive account as it save artifacts to your Drive.


### Local notebook

To run it locally please clone this repo first.

```bash
git clone git@github.com:matthieu-bernard/gee-processing.git
```

Then create a virtual environement for this project (If you do not have pipenv installed a simple pip install pipenv will do the trick, have a llok at it it is a great tool).
```bash
cd gee-processing
pipenv install --dev
pipenv shell
```

Now you can run the jupyter server
```bash
jupyter notebook
```


### Google Earth Engine Code Editor

GEE [code editor](https://code.earthengine.google.com/) allow you to quickly run scripts from your Web Navigator.

Following is a javascirpt that compute average number of rainy days per month from the CHIRPS dataset
You can copy paste and modify play with it to get a feel for the platform

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
        .set('month', m)
        .set('description', ('number of rainy days mean the number of days that have non null rainfall amount over'
                             'the aggregation period'))
        .set('aggregation_period', 'calendar_month')
        .set('long_name', 'number_of_rainy_days')
        .set('original_dataset', {'title': 'CHIRPS Daily: Climate Hazards Group InfraRed Precipitation with Station Data (version 2.0 final',
                                  'version': '2.0',
                                  'description': 'Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS)\nis a 30+ year quasi-global rainfall dataset. CHIRPS incorporates\n0.05° resolution satellite imagery with in-situ station data\nto create gridded rainfall time series for trend analysis and seasonal\ndrought monitoring.\n'
                                 })
        .set('provider', 'matth.bernard@gmail.com');
  }));

print(byMonth);

Map.addLayer(byMonth);
```


