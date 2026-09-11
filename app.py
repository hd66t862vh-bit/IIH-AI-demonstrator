import json

import streamlit as st

from llm_extractor import (
    extract_note_with_llm,
    transcribe_synthetic_audio,
)
from rule_engine import ACTIONS, evaluate


st.set_page_config(
    page_title="IIH AI Demonstrator",
    page_icon="🧠",
    layout="wide",
)


def parse_integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def blank_case():
    """
    Default blank synthetic intake state.

    No clinical facts are pre-populated. Values remain Unknown/blank until
    entered manually, extracted from a synthetic note, dictated, or loaded
    from an explicit synthetic demonstration case.
    """

    return {
        "synthetic_case_id": "SYN-MANUAL-001",
        "age_entered": "",

        "visual_acuity_status": "Unknown",
        "pupil_exam_status": "Unknown",
        "iop_status": "Unknown",
        "formal_perimetry_status": "Unknown",
        "dilated_fundus_status": "Unknown",

        "papilloedema_status": "Unknown",
        "papilloedema_reviewer_level": "Unknown",
        "visual_function_threatened": "Unknown",

        "bp_systolic_text": "",
        "bp_diastolic_text": "",

        "cranial_nerve_exam_status": "Unknown",
        "focal_neurological_signs": "Unknown",
        "reduced_consciousness": "Unknown",
        "meningism": "Unknown",
        "seizure": "Unknown",
        "other_cranial_nerve_abnormality": "Unknown",

        "brain_imaging_status": "Unknown",
        "brain_imaging_modality": "Unknown",
        "secondary_structural_or_meningeal_pathology": "Unknown",
        "radiology_interpretation_uncertain": "Unknown",

        "venography_status": "Unknown",
        "cerebral_venous_sinus_thrombosis": "Unknown",

        "fbc_status": "Unknown",

        "lp_status": "Unknown",
        "lp_technique_valid": "Unknown",
        "lp_opening_pressure_text": "",

        "minimum_csf_tests_complete": "Unknown",
        "csf_contents_status": "Unknown",

        "secondary_cause_screen_complete": "Unknown",
        "secondary_cause_identified": "Unknown",

        "iih_criteria_complete": "Unknown",
        "severe_visual_loss_within_4_weeks": "Unknown",
        "vision_worsening_over_days": "Unknown",
        "typical_profile_flag": "Unknown",

        "visual_function_stable": "Unknown",
        "baseline_disc_docs_available": "Unknown",
        "pseudo_followup_booked": "Unknown",
        "pseudo_followup_weeks_text": "",
        "return_precautions_given": "Unknown",

        "noph_plan_status": "Unknown",
        "active_plan_version": "",
        "callback_requested_due": "Unknown",
        "clinical_deterioration_since_plan": "Unknown",
        "unexpected_result_since_plan": "Unknown",
        "ownership_or_plan_unclear": "Unknown",

        "clinical_owner_documented": "Unknown",
        "disposition_approved": "Unknown",

        "reviewer_name": "",
        "reviewer_role": "Select role",
        "clinician_reviewed_output": False,
        "decision_mode": "Accept workflow output",
        "override_reason": "Select reason",
        "override_rationale": "",

        "synthetic_referral_note": "",
    }


