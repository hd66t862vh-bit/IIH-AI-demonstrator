import json
import os

from openai import OpenAI


MODEL_NAME = "gpt-4o-mini"
TRANSCRIPTION_MODEL = "gpt-4o-transcribe"


SYSTEM_PROMPT = """
You are a strict information-extraction component in a SYNTHETIC-ONLY
demonstrator for a papilloedema / possible idiopathic intracranial
hypertension workflow.

Your task is extraction only.

You must not:
- diagnose papilloedema, IIH, CVST, or any other condition;
- determine urgency or recommend management;
- infer whether visual function is threatened;
- infer whether a clinician has confirmed papilloedema;
- interpret imaging or fundus/OCT images;
- prescribe, admit, discharge, or transfer care;
- create facts that are absent, unclear, or contradictory.

Rules:
1. Extract only facts explicitly stated in the supplied synthetic note.
2. If a fact is absent, unclear, or contradictory, return null or Unknown.
3. Never convert missing information into No, Normal, Completed, or safe.
4. Papilloedema can be Confirmed or Not_confirmed only if a clinician
   confirmation/non-confirmation is explicitly stated.
5. Visual-function threat can be Yes, Possible, or No only if it is
   explicitly documented in the note. Do not infer it from symptoms, visual
   acuity, visual fields, OCT, disc appearance, or demographics.
6. Imaging status can be Completed_adequate only when completion/adequacy is
   explicitly stated. Do not assume that "MRI normal" guarantees adequacy
   unless the note explicitly identifies it as a completed/adequate study.
7. For every non-null/non-Unknown extracted fact, include one exact
   supporting quote copied verbatim from the synthetic note.
8. Use only values permitted by the JSON schema.
9. Do not request, use, or output real patient identifiers.
"""


