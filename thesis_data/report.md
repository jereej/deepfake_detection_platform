# None

_Generated 2026-10-04 08:36 UTC_

DEEPFAKE is the positive class. One table per dataset follows; use those to compare
models. Repeat runs of the same model on the same dataset are pooled into one row, so
`n` is the number of scored items across all of them.

## Per dataset

### SDFVD

_video, 106 item(s) (53 DEEPFAKE / 53 REAL). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Vansh180/VideoMae-ffc23-deepfake-detector |        1 | 106 |   44 |    5 |   48 |    9 | 46.2%      | 47.8%       | 83.0%    | 60.7% | 51.3%   | 51.6%   | 5.7%          | 9.4%         |

### arad-audio

_audio, 100 item(s) (50 DEEPFAKE / 50 REAL), 3 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Hemgg/Deepfake-audio-detection            |        1 | 100 |   41 |    5 |   45 |    9 | 46.0%      | 47.7%       | 82.0%    | 60.3% | 41.2%   | 43.5%   | 0.0%          | 2.0%         |
| MelodyMachine/Deepfake-audio-detection-V2 |        1 | 100 |   26 |   37 |   13 |   24 | 63.0%      | 66.7%       | 52.0%    | 58.4% | 64.6%   | 67.1%   | 16.0%         | 30.0%        |
| mo-thecreator/Deepfake-audio-detection    |        1 | 100 |   34 |   15 |   35 |   16 | 49.0%      | 49.3%       | 68.0%    | 57.1% | 51.4%   | 53.0%   | 4.0%          | 12.0%        |

### cifake

_image, 100 item(s) (50 DEEPFAKE / 50 REAL), 5 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Organika/sdxl-detector                    |        1 | 100 |   13 |   46 |    4 |   37 | 59.0%      | 76.5%       | 26.0%    | 38.8% | 68.7%   | 70.8%   | 22.0%         | 26.0%        |
| dima806/deepfake_vs_real_image_detection  |        1 | 100 |    4 |   46 |    4 |   46 | 50.0%      | 50.0%       | 8.0%     | 13.8% | 45.7%   | 50.0%   | 8.0%          | 10.0%        |
| gemma3:12b                                |        1 | 100 |   45 |    0 |   50 |    5 | 45.0%      | 47.4%       | 90.0%    | 62.1% | n/a     | n/a     | n/a           | n/a          |
| llava                                     |        1 | 100 |   17 |   40 |   10 |   33 | 57.0%      | 63.0%       | 34.0%    | 44.2% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model |        1 | 100 |   50 |    2 |   48 |    0 | 52.0%      | 51.0%       | 100.0%   | 67.6% | 47.3%   | 50.6%   | 4.0%          | 8.0%         |

### dataset_100

_image, 100 item(s) (47 DEEPFAKE / 53 REAL), 5 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Organika/sdxl-detector                    |        1 | 100 |   10 |    8 |   45 |   37 | 18.0%      | 18.2%       | 21.3%    | 19.6% | 9.0%    | 30.0%   | 0.0%          | 0.0%         |
| dima806/deepfake_vs_real_image_detection  |        1 | 100 |    7 |   39 |   14 |   40 | 46.0%      | 33.3%       | 14.9%    | 20.6% | 48.2%   | 48.0%   | 6.4%          | 10.6%        |
| gemma3:12b                                |        1 | 100 |   12 |   25 |   28 |   35 | 37.0%      | 30.0%       | 25.5%    | 27.6% | n/a     | n/a     | n/a           | n/a          |
| llava                                     |        1 | 100 |    9 |   37 |   16 |   38 | 46.0%      | 36.0%       | 19.1%    | 25.0% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model |        1 | 100 |   45 |    0 |   53 |    2 | 45.0%      | 45.9%       | 95.7%    | 62.1% | 43.0%   | 45.8%   | 4.3%          | 14.9%        |

### dataset_53

