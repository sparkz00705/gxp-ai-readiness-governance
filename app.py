import streamlit as st
from datetime import date
import requests


# ============================================================
# CONFIGURATION
# ============================================================

COUNTER_URL = "https://abacus.jasoncameron.dev/hit/sriram-gxp-ai-readiness/visits"

USER_MANUAL_URL = (
    "https://raw.githubusercontent.com/sparkz00705/"
    "gxp-ai-readiness-governance/main/"
    "GxP_AI_Readiness_Governance_User_Manual.pdf"
)

PREVIOUS_PROJECT_URL = "https://ai-risk-issue-dashboard.streamlit.app/"

LINKEDIN_URL = "https://www.linkedin.com/in/sriramsampath81/"


# ============================================================
# VISITOR COUNTER
# ============================================================

def get_visit_count():
    try:
        response = requests.get(COUNTER_URL, timeout=5)
        response.raise_for_status()

        data = response.json()

        return data.get("value", 0)

    except Exception:
        return None


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="GxP AI Readiness & Governance Assessment",
    page_icon="🧪",
    layout="wide",
)


# ============================================================
# CONSTANTS
# ============================================================

ANSWER_SCORE = {
    "Yes": 100,
    "Partly": 70,
    "No": 30,
}

STATUS = {
    "Green": "🟢 Green",
    "Amber": "🟠 Amber",
    "Red": "🔴 Red",
}


# ============================================================
# GxP DOMAIN DESCRIPTIONS
# ============================================================

DOMAIN_DESCRIPTIONS = {

    "GMP":
        "Good Manufacturing Practice — manufacturing, process, "
        "product quality, batch/release, deviations, CAPA and change control.",

    "GLP":
        "Good Laboratory Practice — non-clinical safety studies, "
        "study conduct, raw data, QA oversight, reporting and archiving.",

    "GCP":
        "Good Clinical Practice — clinical trials, participant safety, "
        "protocol conduct, clinical data, oversight and essential records.",

    "GDP":
        "Good Distribution Practice — storage, distribution, transport, "
        "traceability and product integrity.",

    "PV / GVP":
        "Pharmacovigilance / Good Pharmacovigilance Practices — safety "
        "information, case processing, signal detection, reporting and oversight.",

    "GDocP / Data Integrity":
        "Good Documentation Practices / data integrity — complete, "
        "consistent, accurate, attributable and controlled records.",

    "CSV / CSA":
        "Computerized Systems / Computer System Validation / Computer Software "
        "Assurance — fit-for-purpose assurance, evidence, controls and lifecycle.",

    "Multiple / Cross-functional GxP":
        "Use when the AI solution spans more than one regulated GxP area.",

    "Not yet determined":
        "Use when the regulated context is still being assessed; route to "
        "appropriate Quality / Regulatory stakeholders.",
}


# ============================================================
# DOMAIN-SPECIFIC QUESTIONS
# ============================================================

