
for tool in "magic" "netgen" "yosys" "OpenROAD" "open_pdks"
do
  cd /$tool && \
  echo "$tool:$(git log --format="%H" -n 1)"
done
