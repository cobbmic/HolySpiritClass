for f in *.mp3; do
  whisper "$f" --model base --output_format txt
done
