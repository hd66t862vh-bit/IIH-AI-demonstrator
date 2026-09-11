from rule_engine import evaluate


def baseline_confirmed_case():
    return {
        "synthetic_case_id": "SYN-BASELINE",
        "patient_age_years": 29,
        "clinical_owner": "ED",

        "visual_acuity_status": "Completed",
        "pupil_exam_status": "Completed",
        "iop_status": "Completed",
        "formal_perimetry_status": "Completed",
        "dilated_fundus_status": "Completed",

        "papilloedema_status": "Confirmed",
        "papilloedema_reviewer_level": "AO",
        "visual_function_threatened": "No",

        "bp_systolic_mmhg": 130,
        "bp_diastolic_mmhg": 80,

        "cranial_nerve_exam_status": "Completed",
        "focal_neurological_signs": "No",
        "reduced_consciousness": "No",
        "meningism": "No",
        "seizure": "No",
        "other_cranial_nerve_abnormality": "No",
        "major_neuro_red_flag": "No",

        "brain_imaging_status": "Completed_adequate",
        "brain_imaging_modality": "MRI",
        "secondary_structural_or_meningeal_pathology": "No",
        "radiology_interpretation_uncertain": "No",

        "venography_status": "Completed_adequate",
        "cerebral_venous_sinus_thrombosis": "No",

        "fbc_status": "Normal",

        "lp_status": "Completed",
        "lp_technique_valid": "Yes",
        "lp_opening_pressure_cm_csf": 31.0,

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
        "pseudo_followup_weeks": 5,
        "return_precautions_given": "Yes",

        "noph_plan_status": "No_plan",
        "active_plan_version": "",
        "callback_requested_due": "No",
        "clinical_deterioration_since_plan": "No",
        "unexpected_result_since_plan": "No",
        "ownership_or_plan_unclear": "No",

        "clinical_owner_documented": "Yes",
        "disposition_approved": "No",
    }


def baseline_pseudopap_case():
    case = baseline_confirmed_case()

    case.update(
        {
            "synthetic_case_id": "SYN-PSEUDO",
            "papilloedema_status": "Not_confirmed",
            "papilloedema_reviewer_level": "AO",
            "visual_function_threatened": "No",
            "visual_function_stable": "Yes",
            "major_neuro_red_flag": "No",
            "baseline_disc_docs_available": "Yes",
            "pseudo_followup_booked": "Yes",
            "pseudo_followup_weeks": 5,
            "return_precautions_given": "Yes",
            "clinical_owner_documented": "Yes",
            "disposition_approved": "No",
        }
    )

    return case


def assert_action(name, case, expected_action, expected_node=None):
    result = evaluate(case)

    actual_actions = result["action_codes"]

    passed = expected_action in actual_actions

    if expected_node is not None:
        passed = passed and result["current_node"] == expected_node

    status = "PASS" if passed else "FAIL"

    print(f"{status} | {name}")
    print(f"  Expected action: {expected_action}")
    print(f"  Actual action(s): {actual_actions}")
    print(f"  Current node: {result['current_node']}")
    print(f"  Next node: {result['next_node']}")
    print(f"  Urgency: {result['urgency']}")
    print(f"  Blocks disposition: {result['hard_stop']}")
    print()

    return passed


