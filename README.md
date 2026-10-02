# Mini-Jev: Support Inbox Triage

A lightweight, zero-shot customer support triage dashboard built with [Streamlit](https://streamlit.io/) and Hugging Face's [Transformers](https://huggingface.co/docs/transformers).

Mini-Jev is inspired by **Jev** (TypeSafe AI)—designed around the core philosophy: *"It only decides, it never writes."* Rather than relying on heavyweight generative text models to draft replies, Mini-Jev focuses purely on fast, calibrated, structured decision-making for inbox automation.

**Live Demo**: [https://jev-mini-lsoslxry3txvvooarziriy.streamlit.app/](https://jev-mini-lsoslxry3txvvooarziriy.streamlit.app/)

---

## Inspired by Jev

Traditional Large Language Models (LLMs) are often over-engineered for triage workflows: they generate unstructured text, suffer from latency, hallucinate, and require fragile JSON schema extraction. 

**Jev** introduced a "System One" decision model where AI outputs typed decisions with calibrated confidence rather than prose. Mini-Jev implements this paradigm using open-source zero-shot Natural Language Inference (NLI):

- **Decision over Generation**: The system never drafts responses or generates text—it strictly decides routing, sentiment, and urgency.
- **Three Core Primitives**:
  - `choice(text, options)`: Evaluates a message against candidate categories (e.g. routing destinations) and outputs calibrated probabilities.
  - `score(text, levels)`: Evaluates a message along an ordered multi-tier scale (e.g. urgency from 1 to 3).
  - `noul(text, yes, no)`: Performs binary decision evaluation (e.g. angry vs. calm customer sentiment).
- **Confidence-Gated Handoff**: If the top decision confidence does not meet a configurable threshold, the ticket is safely deferred to a human agent rather than making an unconfident automatic choice.

---

## Features

- **Department Auto-Routing**: Categorizes incoming customer messages using zero-shot classification across categories:
  - `billing`
  - `technical problem`
  - `sales question`
  - `thank you`
- **Confidence Thresholding**: Set an auto-route confidence threshold (default 80%). If confidence falls below this threshold, the ticket is flagged to **send to a human** with the model's best guess.
- **Visual Confidence Distribution**: Interactive bar chart displaying probability scores across all routing categories.
- **Frustration & Emotion Detection**: Detects customer sentiment (`angry or frustrated` vs. `calm or happy`) using the `noul` primitive to identify escalations early.
- **Urgency Rating (1–3 Scale)**: Computes a weighted urgency score via the `score` primitive based on time sensitivity:
  - `1.0` – Can wait a week
  - `2.0` – Should be handled today
  - `3.0` – Needs action right now

---

## Tech Stack & Model

- **Frontend**: [Streamlit](https://streamlit.io/)
- **NLP / ML Framework**: [Hugging Face Transformers](https://huggingface.co/transformers), [PyTorch](https://pytorch.org/)
- **Zero-Shot Classification Model**: [`MoritzLaurer/deberta-v3-base-zeroshot-v2.0`](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0) (cached locally using `@st.cache_resource` for fast subsequent queries)

---

## Getting Started

### Prerequisites

- Python 3.9+ installed on your system.
- Standard virtual environment tools (`venv` or `conda`).

### 1. Clone the Repository

```bash
git clone https://github.com/harshsomankar123-tech/jev-mini.git
cd jev-mini
```

### 2. Set Up a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

### 3. Install Dependencies

Install the requirements specifying the CPU wheels for PyTorch as configured in `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note**: On initial run, the DeBERTa model weights (~860 MB) will be downloaded from Hugging Face Hub and cached locally.

### 4. Run the Application

```bash
streamlit run app.py
```

Once running, access the dashboard in your web browser at `http://localhost:8501`.

---

## Usage

1. **Enter Message**: Paste or type the customer inquiry into the text area.
2. **Set Confidence Threshold**: Use the slider (0.50 – 0.99) to define the minimum confidence level required for automatic routing.
3. **Click "Decide"**:
   - Inspect whether the ticket is marked for **Auto-route** or **Send to a human**.
   - Review category probabilities in the distribution chart.
   - Check the **How angry** sentiment metric and the **How urgent** priority score.

---

## Customization

You can easily adapt Mini-Jev to your organization's domain by editing [app.py](file:///Users/harshsomankar/.gemini/antigravity/scratch/jev-mini/app.py):

- **Update Routing Categories**: Modify the `ROUTES` list:
  ```python
  ROUTES = [
      "billing",
      "technical problem",
      "sales question",
      "thank you",
      "account cancellation",
      "feature request"
  ]
  ```
- **Change Urgency Tiers**: Adjust `URGENCY` categories or hypothesis templates in `score()`.
- **Swap the Underlying Model**: Replace `"MoritzLaurer/deberta-v3-base-zeroshot-v2.0"` with any other zero-shot classification model (e.g. `facebook/bart-large-mnli`).

---

## License

This project is licensed under the [MIT License](LICENSE) (or your preferred repository license).