def base_case():
    """
    Fully populated synthetic baseline used only to create demo scenarios.
    This must never be used as the default free-text/dictation intake state.
    """

    return {
        "synthetic_case_id": "SYN-BASELINE",
        "age_entered": "29",

        "visual_acuity_status": "Completed",
        "pupil_exam_status": "Completed",
        "iop_status": "Completed",
        "formal_perimetry_status": "Completed",
        "dilated_fundus_status": "Completed",

        "papilloedema_status": "Confirmed",
        "papilloedema_reviewer_level": "AO",
        "visual_function_threatened": "No",

        "bp_systolic_text": "130",
        "bp_diastolic_text": "80",

        "cranial_nerve_exam_status": "Completed",
        "focal_neurological_signs": "No",
        "reduced_consciousness": "No",
        "meningism": "No",
        "seizure": "No",
        "other_cranial_nerve_abnormality": "No",

        "brain_imaging_status": "Completed_adequate",
        "brain_imaging_modality": "MRI",
        "secondary_structural_or_meningeal_pathology": "No",
        "radiology_interpretation_uncertain": "No",

        "venography_status": "Completed_adequate",
        "cerebral_venous_sinus_thrombosis": "No",

        "fbc_status": "Normal",

        "lp_status": "Completed",
        "lp_technique_valid": "Yes",
        "lp_opening_pressure_text": "31",

        "minimum_csf_tests_complete": "Yes",
        "csf_contents_status": "Normal",

        "secondary_cause_screen_complete": "Yes",
        "secondary_cause_identified": "No",

        "iih_criteria_complete": "Yes",
        "severe_visual_loss_within_4_weeks": "No",
        "vision_worsening_over_days": "No",
        "typical_profile_flag": "Typical",

        "visual_function_stable": "Yes",
        "baseline_disc_docs_available": "Yes",
        "pseudo_followup_booked": "Yes",
        "pseudo_followup_weeks_text": "5",
        "return_precautions_given": "Yes",

        "noph_plan_status": "No_plan",
        "active_plan_version": "",
        "callback_requested_due": "No",
        "clinical_deterioration_since_plan": "No",
        "unexpected_result_since_plan": "No",
        "ownership_or_plan_unclear": "No",

        "clinical_owner_documented": "Yes",
        "disposition_approved": "No",

        "reviewer_name": "",
        "reviewer_role": "Select role",
        "clinician_reviewed_output": False,
        "decision_mode": "Accept workflow output",
        "override_reason": "Select reason",
        "override_rationale": "",

        "synthetic_referral_note": "",
    }


def demo_cases():
    cases = {}

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T03",
            "visual_function_threatened": "Possible",
        }
    )
    cases["T03 — Possible visual threat"] = {
        "expected": "A_IMMEDIATE_NOPH_VISUAL_THREAT",
        "description": (
            "Confirmed papilloedema with possible threatened visual function. "
            "Demonstrates immediate NOPH escalation while work-up continues."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T04",
            "bp_systolic_text": "190",
            "bp_diastolic_text": "122",
        }
    )
    cases["T04 — Hypertensive emergency flag"] = {
        "expected": "A_HYPERTENSIVE_EMERGENCY",
        "description": (
            "Markedly elevated BP demonstrates the alternate emergency "
            "pathway rather than uncomplicated IIH."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T05",
            "cerebral_venous_sinus_thrombosis": "Yes",
        }
    )
    cases["T05 — CVST / secondary venous pathway"] = {
        "expected": "A_SECONDARY_VENOUS_PATHWAY",
        "description": (
            "Causative venous pathology means this must not be labelled "
            "idiopathic."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T06",
            "venography_status": "Not_done",
        }
    )
    cases["T06 — Venography missing"] = {
        "expected": "A_URGENT_VENOGRAPHY",
        "description": (
            "Venography is missing after adequate structural imaging. "
            "The workflow stops before LP or IIH classification."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T07",
            "noph_plan_status": "No_plan",
        }
    )
    cases["T07 — Typical IIH candidate"] = {
        "expected": "A_TYPICAL_IIH_CANDIDATE",
        "description": (
            "Completed compatible synthetic work-up with typical profile. "
            "This remains a candidate state, not a final diagnosis."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T09",
            "lp_opening_pressure_text": "22",
        }
    )
    cases["T09 — Opening pressure below threshold"] = {
        "expected": "A_IIH_NOT_CONFIRMED",
        "description": (
            "Compatible presentation with lower opening pressure. "
            "Demonstrates specialist review for discordance."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T10",
            "csf_contents_status": "Abnormal",
        }
    )
    cases["T10 — Abnormal CSF"] = {
        "expected": "A_ALTERNATE_CSF_PATHWAY",
        "description": (
            "Abnormal CSF prevents idiopathic classification and activates "
            "an alternate diagnostic pathway."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T11",
            "papilloedema_status": "Not_confirmed",
            "papilloedema_reviewer_level": "AO",
            "pseudo_followup_booked": "No",
        }
    )
    cases["T11 — Pseudopap follow-up not booked"] = {
        "expected": "A_BOOK_PSEUDO_4_6W",
        "description": (
            "Stable non-confirmed papilloedema case with no documented "
            "follow-up booking."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T13",
            "noph_plan_status": "Active",
            "active_plan_version": "NOPH-PLAN-001",
            "callback_requested_due": "No",
            "clinical_deterioration_since_plan": "No",
            "unexpected_result_since_plan": "No",
            "ownership_or_plan_unclear": "No",
        }
    )
    cases["T13 — Active plan: duplicate contact suppressed"] = {
        "expected": "A_FOLLOW_EXISTING_PLAN",
        "description": (
            "A current NOPH plan covers the event and no valid recontact "
            "trigger is recorded."
        ),
        "values": case,
    }

    case = base_case()
    case.update(
        {
            "synthetic_case_id": "SYN-T14",
            "noph_plan_status": "Active",
            "active_plan_version": "NOPH-PLAN-001",
            "clinical_deterioration_since_plan": "Yes",
        }
    )
    cases["T14 — Deterioration: recontact NOPH"] = {
        "expected": "A_RECONTACT_NOPH",
        "description": (
            "An active plan exists, but documented deterioration triggers "
            "recontact rather than duplicate-call suppression."
        ),
        "values": case,
    }

    return cases


