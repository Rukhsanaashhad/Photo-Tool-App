import streamlit as st  
from PIL import Image, ImageOps, ImageDraw  
import io  
from rembg import remove  

st.title("Ashhad's Photo Tool")  

uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])  

if 'img_to_display' not in st.session_state:  
    st.session_state.img_to_display = None  
 
if uploaded_image is not None:  
    img = Image.open(uploaded_image).convert("RGBA")  
    st.image(img, caption="Original Image", use_container_width=True)  

    if st.button("Apply Blue Background"):  
        # Remove background
        img_no_bg = remove(uploaded_image.getvalue())  
        img_no_bg = Image.open(io.BytesIO(img_no_bg)).convert("RGBA")  

        # Create solid blue background
        blue_bg = Image.new("RGBA", img_no_bg.size, (0, 102, 204, 255))  

        img_alpha = img_no_bg.split()[-1]  

        # Combine subject with blue background
        combined_image = Image.new("RGBA", img_no_bg.size)  
        combined_image.paste(blue_bg, (0, 0))  
        combined_image.paste(img_no_bg, (0, 0), img_alpha)  

        st.session_state.img_to_display = combined_image  
        st.image(combined_image, caption="Image with Blue Background", use_container_width=True)  

    if st.session_state.img_to_display is not None:  
        rotate_angle = st.slider("Rotate Image", 0, 360, 0)  
        if rotate_angle > 0:  
            rotated_image = st.session_state.img_to_display.rotate(rotate_angle, expand=True)  
            st.session_state.img_to_display = rotated_image  
            st.image(rotated_image, caption=f"Image rotated by {rotate_angle} degrees", use_container_width=True)  

        if st.button("Crop Image"):  
            cropped_img = ImageOps.fit(st.session_state.img_to_display, (300, 300))  
            st.session_state.img_to_display = cropped_img  
            st.image(cropped_img, caption="Cropped Image", use_container_width=True)  

        if st.button("Download Image"):  
            buf = io.BytesIO()  
            st.session_state.img_to_display.save(buf, format="PNG")  
            byte_im = buf.getvalue()  
            st.download_button(label="Download Image", data=byte_im, file_name="blue_background_image.png", mime="image/png")  

else:  
    st.write("Please upload an Image")  
