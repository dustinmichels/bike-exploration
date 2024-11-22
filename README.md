# bike-exploration

Animations of bike exploration in various cities

- Inspired by this [this post](https://www.reddit.com/r/dataisbeautiful/comments/f8nu0c/oc_this_is_how_londons_street_grid_reveals_using/)

See:

- https://medium.com/@tjukanov/animated-routes-with-qgis-9377c1f16021
- https://anitagraser.com/projects/time-manager/

## env

```bash
conda create -c conda-forge -n strava python=3.12 pandas jupyterlab geopandas

pip install gpxpy fitparse tqdm
pip install "rich[jupyter]"
```

## jupyter notebook

Add to .git/config:

```txt
[filter "strip-notebook-output"]
    clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"
```

Create .gitattributes:

```txt
*.ipynb filter=strip-notebook-output
```
