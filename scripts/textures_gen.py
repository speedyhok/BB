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

    # 9. Saul's Iconic US Constitution Wallpaper (1024x512)
    const_img = Image.new("RGBA", (1024, 512), (238, 222, 180, 255)) # Aged parchment
    draw = ImageDraw.Draw(const_img)
    # Aged border & corner filigree
    draw.rectangle([12, 12, 1012, 500], outline=(140, 105, 50, 255), width=8)
    draw.rectangle([22, 22, 1002, 490], outline=(180, 140, 70, 255), width=3)
    # Calligraphic "We the People"
    draw.text((60, 40), "We the People", fill=(45, 28, 12, 255))
    draw.text((60, 110), "of the United States, in Order to form a more perfect Union,", fill=(65, 45, 20, 255))
    draw.text((60, 145), "establish Justice, insure domestic Tranquility, provide for the common defense,", fill=(65, 45, 20, 255))
    draw.text((60, 180), "promote the general Welfare, and secure the Blessings of Liberty to ourselves", fill=(65, 45, 20, 255))
    draw.text((60, 215), "and our Posterity, do ordain and establish this CONSTITUTION for the United States of America.", fill=(65, 45, 20, 255))
    
    # Articles text simulation lines
    for ly in range(265, 450, 18):
        draw.line([(60, ly), (960, ly)], fill=(100, 75, 40, 200), width=2)
    # Gold Foil Presidential / Great Seal on Right
    draw.ellipse([800, 50, 960, 210], fill=(215, 175, 55, 255), outline=(150, 110, 30, 255), width=6)
    draw.ellipse([825, 75, 935, 185], fill=(240, 200, 70, 255), outline=(170, 125, 35, 255), width=3)
    draw.text((845, 120), "CONSTITUTION", fill=(60, 40, 10, 255))
    const_img.save(os.path.join(output_dir, "saul_constitution.png"))

    # 10. Stack of Cash / $100 Bill Money Bricks (512x256)
    money_img = Image.new("RGBA", (512, 256), (200, 225, 205, 255)) # Fed Reserve Green
    draw = ImageDraw.Draw(money_img)
    draw.rectangle([8, 8, 504, 248], outline=(25, 85, 40, 255), width=10)
    draw.rectangle([20, 20, 492, 236], outline=(40, 120, 60, 255), width=4)
    # Vignette portrait oval
    draw.ellipse([190, 45, 322, 210], fill=(225, 240, 225, 255), outline=(25, 85, 40, 255), width=6)
    draw.text((232, 115), "FRANKLIN", fill=(20, 65, 30, 255))
    draw.text((35, 35), "100", fill=(25, 85, 40, 255))
    draw.text((435, 35), "100", fill=(25, 85, 40, 255))
    draw.text((35, 195), "100", fill=(25, 85, 40, 255))
    draw.text((435, 195), "100", fill=(25, 85, 40, 255))
    draw.text((120, 25), "UNITED STATES OF AMERICA", fill=(25, 85, 40, 255))
    draw.text((150, 215), "ONE HUNDRED DOLLARS", fill=(25, 85, 40, 255))
    # Paper currency wrapper band ($10,000 Bank Strap)
    draw.rectangle([210, 6, 302, 250], fill=(250, 250, 245, 255), outline=(180, 140, 40, 255), width=4)
    draw.text((220, 80), "$10,000", fill=(180, 20, 20, 255))
    draw.text((225, 140), "CASH", fill=(30, 30, 30, 255))
    money_img.save(os.path.join(output_dir, "money_cash_bundle.png"))

    # 11. Schraderbräu Homebrew Beer Label (512x512)
    beer_img = Image.new("RGBA", (512, 512), (245, 240, 220, 255))
    draw = ImageDraw.Draw(beer_img)
    draw.rectangle([16, 16, 496, 496], outline=(140, 20, 20, 255), width=12)
    draw.rectangle([28, 28, 484, 484], outline=(200, 160, 40, 255), width=5)
    # German crest arch
    draw.ellipse([100, 60, 412, 220], fill=(160, 25, 25, 255))
    draw.text((140, 115), "SCHRADERBRÄU", fill=(255, 235, 160, 255))
    draw.text((180, 170), "SINCE 2008", fill=(255, 255, 255, 255))
    # Hops & wheat graphic
    draw.ellipse([216, 250, 296, 330], fill=(60, 130, 40, 255), outline=(40, 90, 25, 255), width=4)
    draw.text((120, 360), "SILKY SMOOTH GERMAN LAGER", fill=(40, 30, 20, 255))
    draw.text((150, 400), "HAND-CRAFTED BY HANK SCHRADER", fill=(160, 25, 25, 255))
    draw.text((170, 440), "ALBUQUERQUE, NM - 5.8% ABV", fill=(80, 80, 80, 255))
    beer_img.save(os.path.join(output_dir, "schraderbrau_label.png"))

    # 12. Framed First Dollar Bill - A1A Carwash (512x256)
    frame_img = Image.new("RGBA", (512, 256), (90, 50, 20, 255)) # Walnut frame
    draw = ImageDraw.Draw(frame_img)
    # Velvet matte inner backing
    draw.rectangle([18, 18, 494, 238], fill=(30, 45, 30, 255), outline=(200, 170, 60, 255), width=4)
    # $1 Bill in center
    draw.rectangle([60, 40, 452, 175], fill=(215, 235, 215, 255), outline=(30, 90, 40, 255), width=5)
    draw.ellipse([210, 60, 302, 155], fill=(235, 245, 235, 255), outline=(30, 90, 40, 255), width=3)
    draw.text((230, 100), "WASH #1", fill=(30, 90, 40, 255))
    draw.text((75, 50), "$1", fill=(30, 90, 40, 255))
    draw.text((420, 50), "$1", fill=(30, 90, 40, 255))
    # Brass commemorative plaque below bill
    draw.rectangle([120, 190, 392, 230], fill=(215, 175, 55, 255), outline=(130, 95, 25, 255), width=3)
    draw.text((135, 200), "FIRST DOLLAR EARNED - A-1-A CARWASH", fill=(40, 25, 10, 255))
    frame_img.save(os.path.join(output_dir, "framed_first_dollar.png"))

    # 13. Leaves of Grass - Walt Whitman Book Cover (512x512)
    book_img = Image.new("RGBA", (512, 512), (25, 60, 40, 255)) # Dark green leather
    draw = ImageDraw.Draw(book_img)
    draw.rectangle([16, 16, 496, 496], outline=(215, 180, 65, 255), width=8)
    draw.rectangle([30, 30, 482, 482], outline=(175, 140, 45, 255), width=2)
    # Embossed gold lettering
    draw.text((130, 80), "LEAVES OF GRASS", fill=(235, 205, 85, 255))
    draw.text((180, 140), "WALT WHITMAN", fill=(215, 180, 65, 255))
    # Floral embossed medallion
    draw.ellipse([186, 210, 326, 350], outline=(215, 180, 65, 255), width=4)
    draw.text((215, 270), "POEMS", fill=(235, 205, 85, 255))
    # Gale Boetticher's famous inscription
    draw.text((80, 400), "'To my other favorite W.W.", fill=(215, 195, 120, 255))
    draw.text((80, 435), "It's an honour working with you.' - G.B.", fill=(215, 195, 120, 255))
    book_img.save(os.path.join(output_dir, "leaves_of_grass.png"))

    # 14. Save Walter White Billboard (1024x512)
    sww_img = Image.new("RGBA", (1024, 512), (245, 245, 240, 255))
    draw = ImageDraw.Draw(sww_img)
    draw.rectangle([10, 10, 1014, 502], outline=(30, 90, 160, 255), width=14)
    # Blue top banner
    draw.rectangle([24, 24, 1000, 140], fill=(25, 95, 180, 255))
    draw.text((120, 55), "SAVE WALTER WHITE - DONATING IS HEALING!", fill=(255, 255, 255, 255))
    # Photo placeholder of Walter smiling in glasses
    draw.rectangle([60, 170, 320, 460], fill=(220, 225, 230, 255), outline=(25, 95, 180, 255), width=6)
    draw.text((105, 300), "[ WALT SR. ]", fill=(60, 80, 110, 255))
    draw.text((360, 180), "My dad is a high school chemistry teacher.", fill=(30, 30, 30, 255))
    draw.text((360, 220), "He has stage 3 lung cancer. He is our hero.", fill=(30, 30, 30, 255))
    draw.text((360, 270), "Please help us fund his medical treatment!", fill=(180, 25, 25, 255))
    draw.rectangle([350, 340, 960, 440], fill=(25, 150, 60, 255))
    draw.text((380, 370), "VISIT: WWW.SAVEWALTERWHITE.COM", fill=(255, 255, 255, 255))
    sww_img.save(os.path.join(output_dir, "save_walter_white_billboard.png"))

    # 15. Crosswalk Zebra Stripes Texture (512x512)
    cw_img = Image.new("RGBA", (512, 512), (45, 45, 48, 255)) # Dark asphalt
    draw = ImageDraw.Draw(cw_img)
    for sx in range(20, 500, 70):
        draw.rectangle([sx, 30, sx + 45, 482], fill=(240, 240, 240, 255))
    cw_img.save(os.path.join(output_dir, "crosswalk_stripes.png"))

    # 16. Fleetwood Bounder RV Side Body Stripes (1024x256)
    rv_stripe = Image.new("RGBA", (1024, 256), (228, 220, 204, 255)) # RV Off-white Cream
    draw = ImageDraw.Draw(rv_stripe)
    # Upper tan/caramel stripe
    draw.rectangle([0, 70, 1024, 125], fill=(195, 140, 75, 255))
    # Chrome accent pinstripe
    draw.rectangle([0, 128, 1024, 134], fill=(235, 235, 240, 255))
    # Lower dark chocolate / burnt orange stripe
    draw.rectangle([0, 137, 1024, 215], fill=(110, 50, 25, 255))
    # Classic 80s BOUNDER script badge
    draw.text((720, 155), "BOUNDER", fill=(240, 215, 160, 255))
    draw.text((880, 175), "FLEETWOOD", fill=(210, 185, 130, 255))
    rv_stripe.save(os.path.join(output_dir, "rv_stripe_bulletholes.png"))

    # 17. Iconic RV Door with 5 Bullet Holes & Silver Duct Tape (512x1024)
    rv_door = Image.new("RGBA", (512, 1024), (225, 218, 202, 255)) # Off-white camper door
    draw = ImageDraw.Draw(rv_door)
    # Dark rubber weatherstrip border
    draw.rectangle([12, 12, 500, 1012], outline=(35, 35, 38, 255), width=16)
    draw.rectangle([28, 28, 484, 996], outline=(160, 155, 142, 255), width=4)
    
    # Upper Camper Window with rounded corners and tinted glass
    draw.rounded_rectangle([60, 60, 452, 360], radius=30, fill=(35, 55, 65, 255), outline=(50, 50, 55, 255), width=12)
    draw.rounded_rectangle([80, 80, 432, 340], radius=20, fill=(20, 35, 45, 255))
    # Glass glare highlight
    draw.polygon([(100, 320), (140, 320), (320, 100), (280, 100)], fill=(80, 110, 130, 100))

    # Exterior horizontal body stripe continuing across door
    draw.rectangle([28, 440, 484, 495], fill=(195, 140, 75, 255))
    draw.rectangle([28, 498, 484, 504], fill=(235, 235, 240, 255))
    draw.rectangle([28, 507, 484, 580], fill=(110, 50, 25, 255))

    # Chrome RV Door Paddle Handle & Deadbolt
    draw.rectangle([40, 520, 110, 620], fill=(50, 50, 55, 255), outline=(30, 30, 30, 255), width=4)
    draw.rectangle([55, 535, 95, 595], fill=(210, 212, 215, 255))
    draw.ellipse([70, 600, 80, 610], fill=(20, 20, 20, 255)) # Keyhole

    # The 5 Emilio & Krazy-8 Bullet Holes Sealed with Silver Duct Tape
    bullet_hole_locs = [
        (220, 420),
        (330, 460),
        (260, 530),
        (380, 600),
        (290, 670)
    ]

    for bx, by in bullet_hole_locs:
        # Jagged charred bullet puncture underneath
        draw.ellipse([bx-24, by-24, bx+24, by+24], fill=(20, 15, 12, 255))
        draw.ellipse([bx-12, by-12, bx+12, by+12], fill=(5, 5, 5, 255))
        # Spalling fiberglass cracks
        for dx, dy in [(-30, -10), (32, 8), (-12, 28), (14, -26)]:
            draw.line([(bx, by), (bx+dx, by+dy)], fill=(80, 75, 65, 255), width=2)
        
        # Heavy-duty silver duct tape crisscross patches
        # Tape strip 1 (diagonal)
        draw.polygon([(bx-45, by-18), (bx+45, by+18), (bx+40, by+35), (bx-50, by-0)], fill=(185, 190, 195, 240), outline=(140, 145, 150, 255))
        # Tape strip 2 (cross diagonal)
        draw.polygon([(bx-18, by+45), (bx+18, by-45), (bx+35, by-40), (bx-0, by+50)], fill=(195, 200, 205, 240), outline=(150, 155, 160, 255))
        # Tape texture fiber lines
        draw.line([(bx-40, by-8), (bx+40, by+24)], fill=(215, 220, 225, 180), width=1)
        draw.line([(bx-10, by+40), (bx+24, by-40)], fill=(215, 220, 225, 180), width=1)

    rv_door.save(os.path.join(output_dir, "rv_bullet_holes_door.png"))

    # 18. Walter White's Chemistry Reaction Notebook (512x512)
    lab_notes = Image.new("RGBA", (512, 512), (248, 246, 238, 255)) # Cream graph/ruled paper
    draw = ImageDraw.Draw(lab_notes)
    # Margin & blue ruled horizontal lines
    draw.line([(60, 0), (60, 512)], fill=(225, 90, 90, 255), width=2) # Red margin line
    for ny in range(40, 500, 24):
        draw.line([(0, ny), (512, ny)], fill=(190, 215, 240, 160), width=1)

    # Handwritten reaction notes in neat dark blue ink
    draw.text((80, 18), "REDUCTION PATHWAY - EXPERIMENT 04", fill=(15, 25, 75, 255))
    draw.text((80, 46), "Precursor: P-2-P + Methylamine -> Imine intermediate", fill=(25, 45, 95, 255))
    draw.text((80, 70), "Catalyst: Aluminum-Mercury Amalgam (or HI / Red P)", fill=(25, 45, 95, 255))
    
    # Hand-drawn Chemical Structure: Benzene ring with ethylamine tail
    cx, cy = 190, 175
    # Hexagon benzene ring
    hex_pts = [
        (cx, cy - 40),
        (cx + 35, cy - 20),
        (cx + 35, cy + 20),
        (cx, cy + 40),
        (cx - 35, cy + 20),
        (cx - 35, cy - 20)
    ]
    draw.polygon(hex_pts, outline=(20, 30, 80, 255), width=3)
    draw.ellipse([cx-20, cy-20, cx+20, cy+20], outline=(20, 30, 80, 255), width=2) # Aromatic circle
    # Side chain bonds
    draw.line([(cx+35, cy), (cx+75, cy-15)], fill=(20, 30, 80, 255), width=3)
    draw.line([(cx+75, cy-15), (cx+115, cy)], fill=(20, 30, 80, 255), width=3)
    draw.line([(cx+115, cy), (cx+115, cy+35)], fill=(20, 30, 80, 255), width=3) # CH3
    draw.text((cx+120, cy+20), "CH3", fill=(20, 30, 80, 255))
    draw.line([(cx+115, cy), (cx+155, cy-15)], fill=(20, 30, 80, 255), width=3)
    draw.text((cx+160, cy-25), "NH-CH3", fill=(20, 30, 80, 255))
    
    # Key reaction parameters
    draw.text((80, 245), "PARAMETERS:", fill=(15, 25, 75, 255))
    draw.text((80, 270), "- Reflux Temperature: 82.4 deg C (STRICT CONTROL)", fill=(160, 25, 25, 255))
    draw.text((80, 294), "- Condenser water flow: steady, cold cycle", fill=(25, 45, 95, 255))
    draw.text((80, 318), "- Crystallization: Acetone wash at -10 deg C", fill=(25, 45, 95, 255))
    draw.text((80, 350), "TARGET PURITY: 99.1% (CHEMICALLY PURE)", fill=(15, 120, 45, 255))
    draw.text((80, 380), "Formula: C10H15N . HCl   MW: 185.7 g/mol", fill=(25, 45, 95, 255))
    draw.text((80, 420), "\"Respect the chemistry. The process is sacred.\"", fill=(15, 25, 75, 255))
    draw.text((360, 450), "- W.W.", fill=(15, 25, 75, 255))

    lab_notes.save(os.path.join(output_dir, "rv_lab_notes.png"))

    # 19. Chemical Hazard & Precursor Warning Sign (512x512)
    haz_sign = Image.new("RGBA", (512, 512), (255, 220, 30, 255)) # Vibrant safety yellow
    draw = ImageDraw.Draw(haz_sign)
    draw.rectangle([14, 14, 498, 498], outline=(20, 20, 20, 255), width=18)
    draw.rectangle([34, 34, 478, 120], fill=(20, 20, 20, 255))
    draw.text((105, 55), "DANGER / CAUTION", fill=(255, 220, 30, 255))
    draw.text((65, 150), "HAZARDOUS CHEMICAL VAPORS", fill=(20, 20, 20, 255))
    draw.text((70, 195), "PHOSPHINE & HYDROCHLORIC GAS", fill=(180, 20, 20, 255))
    draw.text((50, 250), "FULL RESPIRATOR & TYVEK SUIT REQUIRED", fill=(20, 20, 20, 255))
    # Gas mask icon circle
    draw.ellipse([180, 300, 332, 452], fill=(20, 20, 20, 255))
    draw.ellipse([200, 330, 240, 370], fill=(255, 220, 30, 255))
    draw.ellipse([272, 330, 312, 370], fill=(255, 220, 30, 255))
    draw.polygon([(240, 370), (272, 370), (256, 420)], fill=(255, 220, 30, 255))
    haz_sign.save(os.path.join(output_dir, "rv_chemical_hazard.png"))

    print("All enhanced textures generated successfully!")

if __name__ == "__main__":
    generate_textures("/home/ubuntu/BB/textures")
