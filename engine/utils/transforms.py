import cv2 as cv
from numpy import ndarray
from engine.schemas.image import CropRegion


def rescale(img: ndarray, scale: float = 0.75):
    """Rescales an image by a given factor.

    Args:
        img: The input image as a NumPy array.
        scale: The factor by which to rescale the image.
            Defaults to 0.75.

    Returns:
        The rescaled image as a NumPy array.

    Example:
        >>> import cv2 as cv
        >>> import numpy as np
        >>> # Create a dummy image for demonstration
        >>> dummy_image = np.zeros((400, 600, 3), dtype=np.uint8)
        >>> # Rescale the image to 50% of its original size
        >>> rescaled_img = rescale(dummy_image, 0.5)
        >>> print(f"Original dimensions: {dummy_image.shape[1]}x{dummy_image.shape[0]}")
        Original dimensions: 600x400
        >>> print(f"Rescaled dimensions: {rescaled_img.shape[1]}x{rescaled_img.shape[0]}")
        Rescaled dimensions: 300x200
    """
    width: int = int(img.shape[1] * scale)
    height: int = int(img.shape[0] * scale)
    dimensions: tuple[int, int] = (width, height)

    return cv.resize(img, dimensions, interpolation=cv.INTER_AREA)


def crop(img: ndarray, region: CropRegion):
    """Crops an image to a specified region using start and end coordinates.

    Args:
        img: The input image as a NumPy array.
        region: A CropRegion object defining the area to crop using start/end coordinates.

    Returns:
        The cropped image as a NumPy array.

    Example:
        >>> import numpy as np
        >>> from engine.schemas.image import CropRegion
        >>> # Create a dummy image
        >>> dummy_image = np.zeros((200, 300, 3), dtype=np.uint8)
        >>> # Define the cropping region from y=0 to y=100 and x=100 to x=200
        >>> crop_area = CropRegion(y_start=0, y_end=100, x_start=100, x_end=200)
        >>> # Crop the image using the region object
        >>> cropped_img = crop(dummy_image, crop_area)
        >>> print(f"Original dimensions: {dummy_image.shape[1]}x{dummy_image.shape[0]}")
        Original dimensions: 300x200
        >>> print(f"Cropped dimensions: {cropped_img.shape[1]}x{cropped_img.shape[0]}")
        Cropped dimensions: 100x100
    """
    y_start = region.y_start
    y_end = region.y_end
    x_start = region.x_start
    x_end = region.x_end

    return img[y_start:y_end, x_start:x_end]
