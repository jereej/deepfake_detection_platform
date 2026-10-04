#!/bin/bash
# Run the complete test suite for all models to be used in the thesis.
#
# Run from anywhere: the script changes into its own directory, so the relative
# dataset paths below and the analyses/ output folder always resolve the same way.
#
# NOTE: requires all default models to be downloaded and the datasets to be unzipped.

set -euo pipefail

cd "$(dirname "$0")"

# Every analysis is written to thesis_data/analyses/, which also collects the
# run-level statistics.csv. The reporter reads that folder by default.
DESTINATION="analyses"
mkdir -p "$DESTINATION"

# Builds a deftor analyze invocation with the arguments every run shares.
# Usage: analyze <dataset-dir> <dataset-name> <labels-file> <output-name> <model> [extra args...]
analyze() {
    local dataset_dir="$1"
    local dataset_name="$2"
    local labels_file="$3"
    local output_name="$4"
    local model="$5"
    shift 5

    echo "${dataset_name} analysis with ${model}"

    deftor analyze "$dataset_dir" \
        -m "$model" \
        -o "$output_name" \
        -f json \
        -d "$DESTINATION" \
        --dataset "$dataset_name" \
        --labels "$labels_file" \
        --positive-label 1 \
        "$@"
}


# Image analysis section
echo "=== Image analysis ==="
# minicpm-v4.6
for model in qwen3.6; do
    analyze image/qwen_dataset/ \
        qwen_dataset \
        image/qwen_dataset/labels.txt \
        "$(echo "$model" | tr ':.' '--')-qwendataset-analysis" \
        "$model"
done

# NOTE: moondream is excluded. It truncated its output on 107 of the 153 dataset_53
# items and returns no usable logprobs, so it cannot contribute AUROC/AUPRC/TPR@FPR.

for model in \
    dima806/deepfake_vs_real_image_detection \
    prithivMLmods/Deep-Fake-Detector-v2-Model \
    Organika/sdxl-detector; do
    analyze image/dataset_53/ \
        dataset_53 \
        image/dataset_53/labels.txt \
        "$(echo "$model" | tr '/:' '--')-dataset53-analysis" \
        "$model"
done

# minicpm-v4.6
for model in llava gemma3:12b  llama3.2-vision:11b; do
    analyze image/dataset_100/ \
        dataset_100 \
        image/dataset_100/labels.txt \
        "$(echo "$model" | tr ':.' '--')-dataset100-analysis" \
        "$model"
done


for model in \
    dima806/deepfake_vs_real_image_detection \
    prithivMLmods/Deep-Fake-Detector-v2-Model \
    Organika/sdxl-detector; do
    analyze image/dataset_100/ \
        dataset_100 \
        image/dataset_100/labels.txt \
        "$(echo "$model" | tr '/:' '--')-dataset100-analysis" \
        "$model"
done

# minicpm-v4.6
for model in llava gemma3:12b  llama3.2-vision:11b; do
    analyze image/cifake/ \
        cifake \
        image/cifake/labels.txt \
        "$(echo "$model" | tr ':.' '--')-cifake-analysis" \
        "$model"
done


for model in \
    dima806/deepfake_vs_real_image_detection \
    prithivMLmods/Deep-Fake-Detector-v2-Model \
    Organika/sdxl-detector; do
    analyze image/cifake/ \
        cifake \
        image/cifake/labels.txt \
        "$(echo "$model" | tr '/:' '--')-cifake-analysis" \
        "$model"
done

# minicpm-v4.6
for model in llava gemma3:12b  llama3.2-vision:11b; do
    analyze image/hemg-images/ \
        hemg-images \
        image/hemg-images/labels.txt \
        "$(echo "$model" | tr ':.' '--')-hemgimages-analysis" \
        "$model"
done


for model in \
    dima806/deepfake_vs_real_image_detection \
    prithivMLmods/Deep-Fake-Detector-v2-Model \
    Organika/sdxl-detector; do
    analyze image/hemg-images/ \
        hemg-images \
        image/hemg-images/labels.txt \
        "$(echo "$model" | tr '/:' '--')-hemgimages-analysis" \
        "$model"
done


# Audio analysis section
echo "=== Audio analysis ==="

for dataset_dir in audio/hemg-deepfakeaudio audio/deepfake-audio-detection audio/arad-audio; do
    dataset_name="$(basename "$dataset_dir")"
    labels_file="$dataset_dir/labels.txt"
    [ -f "$labels_file" ] || labels_file="$dataset_dir/audio_labels.txt"

    for model in \
        mo-thecreator/Deepfake-audio-detection \
        Hemgg/Deepfake-audio-detection \
        MelodyMachine/Deepfake-audio-detection-V2; do
        # NOTE: Hemgg/Deepfake-audio-detection was likely trained on hemg-deepfakeaudio,
        # so expect better performance there than the numbers warrant elsewhere.
        analyze "$dataset_dir" \
            "$dataset_name" \
            "$labels_file" \
            "$(echo "$model" | tr '/:' '--')-analysis-$dataset_name" \
            "$model" \
            --media-type audio
    done
done


# Text analysis section
echo "=== Text analysis ==="

# NOTE: DEFTOR has no transformers pipeline for text (TASK_TYPE only covers
# image/audio/video), so text is Ollama-only. These are the text-capable LLMs
# that are already pulled locally. labels.txt is excluded from the items by
# DEFTOR itself, since it shares the .txt media extension.
for model in gemma3:12b qwen3.6 llama3.2-vision:11b; do
    analyze text/human-ai-text/ \
        human-ai-text \
        text/human-ai-text/labels.txt \
        "$(echo "$model" | tr ':.' '--')-humanaitext-analysis" \
        "$model" \
        --media-type text
done


# Video analysis section
echo "=== Video analysis ==="

analyze video/SDFVD/ \
    SDFVD \
    video/SDFVD/labels.txt \
    vansh180-video-analysis-sdfvd \
    Vansh180/VideoMae-ffc23-deepfake-detector \
    --media-type video

# NOTE: the same DFD model is reused for dfd-video; the SDFVD run above keeps
# its original output name, so the two do not collide in analyses/.
analyze video/dfd-video/ \
    dfd-video \
    video/dfd-video/labels.txt \
    vansh180-video-analysis-dfdvideo \
    Vansh180/VideoMae-ffc23-deepfake-detector \
    --media-type video


# Report generation
echo "=== Generating report ==="
# Reads every analysis in analyses/ and writes the dataset-wise comparison table.
deftor report -a "$DESTINATION" -o report.md --title "DEFTOR Model Performance Report"

echo "Done. Analyses in ${DESTINATION}/, report in report.md"