def initialise_state():
    """
    Initialise session state only once, using blank values.

    The `if key not in st.session_state` condition prevents every Streamlit
    rerun from overwriting values the user has typed, dictated, extracted,
    reviewed, or loaded from a demo case.
    """

    for key, value in blank_case().items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_case(case_values):
    """
    Load an explicitly selected synthetic demo case.
    """

    for key, value in case_values.items():
        st.session_state[key] = value

    st.session_state.pop("workflow_result", None)
    st.session_state.pop("llm_extraction", None)
    st.session_state.pop("llm_evidence_reviewed", None)


def reset_to_blank_case():
    """
    Clear all fields to the blank synthetic intake state.
    """

    for key, value in blank_case().items():
        st.session_state[key] = value

    st.session_state.pop("workflow_result", None)
    st.session_state.pop("llm_extraction", None)
    st.session_state.pop("llm_evidence_reviewed", None)


def apply_llm_extraction(extraction):
    """
    Copy reviewed LLM values into the structured form.

    Unknown/null values are intentionally not applied. They leave the form
    blank/Unknown so that the clinician can decide what to enter next.
    """

    field_mapping = {
        "patient_age_years": "age_entered",
        "bp_systolic_mmhg": "bp_systolic_text",
        "bp_diastolic_mmhg": "bp_diastolic_text",
        "lp_opening_pressure_cm_csf": "lp_opening_pressure_text",
    }

    for field, value in extraction.items():
        if field == "evidence":
            continue

        if value is None or value == "Unknown":
            continue

        target_key = field_mapping.get(field, field)
        st.session_state[target_key] = str(value)

    st.session_state.pop("workflow_result", None)


