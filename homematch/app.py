from typing import Any, List, Optional, Tuple

import gradio as gr
import lancedb
from transformers import CLIPModel, CLIPTokenizerFast

from homematch.config import DATA_DIR, MODEL_ID, TABLE_NAME
from homematch.data.types import ImageData

DEVICE: str = "cpu"
model: CLIPModel = CLIPModel.from_pretrained(MODEL_ID).to(DEVICE)
tokenizer: CLIPTokenizerFast = CLIPTokenizerFast.from_pretrained(MODEL_ID)

uri: str = str(DATA_DIR) + "/.lancedb/"
db = lancedb.connect(uri)
table = db[TABLE_NAME]


def embed_func(query: str) -> Any:
    inputs = tokenizer([query], padding=True, return_tensors="pt").to(DEVICE)
    text_features = model.get_text_features(**inputs)
    return text_features.detach().numpy()[0]


def find_images(query: str) -> List[Tuple[Any, str]]:
    emb = embed_func(query)
    rs = table.search(emb).limit(9).to_pydantic(ImageData)
    return [(image.load_image(), image.text_description) for image in rs]


def update_description(image_info: Optional[Tuple[Any, str]]) -> str:
    print(image_info)
    print("asd")
    if image_info is None or image_info[0] is None:
        return "Select an image to see its description"
    else:
        _, description = image_info
        return description


with gr.Blocks() as demo:
    with gr.Row():
        vector_query: gr.Textbox = gr.Textbox(
            value="A modern building with 2 bathrooms and 3 bedrooms", show_label=False
        )
        b1: gr.Button = gr.Button("Submit")
    with gr.Row():
        gallery: gr.Gallery = gr.Gallery(
            label="Found images",
            show_label=False,
            elem_id="gallery",
            columns=3,
            rows=3,
            object_fit="contain",
            height="auto",
        )

    b1.click(find_images, inputs=vector_query, outputs=gallery)

demo.launch(server_name="127.0.0.1", inline=False)
