import logging as logger
import cv2
from matplotlib import pyplot as plt
import numpy as np

from typing import Optional
from engine.app.core.io import read_image_bgr


RECTIFIED_IMG_FILENAME_PREFIX = "rectified_card_"
RECTIFIED_OUTPUT_DIR_PATH = "data/01_rectified"


def callback(input):
    pass


def rectify_card_image(img: str) -> Optional[np.ndarray]:
    # Find contours and apply perspective transform to get a top-down view of the card
    # This helps in standardizing the card image for better OCR results
    # and improves the accuracy of text extraction.
    # TODO: refactoring needed after implementing the actual rectification logic
    # TODO: improve the edge and contour detection logics for better accuracy
    img_origin = read_image_bgr(img)
    if img_origin is not None and isinstance(img_origin, np.ndarray):
        gray_img = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY)
        assert gray_img is not None, logger.error(
            "Image conversion to grayscale failed."
        )
        gray_img = cv2.bilateralFilter(gray_img, d=9, sigmaColor=75, sigmaSpace=75)
        logger.info("Image successfully read and converted to grayscale.")

        window_name = "Edge Detection Results"
        cv2.namedWindow(window_name)

        while True:
            if cv2.waitKey(1) == ord("q"):
                break
            edges = auto_canny(gray_img)
            cv2.imshow(window_name, edges)

        img_copy = img_origin.copy()
        processed_img, contours = find_card_contours(edges, img_copy)
        # Visualize with OpenCV and Matplotlib
        vis = processed_img.copy()
        if contours is not None:
            # drawContours expects list of (N,1,2) arrays; ensure shape & dtype
            cv2.drawContours(
                vis, [contours.reshape(-1, 1, 2).astype(np.int32)], -1, (0, 255, 0), 3
            )

            # Matplotlib display: convert BGR->RGB for color images
            edges_show = edges  # single-channel OK
            orig_rgb = cv2.cvtColor(img_origin, cv2.COLOR_BGR2RGB)
            vis_rgb = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)

            plt.figure(figsize=(12, 4))
            plt.subplot(1, 3, 1)
            plt.imshow(edges_show, cmap="gray")
            plt.title("Edges")
            plt.axis("off")
            plt.subplot(1, 3, 2)
            plt.imshow(orig_rgb)
            plt.title("Original")
            plt.axis("off")
            plt.subplot(1, 3, 3)
            plt.imshow(vis_rgb)
            plt.title("Detected Card")
            plt.axis("off")
            c = contours.reshape(-1, 2)
            plt.plot([*c[:, 0], c[0, 0]], [*c[:, 1], c[0, 1]], "r-")
            plt.tight_layout()
            plt.show()
        else:
            print("No card contour found")

        cv2.destroyAllWindows()
        return None
    else:
        logger.error("Failed to read image or image is not a valid numpy array.")
    return None


def find_card_contours(edges: np.ndarray, img: np.ndarray):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    card_contours = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 0.02 * (img.shape[0] * img.shape[1]):
            continue

        # Approximate the contour to a polygon
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        if len(approx) == 4 and area > max_area and cv2.isContourConvex(approx):
            points = approx.reshape(4, 2).astype(np.float32)
            rect = order_points(points)
            (top_left, top_right, bottom_right, bottom_left) = rect
            width = (
                np.linalg.norm(bottom_right - bottom_left)
                + np.linalg.norm(top_right - top_left)
            ) / 2
            height = (
                np.linalg.norm(top_right - bottom_right)
                + np.linalg.norm(top_left - bottom_left)
            ) / 2
            if height > 0:
                aspect_ratio = width / height
                if 0.6 < aspect_ratio < 0.9:
                    card_contours = approx
                    max_area = area

    return img, card_contours


def apply_quad_detection(img: np.ndarray) -> Optional[tuple[bool, np.ndarray]]:
    # Placeholder for quad detection logic
    # This function should implement the actual quad detection algorithm
    logger.info("Quad detection not implemented yet.")
    return None


def apply_perspective_transformation() -> Optional[np.ndarray]:
    # Placeholder for perspective transform logic
    # This function should implement the actual perspective transformation algorithm
    logger.info("Perspective transform not implemented yet.")
    return None


def auto_canny(image: np.ndarray, sigma: float = 0.33) -> np.ndarray:
    # Compute the median of the single channel pixel intensities
    v = np.median(image)

    # Apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    return cv2.Canny(image, lower, upper)


def order_points(pts: np.ndarray) -> np.ndarray:
    # Initialize a list of coordinates that will be ordered
    # such that the first entry is the top-left, the second is the top-right,
    # the third is the bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect
