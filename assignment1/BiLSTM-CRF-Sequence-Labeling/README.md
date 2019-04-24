# BiLSTM-CRF Sequence Labeling

## Requirement

- keras
- keras-contrib
- pickle
- h5py

## Run a demo

- Download the data and the pretrained model first. 

https://share.weiyun.com/5UP3jt9

- Segmentation:

```shell
python3 demo.py --data_dir data/seg --model_dir model/seg --mode seg
```

- Named Entity Recognition

```shell
python3 demo.py --data_dir data/ner --model_dir model/ner --mode ner
```

## Training 

You have to download data first.

- Train a segmentation model

```shell
python3 train.py --data_dir data/pos --model_dir model/pos
```

## Predict

- segmentation

```
python3 predict.py
```

