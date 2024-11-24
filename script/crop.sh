dir=boston
label=Boston

# iterate over all png images
for f in out/frames/$dir/*.png; do

  # crop each image to a square
  magick $f -gravity Center -crop 6:5 +repage $f

  # add text to each one
  magick $f -font "Baskerville-SemiBold" -gravity SouthWest -pointsize 50 -fill white -annotate +20+20 "$label" $f
done
