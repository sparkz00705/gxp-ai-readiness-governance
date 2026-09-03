
import streamlit as st
from datetime import date

USER_MANUAL_URL = "https://raw.githubusercontent.com/sparkz00705/gxp-ai-readiness-governance/main/GxP_AI_Readiness_Governance_User_Manual.pdf"

st.set_page_config(
    page_title="GxP AI Readiness & Governance Assessment",
    page_icon="🧪",
    layout="wide",
)

ANSWER_SCORE = {"Yes": 100, "Partly": 70, "No": 30}
STATUS = {
    "Green": "🟢 Green",
    "Amber": "🟠 Amber",
    "Red": "🔴 Red",
}

DOMAIN_DESCRIPTIONS = {
    "GMP": "Good Manufacturing Practice — manufacturing, process, product quality, batch/release, deviations, CAPA, change control.",
    "GLP": "Good Laboratory Practice — non-clinical safety studies, study conduct, raw data, QA oversight, reporting and archiving.",
    "GCP": "Good Clinical Practice — clinical trials, participant safety, protocol conduct, clinical data, oversight and essential records.",
    "GDP": "Good Distribution Practice — storage, distribution, transport, traceability and product integrity.",
    "PV / GVP": "Pharmacovigilance / Good Pharmacovigilance Practices — safety information, case processing, signal detection, reporting and oversight.",
    "GDocP / Data Integrity": "Good Documentation Practices / data integrity — complete, consistent, accurate, attributable and controlled records.",
    "CSV / CSA": "Computerized Systems / Computer System Validation / Computer Software Assurance — fit-for-purpose assurance, evidence, controls and lifecycle.",
    "Multiple / Cross-functional GxP": "Use when the AI solution spans more than one regulated GxP area.",
    "Not yet determined": "Use when the regulated context is still being assessed; route to appropriate quality/regulatory stakeholders.",
}

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
        "Appropriate QA / regulatory stakeholders are engaged",
        "The proposed context of use is documented",
        "A path to determine GxP applicability is defined",
    ],
}

def score_answers(prefix, questions):
    values = []
    for idx, question in enumerate(questions, 1):
        ans = st.radio(
            question,
            ["Yes", "Partly", "No"],
            key=f"{prefix}_{idx}",
            horizontal=True,
        )
        values.append(ANSWER_SCORE[ans])
    return round(sum(values) / len(values))

def score_status(score):
    return "Green" if score >= 80 else "Amber" if score >= 60 else "Red"

def decision_for(score, gxp_level):
    if score >= 80 and gxp_level in ["Low / none", "Moderate"]:
        return "Proceed to the next delivery stage with routine governance and documented QA / validation oversight."
    if score >= 70:
        return "Proceed to controlled pilot planning only after the highest-priority readiness gaps are addressed."
    if score >= 55:
        return "Establish and track a formal gap-closure plan before pilot or validation activities."
    return "Do not proceed to pilot / production yet. Establish the required governance, quality, data and delivery controls first."

def gap_text(section):
    return {
        "Context of Use": "Clarify intended use, accountability, boundaries and human oversight.",
        "GxP Domain Assessment": "Confirm applicable GxP scope with qualified Quality / Regulatory stakeholders.",
        "Data Governance": "Close data-source, lineage, quality and integrity gaps.",
        "Model & Validation": "Define performance criteria, validation / assurance ownership, explainability and change controls.",
        "Human Oversight": "Define accountable human review, escalation and override controls.",
        "CSV / CSA & Quality": "Agree the risk-based assurance / validation strategy and evidence expectations.",
        "Lifecycle Management": "Define monitoring, change triggers, periodic review and retirement / rollback.",
        "Program Readiness": "Confirm governance, roles, resources, dependencies and adoption readiness.",
    }.get(section, "Address the identified readiness gaps.")


# ---------- V3 Sample Assessment ----------
def show_sample_assessment():
    st.success("Sample loaded: GMP — AI-assisted Deviation Triage")
    st.markdown(
        """
**Business objective:** Use AI to prioritize quality deviations for review while keeping final disposition with a qualified human reviewer.

**AI type:** Classification  
**Regulated decision impact:** Supports a regulated decision  
**Primary GxP domain:** GMP

### Illustrative sample result

| Assessment area | Score | Status |
|---|---:|---|
| GxP domain assessment | 75% | 🟠 Amber |
| Context of Use | 68% | 🟠 Amber |
| Data Governance | 64% | 🟠 Amber |
| Model & Validation | 58% | 🔴 Red |
| Human Oversight | 78% | 🟠 Amber |
| CSV / CSA & Quality | 63% | 🟠 Amber |
| Lifecycle Management | 55% | 🔴 Red |
| Program Readiness | 82% | 🟢 Green |

**Overall readiness: 66% — AMBER**

**Top gaps**
1. Model validation / assurance approach is not fully defined.
2. Model and data change triggers are not established.
3. Data lineage and data-quality controls require further evidence.
4. Human escalation and override expectations need clearer documentation.

**Recommended governance action**

> Proceed to controlled pilot planning only after the highest-priority data, validation, lifecycle and human-oversight gaps are addressed.

This sample is illustrative and does not represent a regulatory or compliance conclusion.
"""
    )