_image, 53 item(s) (12 DEEPFAKE / 41 REAL), 5 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Organika/sdxl-detector                    |        1 |  53 |    2 |   16 |   25 |   10 | 34.0%      | 7.4%        | 16.7%    | 10.3% | 43.1%   | 41.7%   | 16.7%         | 16.7%        |
| dima806/deepfake_vs_real_image_detection  |        1 |  53 |    2 |   35 |    6 |   10 | 69.8%      | 25.0%       | 16.7%    | 20.0% | 81.7%   | 64.3%   | 16.7%         | 16.7%        |
| gemma3:12b                                |        1 |  53 |   12 |   12 |   29 |    0 | 45.3%      | 29.3%       | 100.0%   | 45.3% | n/a     | n/a     | n/a           | n/a          |
| llava                                     |        1 |  53 |    5 |   17 |   24 |    7 | 41.5%      | 17.2%       | 41.7%    | 24.4% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model |        1 |  53 |   10 |    0 |   41 |    2 | 18.9%      | 19.6%       | 83.3%    | 31.7% | 0.0%    | 20.1%   | 0.0%          | 0.0%         |

### deepfake-audio-detection

_audio, 100 item(s) (53 DEEPFAKE / 47 REAL), 3 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Hemgg/Deepfake-audio-detection            |        1 | 100 |   37 |   22 |   25 |   16 | 59.0%      | 59.7%       | 69.8%    | 64.3% | 56.4%   | 57.8%   | 9.4%          | 9.4%         |
| MelodyMachine/Deepfake-audio-detection-V2 |        1 | 100 |    4 |   44 |    3 |   49 | 48.0%      | 57.1%       | 7.5%     | 13.3% | 52.9%   | 55.1%   | 3.8%          | 11.3%        |
| mo-thecreator/Deepfake-audio-detection    |        1 | 100 |   37 |   34 |   13 |   16 | 71.0%      | 74.0%       | 69.8%    | 71.8% | 80.2%   | 77.9%   | 26.4%         | 45.3%        |

### dfd-video

_video, 100 item(s) (50 DEEPFAKE / 50 REAL). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Vansh180/VideoMae-ffc23-deepfake-detector |        1 | 100 |   18 |   30 |   20 |   32 | 48.0%      | 47.4%       | 36.0%    | 40.9% | 52.0%   | 50.4%   | 0.0%          | 4.0%         |

### hemg-deepfakeaudio

_audio, 100 item(s) (51 DEEPFAKE / 49 REAL), 3 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1   | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:-----|:--------|:--------|:--------------|:-------------|
| Hemgg/Deepfake-audio-detection            |        1 | 100 |    0 |   49 |    0 |   51 | 49.0%      | n/a         | 0.0%     | n/a  | 54.2%   | 58.1%   | 5.9%          | 19.6%        |
| MelodyMachine/Deepfake-audio-detection-V2 |        1 | 100 |    0 |   49 |    0 |   51 | 49.0%      | n/a         | 0.0%     | n/a  | 57.5%   | 55.8%   | 0.0%          | 9.8%         |
| mo-thecreator/Deepfake-audio-detection    |        1 | 100 |    0 |   49 |    0 |   51 | 49.0%      | n/a         | 0.0%     | n/a  | 77.2%   | 74.7%   | 29.4%         | 37.3%        |

### hemg-images

