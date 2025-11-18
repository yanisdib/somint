from typing import Sequence
from typing import Final

import cv2 as cv
import numpy as np


Mat = np.ndarray
INTERIM_DIR: Final[str] = r"data/interim/"
INTERIM_FILE_SUFFIX: Final[str] = "interim_"
POKEMON_CARD_RESOLUTION: Final[tuple[int, int, int]] = (1505, 2096, 3)
DEFAULT_SIGMA_VALUE: Final[float] = 0.33


# TODO: Edge detection needs finetuning
# Current implementation struggles to find sleeved cards in specific cases
def detect_pokemon_card(filepath: str) -> Mat | None:
    """
    Detects a Pokémon card from a picture, showing each processing step.
    """
    img: Mat | None = cv.imread(filepath)
    if img is None:
        print(f"Could not read image at {filepath}")
        return None

    if is_back_card(filepath):
        gray_img = cv.split(img)[0]
    else:
        gray_img: Mat = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    blurred_img: Mat = cv.GaussianBlur(gray_img, (7, 7), 1)
    binary_img = cv.adaptiveThreshold(
        blurred_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 31, 3
    )
    cv.imshow("Combined", binary_img)

    kernel = cv.getStructuringElement(cv.MORPH_DIAMOND, (3, 3))
    cleaned_img = cv.morphologyEx(binary_img, cv.MORPH_CLOSE, kernel, iterations=1)
    cv.imshow("Cleaned", cleaned_img)
    contours, hierarchy = cv.findContours(
        cleaned_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
    )

    all_contours_vis = img.copy()
    cv.drawContours(all_contours_vis, contours, -1, (0, 255, 0), 1)

    card_shape, area = find_card_shape(contours, hierarchy)
    if card_shape.size == 0:
        print("No card found. Exiting.")
        cv.destroyAllWindows()
        return None

    chosen_contour_vis = img.copy()
    cv.drawContours(chosen_contour_vis, [np.intp(card_shape)], -1, (0, 255, 0), 2)
    cv.imshow("Contoured", chosen_contour_vis)

    width, height, _ = POKEMON_CARD_RESOLUTION
    sorted_corners = sort_corners(card_shape)
    destination_corners = np.array(
        [[0, 0], [width, 0], [width, height], [0, height]], dtype="float32"
    )

    matrix = cv.getPerspectiveTransform(
        np.array(sorted_corners, dtype="float32"), destination_corners
    )
    warped_card: Mat = cv.warpPerspective(
        img, matrix, (width, height), flags=cv.INTER_CUBIC
    )

    print("Step 7: Final Warped Card. Press any key to close all windows.")
    cv.imshow("7. Warped Card", warped_card)
    cv.waitKey(0)

    print("Processing complete.")
    cv.destroyAllWindows()

    return warped_card


def apply_auto_canny(img: Mat, sigma: float = 0.33):
    """Applies automatic edge detection

    Args:
        img (Mat): target image
        sigma (float, optional): quantifier. Defaults to 0.33.

    Returns:
        _type_: _description_
    """
    median_value = np.median(img)
    lower: float = int(min(255, (1.0 + sigma) * median_value))
    higher: float = int(max(0, (1.0 - sigma) * median_value))
    return cv.Canny(img, lower, higher)


def is_back_card(filename: str) -> bool:
    """Detect if the current image is a back shot of the current evaluated card.
    This is particularly needed because non japanese cards have a blue background
    which makes it more difficult to detect edges and contours.

    Args:
        filename (str): path or url of the card picture

    Returns:
        bool: whether is the card's back or not
    """
    return filename.__contains__("back")


def create_blank_image(shape: tuple[int, int, int], dtype=np.uint8) -> Mat:
    """Creates a blank image from shape and data type

    Args:
        shape (tuple[int, int, int]): shape of the image
        dtype (_type_, optional): data type. Defaults to np.uint8.

    Returns:
        Mat: blank image
    """
    return np.zeros(shape, dtype)


def find_card_shape(contours: Sequence[Mat], hierarchy: Mat) -> tuple[Mat, float]:
    """
    Finds a card by looking for a "nested rectangle" structure.
    It looks for a large 4-sided contour that has another 4-sided contour inside it.
    """
    best_candidate = {"contour": None, "area": 0}

    # The hierarchy is wrapped in an extra array, so we access it with hierarchy[0]
    if hierarchy is None:
        return np.array([]), 0.0

    for i, contour in enumerate(contours):
        area = cv.contourArea(contour)

        if area > 5000:
            peri = cv.arcLength(contour, True)
            approx_parent = cv.approxPolyDP(contour, 0.02 * peri, True)

            # Check if this contour is a 4-sided parent
            if len(approx_parent) == 4:
                # The index of the first child is at hierarchy[0][i][2]
                child_index = hierarchy[0][i][2]

                if child_index != -1:
                    if area > best_candidate["area"]:
                        best_candidate["contour"] = contour
                        best_candidate["area"] = area
                else:
                    print("This 4-sided contour has no child.")

    if best_candidate["contour"] is None:
        return np.array([]), 0.0

    # Return precise corners
    rect = cv.minAreaRect(best_candidate["contour"])
    box = cv.boxPoints(rect)

    return box, best_candidate["area"]


def sort_corners(shape: Mat) -> list[Mat]:
    points = shape.reshape(4, 2)
    sums = points.sum(axis=1)
    diffs = np.diff(points, axis=1)

    top_left = np.argmin(sums)
    bottom_right = np.argmax(sums)
    top_right = np.argmin(diffs)
    bottom_left = np.argmax(diffs)

    return [
        points[top_left],
        points[top_right],
        points[bottom_right],
        points[bottom_left],
    ]


def combine_edge_detection(adaptive_img: Mat, canny_img: Mat) -> Mat:
    combined = cv.bitwise_or(adaptive_img, canny_img)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    cleaned = cv.morphologyEx(combined, cv.MORPH_CLOSE, kernel, iterations=1)
    return cleaned
