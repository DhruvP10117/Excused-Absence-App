import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Excused Absences", layout="centered")

st.title("Excused Absence App")
st.divider()

json_path = Path("requests.json")

if json_path.exists():
    with open(json_path, "r") as f:
        requests = json.load(f)
else:
    requests = []

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

with st.sidebar:
    st.header("Navigation")

    if st.button("Dashboard", key="nav_dashboard"):
        st.session_state["page"] = "dashboard"
        st.rerun()

    if st.button("Submit Request", key="nav_request"):
        st.session_state["page"] = "request"
        st.rerun()

if st.session_state["page"] == "dashboard":

    st.subheader("All Requests")

    if len(requests) == 0:
        st.warning("No requests found.")
    else:
        st.dataframe(requests)

        selected_request = st.selectbox(
            "Select a Request",
            options=requests,
            format_func=lambda x: x["student_email"],
            key="select_request"
        )

        with st.expander("Request Details", expanded=True):
            st.write("Status:", selected_request["status"])
            st.write("Course ID:", selected_request["course_id"])
            st.write("Email:", selected_request["student_email"])
            st.write("Date:", selected_request["absence_date"])
            st.write("Type:", selected_request["excuse_type"])
            st.write("Explanation:", selected_request["explanation"])

elif st.session_state["page"] == "request":

    st.subheader("Submit Excused Absence")

    email = st.text_input("Student Email", key="input_email")
    absence_date = st.date_input("Absence Date", key="input_date")
    excuse_type = st.selectbox(
        "Excuse Type",
        ["Medical", "University Competitions", "Other"],
        key="input_type"
    )
    explanation = st.text_area("Explanation", key="input_explanation")

    submit_btn = st.button("Submit Request", key="btn_submit")

    if submit_btn:
        if not email:
            st.warning("Email is required")
        else:
            date_str = absence_date.strftime("%Y-%m-%d")

            new_request = {
                "status": "Pending",
                "course_id": "011101",
                "student_email": email,
                "absence_date": date_str,
                "submitted_timestamp": str(datetime.now()),
                "excuse_type": excuse_type,
                "explanation": explanation,
                "instructor_note": ""
            }

            requests.append(new_request)

            with open(json_path, "w") as f:
                json.dump(requests, f, indent=4)

            st.success("Request Submitted!")

            st.rerun()