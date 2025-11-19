<h2 align="center">Magneto: Combining Small and Large Language Models<br>for Schema Matching</h2>

> Welcome to Magneto 🧲

This repository contains the codebase of our paper: [Magneto: Combining Small and Large Language Models for Schema Matching](https://arxiv.org/abs/2412.08194) (VLDB '25)

Magneto is an innovative framework designed to enhance schema matching (SM) by intelligently combining small, pre-trained language models (SLMs) with large language models (LLMs). Our approach is structured to be both cost-effective and broadly applicable.

The framework operates in two distinct phases:
- **Candidate Retrieval**: This phase involves using SLMs to quickly identify a manageable subset of potential matches from a vast pool of possibilities. Optional LLM-powered fine-tuning can be performed.
- **Match Reranking**: In this phase, LLMs take over to assess and reorder the candidates, simplifying the process for users to review and select the most suitable matches.

## Contents

* [Environment Setup](#environment-setup)
* [Code Structure](#code-structure)
* [Example Usage](#example-usage)
* [Citations](#citation)

## Environment Setup

### Clone the Repository

```bash
git clone https://github.com/VIDA-NYU/magneto-matcher.git
cd magneto-matcher
```

### Install Dependencies

```bash
conda create -n magneto python=3.10 -y
conda activate magneto
pip install --upgrade pip     # optional
pip install -r requirements.txt
```

### Data Preparation

The data folder contains the datasets used for data integration tasks. Download the data folder from [this Google Drive link](https://drive.google.com/drive/folders/19kCWQI0CWHs1ZW9RQEUSeK6nuXoA-5B7?usp=sharing) and place it in the `data` directory. Contents include:
- **`gdc`**: GDC benchmark from the paper. Contains ten tumor analysis study datasets to be matched to Genomics Data Commons (GDC) standards (also available on [Zenodo](https://zenodo.org/records/14963588): DOI 10.5281/zenodo.14963587).
- **`Valentine-datasets`**: Schema matching benchmark from [Valentine paper](https://delftdata.github.io/valentine/) (also available on [Zenodo](https://zenodo.org/records/5084605#.YOgWHBMzY-Q): DOI 10.5281/zenodo.5084605).
- **`synthetic`**: Synthetic data generated using `llm-aug` and `struct-aug` for LLM-based fine-tuning. You can use the provided JSON files directly or regenerate by modifying the underlying LLM model and other configurations in the [code](https://github.com/VIDA-NYU/magneto-matcher/blob/main/algorithms/magneto/finetune/data_generation/synthetic_data_gen.py). Processed data for synthetic match generation is located in the same folder under `unique_columns` directory.

### Download the fine-tuned model for GDC benchmark

This step is optional but required for `MagnetoFT` and `MagnetoFTGPT`. Download the fine-tuned model of your choice from [this Google Drive link](https://drive.google.com/drive/folders/1vlWaTm4rpEH4hs-Kq3mhSfTyffhDEp6P?usp=sharing) and place it in the `models` directory.

### Set the Environment Variable
This step is optional but required for `MagnetoGPT` and `MagnetoFTGPT`. Set the `OPENAI_API_KEY` environment variable using the following commands based on your operating system:
#### For Windows:
```bash
set OPENAI_API_KEY=your_openai_api_key_here
```
#### For macOS/Linux:
```bash
export OPENAI_API_KEY=your_api_key_here
```
To use `LLaMA3.3` as the LLM reranker, you can also set up `LLAMA_API_KEY` accordingly.

## Code Structure
> note that batched benchmark on baseline methods are on this [repo](https://github.com/VIDA-NYU/data-harmonization-benchmark).

```bash
|-- algorithm
    |-- magneto # code for Magneto
        |-- finetune # code for Magneto FT
        |-- magneto # Magneto core
    |-- topk_metrics.py # Introducing Recall @ topk
|-- experiments
    |-- ablations # code for ablation study
    |-- benchmark # code for benchmark study, note that batched benchmark on baseline methods are on this [repo](https://github.com/VIDA-NYU/data-harmonization-benchmark)
|-- results_visualization # notebooks for results visualization
```

## Example Usage
To reproduce the GDC benchmark results, you can run the following command:
```bash
python experiments/benchmarks/gdc_benchmark.py --mode [MODE] --embedding_model [EMBEDDING_MODEL] --llm_model [LLM_MODEL]
```
- `[MODE]`: Specifies the operational mode. Options include: `header-value-default`, `header-value-repeat`, and `header-value-verbose`.
- `[EMBEDDING_MODEL]`: Selects the pre-trained language model to use as the retriever. Available options are `mpnet`, `roberta`, `e5`, `arctic`, or `minilm`. The default model is `mpnet`.
- `[LLM_MODEL]`: Specifies the llm-based reranker. Current options are `gpt-4o-mini` or `llama3.3-70b`.

To reproduce the Valentine benchmark results, you can run the following command:
```bash
python experiments/benchmarks/valentine_benchmark.py --mode [MODE] --dataset [DATASET]
```
where `[MODE]` is similar to the GDC benchmark and `[DATASET]` can be one of the following:
- `chembl`
- `magellan`
- `opendata`
- `tpc`
- `wikidata`

You can also change other Magneto configurations in the corresponding benchmark file.

## Citation

If you use Magneto in your research or project, please cite our paper:

```bibtex
@article{10.14778/3742728.3742757,
  author = {Liu, Yurong and Pena, Eduardo H. M. and Santos, A\'{e}cio and Wu, Eden and Freire, Juliana},
  title = {Magneto: Combining Small and Large Language Models for Schema Matching},
  year = {2025},
  issue_date = {April 2025},
  publisher = {VLDB Endowment},
  volume = {18},
  number = {8},
  issn = {2150-8097},
  url = {https://doi.org/10.14778/3742728.3742757},
  doi = {10.14778/3742728.3742757},
  journal = {Proc. VLDB Endow.},
  month = apr,
  pages = {2681--2694},
  numpages = {14}
}
```
