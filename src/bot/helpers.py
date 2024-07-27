from discord import Attachment


def is_media_attachment(attachment: Attachment) -> bool:
    return attachment.content_type in [
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/webp",
        "video/mp4",
        "video/webm",
        "video/quicktime"
    ]
