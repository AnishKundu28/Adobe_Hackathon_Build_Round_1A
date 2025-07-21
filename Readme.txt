# Connecting the Dots: PDF Outline Extractor

## How to run

docker build --platform=linux/amd64 -t mysolution:tag .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolution:tag

## Approach

See each .py file for logic. Tweak heuristics for accuracy!
