
docker run --rm -p 5000:5000 -p 5678:5678 --mount type=bind,source="$(pwd)",target=/opt/"${PWD##*/}" "${PWD##*/}-debug"