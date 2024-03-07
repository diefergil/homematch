from typing import Any, Dict, Tuple, Union

from transformers import CLIPModel, CLIPProcessor

from homematch.config import DEVICE, MODEL_ID
from homematch.data.types import PropertyListing

model = CLIPModel.from_pretrained(MODEL_ID).to(DEVICE)
processor = CLIPProcessor.from_pretrained(MODEL_ID)


def process_image(
    batch: dict,  # type: ignore
) -> Union[Tuple[CLIPProcessor, Dict[str, Any]], CLIPProcessor]:
    image = processor(
        text=batch["text_description"],
        images=batch["image"],
        return_tensors="pt",
        padding=True,
        truncation=True,
    )["pixel_values"].to(DEVICE)

    # create the image embedding from the processed image and the model
    img_emb = model.get_image_features(image)

    batch["vector"] = img_emb.cpu()
    batch["image_bytes"] = [PropertyListing.pil_to_bytes(img) for img in batch["image"]]
    return batch