DOMAIN_QUESTIONS = {

    "GMP": [

        "Potential impact on manufacturing process or product quality is understood",

        "Deviation / CAPA / change-control implications have been assessed",

        "Batch, release, or disposition impact is understood where applicable",

        "Manufacturing / Quality / Validation ownership is defined",
    ],

    "GLP": [

        "Study context and intended use are clearly defined",

        "Raw data, study records, and traceability expectations are understood",

        "Study Director / QA responsibilities are defined where applicable",

        "Reporting and archiving implications are understood",
    ],

    "GCP": [

        "Clinical-trial context and intended use are clearly defined",

        "Participant safety and subject-protection implications are assessed",

        "Sponsor / investigator / functional ownership is defined",

        "Clinical data and essential-record implications are understood",
    ],

    "GDP": [

        "Storage / transport / distribution impact is understood",

        "Product traceability expectations are defined",

        "Temperature / handling / integrity risks are understood where applicable",

        "Distribution / Quality ownership is defined",
    ],

    "PV / GVP": [

        "Safety-data and case-processing context is clearly defined",

        "Signal detection / assessment / reporting impact is understood",

        "Safety oversight and medical / PV ownership are defined",

        "Audit-trail and case-data traceability expectations are understood",
    ],

    "GDocP / Data Integrity": [

        "Records and documentation affected by the AI use case are identified",

        "Data integrity risks and controls are understood",

        "Attribution, traceability, and audit-trail expectations are defined",

        "Record retention / archival expectations are understood",
    ],

    "CSV / CSA": [

        "System / software assurance scope is identified",

        "Intended use and critical functions are documented",

        "Risk-based assurance and evidence expectations are defined",

        "Change control and release evidence are defined",
    ],

    "Multiple / Cross-functional GxP": [

        "All applicable GxP domains are identified",

        "Cross-domain ownership and governance are defined",

        "Conflicting or overlapping control requirements are assessed",

        "An integrated assurance / validation strategy is defined",
    ],

    "Not yet determined": [

        "Potential regulated impact has been identified",

        "Appropriate Quality / Regulatory stakeholders are engaged",

        "The proposed context of use is documented",

        "A path to determine GxP applicability is defined",
    ],
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def score_answers(prefix, questions):

    values = []

    for idx, question in enumerate(questions, 1):

        answer = st.radio(
            question,
            ["Yes", "Partly", "No"],
            key=f"{prefix}_{idx}",
            horizontal=True,
        )

        values.append(ANSWER_SCORE[answer])

    return round(sum(values) / len(values))


def score_status(score):

    if score >= 80:
        return "Green"

    if score >= 60:
        return "Amber"

    return "Red"


def decision_for(score, gxp_domain):

    high_risk_domains = [
        "GMP",
        "GLP",
        "GCP",
        "PV / GVP",
        "Multiple / Cross-functional GxP",
    ]

    if score >= 80 and gxp_domain not in high_risk_domains:

        return (
            "Proceed to the next delivery stage with routine governance "
            "and documented qualified stakeholder oversight."
        )

    if score >= 75:

        return (
            "Proceed to controlled pilot planning subject to documented "
            "QA, validation and appropriate stakeholder review, with "
            "material readiness gaps tracked to closure."
        )

    if score >= 60:

        return (
            "Proceed to controlled pilot planning only after the "
            "highest-priority readiness gaps are addressed."
        )

    if score >= 50:

        return (
            "Establish and track a formal gap-closure plan before "
            "pilot or validation activities."
        )

    return (
        "Do not proceed to pilot / production yet. Establish the required "
        "governance, quality, data and delivery controls first."
    )


def gap_text(section):

    return {

        "GxP Domain Assessment":
            "Confirm applicable GxP scope and ownership with qualified "
            "Quality / Regulatory stakeholders.",

        "Context of Use":
            "Clarify intended use, accountability, boundaries and "
            "human oversight.",

        "Data Governance":
            "Close data-source, lineage, quality and integrity gaps.",

        "Model & Validation":
            "Define performance criteria, assurance / validation ownership, "
            "explainability and change controls.",

        "Human Oversight":
            "Define accountable human review, escalation and override controls.",

        "Decision Accountability & Traceability":
            "Define how individual AI-supported decisions, approvals / overrides, "
            "timestamps and relevant model/version information will be recorded "
            "and reconstructed.",

        "CSV / CSA & Quality":
            "Agree the risk-based assurance / validation strategy and "
            "evidence expectations.",

        "Lifecycle Management":
            "Define monitoring, change triggers, periodic review and "
            "retirement / rollback.",

        "Program Readiness":
            "Confirm governance, roles, resources, dependencies and "
            "adoption readiness.",
    }.get(
        section,
        "Address the identified readiness gaps.",
    )


# ============================================================
# SAMPLE ASSESSMENT
# ============================================================

def show_sample_assessment():

    st.success(
        "Sample loaded: GMP — AI-assisted Deviation Triage"
    )

    st.markdown(
        """
**Business objective:**  
Use AI to prioritize quality deviations for review while keeping final
disposition with a qualified human reviewer.

**AI type:** Classification

**Regulated decision impact:** Supports a regulated decision

**Primary GxP domain:** GMP
"""
    )

    st.subheader("Illustrative sample result")

    sample_data = [

        ["GxP domain assessment", "75%", "🟠 Amber"],

        ["Context of Use", "68%", "🟠 Amber"],

        ["Data Governance", "64%", "🟠 Amber"],

        ["Model & Validation", "58%", "🔴 Red"],

        ["Human Oversight", "78%", "🟠 Amber"],

        ["Decision Accountability & Traceability", "55%", "🔴 Red"],

        ["CSV / CSA & Quality", "63%", "🟠 Amber"],

        ["Lifecycle Management", "55%", "🔴 Red"],

        ["Program Readiness", "82%", "🟢 Green"],
    ]

    st.table(
        {
            "Assessment area": [row[0] for row in sample_data],
            "Score": [row[1] for row in sample_data],
            "Status": [row[2] for row in sample_data],
        }
    )

    st.markdown(
        """
### Overall readiness: **64% — AMBER**

### Top gaps

1. Model validation / assurance approach is not fully defined.
2. Model and data change triggers are not established.
3. Data lineage and data-quality controls require further evidence.
4. Human escalation and override expectations need clearer documentation.
5. The accountable decision-maker and decision record are not yet fully traceable.

### Recommended governance action

> Proceed to controlled pilot planning only after the highest-priority
> data, validation, lifecycle, human-oversight and decision-traceability
> gaps are addressed.

This sample is illustrative and does not represent a regulatory or
compliance conclusion.
"""
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🧪 GxP AI Readiness & Governance Assessment"
)

st.caption(
    "A Life Sciences project-governance decision-support tool for "
    "assessing AI initiatives across GxP context, data, validation, "
    "human oversight, accountability, lifecycle and delivery readiness."
)


# ============================================================
# IMPORTANT NOTE
# ============================================================

with st.expander(
    "Important: what this tool does (and does not do)",
    expanded=False,
):

    st.write(
        "This is an initial project-readiness assessment. "
        "It does not determine legal or regulatory compliance and does "
        "not replace QA, Validation, Regulatory, Privacy, Security, Data, "
        "Medical, Pharmacovigilance, Clinical, Manufacturing or other "
        "qualified review."
    )


# ============================================================
# NAVIGATION / LANDING AREA
# ============================================================

nav_a, nav_b, nav_c = st.columns([2, 1, 1])

with nav_a:

    st.markdown("### Start here")

    st.caption(
        "Run your own assessment or load a sample to see how the tool works."
    )


with nav_b:

    if st.button(
        "🎯 Load Sample Assessment",
        use_container_width=True,
    ):

        st.session_state["show_sample"] = True


with nav_c:

    st.markdown("**📖 User Manual**")

    st.markdown(
        f"[Open User Manual]({USER_MANUAL_URL})"
    )


if st.session_state.get("show_sample"):

    show_sample_assessment()


# ============================================================
# PREVIOUS PORTFOLIO PROJECT
# ============================================================

with st.expander(
    "Previous PM Portfolio Project",
    expanded=False,
):

    st.markdown(
        f"""
### Intelligent Risk & Issue Management Dashboard

Earlier independent Project Management tool focused on
real-time risk and issue visibility.

[Open the Intelligent Risk & Issue Management Dashboard]({PREVIOUS_PROJECT_URL})
"""
    )


# ============================================================
# ASSESSMENT METHODOLOGY
# ============================================================

with st.expander(
    "Assessment Methodology",
    expanded=False,
):

    st.markdown(
        """
### What is assessed

- GxP domain context
- Context of Use
- Data Governance & Data Integrity
- AI Model & Validation / Assurance
- Human Oversight
- Decision Accountability & Traceability
- CSV / CSA & Quality
- Lifecycle Management
- Program Readiness
- Delivery Risk

### Response scoring

**Yes = 100**

**Partly = 70**

**No = 30**

### Status

🟢 **Green = 80–100%**

🟠 **Amber = 60–79%**

🔴 **Red = below 60%**

The result is an initial project-readiness indicator.

It does **not** declare GMP, GLP, GCP, GDP, GVP or other regulatory
compliance and does not replace qualified stakeholder review.
"""
    )


# ============================================================
# SECTION 1 — PROJECT AND AI USE CASE
# ============================================================

st.header("1. Project & AI Use Case")

c1, c2 = st.columns(2)

with c1:

    project_name = st.text_input(
        "AI project / use case name",
        placeholder="e.g., AI-assisted Deviation Triage",
    )

    business_objective = st.text_area(
        "Business objective",
        placeholder="What problem is the AI intended to solve?",
    )


with c2:

    ai_type = st.selectbox(
        "Primary AI use type",
        [
            "Prediction",
            "Classification",
            "Recommendation",
            "Detection",
            "Document / text analysis",
            "Generative AI",
            "Other",
        ],
    )

    decision_impact = st.selectbox(
        "Impact on regulated decisions",
        [
            "No direct impact",
            "Supports a regulated decision",
            "Influences a regulated decision",
            "Automates part of a regulated decision",
        ],
    )


# ============================================================
# SECTION 2 — GxP DOMAIN
# ============================================================

st.header("2. Select Applicable GxP / Regulated Domain")

gxp_domain = st.selectbox(
    "Primary GxP domain",
    list(DOMAIN_DESCRIPTIONS.keys()),
)

st.info(
    DOMAIN_DESCRIPTIONS[gxp_domain]
)


if gxp_domain == "Multiple / Cross-functional GxP":

    st.multiselect(
        "Additional GxP areas in scope",
        [
            "GMP",
            "GLP",
            "GCP",
            "GDP",
            "PV / GVP",
            "GDocP / Data Integrity",
            "CSV / CSA",
        ],
    )


st.subheader("GxP-specific readiness")

domain_score = score_answers(
    "domain",
    DOMAIN_QUESTIONS[gxp_domain],
)


# ============================================================
# SECTION 3 — CONTEXT OF USE
# ============================================================

st.header("3. Context of Use & Governance")

context_score = score_answers(
    "context",
    [
        "Intended use is clearly documented",

        "Accountability for the final decision is defined",

        "Out-of-scope / prohibited uses are documented",

        "Human review and override expectations are defined",
    ],
)


# ============================================================
# SECTION 4 — DATA
# ============================================================

st.header("4. Data Governance & Data Integrity")

data_score = score_answers(
    "data",
    [
        "Data sources are identified and owned",

        "Data lineage is documented",

        "Data quality has been assessed",

        "Data integrity risks are understood",

        "Training / validation / production data controls are defined",
    ],
)


# ============================================================
# SECTION 5 — MODEL / VALIDATION
# ============================================================

st.header("5. AI Model & Validation / Assurance Readiness")

model_score = score_answers(
    "model",
    [
        "Model purpose and acceptance criteria are defined",

        "Performance measures are defined",

        "Validation / assurance approach and ownership are defined",

        "Explainability / transparency expectations are defined",

        "Model versioning and change controls are defined",
    ],
)


# ============================================================
# SECTION 6 — HUMAN OVERSIGHT
# ============================================================

st.header("6. Human Oversight & Decision Governance")

human_score = score_answers(
    "human",
    [
        "Named human reviewer / accountable owner exists",

        "Human override is possible where required",

        "Escalation criteria are defined",

        "AI limitations / uncertainty are communicated",
    ],
)


# ============================================================
# SECTION 7 — DECISION ACCOUNTABILITY / TRACEABILITY
# ============================================================

st.header("7. Decision Accountability & Traceability")

st.caption(
    "This section checks whether the organization can show who stood "
    "behind an AI-supported decision and reconstruct the relevant "
    "decision record later."
)

decision_traceability_score = score_answers(
    "decision_traceability",
    [
        "The accountable decision-maker for the AI-supported decision is explicitly identified",

        "Each AI-supported decision can be linked to the person who reviewed it",

        "Approval or override by the accountable decision-maker is captured",

        "The organization can reconstruct the decision and relevant AI output later",

        "Timestamp and relevant model / version information are retained where appropriate",
    ],
)


# ============================================================
# SECTION 8 — CSV / CSA
# ============================================================

st.header("8. CSV / CSA & Quality Controls")

validation_score = score_answers(
    "validation",
    [
        "Validation / assurance strategy is agreed",

        "Requirements and intended use are traceable",

        "Testing and evidence expectations are defined",

        "Change control and release approval are defined",
    ],
)


# ============================================================
# SECTION 9 — LIFECYCLE
# ============================================================

st.header("9. Lifecycle Management")

lifecycle_score = score_answers(
    "lifecycle",
    [
        "Production monitoring is defined",

        "Model / data change triggers are defined",

        "Periodic performance review is planned",

        "Retirement / rollback approach is defined",
    ],
)


# ============================================================
# SECTION 10 — PROGRAM READINESS
# ============================================================

st.header("10. Program & Organizational Readiness")

program_score = score_answers(
    "program",
    [
        "Business owner and sponsor are identified",

        "QA / Validation / IT / Data / domain roles are identified",

        "Resources and budget are understood",

        "Key dependencies and milestones are documented",

        "Change, training and adoption needs are understood",
    ],
)


# ============================================================
# SECTION 11 — DELIVERY RISK
# ============================================================

st.header("11. Delivery Risk")

r1, r2, r3 = st.columns(3)

with r1:

    schedule_risk = st.slider(
        "Schedule risk",
        1,
        5,
        3,
    )

with r2:

    dependency_risk = st.slider(
        "Dependency risk",
        1,
        5,
        3,
    )

with r3:

    resource_risk = st.slider(
        "Resource risk",
        1,
        5,
        3,
    )


delivery_risk = round(
    (
        (
            schedule_risk
            + dependency_risk
            + resource_risk
        )
        / 15
    )
    * 100
)


# ============================================================
# OVERALL SCORING
# ============================================================

score_items = [

    ("GxP Domain Assessment", domain_score, 1.4),

    ("Context of Use", context_score, 1.2),

    ("Data Governance", data_score, 1.4),

    ("Model & Validation", model_score, 1.3),

    ("Human Oversight", human_score, 1.2),

    (
        "Decision Accountability & Traceability",
        decision_traceability_score,
        1.3,
    ),

    ("CSV / CSA & Quality", validation_score, 1.4),

    ("Lifecycle Management", lifecycle_score, 1.2),

    ("Program Readiness", program_score, 1.0),
]


overall = round(
    sum(
        score * weight
        for _, score, weight in score_items
    )
    /
    sum(
        weight
        for _, _, weight in score_items
    )
)


if delivery_risk >= 80:

    overall = max(
        0,
        overall - 5,
    )


overall_status = score_status(overall)


decision = decision_for(
    overall,
    gxp_domain,
)


# Decision traceability is a gating control.
if decision_traceability_score < 60:

    decision = (
        "Do not treat the AI use case as ready for controlled pilot "
        "or production until decision accountability and traceability "
        "controls are defined and reviewed."
    )

elif (
    decision_traceability_score < 80
    and overall >= 70
):

    decision = (
        "Proceed to controlled pilot planning only after closing "
        "the decision-traceability gap and completing the appropriate "
        "qualified stakeholder review."
    )


# ============================================================
# RESULTS
# ============================================================

st.header("12. Readiness Results")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Overall Readiness",
        f"{overall}%",
    )