st.title("🧪 GxP AI Readiness & Governance Assessment")
st.caption(
    "A Life Sciences project-governance decision-support tool for assessing AI initiatives "
    "across GxP context, data, validation, human oversight, lifecycle and delivery readiness."
)

with st.expander("Important: what this tool does (and does not do)", expanded=False):
    st.write(
        "This is an initial project-readiness assessment. It does not determine legal or regulatory "
        "compliance and does not replace QA, Validation, Regulatory, Privacy, Security, Data, Medical, "
        "Pharmacovigilance, Clinical, Manufacturing or other qualified review."
    )


# ---------- V3 landing area ----------
nav_a, nav_b, nav_c = st.columns([2, 1, 1])
with nav_a:
    st.markdown("### Start here")
    st.caption("Run your own assessment or load a sample to see how the tool works.")
with nav_b:
    if st.button("🎯 Load Sample Assessment", use_container_width=True):
        st.session_state["show_sample"] = True
with nav_c:
    st.markdown("**📖 User Manual**")
    st.markdown(f"[Open User Manual]({USER_MANUAL_URL})")

if st.session_state.get("show_sample"):
    show_sample_assessment()

with st.expander("Assessment Methodology", expanded=False):
    st.markdown(
        """
**What is assessed:** GxP domain context, Context of Use, Data Governance & Data Integrity,
AI Model & Validation/Assurance, Human Oversight, CSV/CSA & Quality, Lifecycle Management,
Program Readiness and Delivery Risk.

**Response scoring:** Yes = 100, Partly = 70, No = 30.

**Status:** 🟢 Green = 80–100%, 🟠 Amber = 60–79%, 🔴 Red = below 60%.

The result is an initial project-readiness indicator. It does **not** declare GMP, GLP, GCP,
GDP, GVP or other regulatory compliance and does not replace qualified stakeholder review.
"""
    )

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
        ["Prediction", "Classification", "Recommendation", "Detection", "Document / text analysis", "Generative AI", "Other"],
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

st.header("2. Select Applicable GxP / Regulated Domain")
gxp_domain = st.selectbox(
    "Primary GxP domain",
    list(DOMAIN_DESCRIPTIONS.keys()),
)
st.info(DOMAIN_DESCRIPTIONS[gxp_domain])

if gxp_domain == "Multiple / Cross-functional GxP":
    st.multiselect(
        "Additional GxP areas in scope",
        ["GMP", "GLP", "GCP", "GDP", "PV / GVP", "GDocP / Data Integrity", "CSV / CSA"],
        default=["GMP", "GDocP / Data Integrity", "CSV / CSA"],
    )

st.subheader("GxP-specific readiness")
domain_score = score_answers("domain", DOMAIN_QUESTIONS[gxp_domain])

st.header("3. Context of Use & Governance")
context_score = score_answers("context", [
    "Intended use is clearly documented",
    "Accountability for the final decision is defined",
    "Out-of-scope / prohibited uses are documented",
    "Human review and override expectations are defined",
])

st.header("4. Data Governance & Data Integrity")
data_score = score_answers("data", [
    "Data sources are identified and owned",
    "Data lineage is documented",
    "Data quality has been assessed",
    "Data integrity risks are understood",
    "Training / validation / production data controls are defined",
])

st.header("5. AI Model & Validation / Assurance Readiness")
model_score = score_answers("model", [
    "Model purpose and acceptance criteria are defined",
    "Performance measures are defined",
    "Validation / assurance approach and ownership are defined",
    "Explainability / transparency expectations are defined",
    "Model versioning and change controls are defined",
])

st.header("6. Human Oversight & Decision Governance")
human_score = score_answers("human", [
    "Named human reviewer / accountable owner exists",
    "Human override is possible where required",
    "Escalation criteria are defined",
    "AI limitations / uncertainty are communicated",
])

st.header("7. CSV / CSA & Quality Controls")
validation_score = score_answers("validation", [
    "Validation / assurance strategy is agreed",
    "Requirements and intended use are traceable",
    "Testing and evidence expectations are defined",
    "Change control and release approval are defined",
])

st.header("8. Lifecycle Management")
lifecycle_score = score_answers("lifecycle", [
    "Production monitoring is defined",
    "Model / data change triggers are defined",
    "Periodic performance review is planned",
    "Retirement / rollback approach is defined",
])

