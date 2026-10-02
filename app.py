import streamlit as st
from dotenv import load_dotenv

from ai_engine import analyze_information
from document_processor import (
    extract_text_from_pdf,
    extract_text_from_image
)


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="NOVA — AI Bridge",
    page_icon="🧭",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🧭 NOVA")

st.subheader(
    "AI Bridge for Everyday Independence"
)

st.write(
    "NOVA transforms difficult information into "
    "clear actions that are easy to understand."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🧭 NOVA")

    st.markdown(
        """
        ### Understand → Decide → Act

        **1. Understand**  
        NOVA reads the information.

        **2. Decide**  
        NOVA identifies important details.

        **3. Act**  
        NOVA creates a simple action checklist.
        """
    )

    st.divider()

    language = st.selectbox(
        "Output language",
        ["English", "Tamil"]
    )

    st.divider()

    st.caption(
        "NOVA is an AI assistance tool. "
        "Always verify important information "
        "with the original source."
    )


# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "source_text" not in st.session_state:
    st.session_state.source_text = ""


# =========================================================
# INPUT SECTION
# =========================================================

st.header("📥 Give NOVA some information")

tab1, tab2 = st.tabs(
    [
        "📄 Upload document",
        "✍️ Paste text"
    ]
)


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload a PDF or image",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg"
        ],
        help="Upload a notice, instruction sheet, form, or other document."
    )

    if uploaded_file is not None:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "🔍 Analyze document",
            type="primary"
        ):

            try:

                if uploaded_file.type == "application/pdf":

                    text = extract_text_from_pdf(
                        uploaded_file
                    )

                else:

                    text = extract_text_from_image(
                        uploaded_file
                    )

                if not text.strip():

                    st.error(
                        "No readable text was found in the document."
                    )

                else:

                    with st.spinner(
                        "NOVA is understanding the document..."
                    ):

                        result = analyze_information(
                            text,
                            language
                        )

                    st.session_state.source_text = text
                    st.session_state.result = result

                    st.rerun()

            except Exception as e:

                st.error(
                    f"Document processing error: {e}"
                )


# =========================================================
# PASTE TEXT
# =========================================================

with tab2:

    pasted_text = st.text_area(
        "Paste your notice, instruction, announcement, or other information here:",
        value="",
        height=300,
        placeholder=(
            "Paste the information you want NOVA to understand..."
        )
    )

    if st.button(
        "🤖 Analyze pasted information",
        type="primary"
    ):

        if not pasted_text.strip():

            st.warning(
                "Please paste some text first."
            )

        else:

            with st.spinner(
                "NOVA is understanding the information..."
            ):

                result = analyze_information(
                    pasted_text,
                    language
                )

            st.session_state.source_text = pasted_text
            st.session_state.result = result

            st.rerun()


# =========================================================
# RESULTS
# =========================================================

result = st.session_state.result


if result:

    st.divider()

    st.header("🧠 NOVA Analysis")


    # =====================================================
    # AI STATUS
    # =====================================================

    if result.get("demo_mode"):

        st.warning(
            "Demo mode is active. "
            "Please configure your Gemini API key."
        )

    elif result.get("model_used"):

        st.success(
            f"Live Gemini AI analysis is active using "
            f"`{result['model_used']}`."
        )


    # =====================================================
    # KEY INFORMATION
    # =====================================================

    priority = result.get(
        "priority",
        "Not found"
    )

    category = result.get(
        "category",
        "Not found"
    )

    deadline = result.get(
        "deadline",
        "Not found"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown("### Priority")

        st.info(
            priority
        )


    with col2:

        st.markdown("### Category")

        st.info(
            category
        )


    with col3:

        st.markdown("### Deadline")

        st.info(
            deadline
        )


    # =====================================================
    # SUMMARY
    # =====================================================

    st.subheader("📝 Summary")

    st.write(
        result.get(
            "summary",
            "No summary available."
        )
    )


    # =====================================================
    # ACTION CHECKLIST
    # =====================================================

    st.subheader("✅ Action checklist")

    actions = result.get(
        "actions",
        []
    )

    if actions:

        for index, action in enumerate(actions):

            st.checkbox(
                action,
                key=f"action_{index}"
            )

    else:

        st.info(
            "No specific actions found."
        )


    # =====================================================
    # IMPORTANT INFORMATION
    # =====================================================

    st.subheader("📌 Important information")

    important_points = result.get(
        "important_points",
        []
    )

    if important_points:

        for point in important_points:

            st.markdown(
                f"- {point}"
            )

    else:

        st.info(
            "No additional important information found."
        )


    # =====================================================
    # WARNINGS
    # =====================================================

    st.subheader("⚠️ Things to watch")

    warnings = result.get(
        "warnings",
        []
    )

    if warnings:

        for warning in warnings:

            if warning != "Not found":

                st.warning(
                    warning
                )

    else:

        st.info(
            "No warnings found."
        )


    # =====================================================
    # SIMPLE EXPLANATION
    # =====================================================

    st.subheader("💡 Simple explanation")

    st.info(
        result.get(
            "simple_explanation",
            "No simple explanation available."
        )
    )


    # =====================================================
    # SOURCE TEXT
    # =====================================================

    with st.expander(
        "🔎 View extracted source text"
    ):

        st.text(
            st.session_state.source_text
        )


else:

    st.info(
        "Upload a document or paste information above "
        "to start using NOVA."
    )