def build_facts():
    """
    Convert UI session values to the exact fields expected by rule_engine.py.
    """

    major_neuro_red_flag = (
        "Yes"
        if any(
            value == "Yes"
            for value in [
                st.session_state["focal_neurological_signs"],
                st.session_state["reduced_consciousness"],
                st.session_state["meningism"],
                st.session_state["seizure"],
                st.session_state["other_cranial_nerve_abnormality"],
            ]
        )
        else "No"
    )

    return {
        "synthetic_case_id": st.session_state["synthetic_case_id"],
        "patient_age_years": parse_integer(st.session_state["age_entered"]),
        "clinical_owner": "ED",

        "visual_acuity_status": st.session_state["visual_acuity_status"],
        "pupil_exam_status": st.session_state["pupil_exam_status"],
        "iop_status": st.session_state["iop_status"],
        "formal_perimetry_status": st.session_state[
            "formal_perimetry_status"
        ],
        "dilated_fundus_status": st.session_state["dilated_fundus_status"],

        "papilloedema_status": st.session_state["papilloedema_status"],
        "papilloedema_reviewer_level": st.session_state[
            "papilloedema_reviewer_level"
        ],
        "visual_function_threatened": st.session_state[
            "visual_function_threatened"
        ],

        "bp_systolic_mmhg": parse_integer(
            st.session_state["bp_systolic_text"]
        ),
        "bp_diastolic_mmhg": parse_integer(
            st.session_state["bp_diastolic_text"]
        ),

        "cranial_nerve_exam_status": st.session_state[
            "cranial_nerve_exam_status"
        ],
        "focal_neurological_signs": st.session_state[
            "focal_neurological_signs"
        ],
        "reduced_consciousness": st.session_state[
            "reduced_consciousness"
        ],
        "meningism": st.session_state["meningism"],
        "seizure": st.session_state["seizure"],
        "other_cranial_nerve_abnormality": st.session_state[
            "other_cranial_nerve_abnormality"
        ],
        "major_neuro_red_flag": major_neuro_red_flag,

        "brain_imaging_status": st.session_state["brain_imaging_status"],
        "brain_imaging_modality": st.session_state["brain_imaging_modality"],
        "secondary_structural_or_meningeal_pathology": st.session_state[
            "secondary_structural_or_meningeal_pathology"
        ],
        "radiology_interpretation_uncertain": st.session_state[
            "radiology_interpretation_uncertain"
        ],

        "venography_status": st.session_state["venography_status"],
        "cerebral_venous_sinus_thrombosis": st.session_state[
            "cerebral_venous_sinus_thrombosis"
        ],

        "fbc_status": st.session_state["fbc_status"],

        "lp_status": st.session_state["lp_status"],
        "lp_technique_valid": st.session_state["lp_technique_valid"],
        "lp_opening_pressure_cm_csf": parse_float(
            st.session_state["lp_opening_pressure_text"]
        ),

        "minimum_csf_tests_complete": st.session_state[
            "minimum_csf_tests_complete"
        ],
        "csf_contents_status": st.session_state["csf_contents_status"],

        "secondary_cause_screen_complete": st.session_state[
            "secondary_cause_screen_complete"
        ],
        "secondary_cause_identified": st.session_state[
            "secondary_cause_identified"
        ],

        "iih_criteria_complete": st.session_state["iih_criteria_complete"],
        "severe_visual_loss_within_4_weeks": st.session_state[
            "severe_visual_loss_within_4_weeks"
        ],
        "vision_worsening_over_days": st.session_state[
            "vision_worsening_over_days"
        ],
        "typical_profile_flag": st.session_state["typical_profile_flag"],

        "visual_function_stable": st.session_state[
            "visual_function_stable"
        ],
        "baseline_disc_docs_available": st.session_state[
            "baseline_disc_docs_available"
        ],
        "pseudo_followup_booked": st.session_state[
            "pseudo_followup_booked"
        ],
        "pseudo_followup_weeks": parse_integer(
            st.session_state["pseudo_followup_weeks_text"]
        ),
        "return_precautions_given": st.session_state[
            "return_precautions_given"
        ],

        "noph_plan_status": st.session_state["noph_plan_status"],
        "active_plan_version": st.session_state["active_plan_version"],
        "callback_requested_due": st.session_state[
            "callback_requested_due"
        ],
        "clinical_deterioration_since_plan": st.session_state[
            "clinical_deterioration_since_plan"
        ],
        "unexpected_result_since_plan": st.session_state[
            "unexpected_result_since_plan"
        ],
        "ownership_or_plan_unclear": st.session_state[
            "ownership_or_plan_unclear"
        ],

        "clinical_owner_documented": st.session_state[
            "clinical_owner_documented"
        ],
        "disposition_approved": st.session_state[
            "disposition_approved"
        ],
    }