_image, 100 item(s) (50 DEEPFAKE / 50 REAL), 5 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Organika/sdxl-detector                    |        1 | 100 |    4 |   46 |    4 |   46 | 50.0%      | 50.0%       | 8.0%     | 13.8% | 53.3%   | 56.4%   | 2.0%          | 26.0%        |
| dima806/deepfake_vs_real_image_detection  |        1 | 100 |   50 |   49 |    1 |    0 | 99.0%      | 98.0%       | 100.0%   | 99.0% | 99.6%   | 99.6%   | 100.0%        | 100.0%       |
| gemma3:12b                                |        1 | 100 |   23 |   39 |   11 |   27 | 62.0%      | 67.6%       | 46.0%    | 54.8% | n/a     | n/a     | n/a           | n/a          |
| llava                                     |        1 | 100 |   26 |   31 |   19 |   24 | 57.0%      | 57.8%       | 52.0%    | 54.7% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model |        1 | 100 |    3 |    1 |   49 |   47 | 4.0%       | 5.8%        | 6.0%     | 5.9%  | 0.9%    | 31.2%   | 0.0%          | 0.0%         |

## Models per media type

Datasets are pooled here, so a model that was only ever run on one dataset can look
better than one evaluated everywhere. Use the per-dataset tables above for comparisons.

| model                                     | backend     | dataset   | media_type   |   n_datasets |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|:------------|:----------|:-------------|-------------:|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Hemgg/Deepfake-audio-detection            | huggingface | all (3)   | audio        |            3 |        3 | 300 |   78 |   76 |   70 |   76 | 51.3%      | 52.7%       | 50.6%    | 51.7% | 50.8%   | 49.7%   | 1.3%          | 4.5%         |
| MelodyMachine/Deepfake-audio-detection-V2 | huggingface | all (3)   | audio        |            3 |        3 | 300 |   30 |  130 |   16 |  124 | 53.3%      | 65.2%       | 19.5%    | 30.0% | 55.8%   | 58.4%   | 9.7%          | 18.2%        |
| mo-thecreator/Deepfake-audio-detection    | huggingface | all (3)   | audio        |            3 |        3 | 300 |   71 |   98 |   48 |   83 | 56.3%      | 59.7%       | 46.1%    | 52.0% | 61.8%   | 60.1%   | 11.0%         | 18.8%        |
| Organika/sdxl-detector                    | huggingface | all (4)   | image        |            4 |        4 | 353 |   29 |  116 |   78 |  130 | 41.1%      | 27.1%       | 18.2%    | 21.8% | 37.0%   | 36.1%   | 0.0%          | 0.0%         |
| dima806/deepfake_vs_real_image_detection  | huggingface | all (4)   | image        |            4 |        4 | 353 |   63 |  169 |   25 |   96 | 65.7%      | 71.6%       | 39.6%    | 51.0% | 75.9%   | 74.8%   | 34.6%         | 39.0%        |
| gemma3:12b                                | ollama      | all (4)   | image        |            4 |        4 | 353 |   92 |   76 |  118 |   67 | 47.6%      | 43.8%       | 57.9%    | 49.9% | n/a     | n/a     | n/a           | n/a          |
| llava                                     | ollama      | all (4)   | image        |            4 |        4 | 353 |   57 |  125 |   69 |  102 | 51.6%      | 45.2%       | 35.8%    | 40.0% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model | huggingface | all (4)   | image        |            4 |        4 | 353 |  108 |    3 |  191 |   51 | 31.4%      | 36.1%       | 67.9%    | 47.2% | 19.8%   | 30.7%   | 0.0%          | 0.0%         |
| Vansh180/VideoMae-ffc23-deepfake-detector | huggingface | all (2)   | video        |            2 |        2 | 206 |   62 |   35 |   68 |   41 | 47.1%      | 47.7%       | 60.2%    | 53.2% | 50.7%   | 50.2%   | 4.9%          | 7.8%         |

## Coverage

- Scored 2871/2871 items that carried both a label and a prediction.
- 706 item(s) had no fake_score, so AUROC/AUPRC/TPR@FPR are n/a for them. Ollama models do not report a score, so they only get the hard metrics.
- TPR@FPR is the highest true positive rate reachable at any threshold that stays within the given false positive budget, so 0% is a real measurement of a model that catches nothing without false alarms. It is n/a only when the budget is finer than the dataset can express (1/n with n negatives, here about 0.00).