st.header("9. Program & Organizational Readiness")
program_score = score_answers("program", [
    "Business owner and sponsor are identified",
    "QA / Validation / IT / Data / domain roles are identified",
    "Resources and budget are understood",
    "Key dependencies and milestones are documented",
    "Change, training and adoption needs are understood",
])

st.header("10. Delivery Risk")
r1, r2, r3 = st.columns(3)
with r1:
    schedule_risk = st.slider("Schedule risk", 1, 5, 3)
with r2:
    dependency_risk = st.slider("Dependency risk", 1, 5, 3)
with r3:
    resource_risk = st.slider("Resource risk", 1, 5, 3)
delivery_risk = round(((schedule_risk + dependency_risk + resource_risk) / 15) * 100)

# Weighted score. GxP domain, validation, and data are intentionally weighted more heavily.
score_items = [
    ("GxP Domain Assessment", domain_score, 1.4),
    ("Context of Use", context_score, 1.2),
    ("Data Governance", data_score, 1.4),
    ("Model & Validation", model_score, 1.3),
    ("Human Oversight", human_score, 1.2),
    ("CSV / CSA & Quality", validation_score, 1.4),
    ("Lifecycle Management", lifecycle_score, 1.2),
    ("Program Readiness", program_score, 1.0),
]
overall = round(sum(s*w for _, s, w in score_items) / sum(w for _, _, w in score_items))
if delivery_risk >= 80:
    overall = max(0, overall - 5)

overall_status = score_status(overall)
decision = decision_for(overall, {
    "Low / none":"Low / none",
    "Moderate":"Moderate",
    "High":"High",
    "Critical":"Critical",
    "High":"High",
    "Critical":"Critical",
}.get(
    "Moderate" if gxp_domain == "Not yet determined" else "High" if gxp_domain in ["GMP","GCP","GLP","PV / GVP","Multiple / Cross-functional GxP"] else "Moderate"
))

st.header("11. Readiness Results")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Overall Readiness", f"{overall}%")
m2.metric("Status", f"{STATUS[overall_status]}")
m3.metric("Delivery Risk", f"{delivery_risk}%")
m4.metric("GxP Domain", gxp_domain)

rows = []
for name, score, _weight in score_items:
    rows.append({
        "Assessment Area": name,
        "Score": f"{score}%",
        "Status": STATUS[score_status(score)],
    })
st.dataframe(rows, use_container_width=True, hide_index=True)

st.subheader("Top areas requiring attention")
for name, score, _weight in sorted(score_items, key=lambda x: x[1])[:4]:
    if score < 80:
        st.write(f"**{STATUS[score_status(score)]} {name} — {score}%**")
        st.write(gap_text(name))

st.subheader("Recommended governance decision")
st.info(decision)

st.subheader("Suggested immediate PM actions")
actions = []
for name, score, _ in sorted(score_items, key=lambda x: x[1]):
    if score < 80:
        actions.append(f"Address {name.lower()} gaps before the next approval gate.")
for idx, action in enumerate(actions[:6], 1):
    st.write(f"{idx}. {action}")
if not actions:
    st.write("No material assessment gaps identified by the questionnaire; continue routine governance and qualified stakeholder review.")

st.divider()
st.subheader("Assessment summary")
summary = f"""
**AI Project / Use Case:** {project_name or "Not provided"}  
**Business Objective:** {business_objective or "Not provided"}  
**Primary AI Type:** {ai_type}  
**Primary GxP Domain:** {gxp_domain}  
**Assessment Date:** {date.today().isoformat()}

**Overall Readiness:** {overall}% — {overall_status}

**Recommended Governance Decision:**  
{decision}

**Top Assessment Areas:**  
""" + "\n".join([f"- {n}: {s}% — {score_status(s)}" for n,s,_ in sorted(score_items, key=lambda x:x[1])]) + f"""

**Important note:** This tool is a project-governance and readiness aid. It is not legal, regulatory,
quality, validation, privacy, security, clinical, medical, manufacturing, pharmacovigilance or compliance advice.
Final decisions should be made by appropriately qualified stakeholders.
"""
st.markdown(summary)

st.download_button(
    "Download assessment summary",
    data=summary,
    file_name="gxp_ai_readiness_assessment.md",
    mime="text/markdown",
)

st.caption("V2 prototype — keep this app in a separate repository/deployment from your existing live PM Risk & Issue Dashboard.")
st.divider()

st.markdown(
    """
    <div style="text-align:center; font-size:0.85rem;">
        © 2026 Sriram Sampath | GxP AI Readiness & Governance Assessment<br>
        Independent professional project |
        <a href="https://www.linkedin.com/in/sriramsampath81/" target="_blank">
            Connect with me on LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
