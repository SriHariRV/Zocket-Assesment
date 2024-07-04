import os
import requests
import gradio as gr


folder_name = "generated_images"


if not os.path.exists(folder_name):
    os.makedirs(folder_name)


def generate_ad(item):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "authorization": "Bearer sk-jLFIWlPv4AdWtS1p3FzzSMOcnZ1EZVvuBAABIewxJKMJ9Ez9",
        "accept": "image/*"
    }
    data = {
        "prompt": f"generate an ad creative for {item} with attractive visuals and photoshoot background in 4k resolution.",
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


def search_and_replace(image_path, search_prompt, replace_prompt):
    if not search_prompt or not replace_prompt:
        return "Error: Search and replace prompts cannot be empty."

    url = "https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"
    headers = {
        "authorization": "Bearer sk-HuNGtMxLIVwdOMRokWv4nJViItL1TEwIh9angW0oeCD2Ilex",
        "accept": "image/*"
    }

    with open(image_path, 'rb') as img:
        files = {"image": img}
        data = {
            "prompt": replace_prompt,
            "search_prompt": search_prompt,
            "output_format": "jpeg"
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code == 200:
            edited_image_name = f"{folder_name}/edited_{os.path.basename(image_path)}"
            with open(edited_image_name, 'wb') as file:
                file.write(response.content)
            return edited_image_name
        else:
            return f"Error: {response.json()}"


def generate_and_edit_ad(item, search_prompt, replace_prompt):
    
    generated_image_path = generate_ad(item)
    
    if "Error" in generated_image_path:
        return None, generated_image_path

   
    if search_prompt and replace_prompt:
        edited_image_path = search_and_replace(generated_image_path, search_prompt, replace_prompt)
        if "Error" in edited_image_path:
            return generated_image_path, edited_image_path
        else:
            return generated_image_path, edited_image_path
    
    
    return generated_image_path, None


iface = gr.Interface(
    fn=generate_and_edit_ad,
    inputs=[
        gr.Textbox(label="Item for Ad Creative"),
        gr.Textbox(label="Search Prompt (optional)"),
        gr.Textbox(label="Replace Prompt (optional)")
    ],
    outputs=[
        gr.Image(label="Generated Ad Creative"),
        gr.Image(label="Edited Ad Creative (if applicable)")
    ],
    title="Ad Creative Generator with Search and Replace",
    description="Enter the item for the ad creative. Optionally, provide search and replace prompts to edit the generated image."
)

iface.launch()