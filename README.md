# PhysUniBench

**PhysUniBench: An Undergraduate-Level Physics Reasoning Benchmark for Multimodal Models**

PhysUniBench is a large-scale multimodal benchmark specifically designed to evaluate the advanced reasoning capabilities of MLLMs on undergraduate-level physics problems. It provides a challenging and diagnostic dataset that reflects the complexity and multimodal nature of real-world scientific problem solving.

---

## Key Features

- **3304 total physics problems**, all paired with diagrams:
  - **2057 open-ended QA questions**
  - **1247 multiple-choice questions (MCQs)**

- **Multimodal format**: Each problem includes an image + textual context.

- Covers **8 major subfields** of undergraduate physics:
  1. Electromagnetism & Electrodynamics  
  2. Classical Mechanics  
  3. Optics  
  4. Atomic, Molecular, and Subatomic Physics  
  5. Relativity  
  6. Solid-State Physics and Measurement  
  7. Thermodynamics  
  8. Quantum Mechanics

- All problems annotated with a difficulty level from 1 to 5.

---

## Dataset Statistics

| Metric                         | Value   |
|-------------------------------|---------|
| Total questions               | 3304    |
| MCQs                         | 1247    |
| Open-ended QA                | 2057    |
| Unique images                | 3304    |
| Avg. question length (tokens) | 150.7   |
| Avg. answer length (tokens)   | 441.9   |

---

## Benchmark Structure

PhysUniBench is split into:
- `benchmark/`: Code for loading and evaluating data.
- `models/`: Unified model APIs and judge functions.
- `results_*/`: Cached results and evaluation logs.
- `utils/`: Utility functions and expression matching.

We recommend starting from the evaluation scripts inside `script/` if you want to test new models.

---

## Access the Dataset

- 📁 **HuggingFace**: [PrismaX/PhysUniBench](https://huggingface.co/datasets/PrismaX/PhysUniBench)
- 📄 **arXiv Preprint**: _[link to be added]_  
- 🔗 **Demo Website**: [https://prismax-team.github.io/PhysUniBench](https://prismax-team.github.io/PhysUniBench)

---

## Installation

```bash
git clone https://github.com/PrismaX-Team/PhysUniBenchmark.git
cd PhysUniBenchmark




@misc{PhysUniBench2025,
  title={PhysUniBench: An Undergraduate-Level Physics Reasoning Benchmark for Multimodal Models},
  author={Lintao Wang and Encheng Su and Jiaqi Liu and Pengze Li and Peng Xia and Jiabei Xiao and Wenlong Zhang and Xinnan Dai and Mingyu Ding and Lei Bai and Wanli Ouyang and Shixiang Tang and Aoran Wang and Xinzhu Ma},
  year={2025},
  archivePrefix={arXiv},
  eprint={YOUR_ARXIV_ID},
  primaryClass={cs.CL}
}
