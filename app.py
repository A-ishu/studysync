import gradio as gr
import re

def fallacy_and_bias_xray(study_text):
    if not study_text or not study_text.strip():
        return "Please provide valid text / ദയവായി ടെക്സ്റ്റ് നൽകുക / कृपया टेक्स्ट दर्ज करें"

    text_lower = study_text.lower()
    words = text_lower.split()
    word_count = len(words)

    hasty_generalization_words = [
        "always", "never", "everyone", "none", "all", "everybody", "nobody", 
        "എല്ലാവരും", "ഒരിക്കലും", "എപ്പോഴും", "सबको", "कभी_नहीं", "हमेशा"
    ]
    bias_trigger_words = [
        "obviously", "clearly", "undeniably", "absurd", "foolish", 
        "തീർച്ചയായും", "വ്യക്തം", "स्पष्ट", "निःसंशय"
    ]

    found_generalizations = [word for word in hasty_generalization_words if word in words]
    found_biases = [word for word in bias_trigger_words if word in words]

    sentences = [s.strip() for s in re.split(r'[.!?։।]', study_text) if s.strip()]
    circular_flag = False
    if len(sentences) >= 2:
        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                if sentences[i] == sentences[j]:
                    circular_flag = True

    penalties = (len(set(found_generalizations)) * 10) + (len(set(bias_trigger_words)) * 10) + (25 if circular_flag else 0)
    critical_score = max(0, 100 - penalties)

    report = f"""
    STUDY-SYNC CRITICAL THINKING AUDIT REPORT:
    --------------------------------------------------
    • Total Words: {word_count}
    • Total Sentences: {len(sentences)}
    • Critical Thinking Score: {critical_score} / 100
    • Detected Hasty Generalizations: {list(set(found_generalizations)) if found_generalizations else 'None'}
    • Detected Bias Triggers: {list(set(found_biases)) if found_biases else 'None'}
    • Circular Reasoning Flag: {'Yes (Found)' if circular_flag else 'None Detected'}
    • Audit Status: {'Needs Revision' if critical_score < 80 else 'Strong Argumentation'}
    """
    return report

app = gr.Interface(
    fn=fallacy_and_bias_xray,
    inputs=gr.Textbox(lines=6, label="Enter your study notes or essay here (Malayalam, Hindi, English):"),
    outputs=gr.Textbox(label="X-Ray Audit Results"),
    title="StudySync: Logic Fallacy & Bias X-Ray",
    description="Analyze notes for logical flaws, generalizations, and cognitive biases across multiple languages."
)

app.launch(server_name="0.0.0.0", server_port=7860)
  