with m2:

    st.metric(
        "Status",
        STATUS[overall_status],
    )

with m3:

    st.metric(
        "Delivery Risk",
        f"{delivery_risk}%",
    )

with m4:

    st.metric(
        "GxP Domain",
        gxp_domain,
    )


# ============================================================
# RESULTS TABLE
# ============================================================

rows = []

for name, score, _weight in score_items:

    rows.append(
        {
            "Assessment Area": name,
            "Score": f"{score}%",
            "Status": STATUS[score_status(score)],
        }
    )


st.dataframe(
    rows,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# TOP AREAS
# ============================================================

st.subheader(
    "Top areas requiring attention"
)


sorted_sections = sorted(
    score_items,
    key=lambda x: x[1],
)


for name, score, _weight in sorted_sections[:4]:

    if score < 80:

        st.write(
            f"**{STATUS[score_status(score)]} "
            f"{name} — {score}%**"
        )

        st.write(
            gap_text(name)
        )


# ============================================================
# GOVERNANCE DECISION
# ============================================================

st.subheader(
    "Recommended governance decision"
)

st.info(
    decision
)


# ============================================================
# PM ACTIONS
# ============================================================

st.subheader(
    "Suggested immediate PM actions"
)


actions = []


for name, score, _ in sorted_sections:

    if score < 80:

        actions.append(
            f"Address {name.lower()} gaps before the next approval gate."
        )


if actions:

    for idx, action in enumerate(
        actions[:6],
        1,
    ):

        st.write(
            f"{idx}. {action}"
        )

else:

    st.write(
        "No material assessment gaps identified by the questionnaire; "
        "continue routine governance and qualified stakeholder review."
    )


# ============================================================
# SUMMARY
# ============================================================

st.divider()

st.subheader(
    "Assessment summary"
)


summary = f"""
# GxP AI Readiness & Governance Assessment

**AI Project / Use Case:** {project_name or "Not provided"}

**Business Objective:** {business_objective or "Not provided"}

**Primary AI Type:** {ai_type}

**Primary GxP Domain:** {gxp_domain}

**Assessment Date:** {date.today().isoformat()}

**Overall Readiness:** {overall}% — {overall_status}

**Delivery Risk:** {delivery_risk}%

## Assessment Areas

""" + "\n".join(
    [
        f"- **{name}:** {score}% — {score_status(score)}"
        for name, score, _
        in sorted_sections
    ]
) + f"""

## Recommended Governance Decision

{decision}

## Important Note

This tool is a project-governance and readiness aid. It is not legal,
regulatory, quality, validation, privacy, security, clinical, medical,
manufacturing, pharmacovigilance or compliance advice.

Final decisions should be made by appropriately qualified stakeholders.
"""


st.markdown(
    summary
)


# ============================================================
# PDF EXPORT
# ============================================================

try:

    from io import BytesIO

    from reportlab.lib.pagesizes import A4

    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
    )

    from reportlab.lib.styles import (
        getSampleStyleSheet,
        ParagraphStyle,
    )

    from reportlab.lib.enums import TA_CENTER

    REPORTLAB_AVAILABLE = True

