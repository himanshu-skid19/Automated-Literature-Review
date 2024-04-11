from imports import *  # Assuming this imports Streamlit and any other necessary libraries
from read_docs import *  # Assuming this includes the download_pdf function
from build_vector_store import *  # Assuming this includes the build_vector_store function
from query import *  # Assuming this includes the query function

def add_link():
    link = st.session_state.link_input
    if link:  # Check if the input field is not empty
        # Append the link to the list
        st.session_state.links_list.append(link)
        # Download the PDF content after adding the link
        download_pdf(link, "pdf_content.pdf")
        # Extract text and images from the PDF
        text = extract_text_from_pdf("pdf_content.pdf")
        images = extract_images_from_pdf("pdf_content.pdf")
        # Build the vector store with the extracted content
        index = build_vector_store()
        # Store the index in session state for querying later
        st.session_state['vector_store_index'] = index
        # Clear the link input field after processing
        st.session_state.link_input = ""

# Function to store and display chat messages
def display_chat(chat_history):
    for message in chat_history:
        # Use st.write or st.text_area to display the whole message instead of st.text
        st.write(message)  # This will display each entry in chat_history as a block of text

# Function to store and display links
def display_links(links_list):
    for link in links_list:
        st.markdown(f"[{link}]({link})", unsafe_allow_html=True)

# Initialize session states if they don't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'links_list' not in st.session_state:
    st.session_state['links_list'] = []
if 'link_input' not in st.session_state:
    st.session_state['link_input'] = ''
if 'query_result' not in st.session_state:
    st.session_state['query_result'] = ""  # Initialize the query result as an empty string


# Main chat interface
st.title("Chat Interface")
if 'query_results' not in st.session_state:
    st.session_state['query_results'] = []

# Main chat interface
st.title("Chat Interface")

with st.form(key='query_form'):
    # Text input for user query inside the form
    user_input = st.text_input("Type your query here...", key="chat_input")
    # Button to submit the query, now acts as a submit button for the form
    query_button = st.form_submit_button("Submit Query")

if query_button and user_input:
    # Perform the query if a vector store index exists
    if st.session_state['vector_store_index'] is not None:
        # Assuming 'query' is your query function
        # and it needs the query text and the vector store index
        llm = OpenAIMultiModal(
            model="gpt-4-vision-preview", api_key=OPENAI_API_KEY, max_new_tokens=300
        )
        result = query(user_input, st.session_state['vector_store_index'], llm)
        # Update query result
        st.session_state['query_result'] = result
    else:
        st.session_state['query_result'] = "Vector store is not initialized."

# Display query result
st.write("Query Result:")
st.write(st.session_state['query_result'])

# Side pane for links
with st.sidebar:
    st.title("Links")
    # Text input for link
    link_input = st.text_input(
        "Add a link here...", 
        value=st.session_state.link_input, 
        key="link_input", 
        on_change=add_link
    )
    # Display links
    display_links(st.session_state.links_list)