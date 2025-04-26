import streamlit as st  
from PIL import Image, ImageOps  
import io  
from rembg import remove  

st.set_page_config(page_title="Photo App", page_icon="🖼️")
st.title("Ashhad's Photo Tool 📸")  

uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])  

if 'processed_image' not in st.session_state:  
    st.session_state.processed_image = None  

if uploaded_image is not None:  
    img = Image.open(uploaded_image).convert("RGBA")  
    st.image(img, caption="Original Image", use_container_width=True)  

    # Apply background
    if st.button("Apply Blue Background"):  
        img_no_bg = remove(uploaded_image.getvalue())  
        img_no_bg = Image.open(io.BytesIO(img_no_bg)).convert("RGBA")  
        blue_bg = Image.new("RGBA", img_no_bg.size, (0, 102, 204, 255))  
        img_alpha = img_no_bg.split()[-1]  
        combined_image = Image.new("RGBA", img_no_bg.size)  
        combined_image.paste(blue_bg, (0, 0))  
        combined_image.paste(img_no_bg, (0, 0), img_alpha)  
        st.session_state.processed_image = combined_image  

# Image editing section
if st.session_state.processed_image is not None:  
    display_image = st.session_state.processed_image.copy()

    rotate_angle = st.slider("Rotate Image", 0, 360, 0)  
    if rotate_angle > 0:  
        display_image = display_image.rotate(rotate_angle, expand=True)  

    if st.button("Crop Image"):  
        display_image = ImageOps.fit(display_image, (300, 300))  

    # Update session state with latest image
    st.session_state.processed_image = display_image

    # Show final image just once
    st.image(display_image, caption="Processed Image", use_container_width=True)  

    # Download option
    if st.button("Download Image"):  
        buf = io.BytesIO()  
        display_image.save(buf, format="PNG")  
        byte_im = buf.getvalue()  
        st.download_button(label="Download Image", data=byte_im, file_name="final_image.png", mime="image/png")  

else:  
    st.write("Please upload an Image.")  

st.markdown("©️ Developed by [Muhammad Ashhad Khan](https://github.com/Rukhsanaashhad)")
