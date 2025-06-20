# PhysUniBench

**PhysUniBench: An Undergraduate-Level Physics Reasoning Benchmark for Multimodal Models**

PhysUniBench is a large-scale multimodal benchmark specifically designed to evaluate the advanced reasoning capabilities of MLLMs on undergraduate-level physics problems. It provides a challenging and diagnostic dataset that reflects the complexity and multimodal nature of real-world scientific problem solving.

---

## Benchmark Overview

![Overview](assets/images/overview.png)

PhysUniBench includes diverse multi-modal physics questions paired with diagrams, covering symbolic, visual, and conceptual reasoning.

---

## Subfield Distribution

![Distribution](assets/images/distribution.png)

Each problem is annotated with subject and difficulty, spanning 8 major subfields of university physics.

---


## Experimental Results

![Radar Chart](assets/images/radar.png)

The above chart shows model accuracy across subfields for MCQ and QA tasks using several leading MLLMs.

---

## Dataset Structure

PhysUniBench includes:

- `benchmark/`: Dataset loaders and evaluation scripts.
- `models/`: Unified model interface and judge logic.
- `results_*/`: Cached prediction results (optional).
- `assets/images/`: Benchmark visualizations.
- `README.md`: Overview and usage.

---

## Physics Subfields Covered

1. Electromagnetism and Electrodynamics  
2. Classical Mechanics  
3. Optics  
4. Atomic, Molecular, and Subatomic Physics  
5. Relativity  
6. Solid-State Physics and Measurement  
7. Thermodynamics  
8. Quantum Mechanics

---