def run_tests():
    results = []

    case = baseline_confirmed_case()
    case["patient_age_years"] = 12
    results.append(
        assert_action(
            "T01: Paediatric pathway exit",
            case,
            "A_ROUTE_RCH_PEDS",
            "SCOPE-01",
        )
    )

    case = baseline_confirmed_case()
    case["papilloedema_status"] = "Uncertain"
    results.append(
        assert_action(
            "T02: Uncertain papilloedema requires senior review",
            case,
            "A_SENIOR_DISC_REVIEW",
            "DISC-01",
        )
    )

    case = baseline_confirmed_case()
    case["visual_function_threatened"] = "Possible"
    results.append(
        assert_action(
            "T03: Possible visual threat",
            case,
            "A_IMMEDIATE_NOPH_VISUAL_THREAT",
            "RISK-01",
        )
    )

    case = baseline_confirmed_case()
    case["bp_systolic_mmhg"] = 190
    case["bp_diastolic_mmhg"] = 122
    results.append(
        assert_action(
            "T04: Hypertensive emergency flag",
            case,
            "A_HYPERTENSIVE_EMERGENCY",
            "BP-02",
        )
    )

    case = baseline_confirmed_case()
    case["cerebral_venous_sinus_thrombosis"] = "Yes"
    results.append(
        assert_action(
            "T05: Causative venous pathology",
            case,
            "A_SECONDARY_VENOUS_PATHWAY",
            "VEN-02",
        )
    )

    case = baseline_confirmed_case()
    case["venography_status"] = "Not_done"
    results.append(
        assert_action(
            "T06: Venography missing",
            case,
            "A_URGENT_VENOGRAPHY",
            "VEN-01",
        )
    )

    case = baseline_confirmed_case()
    results.append(
        assert_action(
            "T07: Typical IIH candidate",
            case,
            "A_TYPICAL_IIH_CANDIDATE",
            "CG-02",
        )
    )

    case = baseline_confirmed_case()
    case["typical_profile_flag"] = "Atypical"
    results.append(
        assert_action(
            "T08: Atypical IIH candidate",
            case,
            "A_ATYPICAL_IIH_CANDIDATE",
            "CG-02",
        )
    )

    case = baseline_confirmed_case()
    case["lp_opening_pressure_cm_csf"] = 22.0
    results.append(
        assert_action(
            "T09: Opening pressure below threshold",
            case,
            "A_IIH_NOT_CONFIRMED",
            "LP-03",
        )
    )

    case = baseline_confirmed_case()
    case["csf_contents_status"] = "Abnormal"
    results.append(
        assert_action(
            "T10: Abnormal CSF route",
            case,
            "A_ALTERNATE_CSF_PATHWAY",
            "CSF-02",
        )
    )

    case = baseline_pseudopap_case()
    case["pseudo_followup_booked"] = "No"
    results.append(
        assert_action(
            "T11: Pseudopap follow-up not booked",
            case,
            "A_BOOK_PSEUDO_4_6W",
            "PSEUDO-05",
        )
    )

    case = baseline_pseudopap_case()
    results.append(
        assert_action(
            "T12: Pseudopap follow-up package complete",
            case,
            "A_PSEUDO_FOLLOWUP_READY",
            "CLOSE-01",
        )
    )

    case = baseline_confirmed_case()
    case["noph_plan_status"] = "Active"
    case["active_plan_version"] = "NOPH-PLAN-001"
    case["callback_requested_due"] = "No"
    case["clinical_deterioration_since_plan"] = "No"
    case["unexpected_result_since_plan"] = "No"
    case["ownership_or_plan_unclear"] = "No"
    results.append(
        assert_action(
            "T13: Active plan suppresses duplicate call",
            case,
            "A_FOLLOW_EXISTING_PLAN",
            "CG-03",
        )
    )

    case = baseline_confirmed_case()
    case["noph_plan_status"] = "Active"
    case["active_plan_version"] = "NOPH-PLAN-001"
    case["clinical_deterioration_since_plan"] = "Yes"
    results.append(
        assert_action(
            "T14: Deterioration triggers recontact",
            case,
            "A_RECONTACT_NOPH",
            "CG-03",
        )
    )

    case = baseline_confirmed_case()
    case["venography_status"] = "Unknown"
    results.append(
        assert_action(
            "T15: Unknown is not converted to No",
            case,
            "A_URGENT_VENOGRAPHY",
            "VEN-01",
        )
    )

    passed_count = sum(results)
    total_count = len(results)

    print("=" * 60)
    print(f"RESULT: {passed_count}/{total_count} tests passed")
    print("=" * 60)

    if passed_count != total_count:
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()
