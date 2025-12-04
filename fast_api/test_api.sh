#!/bin/bash
# Test the LIP-SYNC Float API

echo "Testing LIP-SYNC Float API..."
echo ""

# Test 1: Health check
echo "1. Health check:"
curl http://localhost:8001/health
echo -e "\n\n"

# Test 2: Generate lip-sync video
echo "2. Generating lip-sync video:"
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "ref_image": "thl2.PNG",
    "audio_file": "thl_trimmed.wav",
    "emotion": "neutral",
    "a_cfg_scale": 2.0,
    "e_cfg_scale": 1.0,
    "seed": 15,
    "nfe": 10
  }'
echo -e "\n\n"

echo "Done! Check results folder for generated video"
