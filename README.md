# bike-exploration

Animations of bike exploration in various cities

- Inspired by this [this post](https://www.reddit.com/r/dataisbeautiful/comments/f8nu0c/oc_this_is_how_londons_street_grid_reveals_using/)

See:

- https://medium.com/@tjukanov/animated-routes-with-qgis-9377c1f16021
- https://anitagraser.com/projects/time-manager/

## Setup

```bash
conda create -c conda-forge -n strava python=3.12 pandas jupyterlab geopandas
pip install gpxpy fitparse tqdm
pip install "rich[jupyter]"
```

### jupyter notebook

So that only the code is saved in the notebook, and not the output,

I added to .git/config:

```ini
[filter "strip-notebook-output"]
    clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"
```

And created .gitattributes:

```txt
*.ipynb filter=strip-notebook-output
```

## Usage

Bulk download all the strava data and put it somewhere, like `data/strava`.

## QGIS Workflow

- Set background to black
- Add shapefile for a city
-
