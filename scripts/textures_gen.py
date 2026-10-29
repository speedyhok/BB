import os
import math
from PIL import Image, ImageDraw, ImageFont

def generate_textures(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating enhanced Breaking Bad textures in {output_dir}...")

    # 1. High-Resolution Los Pollos Hermanos Sign (1024x1024)
    pollos = Image.new("RGBA", (1024, 1024), (255, 255, 255, 0))
    draw = ImageDraw.Draw(pollos)
    # Outer yellow circle with rich red border
    draw.ellipse([30, 30, 994, 994], fill=(245, 185, 25, 255), outline=(180, 20, 20, 255), width=36)
    draw.ellipse([80, 80, 944, 944], fill=(255, 225, 75, 255), outline=(210, 30, 30, 255), width=12)
    # Center white emblem circle
    draw.ellipse([180, 180, 844, 844], fill=(255, 255, 255, 255), outline=(180, 20, 20, 255), width=16)

    # Stylized Roosters: Left Blue, Right Red
    # Left Rooster (Blue)
    draw.ellipse([270, 310, 480, 590], fill=(25, 65, 160, 255))
    draw.ellipse([330, 260, 460, 390], fill=(25, 65, 160, 255))
    draw.polygon([(290, 320), (240, 340), (295, 365)], fill=(245, 160, 20, 255)) # beak
    draw.polygon([(350, 250), (380, 205), (410, 250)], fill=(210, 30, 30, 255)) # comb
    draw.ellipse([410, 295, 435, 320], fill=(255, 255, 255, 255)) # eye white
    draw.ellipse([416, 301, 428, 313], fill=(20, 20, 20, 255)) # pupil
    # Bow tie left
    draw.polygon([(390, 400), (430, 425), (390, 450), (350, 425)], fill=(210, 30, 30, 255))

    # Right Rooster (Red)
    draw.ellipse([544, 310, 754, 590], fill=(210, 35, 35, 255))
    draw.ellipse([564, 260, 694, 390], fill=(210, 35, 35, 255))
    draw.polygon([(734, 320), (784, 340), (729, 365)], fill=(245, 160, 20, 255)) # beak
    draw.polygon([(614, 250), (644, 205), (674, 250)], fill=(25, 65, 160, 255)) # comb
    draw.ellipse([589, 295, 614, 320], fill=(255, 255, 255, 255)) # eye white
    draw.ellipse([595, 301, 607, 313], fill=(20, 20, 20, 255)) # pupil
    # Bow tie right
    draw.polygon([(604, 400), (644, 425), (604, 450), (564, 425)], fill=(25, 65, 160, 255))

    # Sombreros on roosters
    draw.ellipse([320, 225, 470, 265], fill=(240, 200, 100, 255), outline=(140, 90, 30, 255), width=6)
    draw.ellipse([554, 225, 704, 265], fill=(240, 200, 100, 255), outline=(140, 90, 30, 255), width=6)

    # Red arched banner across bottom
    draw.rectangle([120, 610, 904, 730], fill=(185, 22, 22, 255), outline=(255, 215, 0, 255), width=8)
    draw.text((160, 635), "LOS POLLOS HERMANOS", fill=(255, 255, 255, 255))
    draw.text((360, 770), "ALBUQUERQUE", fill=(185, 22, 22, 255))
    pollos.save(os.path.join(output_dir, "pollos_hermanos_logo.png"))

    # 2. Highway Overhead Gantry Sign (1024x512)
    hwy_img = Image.new("RGBA", (1024, 512), (15, 95, 45, 255)) # Highway interstate green
    draw = ImageDraw.Draw(hwy_img)
    draw.rectangle([16, 16, 1008, 496], outline=(255, 255, 255, 255), width=10)
    # Interstate 40 East Shield
    draw.polygon([(80, 60), (220, 60), (240, 160), (150, 220), (60, 160)], fill=(25, 55, 150, 255), outline=(255, 255, 255, 255), width=6)
    draw.rectangle([70, 60, 230, 100], fill=(200, 25, 25, 255))
    draw.text((115, 70), "I-40", fill=(255, 255, 255, 255))
    draw.text((130, 130), "EAST", fill=(255, 255, 255, 255))
    # Destination text
    draw.text((270, 80), "AMARILLO - SANTA FE", fill=(255, 255, 255, 255))
    draw.line([(40, 250), (984, 250)], fill=(255, 255, 255, 255), width=6)
    draw.text((100, 280), "HISTORIC ROUTE 66 / CENTRAL AVE", fill=(255, 255, 255, 255))
    draw.text((100, 340), "NEXT EXIT  1/2 MILE", fill=(255, 255, 255, 255))
    # Arrow
    draw.polygon([(850, 360), (920, 360), (920, 420), (950, 420), (885, 470), (820, 420), (850, 420)], fill=(255, 255, 255, 255))
    hwy_img.save(os.path.join(output_dir, "highway_overhead_sign.png"))

    # 3. Street Name Signs (512x128)
    street_img = Image.new("RGBA", (512, 128), (15, 105, 50, 255))
    draw = ImageDraw.Draw(street_img)
    draw.rectangle([6, 6, 506, 122], outline=(255, 255, 255, 255), width=5)
    draw.text((40, 35), "HISTORIC ROUTE 66", fill=(255, 255, 255, 255))
    draw.text((370, 35), "CENTRAL AVE", fill=(255, 255, 255, 255))
    street_img.save(os.path.join(output_dir, "street_sign_central.png"))

    street_walt = Image.new("RGBA", (512, 128), (15, 105, 50, 255))
    draw = ImageDraw.Draw(street_walt)
    draw.rectangle([6, 6, 506, 122], outline=(255, 255, 255, 255), width=5)
    draw.text((50, 40), "308 NEGRA ARROYO LN", fill=(255, 255, 255, 255))
    street_walt.save(os.path.join(output_dir, "street_sign_negra_arroyo.png"))

    # 4. Ultra-Detailed Roof Pizza (512x512)
    pizza_img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pizza_img)
    # Crust with baked blisters
    draw.ellipse([20, 20, 492, 492], fill=(210, 145, 60, 255), outline=(150, 90, 30, 255), width=16)
    # Golden cheese layer with sauce bleeding through
    draw.ellipse([50, 50, 462, 462], fill=(245, 190, 45, 255))
    # Herb flecks & browned cheese blisters
    for bx in range(80, 440, 35):
        for by in range(80, 440, 35):
            if math.hypot(bx - 256, by - 256) < 185:
                draw.ellipse([bx-4, by-4, bx+4, by+4], fill=(195, 120, 25, 255))
                draw.ellipse([bx+8, by-2, bx+10, by], fill=(35, 95, 30, 255)) # oregano herb

    # 16 Crisp Pepperoni slices
    for i in range(16):
        ang = i * (2 * math.pi / 16)
        r = 110 + (i % 3) * 35
        cx = int(256 + r * math.cos(ang))
        cy = int(256 + r * math.sin(ang))
        draw.ellipse([cx-24, cy-24, cx+24, cy+24], fill=(165, 32, 20, 255), outline=(115, 18, 10, 255), width=4)
        draw.ellipse([cx-12, cy-12, cx+12, cy+12], fill=(185, 45, 30, 255))

    # Center pepperonis
    for cx, cy in [(235, 240), (280, 265), (250, 290)]:
        draw.ellipse([cx-22, cy-22, cx+22, cy+22], fill=(165, 32, 20, 255), outline=(115, 18, 10, 255), width=4)

    # Cutout of missing slice (transparent wedge cutout from 30 deg to 75 deg)
    draw.pieslice([20, 20, 492, 492], 28, 72, fill=(0, 0, 0, 0))
    pizza_img.save(os.path.join(output_dir, "pizza_roof.png"))

    # 5. New Mexico License Plates (512x256)
    plate_img = Image.new("RGBA", (512, 256), (245, 220, 50, 255)) # New Mexico Yellow
    draw = ImageDraw.Draw(plate_img)
    draw.rectangle([8, 8, 504, 248], outline=(200, 20, 20, 255), width=10)
    draw.text((120, 25), "NEW MEXICO USA", fill=(180, 25, 25, 255))
    # Red Zia Sun Symbol in center
    zx, zy = 256, 128
    draw.ellipse([zx-25, zy-25, zx+25, zy+25], outline=(190, 25, 25, 255), width=5)
    for dx in [-45, -35, 35, 45]:
        draw.line([(zx+dx, zy), (zx+dx*0.6, zy)], fill=(190, 25, 25, 255), width=4)
    for dy in [-45, -35, 35, 45]:
        draw.line([(zx, zy+dy), (zx, zy+dy*0.6)], fill=(190, 25, 25, 255), width=4)
    # LWYRUP text
    draw.text((70, 95), "L W Y R U P", fill=(20, 30, 50, 255))
    draw.text((140, 200), "Land of Enchantment", fill=(180, 25, 25, 255))
    plate_img.save(os.path.join(output_dir, "license_plate_lwyrup.png"))

    # 6. Methylamine NFPA Hazard Label (512x512)
    haz_img = Image.new("RGBA", (512, 512), (30, 60, 150, 255))
    draw = ImageDraw.Draw(haz_img)
    # Diamond diamond label
    draw.polygon([(256, 40), (472, 256), (256, 472), (40, 256)], fill=(245, 205, 30, 255), outline=(20, 20, 20, 255), width=8)
    # Madrigal Bee logo in center
    draw.ellipse([230, 160, 282, 340], fill=(20, 20, 20, 255))
    draw.ellipse([180, 190, 250, 290], fill=(20, 20, 20, 255))
    draw.ellipse([262, 190, 332, 290], fill=(20, 20, 20, 255))
    draw.text((110, 360), "GOLDEN MOTH", fill=(20, 20, 20, 255))
    draw.text((120, 390), "CHEMICAL CO.", fill=(20, 20, 20, 255))
    haz_img.save(os.path.join(output_dir, "methylamine_barrel_logo.png"))

    # 7. Manhole Cover & Storm Drain (512x512)
    manhole = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(manhole)
    draw.ellipse([20, 20, 492, 492], fill=(60, 62, 65, 255), outline=(35, 35, 38, 255), width=14)
    for r in range(50, 230, 40):
        draw.ellipse([256-r, 256-r, 256+r, 256+r], outline=(40, 42, 45, 255), width=6)
    draw.text((130, 235), "CITY OF ALBUQUERQUE", fill=(25, 25, 25, 255))
    draw.text((215, 270), "SEWER", fill=(25, 25, 25, 255))
    manhole.save(os.path.join(output_dir, "manhole_cover.png"))

    # 8. Saul Goodman Billboard (1024x512)
    saul = Image.new("RGBA", (1024, 512), (255, 220, 20, 255))
    draw = ImageDraw.Draw(saul)
    draw.rectangle([10, 10, 1014, 502], outline=(180, 15, 15, 255), width=16)
    draw.rectangle([30, 30, 994, 150], fill=(195, 20, 20, 255))
    draw.text((70, 55), "IN TROUBLE? BETTER CALL SAUL!", fill=(255, 255, 255, 255))
    # Scales of justice
    draw.line([(140, 200), (140, 420)], fill=(30, 30, 30, 255), width=10)
    draw.line([(80, 240), (200, 240)], fill=(30, 30, 30, 255), width=8)
    draw.polygon([(60, 310), (100, 310), (80, 340)], fill=(180, 140, 20, 255))
    draw.polygon([(180, 310), (220, 310), (200, 340)], fill=(180, 140, 20, 255))
    # Big text
    draw.text((260, 180), "SAUL GOODMAN & ASSOCIATES", fill=(20, 20, 20, 255))
    draw.text((260, 240), "ATTORNEY AT LAW - CRIMINAL DEFENSE", fill=(180, 20, 20, 255))
    draw.text((260, 310), "(505) 503-4455", fill=(10, 30, 170, 255))
    draw.rectangle([(250, 390), (980, 460)], fill=(195, 20, 20, 255))
    draw.text((280, 405), "'BECAUSE RESULTS MATTER! FREE CONSULTATION'", fill=(255, 255, 255, 255))
    saul.save(os.path.join(output_dir, "saul_goodman_billboard.png"))

    print("All enhanced textures generated successfully!")

if __name__ == "__main__":
    generate_textures("/home/ubuntu/BB/textures")
