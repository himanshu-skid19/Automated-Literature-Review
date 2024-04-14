from imports import *  # Assuming this imports Streamlit and any other necessary libraries
from read_docs import *  # Assuming this includes the download_pdf function
from build_vector_store import *  # Assuming this includes the build_vector_store function
from query import *  # Assuming this includes the query function

st.set_page_config(page_title="MultiModal Chatbot")

# with st.sidebar:
#     openai_api = st.text_input('Enter OpenAI API token:', type='password')
#     os.environ['OPENAI_API_KEY'] = openai_api
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
        index = build_vector_store(text)
        # Store the index in session state for querying later
        st.session_state['vector_store_index'] = index
        # Clear the link input field after processing
        st.session_state.link_input = ""

# Function to store and display chat messages

# Function to store and display links
def display_links(links_list):
    for link in links_list:
        st.markdown(f"[{link}]({link})", unsafe_allow_html=True)

# Initialize session states if they don't exist

if 'links_list' not in st.session_state:
    st.session_state['links_list'] = []
if 'link_input' not in st.session_state:
    st.session_state['link_input'] = ''

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def openai_response(prompt):
    if st.session_state['vector_store_index'] is not None:
        # Assuming 'query' is your query function
        # and it needs the query text and the vector store index
        llm = OpenAIMultiModal(
            model="gpt-4-vision-preview", api_key=OPENAI_API_KEY, max_new_tokens=300
        )
        result = query(prompt, st.session_state['vector_store_index'], llm)
        
    else:
        result = "Vector store is not initialized."
    return result

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = openai_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

# Side pane for links
with st.sidebar:
    st.title('MultiModal Chatbot')
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
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)