EXTRACTION_SCHEMA = {
    "name": "iih_synthetic_note_extraction",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "patient_age_years": {
                "type": ["integer", "null"],
                "description": (
                    "Age in years only if explicitly stated; otherwise null."
                ),
            },
            "bp_systolic_mmhg": {
                "type": ["integer", "null"],
                "description": (
                    "Systolic blood pressure only if explicitly stated as a "
                    "measurement; otherwise null."
                ),
            },
            "bp_diastolic_mmhg": {
                "type": ["integer", "null"],
                "description": (
                    "Diastolic blood pressure only if explicitly stated as a "
                    "measurement; otherwise null."
                ),
            },
            "visual_acuity_status": {
                "type": "string",
                "enum": [
                    "Completed",
                    "Unable_with_reason",
                    "Not_done",
                    "Unknown",
                ],
            },
            "pupil_exam_status": {
                "type": "string",
                "enum": [
                    "Completed",
                    "Unable_with_reason",
                    "Not_done",
                    "Unknown",
                ],
            },
            "iop_status": {
                "type": "string",
                "enum": [
                    "Completed",
                    "Unable_with_reason",
                    "Not_done",
                    "Unknown",
                ],
            },
            "formal_perimetry_status": {
                "type": "string",
                "enum": [
                    "Completed",
                    "Unable_with_reason",
                    "Not_done",
                    "Pending",
                    "Unknown",
                ],
            },
            "dilated_fundus_status": {
                "type": "string",
                "enum": [
                    "Completed",
                    "Unable_with_reason",
                    "Not_done",
                    "Unknown",
                ],
            },
            "papilloedema_status": {
                "type": "string",
                "enum": [
                    "Confirmed",
                    "Not_confirmed",
                    "Uncertain",
                    "Unknown",
                ],
                "description": (
                    "Use Confirmed/Not_confirmed only with explicit clinician "
                    "documentation. Do not infer from image descriptions."
                ),
            },
            "papilloedema_reviewer_level": {
                "type": "string",
                "enum": [
                    "ED_clinician",
                    "AO",
                    "Consultant",
                    "Experienced_clinician",
                    "Unknown",
                ],
            },
            "visual_function_threatened": {
                "type": "string",
                "enum": [
                    "Yes",
                    "Possible",
                    "No",
                    "Unknown",
                ],
            },
            "brain_imaging_status": {
                "type": "string",
                "enum": [
                    "Not_done",
                    "Pending",
                    "Completed_adequate",
                    "Completed_inadequate",
                    "Unknown",
                ],
            },
            "brain_imaging_modality": {
                "type": "string",
                "enum": [
                    "MRI",
                    "CT_then_MRI_pending",
                    "CT_then_MRI_complete",
                    "Other",
                    "Unknown",
                ],
            },
            "secondary_structural_or_meningeal_pathology": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No",
                    "Unknown",
                ],
            },
            "venography_status": {
                "type": "string",
                "enum": [
                    "Not_done",
                    "Pending",
                    "Completed_adequate",
                    "Completed_inadequate",
                    "Unknown",
                ],
            },
            "cerebral_venous_sinus_thrombosis": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No",
                    "Unknown",
                ],
            },
            "fbc_status": {
                "type": "string",
                "enum": [
                    "Not_done",
                    "Pending",
                    "Normal",
                    "Abnormal",
                    "Unknown",
                ],
            },
            "lp_status": {
                "type": "string",
                "enum": [
                    "Not_done",
                    "Pending",
                    "Completed",
                    "Contraindicated",
                    "Formally_deferred_by_senior",
                    "Unknown",
                ],
            },
            "lp_opening_pressure_cm_csf": {
                "type": ["number", "null"],
            },
            "lp_technique_valid": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No",
                    "Unknown",
                ],
            },
            "minimum_csf_tests_complete": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No",
                    "Unknown",
                ],
            },
            "csf_contents_status": {
                "type": "string",
                "enum": [
                    "Normal",
                    "Abnormal",
                    "Pending",
                    "Unknown",
                ],
            },
            "secondary_cause_screen_complete": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No",
                    "Unknown",
                ],
            },
            "secondary_cause_identified": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No",
                    "Unknown",
                ],
            },
            "evidence": {
                "type": "array",
                "description": (
                    "Evidence for all non-null/non-Unknown extracted facts. "
                    "Quotes must be verbatim text from the synthetic note."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "field": {
                            "type": "string",
                        },
                        "value": {
                            "type": [
                                "string",
                                "number",
                                "integer",
                            ],
                        },
                        "quote": {
                            "type": "string",
                        },
                    },
                    "required": [
                        "field",
                        "value",
                        "quote",
                    ],
                },
            },
        },
        "required": [
            "patient_age_years",
            "bp_systolic_mmhg",
            "bp_diastolic_mmhg",
            "visual_acuity_status",
            "pupil_exam_status",
            "iop_status",
            "formal_perimetry_status",
            "dilated_fundus_status",
            "papilloedema_status",
            "papilloedema_reviewer_level",
            "visual_function_threatened",
            "brain_imaging_status",
            "brain_imaging_modality",
            "secondary_structural_or_meningeal_pathology",
            "venography_status",
            "cerebral_venous_sinus_thrombosis",
            "fbc_status",
            "lp_status",
            "lp_opening_pressure_cm_csf",
            "lp_technique_valid",
            "minimum_csf_tests_complete",
            "csf_contents_status",
            "secondary_cause_screen_complete",
            "secondary_cause_identified",
            "evidence",
        ],
    },
}


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. In Terminal, set it before starting "
            "Streamlit. Never write the key inside Python files."
        )

    return OpenAI(api_key=api_key)


def extract_note_with_llm(note):
    """
    Extract explicitly stated facts from a synthetic free-text referral note.

    This function does not make clinical decisions. It produces structured
    candidate facts and verbatim supporting quotes for clinician review.
    """

    if not note or not note.strip():
        raise ValueError(
            "Enter a synthetic referral note before extracting facts."
        )

    client = get_openai_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    "Extract the permitted structured facts from this "
                    "SYNTHETIC referral note only. Return JSON that follows "
                    "the requested schema.\n\n"
                    f"{note}"
                ),
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": EXTRACTION_SCHEMA["name"],
                "strict": True,
                "schema": EXTRACTION_SCHEMA["schema"],
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "The language model returned no structured extraction."
        )

    return json.loads(content)


def transcribe_synthetic_audio(audio_file):
    """
    Transcribe synthetic demonstration audio only.

    Do not submit real patient, identifying, confidential, or clinical audio.
    The returned transcript must be reviewed before LLM extraction or
    deterministic workflow evaluation.
    """

    if audio_file is None:
        raise ValueError(
            "Record or upload synthetic audio before transcribing."
        )

    client = get_openai_client()

    audio_file.name = "synthetic_referral_audio.wav"

    transcription = client.audio.transcriptions.create(
        model=TRANSCRIPTION_MODEL,
        file=audio_file,
        language="en",
        prompt=(
            "This is synthetic ophthalmology referral dictation. "
            "Potential terms include papilloedema, idiopathic intracranial "
            "hypertension, IIH, neuro-ophthalmology, MRV, CT venogram, "
            "CVST, lumbar puncture, opening pressure, CSF, visual acuity, "
            "perimetry, and OCT."
        ),
    )

    return transcription.text