except ImportError:

    REPORTLAB_AVAILABLE = False


def build_pdf(
    summary_text: str,
) -> bytes:

    if not REPORTLAB_AVAILABLE:

        raise RuntimeError(
            "PDF export requires reportlab."
        )


    buffer = BytesIO()


    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        leftMargin=42,

        rightMargin=42,

        topMargin=42,

        bottomMargin=42,

        title=(
            "GxP AI Readiness & Governance Assessment"
        ),

        author="Sriram Sampath",
    )


    styles = getSampleStyleSheet()


    styles.add(

        ParagraphStyle(

            name="GXPTitle",

            parent=styles["Title"],

            alignment=TA_CENTER,

            fontSize=17,

            leading=21,

            spaceAfter=14,
        )
    )


    styles.add(

        ParagraphStyle(

            name="GXPBody",

            parent=styles["BodyText"],

            fontSize=9.2,

            leading=12.5,

            spaceAfter=5,
        )
    )


    story = [

        Paragraph(

            "GxP AI Readiness & Governance Assessment",

            styles["GXPTitle"],
        ),

        Paragraph(

            "Project Readiness & Governance Summary",

            styles["Heading2"],
        ),

        Spacer(
            1,
            6,
        ),
    ]


    for raw_line in summary_text.splitlines():

        line = raw_line.strip()


        if not line:

            story.append(
                Spacer(
                    1,
                    3,
                )
            )

            continue


        if line.startswith("# "):

            continue


        if line.startswith("## "):

            story.append(

                Paragraph(

                    line[3:].replace(
                        "**",
                        "",
                    ),

                    styles["Heading2"],
                )
            )


        elif line.startswith(
            "### "
        ):

            story.append(

                Paragraph(

                    line[4:].replace(
                        "**",
                        "",
                    ),

                    styles["Heading3"],
                )
            )


        elif line.startswith("- "):

            story.append(

                Paragraph(

                    "• "
                    +
                    line[2:].replace(
                        "**",
                        "",
                    ),

                    styles["GXPBody"],
                )
            )


        else:

            safe = (

                line

                .replace(
                    "&",
                    "&amp;",
                )

                .replace(
                    "<",
                    "&lt;",
                )

                .replace(
                    ">",
                    "&gt;",
                )

                .replace(
                    "**",
                    "",
                )
            )


            story.append(

                Paragraph(
                    safe,
                    styles["GXPBody"],
                )
            )


    story.extend(

        [

            Spacer(
                1,
                10,
            ),

            Paragraph(

                "© 2026 Sriram Sampath. "
                "All rights reserved. "
                "Independent professional project.",

                styles["GXPBody"],
            ),

            Paragraph(

                f"LinkedIn: {LINKEDIN_URL}",

                styles["GXPBody"],
            ),

            Paragraph(

                "Related PM project: "
                f"{PREVIOUS_PROJECT_URL}",

                styles["GXPBody"],
            ),

            Paragraph(

                "Important: This assessment is a "
                "project-governance/readiness aid. "
                "It does not determine regulatory "
                "compliance and does not replace "
                "qualified stakeholder review.",

                styles["GXPBody"],
            ),
        ]
    )


    document.build(
        story
    )


    return buffer.getvalue()


