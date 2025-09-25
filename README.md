# PhysUniBench

**PhysUniBench: An Undergraduate-Level Physics Reasoning Benchmark for Multimodal Models**

PhysUniBench is a large-scale multimodal benchmark specifically designed to evaluate the advanced reasoning capabilities of MLLMs on undergraduate-level physics problems. It offers a diverse set of diagram-paired QA and MCQ physics questions.

---

##  Overview

![Overview](assets/images/overview.png)

PhysUniBench includes diverse multimodal physics questions that challenge models in both symbolic and visual reasoning.

---

##  Subfield Distribution

<h3>Subfield Distribution</h3>

<img src="assets/images/distribution.png" alt="Distribution" width="600"/>

**PhysUniBench** is the first large-scale multimodal benchmark designed to evaluate the capabilities of Multimodal Large Language Models (MLLMs) in solving undergraduate-level physics problems that require both visual and symbolic reasoning.

The benchmark contains **3,304 human-verified questions**, each paired with a relevant diagram. It covers **eight core subfields** of physics:

- Classical Mechanics  
- Electromagnetism  
- Optics  
- Molecular, Atomic & Subatomic Physics  
- Thermodynamics  
- Quantum Mechanics  
- Solid-State Physics  
- Relativity

Each problem is labeled with a **difficulty level (1–5)** and is available in both **multiple-choice (MCQ)** and **open-ended (OE)** formats. All questions are sourced from authentic undergraduate curricula and are available in **both English and Chinese**, enabling multilingual evaluation.

Unlike previous benchmarks that focus on text-only reasoning, PhysUniBench emphasizes **multimodal problem solving**, where models must interpret diagrams, understand complex physics concepts, and perform symbolic reasoning in tandem.

We evaluate several state-of-the-art MLLMs, including **GPT-4o, Claude-3.5-Sonnet, Qwen2.5-VL, InternVL-3, and Gemini-2.5**, and find that even the best models achieve **only ~26.5% accuracy** on open-ended questions—indicating substantial room for improvement in physics reasoning under visual and scientific constraints.

**PhysUniBench** offers a rigorous, diverse, and multilingual testbed to push forward the development of scientific AI and multimodal reasoning systems.



