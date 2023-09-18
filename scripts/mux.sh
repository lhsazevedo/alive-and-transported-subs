inputs=''

for f in ./src/en-US-original/*; do inputs="$inputs --input $f"; done

srt-mux $inputs --output dist/tobymac-alive_and_transported.srt
