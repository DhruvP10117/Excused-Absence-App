import streamlit as st
import json
from pathlib import Path
import time
from datetime import datetime

st.set_page_config(page_title="Excused Absence App")

st.title("Excused Absence System")
st.divider()

json_path = Path("requests.json")

if json_path.exists():
    with json_path.open("r", encoding="utf-8") as f:
        requests = json.load(f)
else:
    requests = []

if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

with st.sidebar:
    st.header("Navigation")

    if st.button("Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

    if st.button("New Request"):
        st.session_state["page"] = "Request"
        st.rerun()

if st.session_state["page"] == "Dashboard":

    st.header("Excuse Absence Dashboard")

    if not requests:
        st.warning("No requests found.")
    else:
        event = st.dataframe(
            requests,
            on_select="rerun",
            selection_mode="single-row"
        )

        if event.selection.rows:
            index = event.selection.rows[0]
            selected_request = requests[index]

            with st.expander("Request Details", expanded=True):
                st.write(selected_request)

elif st.session_state["page"] == "Request":

    st.header("Submit Excused Absence Request")

    student_email = st.text_input("Student Email", key="email_input")

    absence_date = st.date_input("Absence Date", key="date_input")
    date_str = absence_date.strftime("%Y-%m-%d")

    excuse_type = st.selectbox(
        "Excuse Type",
        ["Medical", "University Competitions", "Other"],
        key="excuse_type"
    )

    explanation = st.text_area("Explanation", key="explanation")

    instructor_note = st.text_area("Instructor Note", key="note")

    submit_btn = st.button("Submit Request", key="submit_btn")

    if submit_btn:

        if not student_email:
            st.warning("Email required")
        else:
            with st.spinner("Submitting request..."):
                time.sleep(1)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                new_request = {
                    "status": "Pending",
                    "course_id": "011101",
                    "student_email": student_email,
                    "absence_date": date_str,
                    "submitted_timestamp": timestamp,
                    "excuse_type": excuse_type,
                    "explanation": explanation,
                    "instructor_note": instructor_note
                }

                requests.append(new_request)

                with json_path.open("w", encoding="utf-8") as f:
                    json.dump(requests, f, indent=4)

                st.success("Request Submitted!")

                st.session_state["page"] = "Dashboard"
                st.rerun()