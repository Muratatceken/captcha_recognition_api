from transformers import VisionEncoderDecoderModel, TrOCRProcessor
from PIL import Image
import cv2
import numpy as np

class TrOCRModel:
    def __init__(self, config: dict):
        self.model = VisionEncoderDecoderModel.from_pretrained(config['model']['path'])
        self.processor = TrOCRProcessor.from_pretrained(config['processor']['name'])
    def preprocess_image(self, image):
        """Applies connected component filtering to retain only the largest 5 components."""
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Adaptive thresholding to enhance the contrast between characters and background
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        # Find connected components
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh, connectivity=8)

        # Create an output image to retain only the largest 5 components
        output_image = np.zeros_like(thresh)

        # Sort components by size (stat array is [x, y, width, height, area])
        areas = stats[:, cv2.CC_STAT_AREA]
        largest_indices = np.argsort(areas)[::-1][:6]  # Get indices of the 5 largest components + 1 for background

        for i in largest_indices:
            if i == 0:
                continue  # Skip the background component
            output_image[labels == i] = 255

        mask = output_image

        # Invert the mask
        inverted_mask = cv2.bitwise_not(mask)

        # Convert the single-channel mask to 3 channels
        inverted_mask = cv2.cvtColor(inverted_mask, cv2.COLOR_GRAY2BGR)

        # Apply the mask to the image
        result_image = cv2.bitwise_or(image, inverted_mask)

        return result_image

    def recognize_text(self, image_path: str) -> str:
        # Load the image
        image = cv2.imread(image_path)
        
        # Preprocess the image
        preprocessed_image = self.preprocess_image(image)

        # Convert the preprocessed image to PIL format
        pil_image = Image.fromarray(cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB))

        # Prepare the image for the model
        pixel_values = self.processor(images=pil_image, return_tensors="pt").pixel_values
        output_ids = self.model.generate(pixel_values)
        predicted_text = self.processor.batch_decode(output_ids, skip_special_tokens=True)[0]
        return predicted_text