def show_result(result):
    """
    Render the deterministic workflow result without changing the rules.
    """

    action_codes = result["action_codes"]
    primary_action = action_codes[0]
    urgency = result["urgency"]
    disposition_blocked = result["hard_stop"]

    if urgency == "Immediate":
        urgency_label = "IMMEDIATE ACTION REQUIRED"
        urgency_colour = "#B42318"
        background_colour = "#FEF3F2"
        border_colour = "#FDA29B"

    elif urgency in {"Same_shift", "Within_24h"}:
        urgency_label = "URGENT WORKFLOW ACTION"
        urgency_colour = "#B54708"
        background_colour = "#FFFAEB"
        border_colour = "#FEC84B"

    elif urgency == "Before_disposition":
        urgency_label = "REQUIRED BEFORE WORKFLOW CLOSURE"
        urgency_colour = "#175CD3"
        background_colour = "#EFF8FF"
        border_colour = "#84CAFF"

    elif urgency == "Local_define":
        urgency_label = "LOCAL PROTOCOL DECISION REQUIRED"
        urgency_colour = "#6941C6"
        background_colour = "#F9F5FF"
        border_colour = "#D6BBFB"

    else:
        urgency_label = "NO NEW WORKFLOW ACTION"
        urgency_colour = "#027A48"
        background_colour = "#ECFDF3"
        border_colour = "#6CE9A6"

    st.divider()
    st.header("Clinical workflow result")

    st.markdown(
        f"""
        <div style="
            background-color: {background_colour};
            border: 1px solid {border_colour};
            border-left: 8px solid {urgency_colour};
            border-radius: 10px;
            padding: 18px 22px;
            margin: 12px 0 22px 0;
        ">
            <div style="
                color: {urgency_colour};
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.05em;
                margin-bottom: 6px;
            ">
                {urgency_label}
            </div>
            <div style="
                font-size: 26px;
                font-weight: 700;
                color: #101828;
                margin-bottom: 6px;
            ">
                {primary_action}
            </div>
            <div style="
                font-size: 17px;
                line-height: 1.45;
                color: #344054;
            ">
                {ACTIONS[primary_action]["text"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Current workflow node", result["current_node"])

    with col2:
        st.metric("Next workflow node", result["next_node"])

    with col3:
        st.metric("Urgency", urgency.replace("_", " "))

    with col4:
        st.metric(
            "Disposition status",
            "BLOCKED" if disposition_blocked else "NOT BLOCKED",
        )

    if disposition_blocked:
        st.error(
            "Workflow closure is blocked. This demonstrator cannot authorise "
            "discharge, admission, transfer, diagnosis, or treatment."
        )
    else:
        st.success(
            "No workflow closure block is currently raised. Human clinical "
            "responsibility and local policy still apply."
        )

    st.subheader("Why this action was triggered")

    st.write(
        f"The deterministic rule engine evaluated node "
        f"`{result['current_node']}` and returned `{primary_action}`."
    )

    if result["missing_required_fields"]:
        st.subheader("Information still required")

        for field in result["missing_required_fields"]:
            st.markdown(f"- `{field}`")

    if len(action_codes) > 1:
        st.subheader("Additional workflow actions")

        for action_code in action_codes[1:]:
            action = ACTIONS.get(action_code)

            if action:
                st.markdown(f"#### `{action_code}`")
                st.write(action["text"])

    st.subheader("Human control")

    st.info(
        "This is a workflow recommendation from fixed rules. A named clinician "
        "retains responsibility for review, escalation, diagnosis, treatment, "
        "and disposition."
    )

    st.subheader("Simulated clinician sign-off")

    reviewer_name = st.text_input(
        "Reviewer name",
        key="reviewer_name",
        placeholder="Synthetic demonstrator user",
    )

    reviewer_role = st.selectbox(
        "Reviewer role",
        [
            "Select role",
            "ED clinician",
            "Ophthalmology registrar",
            "Neuro-ophthalmology clinician",
            "Consultant",
            "Other authorised reviewer",
        ],
        key="reviewer_role",
    )

    clinician_reviewed_output = st.checkbox(
        "I confirm that I have reviewed this workflow output.",
        key="clinician_reviewed_output",
    )

    decision_mode = st.radio(
        "Clinician response to deterministic workflow output",
        [
            "Accept workflow output",
            "Record a clinician override",
        ],
        key="decision_mode",
    )

    if decision_mode == "Record a clinician override":
        st.warning(
            "The original rule-engine output remains visible. An override "
            "does not delete or silently replace the deterministic result."
        )

        override_reason = st.selectbox(
            "Override reason",
            [
                "Select reason",
                "Additional clinical information not represented in the demonstrator",
                "Local protocol or service arrangement",
                "Senior specialist instruction",
                "Patient-specific procedural or safety constraint",
                "Workflow/data-entry error identified",
                "Other",
            ],
            key="override_reason",
        )

        override_rationale = st.text_area(
            "Override rationale",
            key="override_rationale",
            placeholder=(
                "Enter a synthetic rationale explaining why the workflow "
                "output is being overridden."
            ),
        )

        override_complete = (
            reviewer_name.strip() != ""
            and reviewer_role != "Select role"
            and clinician_reviewed_output
            and override_reason != "Select reason"
            and override_rationale.strip() != ""
        )

        if override_complete:
            st.success(
                "Simulated override record complete. The original workflow "
                "output remains displayed above."
            )

            override_record = {
                "reviewer_name": reviewer_name,
                "reviewer_role": reviewer_role,
                "reviewed_output": True,
                "override_reason": override_reason,
                "override_rationale": override_rationale,
                "original_action_codes": action_codes,
                "original_current_node": result["current_node"],
                "original_next_node": result["next_node"],
            }

            with st.expander("Simulated override record"):
                st.code(
                    json.dumps(override_record, indent=2),
                    language="json",
                )

        else:
            st.info(
                "To complete the simulated override, enter reviewer name, "
                "role, review confirmation, override reason, and rationale."
            )

    else:
        signoff_complete = (
            reviewer_name.strip() != ""
            and reviewer_role != "Select role"
            and clinician_reviewed_output
        )

        if signoff_complete:
            st.success(
                "Simulated clinician review recorded. The deterministic "
                "workflow output remains the displayed recommendation."
            )
        else:
            st.info(
                "To complete simulated review, enter a reviewer name, select "
                "a role, and confirm review of the output."
            )

    with st.expander("Technical audit output"):
        st.json(result)


initialise_state()
all_demo_cases = demo_cases()

st.sidebar.header("Demonstration controls")

selected_case_name = st.sidebar.selectbox(
    "Load a synthetic test case",
    ["Manual entry / dictation"] + list(all_demo_cases.keys()),
)

if selected_case_name != "Manual entry / dictation":
    selected_case = all_demo_cases[selected_case_name]

    st.sidebar.info(selected_case["description"])
    st.sidebar.caption(
        f"Expected primary action: {selected_case['expected']}"
    )

    if st.sidebar.button("Load selected demonstration case"):
        load_case(selected_case["values"])
        st.rerun()

if st.sidebar.button("Reset to blank synthetic case"):
    reset_to_blank_case()
    st.rerun()

st.title("IIH AI Demonstrator")

st.caption(
    "DEMONSTRATION ONLY — SYNTHETIC DATA ONLY — "
    "NOT VALIDATED FOR CLINICAL USE — "
    "NO AUTONOMOUS DIAGNOSIS, TREATMENT, ADMISSION OR DISCHARGE"
)

st.error(
    "DO NOT enter or dictate real patient, identifying, confidential, "
    "or clinical information. This application is a synthetic-data "
    "demonstrator only."
)

st.subheader("Synthetic dictation input")

st.caption(
    "Record synthetic demonstration audio only. Audio is sent to the "
    "configured transcription API, then returned as editable text for "
    "review before any LLM extraction or workflow evaluation."
)

audio_recording = st.audio_input(
    "Record synthetic referral note",
    sample_rate=16000,
)

if audio_recording is not None:
    st.audio(audio_recording)

    if st.button("Transcribe synthetic dictation"):
        try:
            with st.spinner("Transcribing synthetic audio..."):
                transcript = transcribe_synthetic_audio(audio_recording)

            st.session_state["synthetic_referral_note"] = transcript
            st.session_state.pop("llm_extraction", None)
            st.session_state.pop("workflow_result", None)

            st.success(
                "Synthetic dictation transcribed. Review and edit the "
                "transcript before asking the LLM to extract facts."
            )

            st.rerun()

        except Exception as error:
            st.error(f"Transcription did not complete: {error}")

st.divider()
st.subheader("LLM synthetic referral-note intake")

st.caption(
    "The LLM extracts explicitly stated facts and evidence quotes only. "
    "It does not determine urgency, diagnose papilloedema or IIH, interpret "
    "images, prescribe, admit, discharge, or transfer responsibility."
)

st.text_area(
    "Synthetic referral note",
    key="synthetic_referral_note",
    height=180,
    placeholder=(
        "Synthetic example only: A 29-year-old woman has papilloedema "
        "confirmed by an AO. Visual function is explicitly documented as "
        "not threatened. BP is 130/80. MRI brain is normal and adequately "
        "reported. MRV is normal and adequately reported. FBC is normal."
    ),
)

if st.button("Extract with LLM from synthetic note"):
    try:
        with st.spinner("Extracting stated facts and evidence quotes..."):
            st.session_state["llm_extraction"] = extract_note_with_llm(
                st.session_state["synthetic_referral_note"]
            )

        st.session_state["llm_evidence_reviewed"] = False
        st.session_state.pop("workflow_result", None)

        st.success(
            "LLM extraction completed. Review extracted facts and evidence "
            "quotes before applying them to the structured form."
        )

    except Exception as error:
        st.error(f"LLM extraction did not complete: {error}")

if "llm_extraction" in st.session_state:
    extraction = st.session_state["llm_extraction"]

    st.subheader("LLM extraction review")

    st.warning(
        "Review every extracted value against its supporting quote. "
        "The LLM output is not a diagnosis or a workflow decision."
    )

    extracted_values = {
        key: value
        for key, value in extraction.items()
        if key != "evidence"
    }

    st.write("### Extracted structured values")
    st.json(extracted_values)

    st.write("### Supporting evidence quotes")

    evidence = extraction.get("evidence", [])

    if evidence:
        for item in evidence:
            st.markdown(
                f"- **{item['field']}** = `{item['value']}`  \n"
                f"  > {item['quote']}"
            )
    else:
        st.error(
            "No evidence quotes were returned. This extraction cannot be "
            "applied to the structured form."
        )

    st.checkbox(
        "I confirm that I reviewed the extracted values and evidence quotes.",
        key="llm_evidence_reviewed",
    )

    if st.session_state["llm_evidence_reviewed"] and evidence:
        if st.button("Apply reviewed LLM extraction to structured form"):
            apply_llm_extraction(extraction)

            st.success(
                "Reviewed extraction applied. Review/correct the structured "
                "form before running the deterministic workflow."
            )

            st.rerun()

    else:
        st.info(
            "Tick the review confirmation and ensure evidence quotes are "
            "present before applying extracted values."
        )

exam_options = [
    "Unknown",
    "Completed",
    "Unable_with_reason",
    "Not_done",
]

tri_state_options = [
    "Unknown",
    "Yes",
    "No",
]

imaging_options = [
    "Unknown",
    "Not_done",
    "Pending",
    "Completed_adequate",
    "Completed_inadequate",
]

with st.form("case_form"):
    st.header("Structured synthetic case input")

    st.text_input(
        "Synthetic case ID",
        key="synthetic_case_id",
        help="Use synthetic identifiers only. Do not enter real patient data.",
    )

    st.text_input(
        "Age in completed years",
        key="age_entered",
    )

    st.divider()
    st.subheader("Core ocular examination")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Visual acuity status",
            exam_options,
            key="visual_acuity_status",
        )

        st.selectbox(
            "Pupil examination status",
            exam_options,
            key="pupil_exam_status",
        )

        st.selectbox(
            "IOP status",
            exam_options,
            key="iop_status",
        )

    with col2:
        st.selectbox(
            "Formal perimetry status",
            exam_options,
            key="formal_perimetry_status",
        )

        st.selectbox(
            "Dilated fundus examination status",
            exam_options,
            key="dilated_fundus_status",
        )

    st.divider()
    st.subheader("Disc status and visual risk")

    st.selectbox(
        "Papilloedema status",
        ["Unknown", "Confirmed", "Not_confirmed", "Uncertain"],
        key="papilloedema_status",
    )

    st.selectbox(
        "Reviewer level",
        [
            "Unknown",
            "ED_clinician",
            "AO",
            "Consultant",
            "Experienced_clinician",
        ],
        key="papilloedema_reviewer_level",
    )

    st.selectbox(
        "Is visual function threatened or possibly threatened?",
        ["Unknown", "Yes", "Possible", "No"],
        key="visual_function_threatened",
    )

    st.divider()
    st.subheader("Blood pressure")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Systolic blood pressure (mmHg)",
            key="bp_systolic_text",
        )

    with col2:
        st.text_input(
            "Diastolic blood pressure (mmHg)",
            key="bp_diastolic_text",
        )

    st.divider()
    st.subheader("Neurological examination")

    st.selectbox(
        "Cranial nerve examination status",
        exam_options,
        key="cranial_nerve_exam_status",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Focal neurological signs beyond isolated CN VI palsy?",
            tri_state_options,
            key="focal_neurological_signs",
        )

        st.selectbox(
            "Reduced consciousness?",
            tri_state_options,
            key="reduced_consciousness",
        )

        st.selectbox(
            "Meningism?",
            tri_state_options,
            key="meningism",
        )

    with col2:
        st.selectbox(
            "Seizure in this presentation?",
            tri_state_options,
            key="seizure",
        )

        st.selectbox(
            "Other cranial nerve abnormality?",
            tri_state_options,
            key="other_cranial_nerve_abnormality",
        )

    st.divider()
    st.subheader("Brain imaging")

    st.selectbox(
        "Brain imaging status",
        imaging_options,
        key="brain_imaging_status",
    )

    st.selectbox(
        "Brain imaging modality",
        [
            "Unknown",
            "MRI",
            "CT_then_MRI_pending",
            "CT_then_MRI_complete",
            "Other",
        ],
        key="brain_imaging_modality",
    )

    st.selectbox(
        "Structural, vascular, hydrocephalic or meningeal cause identified?",
        tri_state_options,
        key="secondary_structural_or_meningeal_pathology",
    )

    st.selectbox(
        "Is the radiology interpretation uncertain?",
        tri_state_options,
        key="radiology_interpretation_uncertain",
    )

    st.divider()
    st.subheader("Venography")

    st.selectbox(
        "CT/MR venography status",
        imaging_options,
        key="venography_status",
    )

    st.selectbox(
        "CVST or another causative venous pathology identified?",
        tri_state_options,
        key="cerebral_venous_sinus_thrombosis",
    )

    st.divider()
    st.subheader("Laboratory")

    st.selectbox(
        "Full blood count status",
        ["Unknown", "Not_done", "Pending", "Normal", "Abnormal"],
        key="fbc_status",
    )

    st.divider()
    st.subheader("Lumbar puncture")

    st.selectbox(
        "Lumbar puncture status after normal imaging and venography",
        [
            "Unknown",
            "Not_done",
            "Pending",
            "Completed",
            "Contraindicated",
            "Formally_deferred_by_senior",
        ],
        key="lp_status",
    )

    st.selectbox(
        "Opening-pressure measurement technically valid?",
        tri_state_options,
        key="lp_technique_valid",
    )

    st.text_input(
        "Opening pressure (cm CSF)",
        key="lp_opening_pressure_text",
    )

    st.divider()
    st.subheader("CSF results")

    st.selectbox(
        "Minimum CSF protein, glucose and cell count available?",
        tri_state_options,
        key="minimum_csf_tests_complete",
    )

    st.selectbox(
        "CSF contents status",
        ["Unknown", "Pending", "Normal", "Abnormal"],
        key="csf_contents_status",
    )

    st.divider()
    st.subheader("Secondary-cause screen")

    st.selectbox(
        "Secondary-cause and association screen complete?",
        tri_state_options,
        key="secondary_cause_screen_complete",
    )

    st.selectbox(
        "Cause or association identified that may explain raised ICP?",
        tri_state_options,
        key="secondary_cause_identified",
    )

    st.divider()
    st.subheader("Criteria and classification")

    st.selectbox(
        "Are all IIH criteria elements complete and internally consistent?",
        ["Unknown", "Yes", "No", "Conflict"],
        key="iih_criteria_complete",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Severe visual loss within 4 weeks?",
            tri_state_options,
            key="severe_visual_loss_within_4_weeks",
        )

    with col2:
        st.selectbox(
            "Vision worsening rapidly over days?",
            tri_state_options,
            key="vision_worsening_over_days",
        )

    st.selectbox(
        "Typical IIH demographic profile",
        ["Unknown", "Typical", "Atypical"],
        key="typical_profile_flag",
    )

    st.divider()
    st.subheader("Non-confirmed papilloedema / pseudopapilloedema route")

    st.selectbox(
        "Is visual function stable?",
        ["Unknown", "Yes", "No", "Uncertain"],
        key="visual_function_stable",
    )

    st.selectbox(
        "Baseline OCT or disc photographs available?",
        tri_state_options,
        key="baseline_disc_docs_available",
    )

    st.selectbox(
        "Repeat clinic and OCT follow-up booked?",
        tri_state_options,
        key="pseudo_followup_booked",
    )

    st.text_input(
        "Pseudopapilloedema follow-up interval (weeks)",
        key="pseudo_followup_weeks_text",
    )

    st.selectbox(
        "Return precautions documented?",
        tri_state_options,
        key="return_precautions_given",
    )

    st.divider()
    st.subheader("Neuro-ophthalmology contact plan")

    st.selectbox(
        "Current documented neuro-ophthalmology plan status",
        ["Unknown", "No_plan", "Active", "Expired", "Unclear"],
        key="noph_plan_status",
    )

    st.text_input(
        "Active NOPH plan version or identifier",
        key="active_plan_version",
    )

    st.selectbox(
        "Did the active plan request callback at this time/result?",
        tri_state_options,
        key="callback_requested_due",
    )

    st.selectbox(
        "Clinical or visual deterioration since the active plan?",
        tri_state_options,
        key="clinical_deterioration_since_plan",
    )

    st.selectbox(
        "Unexpected result outside the active plan?",
        tri_state_options,
        key="unexpected_result_since_plan",
    )

    st.selectbox(
        "Is clinical ownership or the current plan unclear?",
        tri_state_options,
        key="ownership_or_plan_unclear",
    )

    st.divider()
    st.subheader("Human-authorised workflow closure")

    st.selectbox(
        "Clinical owner documented?",
        tri_state_options,
        key="clinical_owner_documented",
    )

    st.selectbox(
        "Disposition approved by an authorised clinician?",
        tri_state_options,
        key="disposition_approved",
    )

    submitted = st.form_submit_button("Evaluate deterministic workflow")

if submitted:
    st.session_state["workflow_result"] = evaluate(build_facts())

if "workflow_result" in st.session_state:
    show_result(st.session_state["workflow_result"])
