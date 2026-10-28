# None

_Generated 2026-10-28 15:35 UTC_

DEEPFAKE is the positive class. One table per dataset follows; use those to compare
models. Repeat runs of the same model on the same dataset are pooled into one row, so
`n` is the number of scored items across all of them.

## Per dataset

### SDFVD

_video, 106 item(s) (53 DEEPFAKE / 53 REAL). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Vansh180/VideoMae-ffc23-deepfake-detector |        1 | 106 |   48 |    9 |   44 |    5 | 53.8%      | 52.2%       | 90.6%    | 66.2% | 48.7%   | 51.3%   | 3.8%          | 11.3%        |

### arad-audio

_audio, 100 item(s) (50 DEEPFAKE / 50 REAL), 3 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Hemgg/Deepfake-audio-detection            |        1 | 100 |   45 |    9 |   41 |    5 | 54.0%      | 52.3%       | 90.0%    | 66.2% | 58.8%   | 62.8%   | 18.0%         | 28.0%        |
| MelodyMachine/Deepfake-audio-detection-V2 |        1 | 100 |   13 |   24 |   26 |   37 | 37.0%      | 33.3%       | 26.0%    | 29.2% | 35.4%   | 40.7%   | 0.0%          | 4.0%         |
| mo-thecreator/Deepfake-audio-detection    |        1 | 100 |   35 |   16 |   34 |   15 | 51.0%      | 50.7%       | 70.0%    | 58.8% | 48.6%   | 49.2%   | 2.0%          | 8.0%         |

### cifake

_image, 100 item(s) (50 DEEPFAKE / 50 REAL), 5 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Organika/sdxl-detector                    |        1 | 100 |    4 |   37 |   13 |   46 | 41.0%      | 23.5%       | 8.0%     | 11.9% | 31.3%   | 39.2%   | 0.0%          | 0.0%         |
| dima806/deepfake_vs_real_image_detection  |        1 | 100 |    4 |   46 |    4 |   46 | 50.0%      | 50.0%       | 8.0%     | 13.8% | 54.3%   | 53.1%   | 4.0%          | 12.0%        |
| gemma3:12b                                |        1 | 100 |   50 |    5 |   45 |    0 | 55.0%      | 52.6%       | 100.0%   | 69.0% | n/a     | n/a     | n/a           | n/a          |
| llava                                     |        1 | 100 |   10 |   33 |   17 |   40 | 43.0%      | 37.0%       | 20.0%    | 26.0% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model |        1 | 100 |   48 |    0 |   50 |    2 | 48.0%      | 49.0%       | 96.0%    | 64.9% | 52.7%   | 52.9%   | 6.0%          | 12.0%        |

### dataset_100

_image, 100 item(s) (53 DEEPFAKE / 47 REAL), 5 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Organika/sdxl-detector                    |        1 | 100 |   45 |   37 |   10 |    8 | 82.0%      | 81.8%       | 84.9%    | 83.3% | 91.0%   | 92.9%   | 64.2%         | 69.8%        |
| dima806/deepfake_vs_real_image_detection  |        1 | 100 |   14 |   40 |    7 |   39 | 54.0%      | 66.7%       | 26.4%    | 37.8% | 51.8%   | 55.4%   | 1.9%          | 9.4%         |
| gemma3:12b                                |        1 | 100 |   28 |   35 |   12 |   25 | 63.0%      | 70.0%       | 52.8%    | 60.2% | n/a     | n/a     | n/a           | n/a          |
| llava                                     |        1 | 100 |   16 |   38 |    9 |   37 | 54.0%      | 64.0%       | 30.2%    | 41.0% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model |        1 | 100 |   53 |    2 |   45 |    0 | 55.0%      | 54.1%       | 100.0%   | 70.2% | 57.0%   | 57.4%   | 7.5%          | 7.5%         |

### dataset_53

_image, 53 item(s) (41 DEEPFAKE / 12 REAL), 5 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1    | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:------|:--------|:--------|:--------------|:-------------|
| Organika/sdxl-detector                    |        1 |  53 |   25 |   10 |    2 |   16 | 66.0%      | 92.6%       | 61.0%    | 73.5% | 56.9%   | 82.9%   | n/a           | 0.0%         |
| dima806/deepfake_vs_real_image_detection  |        1 |  53 |    6 |   10 |    2 |   35 | 30.2%      | 75.0%       | 14.6%    | 24.5% | 18.3%   | 71.1%   | n/a           | 0.0%         |
| gemma3:12b                                |        1 |  53 |   29 |    0 |   12 |   12 | 54.7%      | 70.7%       | 70.7%    | 70.7% | n/a     | n/a     | n/a           | n/a          |
| llava                                     |        1 |  53 |   24 |    7 |    5 |   17 | 58.5%      | 82.8%       | 58.5%    | 68.6% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model |        1 |  53 |   41 |    2 |   10 |    0 | 81.1%      | 80.4%       | 100.0%   | 89.1% | 100.0%  | 100.0%  | n/a           | 100.0%       |

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

