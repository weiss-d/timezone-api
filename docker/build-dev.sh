docker buildx build --tag "${PWD##*/}-dev" --target development --file docker/Dockerfile . 