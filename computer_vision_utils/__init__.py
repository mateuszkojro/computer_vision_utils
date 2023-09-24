import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation_my
import cv2


def load_video(video_path, rotate=False, natural_colors=True):
    stream = cv2.VideoCapture(video_path)

    if not stream.isOpened():
        return None

    status, first_frame = stream.read()
    if not status:
        return None

    num_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
    (width, height, chanels) = first_frame.shape

    video = np.empty((num_frames, width, height, chanels), dtype=np.uint8)
    video[0] = first_frame

    for frame_idx in range(1, num_frames):
        stream.read(video[frame_idx])
        
        if natural_colors:
            video[frame_idx] = bgr_to_rgb(video[frame_idx])
        
        if rotate:
            np.rot90(video[frame_idx])

    return video


def iter_frames(video_path):
    stream = cv2.VideoCapture(video_path)

    while stream.isOpened():
        status, frame = stream.read()

        if not status:
            break

        yield frame

    stream.release()


def save_video(path, data, format="XVID", fps=30):
    num_frames, width, height, colors = data.shape
    video_writer = cv2.VideoWriter(
        path, cv2.VideoWriter_fourcc(*format), fps, (height, width)
    )

    for frame in data:
        video_writer.write(frame)

    video_writer.release()


def bgr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def notebook_display_video(video, fig=None, backend="js_html"):
    if fig is None:
        fig = plt.figure()

    animation_frames = [
        (
            plt.imshow(
                frame,
            ),
        )
        for frame in video
    ]

    anim = animation_my.ArtistAnimation(
        fig, animation_frames, interval=100, blit=True, repeat_delay=10
    )

    if backend == "js_html":
        output = anim.to_jshtml()
    elif backend == "html5":
        output = anim.to_html5_video()
    else:
        raise ValueError('Backend needs to be one of ("js_html", "html5")')

    try:
        from IPython.utils import io
        from IPython.display import HTML

        return HTML(output)
    except ImportError:
        return anim


def add_watermark(image, overlay, opacity):
    width, height, _ = overlay.shape
    destination = image[:width, :height]
    result = cv2.addWeighted(destination, 1, overlay, opacity, 0)
    image[:width, :height] = result
    return image


def add_point(image, position, radius=5, color=(255, 0, 0), thickness=-1):
    return cv2.circle(image, position, radius, color, thickness)


def add_line(image, start, end, color=(255, 0, 0), thickness=2):
    return cv2.line(image, start, end, color, thickness)


def add_rectangle(image, top_left, down_right, color=(255, 0, 0), line_weight=3):
    return cv2.rectangle(image, top_left, down_right, color, line_weight)


def add_text(
    image,
    text,
    position,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=1,
    color=(255, 0, 0),
    thickness=2,
):
    return cv2.putText(
        image, text, position, font, font_scale, color, thickness, cv2.LINE_AA
    )
