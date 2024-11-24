# scale=710:804
# scale=1920:1920'

fps=15
speed=medium
quality=23
city=boston

ffmpeg -r $fps -y -i out/frames/$city/frame%04d.png -vf 'scale=1200:1000' \
  -c:v libx264 -profile:v baseline -preset $speed -tune animation \
  -crf $quality -pix_fmt yuv420p out/$city.mp4

ffmpeg out/$city.mp4 out/$city.gif
