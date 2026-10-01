! /bin/bash

Run the complete test suite for all models to be used in the thesis
NOTE: requires all default models to be downloaded and the datasets to be unzipped

# Image analysis section
echo "53-item dataset analysis with llava"
deftor analyze image/dataset_53/ \
-m llava \
-o llava-dataset53-analysis \
-f json

echo "53-item dataset analysis with gemma3:12b"
deftor analyze image/dataset_53/ \
-m gemma3:12b \
-o gemma3-dataset53-analysis \
-f json

# NOTE: EXCLUDING QWEN DUE TO PROBLEMS TO-BE-FIXED
# echo "53-item dataset analysis with qwen3.6"
# deftor analyze image/dataset_53/ \
# -m qwen3.6 \
# -o qwen36-dataset53-analysis \
# -f json

echo "53-item dataset analysis with minicpm-v4.6"
deftor analyze image/dataset_53/ \
-m minicpm-v4.6 \
-o minicpmv46-dataset53-analysis \
-f json

echo "53-item dataset analysis with llama3.2-vision:11b"
deftor analyze image/dataset_53/ \
-m llama3.2-vision:11b \
-o llama32-dataset53-analysis \
-f json

echo "53-item dataset analysis with moondream"
deftor analyze image/dataset_53/ \
-m moondream \
-o moondream-dataset53-analysis \
-f json

echo "53-item dataset analysis with dima806/deepfake_vs_real_image_detection"
deftor analyze image/dataset_53/ \
-m dima806/deepfake_vs_real_image_detection \
-o dima806-dataset53-analysis \
-f json

echo "53-item dataset analysis with prithibMLmods/Deep-Fake-Detector-v2-Model"
deftor analyze image/dataset_53/ \
-m prithibMLmods/Deep-Fake-Detector-v2-Model \
-o prithibmlmods-dataset53-analysis \
-f json

echo "53-item dataset analysis with Organika/sdxl-detector"
deftor analyze image/dataset_53/ \
-m Organika/sdxl-detector \
-o organikasdxl-dataset53-analysis \
-f json

echo "100-item dataset analysis with llava"
deftor analyze image/dataset_100/ \
-m llava \
-o llava-dataset53-analysis \
-f json

echo "100-item dataset analysis with gemma3:12b"
deftor analyze image/dataset_100/ \
-m gemma3:12b \
-o gemma3-dataset100-analysis \
-f json

# NOTE: EXCLUDING QWEN DUE TO PROBLEMS THAT ARE TO-BE-FIXED
# echo "100-item dataset analysis with qwen3.6"
# deftor analyze image/dataset_100/ \
# -m qwen3.6 \
# -o qwen36-dataset100-analysis \
# -f json

echo "100-item dataset analysis with minicpm-v4.6"
deftor analyze image/dataset_100/ \
-m minicpm-v4.6 \
-o minicpmv46-dataset100-analysis \
-f json

echo "100-item dataset analysis with llama3.2-vision:11b"
deftor analyze image/dataset_100/ \
-m llama3.2-vision:11b \
-o llama32-dataset100-analysis \
-f json

echo "100-item dataset analysis with moondream"
deftor analyze image/dataset_100/ \
-m moondream \
-o moondream-dataset100-analysis \
-f json

echo "100-item dataset analysis with dima806/deepfake_vs_real_image_detection"
deftor analyze image/dataset_100/ \
-m dima806/deepfake_vs_real_image_detection \
-o dima806-dataset100-analysis \
-f json

echo "100-item dataset analysis with prithibMLmods/Deep-Fake-Detector-v2-Model"
deftor analyze image/dataset_100/ \
-m prithibMLmods/Deep-Fake-Detector-v2-Model \
-o prithibmlmods-dataset100-analysis \
-f json

echo "100-item dataset analysis with Organika/sdxl-detector"
deftor analyze image/dataset_100/ \
-m Organika/sdxl-detector \
-o organikasdxl-dataset100-analysis \
-f json


# Audio analysis section
echo "hemg-deepfakeaudio dataset analysis with mo-thecreator/Deepfake-audio-detection"
deftor analyze /home/jere/deepfake_detection_platform/thesis_data/audio/hemg-deepfakeaudio/ \
-m mo-thecreator/Deepfake-audio-detection \
-o mothecreator-analysis-hemg-deepfakeaudio \
-f json \
--media-type audio

echo "hemg-deepfakeaudio dataset analysis with Hemgg/Deepfake-audio-detection"
# NOTE: This model was likely trained on this dataset -> leads to better performance
deftor analyze audio/hemg-deepfakeaudio/ \
-m Hemgg/Deepfake-audio-detection \
-o hemgg-analysis-hemg-deepfakeaudio \
-f json \
--media-type audio

echo "hemg-deepfakeaudio dataset analysis with MelodyMachine/Deepfake-audio-detection-V2"
deftor analyze audio/hemg-deepfakeaudio/ \
-m MelodyMachine/Deepfake-audio-detection-V2 \
-o melodymachine-analysis-hemg-deepfakeaudio \
-f json \
--media-type audio

echo "deepfake-audio-detection dataset analysis with mo-thecreator/Deepfake-audio-detection"
deftor analyze audio/deepfake-audio-detection/ \
-m mo-thecreator/Deepfake-audio-detection \
-o mothecreator-analysis-hemg-deepfakeaudio \
-f json \
--media-type audio

echo "deepfake-audio-detection dataset analysis with Hemgg/Deepfake-audio-detection"
deftor analyze audio/deepfake-audio-detection/ \
-m Hemgg/Deepfake-audio-detection \
-o hemgg-analysis-hemg-deepfakeaudio \
-f json \
--media-type audio

echo "deepfake-audio-detection dataset analysis with MelodyMachine/Deepfake-audio-detection-V2"
deftor analyze audio/deepfake-audio-detection/ \
-m MelodyMachine/Deepfake-audio-detection-V2 \
-o melodymachine-analysis-hemg-deepfakeaudio \
-f json \
--media-type audio


# Video analysis section
echo "SDFVD dataset analysis with Vansh180/VideoMae-ffc23-deepfake-detector"
deftor analyze video/SDFVD/ \
-m Vansh180/VideoMae-ffc23-deepfake-detector \
-o vansh180-video-analysis-sdfvd \
-f json \
--media-type video
