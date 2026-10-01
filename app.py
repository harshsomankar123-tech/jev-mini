
import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_model():
    return pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
    )


classifier = load_model()

ROUTES = [
    "billing",
    "technical problem",
    "sales question",
    "thank you"
]


def choice(text, options, template="This message is about {}."):
    r = classifier(
        text,
        candidate_labels=options,
        hypothesis_template=template
    )
    return {
        label: round(p, 3)
        for label, p in zip(r["labels"], r["scores"])
    }


URGENCY = [
    "it can wait a week",
    "it should be handled today",
    "it needs action right now"
]


def score(text, levels, template="For support, {}."):
    probs = choice(text, levels, template)
    value = sum(
        (levels.index(level) + 1) * p
        for level, p in probs.items()
    )
    return round(value, 2)


def noul(text, yes, no, template="The customer is {}."):
    return choice(text, [yes, no], template)


st.title("Mini-Jev: support inbox triage")

st.caption(
    "A free, weaker imitation of Jev. "
    "It only decides, it never writes."
)


message = st.text_area(
    "Customer message",
    "I was charged twice this month and nobody is answering."
)


threshold = st.slider(
    "Auto-route only if at least this sure",
    0.50,
    0.99,
    0.80
)


if st.button("Decide"):

    route = choice(message, ROUTES)
    top, p = next(iter(route.items()))

    if p >= threshold:
        st.success(
            f"Auto-route to {top} ({p:.0%} sure)"
        )
    else:
        st.warning(
            f"Send to a human. "
            f"Best guess: {top}, only {p:.0%} sure"
        )

    st.bar_chart(route)

    angry = noul(
        message,
        "angry or frustrated",
        "calm or happy"
    )

    st.metric(
        "How angry",
        f"{angry['angry or frustrated']:.0%}"
    )

    st.metric(
        "How urgent (1 to 3)",
        score(message, URGENCY)
    )