if REPORTLAB_AVAILABLE:

    pdf_bytes = build_pdf(
        summary
    )


    st.download_button(

        "📄 Download Assessment Summary (PDF)",

        data=pdf_bytes,

        file_name=(
            "gxp_ai_readiness_assessment.pdf"
        ),

        mime="application/pdf",

        type="primary",
    )

else:

    st.error(
        "PDF export is unavailable because "
        "the reportlab package is not installed. "
        "Please add reportlab to requirements.txt "
        "and redeploy."
    )


# ============================================================
# PROFESSIONAL FOOTER
# ============================================================

st.divider()

st.markdown(

    f"""
    <div style="text-align:center; font-size:0.85rem;">

        <b>
            GxP AI Readiness & Governance Assessment
        </b>

        <br>

        © 2026 Sriram Sampath. All rights reserved.

        <br>

        <a href="{LINKEDIN_URL}" target="_blank">
            LinkedIn
        </a>

        &nbsp;|&nbsp;

        <a href="{PREVIOUS_PROJECT_URL}" target="_blank">
            Previous Project: Intelligent Risk & Issue Management Dashboard
        </a>

    </div>
    """,

    unsafe_allow_html=True,
)


# ============================================================
# VISITOR COUNT
# ============================================================

visit_count = get_visit_count()

st.divider()

if visit_count is not None:

    st.markdown(

        f"""
        <div style="text-align:center; font-size:0.85rem;">
            👁️ <b>Visits: {visit_count}</b>
        </div>
        """,

        unsafe_allow_html=True,
    )

else:

    st.markdown(

        """
        <div style="text-align:center; font-size:0.85rem;">
            👁️ <b>Visits: —</b>
        </div>
        """,

        unsafe_allow_html=True,
    )
