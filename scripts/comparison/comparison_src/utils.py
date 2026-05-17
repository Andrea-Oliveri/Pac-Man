import cv2


def load_image(path, transparency, resize_kwargs = None):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED if transparency else cv2.IMREAD_COLOR)
    _, _, n_channels = image.shape

    if transparency and n_channels != 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        _, _, n_channels = image.shape

    if resize_kwargs is not None:
        image = resize_image(image, **resize_kwargs)

    # Sanity check.
    expected_n_channels = 4 if transparency else 3
    if n_channels != expected_n_channels:
        raise RuntimeError(f"Programming error caused image to be loaded with {n_channels} instead of {expected_n_channels} with transparency={transparency}")

    return image


def resize_image(image, height = None, width = None, scale_width = None, scale_height = None):
    shrinking_width = None
    shrinking_height = None
    use_scale = None
    if height is None and width is None and scale_width is not None and scale_height is not None:
        shrinking_width = scale_width <= 1
        shrinking_height = scale_height <= 1
        use_scale = True
    elif height is not None and width is not None and scale_width is None and scale_height is None:
        shrinking_width = width <= image.shape[1]
        shrinking_height = height <= image.shape[0]
        use_scale = False
    else:
        raise ValueError("this function expects either 'width' and 'height' or 'scale_width' and 'scale_height' to be provided at the same time")

    interpolation = choose_best_interpolation(shrinking_width, shrinking_height)

    return cv2.resize(
        image,
        None if use_scale else (width, height),
        fx = scale_width,
        fy = scale_height,
        interpolation = interpolation
    )


def choose_best_interpolation(shrinking_width, shrinking_height):
    return (
        cv2.INTER_AREA if shrinking_width and shrinking_height
        else cv2.INTER_LANCZOS4
    )
