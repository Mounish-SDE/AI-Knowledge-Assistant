
import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

# Load API key
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize Gemini
api_key = os.getenv("GOOGLE_API_KEY")

# Sidebar
with st.sidebar:
    st.title("📚 AI Knowledge Assistant")
    st.write("Upload documents and ask questions.")
    st.markdown("---")
    st.markdown("### Features")
    st.write("📄 PDF document upload")
    st.write("🔍 Document text extraction")
    st.write("🤖 Gemini AI answers")
    st.write("📖 Document-based questions")

# Main interface
st.title("📚 AI Knowledge Assistant")

st.markdown(
    "Upload your PDF documents and ask questions "
    "about their contents."
)

if not api_key:
    st.error("Gemini API key not found. Please configure .env.")
    st.stop()

client = genai.Client(api_key=api_key)

# Upload documents
uploaded_files = st.file_uploader(
    "Upload your PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

document_text = ""

if uploaded_files:

    for uploaded_file in uploaded_files:

        try:
            reader = PdfReader(uploaded_file)

            for page_number, page in enumerate(
                reader.pages, start=1
            ):

                text = page.extract_text() or ""

                if text.strip():

                    document_text += (
                        f"\n\nDocument: {uploaded_file.name}\n"
                        f"Page: {page_number}\n"
                        f"{text}"
                    )

        except Exception as error:
            st.error(
                f"Unable to read {uploaded_file.name}: {error}"
            )

    if document_text.strip():

        st.success(
            f"{len(uploaded_files)} PDF(s) uploaded successfully!"
        )

        st.info(
            f"Extracted {len(document_text):,} characters."
        )

        # Question input
        question = st.text_area(
            "Ask a question about your documents",
            placeholder="Example: Summarize this document...",
            height=100
        )

        if st.button("🤖 Generate Answer", type="primary"):

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                prompt = f"""
You are an AI Knowledge Assistant.

Answer the user's question using ONLY the
information provided in the documents.

Instructions:
1. Give a clear and accurate answer.
2. Do not invent information.
3. If the answer is unavailable, say so.
4. Mention document names and page numbers
   when relevant.
5. Use headings and bullet points when helpful.

DOCUMENT CONTENT:

{document_text[:100000]}

USER QUESTION:

{question}
"""

                with st.spinner("Gemini is analyzing documents..."):

                    try:

                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )

                        st.markdown("---")
                        st.subheader("🤖 AI Answer")

                        st.markdown(response.text)

                    except Exception as error:

                        st.error(
                            "Unable to generate answer. "
                            "Check your API key, model availability "
                            "and internet connection."
                        )

                        st.caption(str(error))

    else:

        st.warning(
            "No readable text found in the uploaded PDFs."
        )

else:

    st.info(
        "👆 Upload a PDF document to get started."
    )

    st.markdown("""
    ### What you can do

    - Upload PDF documents
    - Extract document text
    - Ask questions about your documents
    - Generate AI-powered answers
    """)
