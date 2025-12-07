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

    sobel_x = cv.Sobel(gray_img, cv.CV_64F, 2, 0, ksize=3)
    sobel_y = cv.Sobel(gray_img, cv.CV_64F, 0, 2, ksize=3)
    gradient_magnitude = cv.magnitude(sobel_x, sobel_y)
    gradient_magnitude = cv.convertScaleAbs(gradient_magnitude)

    blurred_img: Mat = cv.GaussianBlur(gradient_magnitude, (5, 5), 1)
    _, binary_img = cv.threshold(blurred_img, 30, 255, cv.THRESH_BINARY)

    kernel_clean = cv.getStructuringElement(cv.MORPH_RECT + cv.MORPH_ELLIPSE, (3, 3))
    thresh_clean = cv.morphologyEx(
        binary_img, cv.MORPH_OPEN, kernel_clean, iterations=4
    )
    thresh_clean = cv.morphologyEx(
        thresh_clean, cv.MORPH_CLOSE, kernel_clean, iterations=7
    )

    cv.imshow("Cleaned", thresh_clean)
    contours, hierarchy = cv.findContours(
        thresh_clean, cv.RETR_TREE, cv.CHAIN_APPROX_NONE
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

    if hierarchy is None:
        return np.array([]), 0.0

    for i, contour in enumerate(contours):
        area = cv.contourArea(contour)

        if area > 5000:
            peri = cv.arcLength(contour, True)
            approx_parent = cv.approxPolyDP(contour, 0.02 * peri, True)

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
