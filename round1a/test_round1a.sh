#!/bin/bash
echo "Testing Round 1A PDF Outline Extractor..."
echo "Building Docker image..."
sudo docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .
echo "Running test..."
sudo docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:v1.0
echo "Checking output..."
cat output/sample.json
echo "Test completed!"
