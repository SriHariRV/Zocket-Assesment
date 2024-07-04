import os
import requests
import gradio as gr

# Define the folder name
folder_name = "generated_images"

# Create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Function to generate an ad creative
def generate_ad(item):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "authorization": "Bearer sk-4Tdagt670h7PuU9zcG7uyNEIQvdkBzL8Cx9bXRBd6gQydvp5",
        "accept": "image/*"
    }
    data = {
        "prompt": f"generate an ad creative for {item} with attractive visuals and associated amenities as and photoshoot background in 4k resolution.",
        "output_format": "jpeg"
    }

    response = requests.post(url, headers=headers, files={"none": ''}, data=data)

    if response.status_code == 200:
        image_name = f"{folder_name}/ad_creative_{len(os.listdir(folder_name)) + 1}.jpeg"
        with open(image_name, 'wb') as file:
            file.write(response.content)
        return image_name
    else:
        return f"Error: {response.json()}"

# Gradio UI setup
def gradio_interface(item):
    image_path = generate_ad(item)
    if "Error" in image_path:
        return image_path
    else:
        return image_path

# Set up the Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="image",
    title="Ad Creative Generator",
    description="Enter the item you want to generate an ad creative for and get a 4K resolution image."
)

iface.launch()
