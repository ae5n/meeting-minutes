import streamlit as st
import modal

def main():
    st.title("Meeting Minutes Generator")

    # Upload the .vtt file for the transcript
    uploaded_file = st.file_uploader("Choose a .vtt file for the transcript", type="vtt")
    if uploaded_file:
        transcript = uploaded_file.read().decode()
    else:
        transcript = ""

    # Optional field for the meeting agenda
    meeting_agenda = st.text_area("Meeting Agenda (optional)")

    if st.button("Generate Meeting Minutes"):
        if not transcript:
            st.error("Please upload a .vtt file for the transcript before generating the minutes.")
            return

        if meeting_agenda:
            instructPrompt = f"""
            Given the provided meeting agenda and transcript, generate concise and organized meeting minutes that capture key points, decisions, and action items. Ensure the minutes:

            - Are structured based on the meeting agenda.
            - Exclude attendees' names.
            - Integrate highlights, decisions, or action items directly under the relevant agenda points.
            - Do not have a separate section for Action Items.
            - Consider any schedule or time associated with each action item or decision.
            - Assign the person responsible for each action or decision, if mentioned in the transcript.
            - Exclude the date and time mentioned at the beginning of the transcript.

            Agenda:
            {meeting_agenda}

            ---

            Note: The minutes should be clear, concise, and organized.
            """
        else:
            instructPrompt = f"""
            Given the provided meeting transcript, generate concise and organized meeting minutes that capture key points, decisions, and action items. Ensure the minutes:

            - Exclude attendees' names.
            - Do not have a separate section for Action Items.
            - Consider any schedule or time associated with each action item or decision.
            - Assign the person responsible for each action or decision, if mentioned in the transcript.
            - Exclude the date and time mentioned at the beginning of the transcript.

            ---

            Note: The minutes should be clear, concise, and organized.
            """

        # if meeting_agenda:
        #     instructPrompt = f"""
        #     Given the provided meeting agenda and transcript, generate concise and organized meeting minutes that capture key points, decisions, and action items:

        #     Agenda:
        #     {meeting_agenda}

        #     ---

        #     Note: Ensure the minutes are structured based on the meeting agenda and highlight any important decisions or action items.
        #     """
        # else:
        #     instructPrompt = f"""
        #     Given the provided meeting transcript, generate concise and organized meeting minutes that capture key points, decisions, and action items:

        #     ---

        #     Note: Highlight any important decisions or action items.
        #     """

        # Construct the request
        request = instructPrompt + "\n\nTranscript:\n" + transcript

        # Call the Modal function to generate the minutes
        f = modal.Function.lookup("minutes-project", "generate_minutes")
        minutes = f.call(request)
        st.subheader("Generated Meeting Minutes:")
        st.write(minutes)

if __name__ == '__main__':
    main()
