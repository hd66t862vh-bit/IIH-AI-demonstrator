from datetime import datetime, timezone

PROTOCOL_VERSION = "0.1"

ACTIONS = {
    "A_NONE": {
        "text": "No new action; continue to the next node.",
        "urgency": "None",
        "blocks_discharge": False,
        "human_review_required": False,
    },
    "A_MISSING_AGE": {
        "text": "Record the patient's age before applying the pathway scope rule.",
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_ROUTE_RCH_PEDS": {
        "text": "Use the locally approved paediatric pathway / Royal Children's Hospital route.",
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_COMPLETE_OCULAR_EXAM": {
        "text": "Complete or document inability to complete the required ocular examination items.",
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_SENIOR_DISC_REVIEW": {
        "text": (
            "Obtain AO, consultant, or experienced-clinician review of the "
            "optic discs before invasive testing where possible."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_REQUEST_NOPH_UNCERTAIN_DISC": {
        "text": (
            "Request early neuro-ophthalmology review because papilloedema "
            "remains uncertain after senior assessment."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_ASSESS_VISUAL_RISK": {
        "text": (
            "Obtain senior assessment of whether visual function is "
            "threatened."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_IMMEDIATE_NOPH_VISUAL_THREAT": {
        "text": (
            "Contact neuro-ophthalmology immediately for threatened or "
            "possibly threatened visual function and continue urgent work-up."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_MEASURE_BP": {
        "text": "Measure and record systolic and diastolic blood pressure.",
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_HYPERTENSIVE_EMERGENCY": {
        "text": (
            "Treat as possible malignant hypertension or hypertensive "
            "emergency under the local emergency pathway and obtain "
            "appropriate medical review."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_COMPLETE_NEURO_EXAM": {
        "text": (
            "Complete the cranial nerve and major neurological red-flag "
            "examination."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_SENIOR_NEURO_REVIEW": {
        "text": (
            "Obtain senior review because neurological red-flag status is "
            "incomplete or uncertain."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_URGENT_ALTERNATE_NEURO": {
        "text": (
            "Broaden evaluation and seek urgent neurology or "
            "neuro-ophthalmology input; do not assume uncomplicated IIH."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_URGENT_BRAIN_IMAGING": {
        "text": (
            "Arrange urgent brain imaging within 24 hours using the locally "
            "approved MRI/CT pathway."
        ),
        "urgency": "Within_24h",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_NOPH_CHECKPOINT_AFTER_IMAGING": {
        "text": (
            "Apply the locally approved neuro-ophthalmology checkpoint after "
            "structural imaging; run the contact gate before a non-emergency "
            "repeat call."
        ),
        "urgency": "Local_define",
        "blocks_discharge": False,
        "human_review_required": True,
    },
    "A_RADIOLOGY_REVIEW": {
        "text": (
            "Obtain senior radiology review of inadequate or uncertain imaging "
            "or venography before progressing."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_URGENT_ALTERNATE_IMAGING": {
        "text": (
            "Escalate the identified structural, vascular, hydrocephalic, or "
            "meningeal abnormality to the appropriate service; exit the "
            "idiopathic pathway."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_URGENT_VENOGRAPHY": {
        "text": (
            "Arrange adequate CT or MR venography within the locally approved "
            "urgent timeframe."
        ),
        "urgency": "Within_24h",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_SECONDARY_VENOUS_PATHWAY": {
        "text": (
            "Manage as secondary intracranial hypertension or venous pathology "
            "with urgent specialist input; do not label as idiopathic."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_OBTAIN_FBC": {
        "text": (
            "Obtain a full blood count; feed abnormal results into the "
            "secondary-cause screen."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": False,
        "human_review_required": True,
    },
    "A_LP_REQUIRED": {
        "text": (
            "After adequate normal imaging and venography, arrange lumbar "
            "puncture under the treating team's safety assessment."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_LP_DEFERRED_REVIEW": {
        "text": (
            "Obtain named senior or neuro-ophthalmology review of a "
            "contraindicated, deferred, or unresolved lumbar-puncture plan."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_REVIEW_LP_VALIDITY": {
        "text": (
            "Review opening-pressure technique and the clinical/imaging "
            "context before interpreting the result."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_IIH_NOT_CONFIRMED": {
        "text": (
            "Do not confirm IIH from this pathway; request specialist review "
            "if suspicion remains or findings are discordant."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_WAIT_CSF": {
        "text": (
            "Obtain or await minimum CSF protein, glucose, and cell-count "
            "results before classification."
        ),
        "urgency": "Before_disposition",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_ALTERNATE_CSF_PATHWAY": {
        "text": (
            "Abnormal CSF contents prevent an idiopathic classification; "
            "broaden evaluation and seek the appropriate specialist input."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_COMPLETE_SECONDARY_SCREEN": {
        "text": (
            "Complete the locally approved secondary-cause and association "
            "screen."
        ),
        "urgency": "Before_disposition",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_SECONDARY_CAUSE_REVIEW": {
        "text": (
            "Obtain senior review because the secondary-cause screen or "
            "relevance of an association is uncertain."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_SECONDARY_IH_PATHWAY": {
        "text": (
            "Use a secondary intracranial-hypertension pathway; do not label "
            "the presentation idiopathic."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_REVIEW_CRITERIA_CONFLICT": {
        "text": (
            "Resolve missing or internally conflicting IIH criteria with "
            "senior or neuro-ophthalmology review."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_FULMINANT_IIH_CANDIDATE": {
        "text": (
            "Flag fulminant-IIH candidate and contact neuro-ophthalmology "
            "immediately for a vision-protection plan."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_TYPICAL_IIH_CANDIDATE": {
        "text": (
            "Criteria appear complete with a typical demographic profile. "
            "Generate a consolidated summary and request or confirm the "
            "neuro-ophthalmology plan."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_ATYPICAL_IIH_CANDIDATE": {
        "text": (
            "Criteria appear complete but the profile is atypical. Request or "
            "confirm neuro-ophthalmology review and broader secondary-cause "
            "scrutiny."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_ATYPICAL_PROFILE_REVIEW": {
        "text": (
            "Clarify demographic/BMI fields or treat the profile as atypical "
            "for scrutiny until reviewed."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_PSEUDO_RED_FLAG": {
        "text": (
            "Exit routine pseudopapilloedema follow-up and obtain urgent "
            "neuro-ophthalmology review for red flags or unstable vision."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_PSEUDO_UNSTABLE_REVIEW": {
        "text": (
            "Obtain neuro-ophthalmology review because visual function is "
            "unstable or uncertain."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_OBTAIN_BASELINE_DISC_DOCS": {
        "text": (
            "Obtain the locally required baseline OCT or disc documentation "
            "before routine follow-up."
        ),
        "urgency": "Before_disposition",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_BOOK_PSEUDO_4_6W": {
        "text": (
            "Book repeat clinic assessment and OCT in 4–6 weeks under the "
            "locally approved pseudopapilloedema pathway."
        ),
        "urgency": "Before_disposition",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_COMPLETE_SAFETY_NET": {
        "text": (
            "Document return precautions and the service responsible for "
            "follow-up."
        ),
        "urgency": "Before_disposition",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_PSEUDO_FOLLOWUP_READY": {
        "text": (
            "Stable non-confirmed papilloedema/pseudopapilloedema follow-up "
            "package appears complete; obtain authorised disposition approval."
        ),
        "urgency": "Before_disposition",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_CONTACT_NOPH_IMMEDIATE": {
        "text": (
            "Contact neuro-ophthalmology immediately; record reason, time, "
            "responder, and plan version."
        ),
        "urgency": "Immediate",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_CONTACT_NOPH": {
        "text": (
            "Contact neuro-ophthalmology with one consolidated summary because "
            "no active plan exists."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_RECONTACT_NOPH": {
        "text": (
            "Recontact neuro-ophthalmology and state the documented trigger: "
            "requested callback, deterioration, unexpected result, or unclear "
            "plan/ownership."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_FOLLOW_EXISTING_PLAN": {
        "text": (
            "Do not make a duplicate call. Display and follow the current "
            "neuro-ophthalmology plan because the patient is unchanged and "
            "the event is covered."
        ),
        "urgency": "None",
        "blocks_discharge": False,
        "human_review_required": True,
    },
    "A_CLARIFY_ACTIVE_PLAN": {
        "text": (
            "Clarify whether a current neuro-ophthalmology plan exists and "
            "who owns it."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_SENIOR_CONTACT_REVIEW": {
        "text": (
            "Obtain senior review because contact urgency or recontact-trigger "
            "status is unclear."
        ),
        "urgency": "Same_shift",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_BLOCK_DISPOSITION": {
        "text": (
            "Do not close, discharge, or transfer the workflow until authorised "
            "disposition and clinical ownership are documented."
        ),
        "urgency": "Before_disposition",
        "blocks_discharge": True,
        "human_review_required": True,
    },
    "A_CLOSED": {
        "text": (
            "Record workflow closure, final owner/disposition, plan version, "
            "and audit timestamp."
        ),
        "urgency": "None",
        "blocks_discharge": False,
        "human_review_required": True,
    },
}


def action_result(action_code, current_node, next_node, facts, missing=None):
    action = ACTIONS[action_code]

    return {
        "protocol_version": PROTOCOL_VERSION,
        "synthetic_case_id": facts.get("synthetic_case_id", "SYN-UNSET"),
        "current_node": current_node,
        "next_node": next_node,
        "facts": facts,
        "missing_required_fields": missing or [],
        "action_codes": [action_code],
        "urgency": action["urgency"],
        "hard_stop": action["blocks_discharge"],
        "human_review_required": action["human_review_required"],
        "clinical_owner": facts.get("clinical_owner", "ED"),
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def core_exam_complete(facts):
    fields = [
        "visual_acuity_status",
        "pupil_exam_status",
        "iop_status",
        "formal_perimetry_status",
        "dilated_fundus_status",
    ]

    valid_statuses = {"Completed", "Unable_with_reason"}

    return all(facts.get(field) in valid_statuses for field in fields)


def neuro_exam_complete(facts):
    if facts.get("cranial_nerve_exam_status") not in {
        "Completed",
        "Unable_with_reason",
    }:
        return False

    required_fields = [
        "focal_neurological_signs",
        "reduced_consciousness",
        "meningism",
        "seizure",
        "other_cranial_nerve_abnormality",
    ]

    return all(facts.get(field) in {"Yes", "No"} for field in required_fields)


def contact_gate(facts, pending_node, immediate_trigger=False):
    """
    Cross-cutting NOPH contact de-duplication gate.
    It returns to pending_node after the contact-plan decision.
    """

    if immediate_trigger:
        return action_result(
            "A_CONTACT_NOPH_IMMEDIATE",
            current_node="CG-01",
            next_node=pending_node,
            facts=facts,
        )

    plan_status = facts.get("noph_plan_status")
    active_plan_version = facts.get("active_plan_version")

    if plan_status in {None, "", "Unknown", "Unclear"}:
        return action_result(
            "A_CLARIFY_ACTIVE_PLAN",
            current_node="CG-02",
            next_node="CG-02",
            facts=facts,
            missing=["noph_plan_status", "active_plan_version"],
        )

    if plan_status != "Active" or not active_plan_version:
        return action_result(
            "A_CONTACT_NOPH",
            current_node="CG-02",
            next_node=pending_node,
            facts=facts,
        )

    recontact_fields = [
        "callback_requested_due",
        "clinical_deterioration_since_plan",
        "unexpected_result_since_plan",
        "ownership_or_plan_unclear",
    ]

    values = [facts.get(field) for field in recontact_fields]

    if any(value == "Yes" for value in values):
        return action_result(
            "A_RECONTACT_NOPH",
            current_node="CG-03",
            next_node=pending_node,
            facts=facts,
        )

    if any(value in {None, "", "Unknown"} for value in values):
        missing = [
            field
            for field in recontact_fields
            if facts.get(field) in {None, "", "Unknown"}
        ]

        return action_result(
            "A_SENIOR_CONTACT_REVIEW",
            current_node="CG-03",
            next_node="CG-03",
            facts=facts,
            missing=missing,
        )

    return action_result(
        "A_FOLLOW_EXISTING_PLAN",
        current_node="CG-03",
        next_node=pending_node,
        facts=facts,
    )


def closure_gate(facts):
    """
    Workflow closure only.
    This does not direct discharge, admission, transfer, diagnosis, or treatment.
    """

    missing = []

    if facts.get("clinical_owner_documented") != "Yes":
        missing.append("clinical_owner_documented")

    if facts.get("disposition_approved") != "Yes":
        missing.append("disposition_approved")

    if missing:
        return action_result(
            "A_BLOCK_DISPOSITION",
            current_node="CLOSE-01",
            next_node="CLOSE-01",
            facts=facts,
            missing=missing,
        )

    return action_result(
        "A_CLOSED",
        current_node="CLOSE-01",
        next_node="END-CLOSED",
        facts=facts,
    )


def evaluate_pseudopap_route(facts):
    """
    Route 2: clinician-authorised Not_confirmed papilloedema pathway.
    This is a follow-up and safety workflow, never autonomous discharge.
    """

    disc_status = facts.get("papilloedema_status")
    reviewer = facts.get("papilloedema_reviewer_level")

    # PSEUDO-01
    if disc_status == "Uncertain" or reviewer in {None, "", "Unknown"}:
        return contact_gate(
            facts,
            pending_node="PSEUDO-01",
            immediate_trigger=False,
        )

    visual_stable = facts.get("visual_function_stable")
    visual_threat = facts.get("visual_function_threatened")
    major_neuro_red_flag = facts.get("major_neuro_red_flag")

    # PSEUDO-02: instability or red flags
    if (
        visual_stable == "No"
        or visual_threat in {"Yes", "Possible"}
        or major_neuro_red_flag == "Yes"
    ):
        return action_result(
            "A_PSEUDO_RED_FLAG",
            current_node="PSEUDO-02",
            next_node="CG-01",
            facts=facts,
        )

    if (
        visual_stable in {None, "", "Unknown", "Uncertain"}
        or visual_threat in {None, "", "Unknown"}
        or major_neuro_red_flag in {None, "", "Unknown"}
    ):
        return action_result(
            "A_PSEUDO_UNSTABLE_REVIEW",
            current_node="PSEUDO-02",
            next_node="CG-01",
            facts=facts,
            missing=[
                field
                for field in [
                    "visual_function_stable",
                    "visual_function_threatened",
                    "major_neuro_red_flag",
                ]
                if facts.get(field) in {None, "", "Unknown", "Uncertain"}
            ],
        )

    # PSEUDO-03: baseline OCT/disc documentation
    if facts.get("baseline_disc_docs_available") != "Yes":
        return action_result(
            "A_OBTAIN_BASELINE_DISC_DOCS",
            current_node="PSEUDO-03",
            next_node="PSEUDO-03",
            facts=facts,
            missing=["baseline_disc_docs_available"],
        )

    # PSEUDO-04: formal stability gate
    if visual_stable != "Yes":
        return action_result(
            "A_PSEUDO_UNSTABLE_REVIEW",
            current_node="PSEUDO-04",
            next_node="CG-01",
            facts=facts,
            missing=["visual_function_stable"],
        )

    # PSEUDO-05: booked 4–6 week review
    followup_booked = facts.get("pseudo_followup_booked")
    followup_weeks = facts.get("pseudo_followup_weeks")

    followup_valid = (
        followup_booked == "Yes"
        and isinstance(followup_weeks, int)
        and 4 <= followup_weeks <= 6
    )

    if not followup_valid:
        missing = []

        if followup_booked != "Yes":
            missing.append("pseudo_followup_booked")

        if (
            not isinstance(followup_weeks, int)
            or followup_weeks < 4
            or followup_weeks > 6
        ):
            missing.append("pseudo_followup_weeks")

        return action_result(
            "A_BOOK_PSEUDO_4_6W",
            current_node="PSEUDO-05",
            next_node="PSEUDO-05",
            facts=facts,
            missing=missing,
        )

    # PSEUDO-06: safety net and ownership
    safety_missing = []

    if facts.get("return_precautions_given") != "Yes":
        safety_missing.append("return_precautions_given")

    if facts.get("clinical_owner_documented") != "Yes":
        safety_missing.append("clinical_owner_documented")

    if safety_missing:
        return action_result(
            "A_COMPLETE_SAFETY_NET",
            current_node="PSEUDO-06",
            next_node="PSEUDO-06",
            facts=facts,
            missing=safety_missing,
        )

    # Follow-up package complete; now apply human-authorised closure gate.
    followup_result = action_result(
        "A_PSEUDO_FOLLOWUP_READY",
        current_node="PSEUDO-06",
        next_node="CLOSE-01",
        facts=facts,
    )

    closure_result = closure_gate(facts)

    closure_result["action_codes"] = [
        "A_PSEUDO_FOLLOWUP_READY",
        closure_result["action_codes"][0],
    ]

    return closure_result


def evaluate(facts):
    """
    Deterministic rule engine for synthetic demonstration data only.

    Unknown is intentionally never converted to No. The function returns the
    earliest active hard stop or required action in the defined workflow.
    """

    age = facts.get("patient_age_years")

    # ENTRY-01
    if not isinstance(age, int) or age < 0 or age > 120:
        return action_result(
            "A_MISSING_AGE",
            current_node="ENTRY-01",
            next_node="ENTRY-01",
            facts=facts,
            missing=["patient_age_years"],
        )

    # SCOPE-01
    if age < 16:
        return action_result(
            "A_ROUTE_RCH_PEDS",
            current_node="SCOPE-01",
            next_node="CLOSE-01",
            facts=facts,
        )

    # EXAM-01
    if not core_exam_complete(facts):
        exam_fields = [
            "visual_acuity_status",
            "pupil_exam_status",
            "iop_status",
            "formal_perimetry_status",
            "dilated_fundus_status",
        ]

        missing = [
            field
            for field in exam_fields
            if facts.get(field) not in {"Completed", "Unable_with_reason"}
        ]

        return action_result(
            "A_COMPLETE_OCULAR_EXAM",
            current_node="EXAM-01",
            next_node="EXAM-01",
            facts=facts,
            missing=missing,
        )

    disc_status = facts.get("papilloedema_status")
    reviewer = facts.get("papilloedema_reviewer_level")

    # DISC-01 and DISC-02
    if disc_status == "Not_confirmed":
        return evaluate_pseudopap_route(facts)

    if disc_status == "Uncertain":
        return action_result(
            "A_SENIOR_DISC_REVIEW",
            current_node="DISC-01",
            next_node="DISC-02",
            facts=facts,
            missing=["papilloedema_status", "papilloedema_reviewer_level"],
        )

    if disc_status != "Confirmed" or reviewer in {None, "", "Unknown"}:
        return action_result(
            "A_SENIOR_DISC_REVIEW",
            current_node="DISC-01",
            next_node="DISC-02",
            facts=facts,
            missing=["papilloedema_status", "papilloedema_reviewer_level"],
        )

    # RISK-01
    visual_risk = facts.get("visual_function_threatened")

    if visual_risk in {"Yes", "Possible"}:
        return action_result(
            "A_IMMEDIATE_NOPH_VISUAL_THREAT",
            current_node="RISK-01",
            next_node="BP-01",
            facts=facts,
        )

    if visual_risk != "No":
        return action_result(
            "A_ASSESS_VISUAL_RISK",
            current_node="RISK-01",
            next_node="RISK-01",
            facts=facts,
            missing=["visual_function_threatened"],
        )

    # BP-01
    sbp = facts.get("bp_systolic_mmhg")
    dbp = facts.get("bp_diastolic_mmhg")

    if not isinstance(sbp, int) or not isinstance(dbp, int):
        missing = []

        if not isinstance(sbp, int):
            missing.append("bp_systolic_mmhg")

        if not isinstance(dbp, int):
            missing.append("bp_diastolic_mmhg")

        return action_result(
            "A_MEASURE_BP",
            current_node="BP-01",
            next_node="BP-01",
            facts=facts,
            missing=missing,
        )

    # BP-02
    if sbp >= 180 or dbp >= 120:
        return action_result(
            "A_HYPERTENSIVE_EMERGENCY",
            current_node="BP-02",
            next_node="CLOSE-01",
            facts=facts,
        )

    # NEURO-01
    if not neuro_exam_complete(facts):
        required_neuro_fields = [
            "cranial_nerve_exam_status",
            "focal_neurological_signs",
            "reduced_consciousness",
            "meningism",
            "seizure",
            "other_cranial_nerve_abnormality",
        ]

        missing = [
            field
            for field in required_neuro_fields
            if facts.get(field) in {None, "", "Unknown", "Not_done"}
        ]

        return action_result(
            "A_COMPLETE_NEURO_EXAM",
            current_node="NEURO-01",
            next_node="NEURO-01",
            facts=facts,
            missing=missing,
        )

    # NEURO-02
    neuro_red_flag = any(
        facts.get(field) == "Yes"
        for field in [
            "focal_neurological_signs",
            "reduced_consciousness",
            "meningism",
            "seizure",
            "other_cranial_nerve_abnormality",
        ]
    )

    if neuro_red_flag:
        return action_result(
            "A_URGENT_ALTERNATE_NEURO",
            current_node="NEURO-02",
            next_node="CLOSE-01",
            facts=facts,
        )

    # IMG-01
    if facts.get("brain_imaging_status") != "Completed_adequate":
        return action_result(
            "A_URGENT_BRAIN_IMAGING",
            current_node="IMG-01",
            next_node="IMG-01",
            facts=facts,
            missing=["brain_imaging_status", "brain_imaging_modality"],
        )

    # IMG-02
    if facts.get("radiology_interpretation_uncertain") in {
        None,
        "",
        "Unknown",
        "Yes",
    }:
        return action_result(
            "A_RADIOLOGY_REVIEW",
            current_node="IMG-02",
            next_node="IMG-02",
            facts=facts,
            missing=["radiology_interpretation_uncertain"],
        )

    if facts.get("secondary_structural_or_meningeal_pathology") == "Yes":
        return action_result(
            "A_URGENT_ALTERNATE_IMAGING",
            current_node="IMG-02",
            next_node="CLOSE-01",
            facts=facts,
        )

    if facts.get("secondary_structural_or_meningeal_pathology") != "No":
        return action_result(
            "A_RADIOLOGY_REVIEW",
            current_node="IMG-02",
            next_node="IMG-02",
            facts=facts,
            missing=["secondary_structural_or_meningeal_pathology"],
        )

    # VEN-01
    if facts.get("venography_status") != "Completed_adequate":
        return action_result(
            "A_URGENT_VENOGRAPHY",
            current_node="VEN-01",
            next_node="VEN-01",
            facts=facts,
            missing=["venography_status"],
        )

    # VEN-02
    if facts.get("cerebral_venous_sinus_thrombosis") == "Yes":
        return action_result(
            "A_SECONDARY_VENOUS_PATHWAY",
            current_node="VEN-02",
            next_node="CLOSE-01",
            facts=facts,
        )

    if facts.get("cerebral_venous_sinus_thrombosis") != "No":
        return action_result(
            "A_RADIOLOGY_REVIEW",
            current_node="VEN-02",
            next_node="VEN-02",
            facts=facts,
            missing=["cerebral_venous_sinus_thrombosis"],
        )

    # FBC-01
    if facts.get("fbc_status") not in {"Normal", "Abnormal"}:
        return action_result(
            "A_OBTAIN_FBC",
            current_node="FBC-01",
            next_node="LP-01",
            facts=facts,
            missing=["fbc_status"],
        )

    # LP-01
    lp_status = facts.get("lp_status")

    if lp_status == "Completed":
        pass
    elif lp_status in {
        "Contraindicated",
        "Formally_deferred_by_senior",
        "Unknown",
        None,
        "",
    }:
        return action_result(
            "A_LP_DEFERRED_REVIEW",
            current_node="LP-01",
            next_node="CG-01",
            facts=facts,
            missing=["lp_status"],
        )
    else:
        return action_result(
            "A_LP_REQUIRED",
            current_node="LP-01",
            next_node="LP-01",
            facts=facts,
            missing=["lp_status"],
        )

    # LP-02
    if facts.get("lp_technique_valid") != "Yes":
        return action_result(
            "A_REVIEW_LP_VALIDITY",
            current_node="LP-02",
            next_node="CG-01",
            facts=facts,
            missing=["lp_technique_valid"],
        )

    # LP-03
    opening_pressure = facts.get("lp_opening_pressure_cm_csf")

    if not isinstance(opening_pressure, (int, float)):
        return action_result(
            "A_REVIEW_LP_VALIDITY",
            current_node="LP-03",
            next_node="CG-01",
            facts=facts,
            missing=["lp_opening_pressure_cm_csf"],
        )

    if opening_pressure <= 25:
        return action_result(
            "A_IIH_NOT_CONFIRMED",
            current_node="LP-03",
            next_node="CG-01",
            facts=facts,
        )

    # CSF-01
    minimum_csf_tests_complete = facts.get("minimum_csf_tests_complete")
    csf_contents_status = facts.get("csf_contents_status")

    if (
        minimum_csf_tests_complete != "Yes"
        or csf_contents_status in {None, "", "Unknown", "Pending"}
    ):
        missing = []

        if minimum_csf_tests_complete != "Yes":
            missing.append("minimum_csf_tests_complete")

        if csf_contents_status in {None, "", "Unknown", "Pending"}:
            missing.append("csf_contents_status")

        return action_result(
            "A_WAIT_CSF",
            current_node="CSF-01",
            next_node="CSF-01",
            facts=facts,
            missing=missing,
        )

    # CSF-02
    if csf_contents_status == "Abnormal":
        return action_result(
            "A_ALTERNATE_CSF_PATHWAY",
            current_node="CSF-02",
            next_node="CLOSE-01",
            facts=facts,
        )

    if csf_contents_status != "Normal":
        return action_result(
            "A_WAIT_CSF",
            current_node="CSF-02",
            next_node="CSF-01",
            facts=facts,
            missing=["csf_contents_status"],
        )

    # SEC-01
    if facts.get("secondary_cause_screen_complete") != "Yes":
        return action_result(
            "A_COMPLETE_SECONDARY_SCREEN",
            current_node="SEC-01",
            next_node="SEC-01",
            facts=facts,
            missing=["secondary_cause_screen_complete"],
        )

    # SEC-02
    secondary_cause_identified = facts.get("secondary_cause_identified")

    if secondary_cause_identified == "Yes":
        return action_result(
            "A_SECONDARY_IH_PATHWAY",
            current_node="SEC-02",
            next_node="CLOSE-01",
            facts=facts,
        )

    if secondary_cause_identified != "No":
        return action_result(
            "A_SECONDARY_CAUSE_REVIEW",
            current_node="SEC-02",
            next_node="CG-01",
            facts=facts,
            missing=["secondary_cause_identified"],
        )

    # DIAG-01
    iih_criteria_complete = facts.get("iih_criteria_complete")

    if iih_criteria_complete == "Conflict":
        return action_result(
            "A_REVIEW_CRITERIA_CONFLICT",
            current_node="DIAG-01",
            next_node="CG-01",
            facts=facts,
        )

    if iih_criteria_complete != "Yes":
        return action_result(
            "A_IIH_NOT_CONFIRMED",
            current_node="DIAG-01",
            next_node="CG-01",
            facts=facts,
            missing=["iih_criteria_complete"],
        )

    # FULM-01
    severe_visual_loss = facts.get("severe_visual_loss_within_4_weeks")
    rapid_worsening = facts.get("vision_worsening_over_days")

    if severe_visual_loss == "Yes" and rapid_worsening == "Yes":
        return action_result(
            "A_FULMINANT_IIH_CANDIDATE",
            current_node="FULM-01",
            next_node="CLOSE-01",
            facts=facts,
        )

    if (
        severe_visual_loss in {None, "", "Unknown"}
        or rapid_worsening in {None, "", "Unknown"}
    ):
        return action_result(
            "A_ASSESS_VISUAL_RISK",
            current_node="FULM-01",
            next_node="RISK-01",
            facts=facts,
            missing=[
                field
                for field in [
                    "severe_visual_loss_within_4_weeks",
                    "vision_worsening_over_days",
                ]
                if facts.get(field) in {None, "", "Unknown"}
            ],
        )

    # TYPE-01
    typical_profile_flag = facts.get("typical_profile_flag")

    if typical_profile_flag == "Typical":
        candidate_result = action_result(
            "A_TYPICAL_IIH_CANDIDATE",
            current_node="TYPE-01",
            next_node="CG-01",
            facts=facts,
        )

        contact_result = contact_gate(
            facts,
            pending_node="CLOSE-01",
            immediate_trigger=False,
        )

        contact_result["action_codes"] = [
            "A_TYPICAL_IIH_CANDIDATE",
            contact_result["action_codes"][0],
        ]

        return contact_result

    if typical_profile_flag == "Atypical":
        candidate_result = action_result(
            "A_ATYPICAL_IIH_CANDIDATE",
            current_node="TYPE-01",
            next_node="CG-01",
            facts=facts,
        )

        contact_result = contact_gate(
            facts,
            pending_node="CLOSE-01",
            immediate_trigger=False,
        )

        contact_result["action_codes"] = [
            "A_ATYPICAL_IIH_CANDIDATE",
            contact_result["action_codes"][0],
        ]

        return contact_result

    return action_result(
        "A_ATYPICAL_PROFILE_REVIEW",
        current_node="TYPE-01",
        next_node="CG-01",
        facts=facts,
        missing=["typical_profile_flag"],
    )
