from PIL import Image, ImageDraw, ImageFont

def draw_detection_on_image(image_path, result):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    plate = result.get("plate", "UNKNOWN").upper()
    box = result.get("box", None)

    # Coba muat font tebal besar, fallback jika gagal
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        try:
            font = ImageFont.truetype("arialbd.ttf", 40)
        except:
            font = ImageFont.load_default()

    if box:
        # Dukung dua format box:
        if all(k in box for k in ("x", "y", "width", "height")):
            x, y, w, h = box["x"], box["y"], box["width"], box["height"]
            x1, y1, x2, y2 = x, y, x + w, y + h
        elif all(k in box for k in ("xmin", "ymin", "xmax", "ymax")):
            x1, y1, x2, y2 = box["xmin"], box["ymin"], box["xmax"], box["ymax"]
        else:
            # Format tidak dikenali
            draw.text((10, 10), plate, fill="red", font=font)
            return image, plate

        # Gambar kotak deteksi merah
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=6)

        # Hitung posisi teks
        text_bbox = draw.textbbox((0, 0), plate, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (x1 + x2) // 2 - text_width // 2
        text_y = y1 - text_height - 10 if y1 - text_height - 10 > 0 else y2 + 10

        # Gambar teks plat nomor
        draw.text((text_x, text_y), plate, fill="red", font=font)

    else:
        # Jika tidak ada box, tampilkan teks di pojok
        draw.text((10, 10), plate, fill="red", font=font)

    return image, plate