_audio, 100 item(s) (49 DEEPFAKE / 51 REAL), 3 model(s). Repeat runs of a model are pooled into one row._

| model                                     |   n_runs |   n |   tp |   tn |   fp |   fn | accuracy   | precision   | recall   | f1   | auroc   | auprc   | tpr@fpr0.05   | tpr@fpr0.1   |
|:------------------------------------------|---------:|----:|-----:|-----:|-----:|-----:|:-----------|:------------|:---------|:-----|:--------|:--------|:--------------|:-------------|
| Hemgg/Deepfake-audio-detection            |        1 | 100 |    0 |   51 |    0 |   49 | 51.0%      | n/a         | 0.0%     | n/a  | 45.8%   | 45.9%   | 4.1%          | 6.1%         |
| MelodyMachine/Deepfake-audio-detection-V2 |        1 | 100 |    0 |   51 |    0 |   49 | 51.0%      | n/a         | 0.0%     | n/a  | 42.5%   | 48.4%   | 6.1%          | 8.2%         |
| mo-thecreator/Deepfake-audio-detection    |        1 | 100 |    0 |   51 |    0 |   49 | 51.0%      | n/a         | 0.0%     | n/a  | 22.8%   | 36.9%   | 2.0%          | 2.0%         |

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
| Hemgg/Deepfake-audio-detection            | huggingface | all (3)   | audio        |            3 |        3 | 300 |   82 |   82 |   66 |   70 | 54.7%      | 55.4%       | 53.9%    | 54.7% | 55.7%   | 57.2%   | 10.5%         | 16.4%        |
| MelodyMachine/Deepfake-audio-detection-V2 | huggingface | all (3)   | audio        |            3 |        3 | 300 |   17 |  119 |   29 |  135 | 45.3%      | 37.0%       | 11.2%    | 17.2% | 46.6%   | 46.7%   | 1.3%          | 3.3%         |
| mo-thecreator/Deepfake-audio-detection    | huggingface | all (3)   | audio        |            3 |        3 | 300 |   72 |  101 |   47 |   80 | 57.7%      | 60.5%       | 47.4%    | 53.1% | 55.4%   | 55.9%   | 4.6%          | 11.8%        |
| Organika/sdxl-detector                    | huggingface | all (4)   | image        |            4 |        4 | 353 |   78 |  130 |   29 |  116 | 58.9%      | 72.9%       | 40.2%    | 51.8% | 65.0%   | 72.4%   | 19.1%         | 25.8%        |
| dima806/deepfake_vs_real_image_detection  | huggingface | all (4)   | image        |            4 |        4 | 353 |   74 |  145 |   14 |  120 | 62.0%      | 84.1%       | 38.1%    | 52.5% | 71.1%   | 78.1%   | 30.4%         | 39.7%        |
| gemma3:12b                                | ollama      | all (4)   | image        |            4 |        4 | 353 |  130 |   79 |   80 |   64 | 59.2%      | 61.9%       | 67.0%    | 64.4% | n/a     | n/a     | n/a           | n/a          |
| llava                                     | ollama      | all (4)   | image        |            4 |        4 | 353 |   76 |  109 |   50 |  118 | 52.4%      | 60.3%       | 39.2%    | 47.5% | n/a     | n/a     | n/a           | n/a          |
| prithivMLmods/Deep-Fake-Detector-v2-Model | huggingface | all (4)   | image        |            4 |        4 | 353 |  145 |    5 |  154 |   49 | 42.5%      | 48.5%       | 74.7%    | 58.8% | 36.8%   | 48.0%   | 0.0%          | 3.6%         |
| Vansh180/VideoMae-ffc23-deepfake-detector | huggingface | all (2)   | video        |            2 |        2 | 206 |   66 |   39 |   64 |   37 | 51.0%      | 50.8%       | 64.1%    | 56.7% | 50.0%   | 50.2%   | 2.9%          | 9.7%         |

## Coverage

- Scored 2871/2871 items that carried both a label and a prediction.
- 706 item(s) had no fake_score, so AUROC/AUPRC/TPR@FPR are n/a for them. Ollama models do not report a score, so they only get the hard metrics.
- TPR@FPR is the highest true positive rate reachable at any threshold that stays within the given false positive budget, so 0% is a real measurement of a model that catches nothing without false alarms. It is n/a only when the budget is finer than the dataset can express (1/n with n negatives, here about 0.00).
