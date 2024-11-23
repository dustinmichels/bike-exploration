# iterate over all png images out/frames/gothenburg
for f in out/frames/gothenburg/*.png; do
  # crop each image to a square
  magick $f -gravity center -crop "$(identify -format '%[fx:min(w,h)]' $f)x$(identify -format '%[fx:min(w,h)]' $f)+0+0" +repage $f
  # add text to each one
  magick $f -font "Baskerville-SemiBold" -gravity SouthWest -pointsize 80 -fill white -annotate +20+20 "Gothenburg" $f
done
