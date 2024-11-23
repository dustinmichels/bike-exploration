# scale=710:804
# scale=1920:1920'

fps=10
speed=medium
quality=23

ffmpeg -r $fps -y -i out/frames/gothenburg/frame%04d.png -vf 'scale=720:720' \
  -c:v libx264 -profile:v baseline -preset $speed -tune animation \
  -crf $quality -pix_fmt yuv420p outfile.mp4
