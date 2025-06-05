def draw_detection_on_image(image_path, detection_result):
    from PIL import Image, ImageDraw, ImageFont
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    plate = detection_result["plate"].upper()
    box = detection_result["box"]

    draw.rectangle([(box["xmin"], box["ymin"]), (box["xmax"], box["ymax"])] , outline="red", width=4)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
    except:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), plate, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (box["xmin"] + box["xmax"]) // 2 - text_width // 2
    text_y = box["ymin"] - text_height - 10
    if text_y < 0:
        text_y = box["ymin"] + 10

    draw.text((text_x, text_y), plate, fill="red", font=font)
    return image, plate
