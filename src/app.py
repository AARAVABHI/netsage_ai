import streamlit as st

from src.engine import load_cases, run_diagnosis


@st.cache_data
def get_cases():
    return load_cases()


def main():
    st.set_page_config(page_title='NetSage AI', page_icon='🛰️', layout='wide')

    cases = get_cases()
    st.title('NetSage AI: Automated Network Diagnostic Platform')

    case_id = st.selectbox('Select Network Case', cases['case_id'].tolist())
    selected = cases[cases['case_id'] == case_id].iloc[0].to_dict()

    st.subheader('Case Details')
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Symptom: {selected['symptom']}")
        st.write(f"Topology Note: {selected['topology_note']}")
    with col2:
        st.write(f"Concept Tag: {selected['concept_tag']}")
        st.write(f"Severity: {selected['severity']}")

    st.text_area('Captured Show Outputs', selected['show_outputs'], height=200)

    result = run_diagnosis(selected)

    st.subheader('Diagnosis')
    st.json(result)

    st.subheader('Human Approval Gate')
    approve = st.button('Approve & Deploy Fix')
    edit = st.button('Edit Commands')
    reject = st.button('Reject')

    if approve:
        st.success('Fix approved and logged for deployment review.')
    if edit:
        st.warning('Operator override enabled; commands can be manually adjusted before deployment.')
    if reject:
        st.error('Diagnosis rejected and recorded as false positive for audit review.')

    with st.expander('Audit Log Preview'):
        st.write({
            'case_id': selected['case_id'],
            'decision': 'pending',
            'status': 'human review required'
        })


if __name__ == '__main__':
    main()
