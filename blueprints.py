import streamlit as st
from openai import OpenAI
from io import BytesIO
from PIL import Image
import base64

st.set_page_config(page_title="Blueprint take-off AI", page_icon="👁️")

st.title("CAD Blueprint take-off AI")

api_key = st.text_input("OpenAI API Key", type="password")
img_input = st.file_uploader(
    "Upload drawing images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if st.button("Send"):
    if not api_key:
        st.warning("API Key required")
        st.stop()

    if not img_input:
        st.warning("Please upload at least one image")
        st.stop()

    client = OpenAI(api_key=api_key)

    content = [
        {
            "type": "input_text",
            "text": (
                "Review these engineering drawing images and count all electrical sockets, "
                "switches, and other clearly identifiable electrical points shown. "
                "Return the result ONLY as a markdown table with columns: "
                "Item | Count | Notes."
            )
        }
    ]

    for img in img_input:
        encoded_img = base64.b64encode(img.read()).decode("utf-8")
        content.append(
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{encoded_img}",
                "detail": "high"
            }
        )

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": content
            }
        ]
    )

    response_text = response.output_text

    with st.chat_message("user"):
        st.write("Please review these uploaded drawings.")
        for img in img_input:
            img.seek(0)
            preview = Image.open(BytesIO(img.read()))
            st.image(preview, caption=img.name)

    with st.chat_message("assistant"):
        st.markdown(response_text)