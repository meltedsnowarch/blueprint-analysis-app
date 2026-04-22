import streamlit as st
from openai import OpenAI
from io import BytesIO
from PIL import Image
import base64

st.set_page_config(page_title='Blueprint take-off AI', page_icon='👁️')

st.markdown('# CAD Blueprint take-off AI')

api_key = st.text_input('OpenAI API Key', '', type='password')

# Upload images (PDF later)
img_input = st.file_uploader('Images', accept_multiple_files=True)

if st.button('Send'):

    if not api_key:
        st.warning('API Key required')
        st.stop()

    if not img_input:
        st.warning('Upload at least one image')
        st.stop()

    msg = {
        'role': 'user',
        'content': []
    }

    # ✅ CLEAR instruction (your actual goal)
    msg['content'].append({
        'type': 'text',
        'text': 'Count all electrical sockets and switches shown on this drawing. Use the legend if present. Return ONLY a markdown table with columns: Item | Count.'
    })

    for img in img_input:
        if img.name.split('.')[-1].lower() not in ['png', 'jpg', 'jpeg', 'webp']:
            st.warning('Only .jpg, .png, .webp supported')
            st.stop()

        encoded_img = base64.b64encode(img.read()).decode('utf-8')

        msg['content'].append({
            'type': 'input_image',
            'image_url': f"data:image/jpeg;base64,{encoded_img}"
        })

    # ✅ NEW API (this fixes your earlier error)
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4o",
        input=[msg]
    )

    response_msg = response.output_text

    # Display input
    with st.chat_message('user'):
        for i in msg['content']:
            if i['type'] == 'text':
                st.write(i['text'])
            else:
                with st.expander('Attached Image'):
                    img = Image.open(BytesIO(base64.b64decode(i['image_url'].split(",")[1])))
                    st.image(img)

    # Display output
    if response_msg:
        with st.chat_message('assistant'):
            st.markdown(response_msg)