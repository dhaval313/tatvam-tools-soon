import os
import glob
import base64

# Base paths
BASE_DIR = r"d:\Project\Tatvam Tools"
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "products", "Coolant-Pipe")
OUTPUT_DIR = os.path.join(BASE_DIR, "Catalog pages")

# Price list mapping: (size, length) -> price (in INR)
# 2" prices are extrapolated since the PDF list starts from 4"
PRICES = {
    # 1/4" Coolant Pipe Prices
    ("1/4", "2"): 50.00,
    ("1/4", "4"): 60.00,
    ("1/4", "6"): 70.00,
    ("1/4", "8"): 80.00,
    ("1/4", "10"): 88.00,
    ("1/4", "12"): 99.00,
    ("1/4", "18"): 143.00,
    ("1/4", "24"): 198.00,
    
    # 3/8" Coolant Pipe Prices
    ("3/8", "2"): 50.00,
    ("3/8", "4"): 65.00,
    ("3/8", "6"): 80.00,
    ("3/8", "8"): 99.00,
    ("3/8", "10"): 119.00,
    ("3/8", "12"): 143.00,
    ("3/8", "18"): 214.00,
    ("3/8", "24"): 286.00,
    ("3/8", "30"): 357.00,
    
    # 1/2" Coolant Pipe Prices
    ("1/2", "2"): 55.00,
    ("1/2", "4"): 72.00,
    ("1/2", "6"): 99.00,
    ("1/2", "8"): 129.00,
    ("1/2", "10"): 169.00,
    ("1/2", "12"): 209.00,
    ("1/2", "18"): 297.00,
    ("1/2", "24"): 407.00,
    ("1/2", "30"): 484.00,
    
    # 3/4" Coolant Pipe Prices
    ("3/4", "12"): 426.00,
    ("3/4", "18"): 644.00,
    ("3/4", "24"): 856.00,
}

# Mapping size folder to display label
SIZE_LABELS = {
    "1-4": "1/4\"",
    "3-8": "3/8\"",
    "1-2": "1/2\"",
    "3-4": "3/4\""
}

# Helper to convert image files to Base64 data URLs
def get_base64_image(image_path_or_rel):
    if image_path_or_rel.startswith("../"):
        clean_path = image_path_or_rel.lstrip("../").replace("/", os.sep)
        abs_path = os.path.join(BASE_DIR, clean_path)
    else:
        abs_path = image_path_or_rel
        
    if not os.path.exists(abs_path):
        return image_path_or_rel
        
    ext = os.path.splitext(abs_path)[1].lower().replace(".", "")
    if ext in ["jpg", "jpeg"]:
        mime = "image/jpeg"
    elif ext == "png":
        mime = "image/png"
    else:
        mime = f"image/{ext}"
        
    with open(abs_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        
    return f"data:{mime};base64,{encoded}"

# CSS Styles template (shared across all pages)
CSS_TEMPLATE = """
        /* Design Tokens (Matching Tatvam Tools Site) */
        :root {
            --primary: #00a759;           /* Emerald Brand Green */
            --primary-dark: #008847;      /* Deep Forest Green */
            --primary-light: rgba(0, 167, 89, 0.08);
            --dark: #1a1a2e;              /* Midnight Dark Blue */
            --dark-light: #16213e;        /* Secondary Dark */
            --text-dark: #212529;
            --text-muted: #6c757d;
            --bg-light: #f8f9fa;
            --border-color: #dee2e6;
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --radius-md: 8px;
            --radius-sm: 4px;
        }

        /* Reset and Base Styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: #e9ecef;
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            line-height: 1.4;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        /* Non-Printable Utility Control Bar */
        .utility-bar {
            width: 210mm;
            background: var(--dark);
            color: white;
            padding: 12px 24px;
            border-radius: var(--radius-md);
            margin-bottom: 15px;
            box-shadow: var(--shadow-lg);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .utility-title {
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .utility-title span {
            color: var(--primary);
            font-weight: bold;
        }

        .print-btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 8px 18px;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 13px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: background-color 0.2s ease;
            text-decoration: none;
        }

        .print-btn:hover {
            background-color: var(--primary-dark);
        }

        .back-btn {
            background-color: transparent;
            color: #dee2e6;
            border: 1px solid var(--border-color);
            padding: 8px 18px;
            font-family: 'Outfit', sans-serif;
            font-weight: 500;
            font-size: 13px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .back-btn:hover {
            background-color: rgba(255,255,255,0.1);
            color: white;
        }

        /* A4 Page Container (Screen Representation) */
        .a4-page {
            width: 210mm;
            height: 297mm; /* Strictly fixed height to enforce single page */
            background: white;
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
            padding: 5mm 10mm; /* Reduced top/bottom padding to make room for footer */
            box-sizing: border-box;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden; /* Avoid overflow spilling */
        }

        /* Header Layout */
        .catalog-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid var(--primary);
            padding-bottom: 5px;
            margin-bottom: 6px;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-img {
            height: 38px;
            width: 38px;
            min-width: 38px;
            flex-shrink: 0;
            object-fit: contain;
        }

        .brand-info {
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }

        .brand-name {
            font-family: 'Outfit', sans-serif;
            font-size: 22px;
            font-weight: 800;
            color: var(--dark);
            letter-spacing: -0.5px;
            line-height: 1.1;
        }

        .brand-name span {
            color: var(--primary);
        }

        .brand-tagline {
            font-size: 8.5px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .contact-header-info {
            text-align: right;
            font-size: 9.5px;
            color: var(--text-dark);
            line-height: 1.3;
        }

        .contact-header-info strong {
            color: var(--dark);
        }

        .make-in-india-logo {
            height: 30px;
            margin-left: 10px;
            object-fit: contain;
        }

        .header-right {
            display: flex;
            align-items: center;
        }

        /* Product Title Banner */
        .product-title-bar {
            background: linear-gradient(135deg, var(--dark) 0%, var(--dark-light) 100%);
            color: white;
            padding: 6px 12px;
            border-radius: var(--radius-sm);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 5px solid var(--primary);
        }

        .product-title {
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .product-subtitle {
            font-size: 10px;
            color: var(--primary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Zig-Zag Rows Container */
        .zigzag-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex-grow: 1;
            margin-bottom: 4px;
        }

        /* Zig-Zag Row Definition */
        .zigzag-row {
            display: flex;
            align-items: center;
            gap: 24px;
            min-height: 210px;
        }

        /* Alternate directions for images and info */
        .zigzag-row:nth-child(even) {
            flex-direction: row-reverse;
        }

        /* Custom alignment for pure image row */
        .zigzag-row.images-only {
            justify-content: center;
            gap: 30px;
            min-height: auto;
            flex-direction: row !important;
        }

        /* Square Image Block (210px x 210px) */
        .image-block {
            width: 210px;
            height: 210px;
            background: var(--bg-light);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: var(--shadow-md);
            flex-shrink: 0;
        }

        .product-image {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        .info-block {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* Full width text block when no image */
        .info-block.full-width {
            width: 100%;
        }

        /* Section headers in columns (Bigger text) */
        .section-header {
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: var(--dark);
            border-bottom: 2px solid var(--primary);
            padding-bottom: 3px;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Specs table styled larger */
        .specs-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12.5px;
        }

        .specs-table tr {
            border-bottom: 1px solid var(--border-color);
        }

        .specs-table tr:last-child {
            border-bottom: none;
        }

        .specs-table td {
            padding: 5px 3px;
        }

        .specs-label {
            font-weight: 600;
            color: var(--dark);
            width: 38%;
        }

        .specs-value {
            color: var(--text-dark);
            width: 62%;
        }

        /* Title & Price Display Layout (Row 1 Info) */
        .title-price-wrapper {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .title-block-main {
            border-left: 4px solid var(--primary);
            padding-left: 12px;
        }

        .main-product-title {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 850;
            color: var(--dark);
            line-height: 1.2;
        }

        .main-product-subtitle {
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }


        .price-lbl-badge {
            background-color: var(--primary);
            color: white;
            font-size: 10px;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: var(--radius-sm);
            text-transform: uppercase;
        }

        /* Description & Features styling (Larger text) */
        .product-desc {
            font-size: 12.5px;
            color: var(--text-dark);
            line-height: 1.45;
            margin-bottom: 8px;
            text-align: justify;
        }

        .features-box {
            background: var(--primary-light);
            border-left: 2.5px solid var(--primary);
            padding: 8px 10px;
            border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        }

        .features-list {
            list-style-type: none;
            font-size: 12.5px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .features-list li {
            position: relative;
            padding-left: 14px;
            color: var(--text-dark);
        }

        .features-list li::before {
            content: "✓";
            color: var(--primary);
            font-weight: bold;
            position: absolute;
            left: 0;
        }

        /* Redesigned Bottom Info Card */
        .bottom-info-card {
            background-color: var(--bg-light);
            border: 1px solid var(--border-color);
            border-top: 3px solid var(--primary);
            border-radius: var(--radius-md);
            padding: 8px 12px;
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 16px;
            margin-top: 4px;
            box-shadow: var(--shadow-sm);
        }

        .bottom-card-col {
            display: flex;
            flex-direction: column;
        }

        .bottom-card-col.right-col {
            border-left: 1.5px solid var(--border-color);
            padding-left: 16px;
        }

        .bottom-card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 10.5px;
            font-weight: 700;
            color: var(--dark);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
        }

        .bottom-card-title::after {
            content: "";
            flex-grow: 1;
            height: 1px;
            background-color: var(--border-color);
            margin-left: 8px;
        }

        .bottom-card-terms {
            list-style-type: none;
            font-size: 10px;
            color: var(--text-dark);
            display: flex;
            flex-direction: column;
            gap: 3px;
        }

        .bottom-card-terms li {
            position: relative;
            padding-left: 10px;
            line-height: 1.35;
        }

        .bottom-card-terms li::before {
            content: "•";
            color: var(--primary);
            font-weight: bold;
            position: absolute;
            left: 0;
        }

        .bottom-card-contact {
            font-size: 10px;
            color: var(--text-dark);
            line-height: 1.35;
        }

        .bottom-card-contact strong {
            color: var(--dark);
        }

        .bottom-card-address {
            font-size: 10px;
            color: var(--text-dark);
            line-height: 1.35;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
        }

        .bottom-card-address strong {
            color: var(--dark);
        }

        .bottom-card-address .make-in-india-logo {
            height: 28px;
            width: auto;
            object-fit: contain;
        }

        .bottom-section {
            margin-top: 4px;
        }

        .footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 9px;
            color: var(--text-muted);
            margin-top: 4px;
            border-top: 1px solid var(--border-color);
            padding-top: 4px;
        }

        .footer-brand {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
        }

        /* Print Styles */
        @media print {
            body {
                background-color: white;
                padding: 0;
                margin: 0;
                width: 210mm;
                height: 297mm;
            }

            .no-print {
                display: none !important;
            }

            .a4-page {
                box-shadow: none;
                margin: 0;
                padding: 5mm 10mm;
                width: 210mm;
                height: 297mm;
                overflow: hidden;
            }
        }
"""

def generate_catalog_pages():
    # Make sure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generated_pages = []

    # Get Base64 for the logos
    logo_base64 = get_base64_image("../assets/images/logos/logo.png")
    make_in_india_base64 = get_base64_image("../assets/images/logos/make-in-india.png")

    # Get all sizes directories
    size_dirs = ["1-4", "3-8", "1-2", "3-4"]
    for size_dir in size_dirs:
        size_path = os.path.join(IMAGE_DIR, size_dir)
        if not os.path.exists(size_path):
            continue
        
        # Get all length folders in this size directory
        for length_dir in os.listdir(size_path):
            length_path = os.path.join(size_path, length_dir)
            if not os.path.isdir(length_path):
                continue
            
            if "x" not in length_dir:
                continue
            
            parts = length_dir.split("x")
            length = parts[1] # e.g. "12" or "2"
            size_raw = parts[0] # e.g. "1-4"
            size_display = SIZE_LABELS.get(size_raw, size_raw.replace("-", "/"))
            
            # Key for price lookup
            price_key_size = size_display.replace('"', '') # e.g. "1/4"
            price = PRICES.get((price_key_size, length), 0.0)
            
            # Get images in this folder
            images = [f for f in os.listdir(length_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            images.sort()
            
            if not images:
                print(f"Warning: No images found in {length_path}. Skipping.")
                continue
            
            # Convert all images to Base64 data URLs
            base64_images = []
            for img in images:
                img_rel = f"../assets/images/products/Coolant-Pipe/{size_dir}/{length_dir}/{img}"
                base64_images.append(get_base64_image(img_rel))
            
            # Build HTML content
            file_name = f"catalog_{size_raw}x{length}.html"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            
            html_content = build_page_html(size_raw, size_display, length, price, base64_images, logo_base64, make_in_india_base64)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            generated_pages.append({
                "file": file_name,
                "size": size_display,
                "length": f"{length}\"",
                "price": f"₹ {price:.2f}"
            })
            print(f"Generated: {file_name} (Self-contained Base64)")
            
    return generated_pages

def build_page_html(size_raw, size, length, price, images, logo_base64, make_in_india_base64):
    # Length calculation in mm
    try:
        mm_val = int(length) * 25
    except ValueError:
        mm_val = 300 # fallback

    # Determine size-specific bending angle footnote based on size_raw
    if "1-4" in size_raw:
        bending_footnote = "length size 195mm and above"
    elif "3-8" in size_raw:
        bending_footnote = "length size 240mm and above"
    elif "1-2" in size_raw:
        bending_footnote = "length size 300mm and above"
    elif "3-4" in size_raw:
        bending_footnote = "length size 450mm and above"
    else:
        bending_footnote = "length size 195mm and above"
        
    # Specs setup
    specs_html = f"""
                        <h3 class="section-header">Technical Specifications</h3>
                        <table class="specs-table">
                            <tr>
                                <td class="specs-label">Material</td>
                                <td class="specs-value">High-Quality Polypropylene (PP++)</td>
                            </tr>
                            <tr>
                                <td class="specs-label">Thread Connection</td>
                                <td class="specs-value">{size} BSP (Standard Pipe Thread)</td>
                            </tr>
                            <tr>
                                <td class="specs-label">Hose Length</td>
                                <td class="specs-value">{length}" Inches (~ {mm_val} mm)</td>
                            </tr>
                            <tr>
                                <td class="specs-label">Nozzle Options</td>
                                <td class="specs-value">Round Nozzle & Flat Nozzle</td>
                            </tr>
                            <tr>
                                <td class="specs-label">Bending Angle</td>
                                <td class="specs-value">360° Fully Flexible Bending Radius ({bending_footnote})</td>
                            </tr>
                        </table>
    """
    
    # Description setup
    desc_html = """
                        <h3 class="section-header">Product Description</h3>
                        <p class="product-desc">
                            Engineered from premium Acetal Copolymer (PP++), KRC® plastic coolant hoses offer exceptional chemical resistance to cutting oils, solvents, and emulsions. The modular segment design holds its exact position under fluid pressure with zero springback.
                        </p>
                        <div class="features-box">
                            <ul class="features-list">
                                <li>Targeted coolant placement reduces thermal wear.</li>
                                <li>Non-conductive properties are ideal for EDM machines.</li>
                            </ul>
                        </div>
    """

    # Build rows based on image count N
    rows_html = ""
    N = len(images)
    
    # Row 1 (Image 1 + Title/Price)
    img_1 = images[0] if N >= 1 else ""
    rows_html += f"""
                <!-- Row 1: Image 1 (Left) | Title & Price Box (Right) -->
                <div class="zigzag-row">
                    <div class="image-block">
                        <img src="{img_1}" alt="Plastic Coolant Pipe {size} x {length} - Primary view" class="product-image">
                    </div>
                    <div class="info-block title-price-wrapper">
                        <div class="title-block-main">
                            <h2 class="main-product-title">Plastic Flexible Coolant Pipe</h2>
                            <div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;">
                                <span class="main-product-subtitle">{size} Thread Size × {length}" Hose Length</span>
                                <span class="price-lbl-badge">KRC® Brand</span>
                            </div>
                        </div>
                    </div>
                </div>
    """
    
    # Row 2 (Image 2 + Specs Table)
    img_2 = images[1] if N >= 2 else ""
    if img_2:
        rows_html += f"""
                <!-- Row 2: Image 2 (Right) | Specs Table (Left) -->
                <div class="zigzag-row">
                    <div class="image-block">
                        <img src="{img_2}" alt="Plastic Coolant Pipe {size} x {length} - Technical Specifications view" class="product-image">
                    </div>
                    <div class="info-block">
                        {specs_html}
                    </div>
                </div>
        """
    else:
        rows_html += f"""
                <div class="zigzag-row">
                    <div class="info-block full-width">
                        {specs_html}
                    </div>
                </div>
        """
        
    # Row 3 (Image 3 + Description or Text-only Description)
    img_3 = images[2] if N >= 3 else ""
    if img_3:
        rows_html += f"""
                <!-- Row 3: Image 3 (Left) | Description & Advantages (Right) -->
                <div class="zigzag-row">
                    <div class="image-block">
                        <img src="{img_3}" alt="Plastic Coolant Pipe {size} x {length} - Application view" class="product-image">
                    </div>
                    <div class="info-block">
                        {desc_html}
                    </div>
                </div>
        """
    else:
        rows_html += f"""
                <!-- Row 3: Description & Advantages (Full width, text-only) -->
                <div class="zigzag-row" style="min-height: auto; padding: 10px 0;">
                    <div class="info-block full-width">
                        {desc_html}
                    </div>
                </div>
        """
        
    # Row 4 (Extra Images Centered Side-by-Side)
    extra_images = images[3:]
    if extra_images:
        images_html = ""
        for idx, img in enumerate(extra_images):
            images_html += f"""
                    <div class="image-block">
                        <img src="{img}" alt="Plastic Coolant Pipe {size} x {length} - Gallery view {idx+1}" class="product-image">
                    </div>"""
        
        rows_html += f"""
                <!-- Row 4: Extra Images Side-by-Side -->
                <div class="zigzag-row images-only">
                    {images_html}
                </div>
        """

    # Complete page HTML assembly
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catalog - {size} x {length}" Plastic Flexible Coolant Pipe | Tatvam Tools</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        {CSS_TEMPLATE}
    </style>
</head>
<body>

    <!-- Utility Bar (Visible on screen, hidden during printing) -->
    <div class="utility-bar no-print">
        <div class="utility-title">
            Catalog Preview: <span>{size} x {length}" Plastic Coolant Pipe</span>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="index.html" class="back-btn">
                ← Back to Dashboard
            </a>
            <button class="print-btn" onclick="downloadPDF()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Download A4 PDF
            </button>
        </div>
    </div>

    <!-- Printable A4 Sheet (Strictly One Page) -->
    <div class="a4-page">
        <div>
            <!-- Header -->
            <header class="catalog-header">
                <div class="logo-section">
                    <img src="{logo_base64}" alt="Tatvam Tools Logo" class="logo-img">
                    <div class="brand-info">
                        <span class="brand-name">Tatvam<span>™</span></span>
                        <span class="brand-tagline">Quality & Excellence</span>
                    </div>
                </div>
            </header>

            <!-- Product Title Banner -->
            <div class="product-title-bar">
                <h1 class="product-title">PLASTIC FLEXIBLE COOLANT PIPE</h1>
                <span class="product-subtitle">{size} THREAD × {length}" LENGTH</span>
            </div>

            <!-- Main Zig-Zag Content Container -->
            <div class="zigzag-container">
                {rows_html}
            </div>

            <!-- Bottom Info Card (Address & Contact) -->
            <div class="bottom-info-card">
                <div class="bottom-card-col">
                    <h4 class="bottom-card-title">Showroom Address</h4>
                    <div class="bottom-card-address">
                        <div>
                            <strong>Tatvam Tools</strong><br>
                            Showroom - 9, "Ram-Shyam" Apartment, Gondal Road,<br>
                            Opp. DMart, Rajkot - 360004, Gujarat, India
                        </div>
                        <img src="{make_in_india_base64}" alt="Make in India" class="make-in-india-logo">
                    </div>
                </div>
                <div class="bottom-card-col right-col">
                    <h4 class="bottom-card-title">Contact for Bulk Orders</h4>
                    <div class="bottom-card-contact">
                        <strong>TATVAM TOOLS</strong><br>
                        <strong>Email:</strong> sales@tatvamtools.com
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer Terms & Contact Section -->
        <footer class="bottom-section">
            <div class="footer-bar">
                <span class="footer-brand">Tatvam Tools Catalog © 2026</span>
                <span>Product Family: Plastic Flexible Coolant Pipes (KRC®)</span>
                <span>Page 1 of 1</span>
            </div>
        </footer>
    </div>

    <!-- html2pdf Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script>
        function downloadPDF() {{
            const btn = document.querySelector('.print-btn');
            const originalText = btn ? btn.innerHTML : "Download";
            if (btn) {{
                btn.innerHTML = "Generating PDF...";
                btn.style.opacity = "0.7";
                btn.style.pointerEvents = "none";
            }}

            const currentScrollY = window.scrollY;
            const currentScrollX = window.scrollX;
            window.scrollTo(0, 0);

            const element = document.querySelector('.a4-page');
            const opt = {{
                margin:       0,
                filename:     'catalog_{size_raw}x{length}.pdf',
                image:        {{ type: 'jpeg', quality: 0.98 }},
                html2canvas:  {{ scale: 2.5, useCORS: true, logging: false, scrollX: 0, scrollY: 0, windowWidth: 794 }},
                jsPDF:        {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
            }};

            return html2pdf().set(opt).from(element).save().then(() => {{
                window.scrollTo(currentScrollX, currentScrollY);
                if (btn) {{
                    btn.innerHTML = originalText;
                    btn.style.opacity = "1";
                    btn.style.pointerEvents = "auto";
                }}
            }}).catch(err => {{
                console.error("PDF generation failed:", err);
                window.scrollTo(currentScrollX, currentScrollY);
                if (btn) {{
                    btn.innerHTML = originalText;
                    btn.style.opacity = "1";
                    btn.style.pointerEvents = "auto";
                }}
                alert("Failed to generate PDF. Opening standard print window instead.");
                window.print();
            }});
        }}

        // Auto-download listener for window.open trigger
        window.addEventListener('load', () => {{
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('download') === 'true') {{
                setTimeout(() => {{
                    if (typeof html2pdf !== 'undefined') {{
                        downloadPDF().then(() => {{
                            setTimeout(() => {{
                                try {{
                                    window.close();
                                }} catch (e) {{
                                    console.error("Failed to close window:", e);
                                }}
                            }}, 1500);
                        }}).catch(err => {{
                            console.error("Auto-download failed:", err);
                            setTimeout(() => {{
                                try {{
                                    window.close();
                                }} catch (e) {{
                                    console.error("Failed to close window:", e);
                                }}
                            }}, 2000);
                        }});
                    }} else {{
                        setTimeout(() => {{ window.close(); }}, 1000);
                    }}
                }}, 500);
            }}
        }});
    </script>

</body>
</html>
"""
    return html


def generate_consolidated_catalog():
    print("Generating Consolidated 4-Page Catalog...")
    
    # Get Base64 for the logos
    logo_base64 = get_base64_image("../assets/images/logos/logo.png")
    make_in_india_base64 = get_base64_image("../assets/images/logos/make-in-india.png")

    pages_html = ""
    size_dirs = ["1-4", "3-8", "1-2", "3-4"]
    
    for page_idx, size_dir in enumerate(size_dirs):
        size_path = os.path.join(IMAGE_DIR, size_dir)
        if not os.path.exists(size_path):
            continue
            
        size_display = SIZE_LABELS.get(size_dir, size_dir.replace("-", "/"))
        
        # 1. Get available lengths by scanning the folders
        lengths = []
        for d in os.listdir(size_path):
            if os.path.isdir(os.path.join(size_path, d)) and "x" in d:
                len_str = d.split("x")[1]
                lengths.append(len_str)
        # Sort lengths numerically
        lengths.sort(key=lambda l: int(l))
        
        # 2. Get first 4 images from the 12" length folder
        len_12_dir = f"{size_dir}x12"
        len_12_path = os.path.join(size_path, len_12_dir)
        
        base64_images = []
        if os.path.exists(len_12_path):
            images = [f for f in os.listdir(len_12_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            images.sort()
            # Select first 4 images
            selected_images = images[:4]
            for img in selected_images:
                img_rel = f"../assets/images/products/Coolant-Pipe/{size_dir}/{len_12_dir}/{img}"
                base64_images.append(get_base64_image(img_rel))
        
        # If we couldn't find 4 images, fill with empty string
        while len(base64_images) < 4:
            base64_images.append("")
            
        # 3. Build specifications and description HTML
        if "1-4" in size_dir:
            bending_footnote = "length size 195mm and above"
        elif "3-8" in size_dir:
            bending_footnote = "length size 240mm and above"
        elif "1-2" in size_dir:
            bending_footnote = "length size 300mm and above"
        elif "3-4" in size_dir:
            bending_footnote = "length size 450mm and above"
        else:
            bending_footnote = "length size 195mm and above"
            
        nozzle_options = "Round Nozzle & Flat Nozzle"
            
        specs_html = f"""
                            <table class="specs-table">
                                <tr>
                                    <td class="specs-label">Material</td>
                                    <td class="specs-value">High-Quality Polypropylene (PP++)</td>
                                </tr>
                                <tr>
                                    <td class="specs-label">Thread Connection</td>
                                    <td class="specs-value">{size_display} BSP (Standard Pipe Thread)</td>
                                </tr>
                                <tr>
                                    <td class="specs-label">Nozzle Options</td>
                                    <td class="specs-value">{nozzle_options}</td>
                                </tr>
                                <tr>
                                    <td class="specs-label">Bending Angle</td>
                                    <td class="specs-value">360° Fully Flexible Bending Radius ({bending_footnote})</td>
                                </tr>
                            </table>
        """
        
        desc_html = """
                            <p class="product-desc">
                                Engineered from premium Acetal Copolymer (PP++), KRC® plastic coolant hoses offer exceptional chemical resistance to cutting oils, solvents, and emulsions. The modular segment design holds its exact position under fluid pressure with zero springback.
                            </p>
                            <div class="features-box">
                                <ul class="features-list">
                                    <li>Targeted coolant placement reduces thermal wear.</li>
                                    <li>Non-conductive properties are ideal for EDM machines.</li>
                                </ul>
                            </div>
        """
        
        # 4. Available lengths table rows HTML (Exactly 2 columns: Inches & Metric)
        table_rows_html = ""
        for len_val in lengths:
            mm_val = int(len_val) * 25
            table_rows_html += f"""
                                <tr>
                                    <td style="font-weight: 600; color: var(--dark);">{len_val}"</td>
                                    <td>~ {mm_val} mm</td>
                                </tr>
            """
            
        # 5. Build A4 page HTML for this thread size
        pages_html += f"""
        <!-- Page {page_idx + 1}: {size_display} Thread Size -->
        <div class="a4-page">
            <div style="display: flex; flex-direction: column; flex-grow: 1;">
                <!-- Header -->
                <header class="catalog-header">
                    <div class="logo-section">
                        <img src="{logo_base64}" alt="Tatvam Tools Logo" class="logo-img">
                        <div class="brand-info">
                            <span class="brand-name">Tatvam<span>™</span></span>
                            <span class="brand-tagline">Quality & Excellence</span>
                        </div>
                    </div>
                </header>

                <!-- Product Title Banner -->
                <div class="product-title-bar">
                    <h1 class="product-title">PLASTIC FLEXIBLE COOLANT PIPE</h1>
                    <span class="product-subtitle">CONSOLIDATED CATALOG - {size_display} THREAD SIZE</span>
                </div>

                <!-- Main Content Container (Zig-Zag Rows) -->
                <div class="zigzag-container">
                    <!-- Row 1: Image 1 Left, Specs Table Right -->
                    <div class="zigzag-row">
                        <div class="image-block">
                            <img src="{base64_images[0]}" alt="12 Model View 1" class="product-image">
                        </div>
                        <div class="info-block">
                            <h3 class="section-header" style="margin-top: 0;">Technical Specifications</h3>
                            {specs_html}
                        </div>
                    </div>

                    <!-- Row 2: Product Description & Features Left, Image 2 Right -->
                    <div class="zigzag-row">
                        <div class="image-block">
                            <img src="{base64_images[1]}" alt="12 Model View 2" class="product-image">
                        </div>
                        <div class="info-block">
                            <h3 class="section-header" style="margin-top: 0;">Product Description</h3>
                            {desc_html}
                        </div>
                    </div>

                    <!-- Row 3: Image 3 Left, Available Lengths Table Right -->
                    <div class="zigzag-row">
                        <div class="image-block">
                            <img src="{base64_images[2]}" alt="12 Model View 3" class="product-image">
                        </div>
                        <div class="info-block">
                            <h3 class="section-header" style="margin-top: 0;">Available Lengths</h3>
                            <table class="lengths-table">
                                <thead>
                                    <tr>
                                        <th>Hose Length (Inches)</th>
                                        <th>Hose Length (Metric)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {table_rows_html}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Row 4: Showroom Address & Contact Left, Image 4 Right -->
                    <div class="zigzag-row">
                        <div class="image-block">
                            <img src="{base64_images[3]}" alt="12 Model View 4" class="product-image">
                        </div>
                        <div class="info-block">
                            <div class="showroom-contact-box" style="border: 1px solid var(--border-color); border-top: 3px solid var(--primary); border-radius: var(--radius-md); padding: 8px 12px; background: var(--bg-light); box-shadow: var(--shadow-sm);">
                                <h4 class="section-header" style="margin-top: 0; font-size: 11px; border-bottom: none; padding-bottom: 0; margin-bottom: 2px;">Showroom Address</h4>
                                <div style="font-size: 9px; line-height: 1.3; color: var(--text-dark); margin-bottom: 6px;">
                                    <strong>Tatvam Tools</strong><br>
                                    Showroom - 9, "Ram-Shyam" Apartment, Gondal Road,<br>
                                    Opp. DMart, Rajkot - 360004, Gujarat, India
                                </div>
                                <h4 class="section-header" style="margin-top: 0; font-size: 11px; border-bottom: none; padding-bottom: 0; margin-bottom: 2px;">Bulk Orders Contact</h4>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 9px; color: var(--text-dark); font-weight: 600;">sales@tatvamtools.com</span>
                                    <img src="{make_in_india_base64}" alt="Make in India" style="height: 18px; width: auto; object-fit: contain;">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer Bar -->
            <footer class="footer-bar">
                <span class="footer-brand">Tatvam Tools Catalog © 2026</span>
                <span>Product Family: Plastic Flexible Coolant Pipes (KRC®)</span>
                <span>Page {page_idx + 1} of 4</span>
            </footer>
        </div>
        """
        
    # CSS Styles specifically for the consolidated catalog
    consolidated_css = """
    <style>
        /* Design Tokens */
        :root {
            --primary: #00a759;
            --primary-dark: #008847;
            --primary-light: rgba(0, 167, 89, 0.08);
            --dark: #1a1a2e;
            --dark-light: #16213e;
            --text-dark: #212529;
            --text-muted: #6c757d;
            --bg-light: #f8f9fa;
            --border-color: #dee2e6;
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --radius-md: 8px;
            --radius-sm: 4px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            line-height: 1.35;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        body:not(.printing-pdf) {
            background-color: #e9ecef;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
        }

        body.printing-pdf {
            background-color: white;
            padding: 0;
            margin: 0;
            width: 210mm !important;
            min-width: 210mm !important;
            overflow-x: hidden !important;
        }

        /* Non-Printable Utility Control Bar */
        .utility-bar {
            width: 210mm;
            background: var(--dark);
            color: white;
            padding: 12px 24px;
            border-radius: var(--radius-md);
            margin-bottom: 15px;
            box-shadow: var(--shadow-lg);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .utility-title {
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .utility-title span {
            color: var(--primary);
            font-weight: bold;
        }

        .print-btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 8px 18px;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 13px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: background-color 0.2s ease;
            text-decoration: none;
        }

        .print-btn:hover {
            background-color: var(--primary-dark);
        }

        .back-btn {
            background-color: transparent;
            color: #dee2e6;
            border: 1px solid var(--border-color);
            padding: 8px 18px;
            font-family: 'Outfit', sans-serif;
            font-weight: 500;
            font-size: 13px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .back-btn:hover {
            background-color: rgba(255,255,255,0.1);
            color: white;
        }

        /* A4 Page Container */
        .a4-page {
            width: 210mm;
            height: 297mm;
            background: white;
            box-sizing: border-box;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }

        body:not(.printing-pdf) .a4-page {
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
            padding: 5mm 10mm;
            margin-bottom: 20px;
        }

        body.printing-pdf .a4-page {
            height: 295mm !important; /* Slightly less than A4 height to prevent double page breaks */
            padding: 5mm 10mm;
            margin: 0 !important;
            box-shadow: none !important;
            page-break-after: always !important;
            page-break-inside: avoid !important;
        }

        body.printing-pdf .a4-page:last-child {
            page-break-after: avoid !important;
        }

        /* Header Layout */
        .catalog-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid var(--primary);
            padding-bottom: 5px;
            margin-bottom: 6px;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-img {
            height: 38px;
            width: 38px;
            min-width: 38px;
            flex-shrink: 0;
            object-fit: contain;
        }

        .brand-info {
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }

        .brand-name {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 800;
            color: var(--dark);
            line-height: 1.1;
        }

        .brand-name span {
            font-size: 10px;
            vertical-align: super;
            color: var(--primary);
        }

        .brand-tagline {
            font-size: 8px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-top: 1px;
        }

        /* Product Title Banner */
        .product-title-bar {
            background: linear-gradient(135deg, var(--dark) 0%, var(--dark-light) 100%);
            color: white;
            padding: 6px 12px;
            border-radius: var(--radius-sm);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 5px solid var(--primary);
        }

        .product-title {
            font-family: 'Outfit', sans-serif;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .product-subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 12px;
            font-weight: 600;
            color: var(--primary);
            letter-spacing: 0.5px;
        }

        /* Content Styles */
        .section-header {
            font-family: 'Outfit', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: var(--dark);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            padding-left: 8px;
            border-left: 3px solid var(--primary);
            display: flex;
            align-items: center;
        }

        /* Specs Table */
        .specs-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 8px;
        }

        .specs-label {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            padding: 4px 0;
            width: 35%;
            border-bottom: 1px solid var(--border-color);
        }

        .specs-value {
            font-size: 11px;
            font-weight: 500;
            color: var(--text-dark);
            padding: 4px 0;
            border-bottom: 1px solid var(--border-color);
        }

        /* Product Description */
        .product-desc {
            font-size: 10.5px;
            color: var(--text-dark);
            line-height: 1.35;
            margin-bottom: 6px;
        }

        .features-box {
            background-color: var(--bg-light);
            border-radius: var(--radius-sm);
            padding: 6px 10px;
            border-left: 2px solid var(--primary);
        }

        .features-list {
            list-style-type: none;
        }

        .features-list li {
            font-size: 10px;
            color: var(--text-dark);
            position: relative;
            padding-left: 10px;
            line-height: 1.35;
        }

        .features-list li::before {
            content: "•";
            color: var(--primary);
            font-weight: bold;
            position: absolute;
            left: 0;
        }

        /* Zig-Zag Rows Layout */
        .zigzag-container {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            flex-grow: 1;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .zigzag-row {
            display: flex;
            align-items: center;
            gap: 24px;
            min-height: 210px;
        }

        .zigzag-row:nth-child(even) {
            flex-direction: row-reverse;
        }

        .image-block {
            width: 280px;
            height: 210px;
            background: var(--bg-light);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: var(--shadow-md);
            flex-shrink: 0;
        }

        .product-image {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        .info-block {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* Lengths Table */
        .lengths-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11.5px;
        }

        .lengths-table th {
            background-color: var(--dark);
            color: white;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            text-align: left;
            padding: 4px 8px;
            border: 1px solid var(--border-color);
        }

        .lengths-table td {
            padding: 3px 8px;
            border: 1px solid var(--border-color);
            color: var(--text-dark);
        }

        .lengths-table tr:nth-child(even) {
            background-color: var(--bg-light);
        }

        .footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 9px;
            color: var(--text-muted);
            margin-top: 3px;
            border-top: 1px solid var(--border-color);
            padding-top: 3px;
        }

        .footer-brand {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
        }

        /* Print Styles */
        @media print {
            @page {
                size: A4;
                margin: 0;
            }

            body {
                background-color: white;
                padding: 0;
                margin: 0;
            }

            .no-print {
                display: none !important;
            }

            .a4-page {
                box-shadow: none;
                margin: 0 !important;
                padding: 5mm 10mm;
                width: 210mm;
                height: 295mm !important; /* Slightly less than A4 height to prevent double page breaks */
                overflow: hidden;
                page-break-after: always !important;
                page-break-inside: avoid !important;
            }

            .a4-page:last-child {
                page-break-after: avoid !important;
            }
        }
    </style>
    """

    # Combined HTML document structure
    combined_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consolidated Catalog - Plastic Flexible Coolant Pipes | Tatvam Tools</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    {consolidated_css}
</head>
<body>

    <!-- Utility Bar (Visible on screen, hidden during printing) -->
    <div class="utility-bar no-print">
        <div class="utility-title">
            Consolidated Catalog: <span>4-Page Thread-Size Summary</span>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="index.html" class="back-btn">
                ← Back to Dashboard
            </a>
            <button class="print-btn" onclick="downloadPDF()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Download Consolidated PDF (4 Pages)
            </button>
        </div>
    </div>

    <!-- Printable Catalog Content Wrapper (4 A4 Pages Stacked) -->
    <div id="catalog-content">
        {pages_html}
    </div>

    <!-- html2pdf Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script>
        function downloadPDF() {{
            const btn = document.querySelector('.print-btn');
            const originalText = btn.innerHTML;
            btn.innerHTML = "Generating 4-Page PDF...";
            btn.style.opacity = "0.7";
            btn.style.pointerEvents = "none";

            const currentScrollY = window.scrollY;
            const currentScrollX = window.scrollX;
            window.scrollTo(0, 0);

            // Add print-ready class to body to prevent margins and shadow offset issues
            document.body.classList.add('printing-pdf');

            const element = document.getElementById('catalog-content');
            const opt = {{
                margin:       0,
                filename:     'tatvam_tools_consolidated_catalog.pdf',
                image:        {{ type: 'jpeg', quality: 0.98 }},
                html2canvas:  {{ scale: 2.2, useCORS: true, logging: false, scrollX: 0, scrollY: 0, windowWidth: 794 }},
                jsPDF:        {{ unit: 'mm', format: 'a4', orientation: 'portrait' }},
                pagebreak:    {{ mode: ['css'] }}
            }};

            return html2pdf().set(opt).from(element).save().then(() => {{
                document.body.classList.remove('printing-pdf');
                window.scrollTo(currentScrollX, currentScrollY);
                btn.innerHTML = originalText;
                btn.style.opacity = "1";
                btn.style.pointerEvents = "auto";
            }}).catch(err => {{
                console.error("PDF generation failed:", err);
                document.body.classList.remove('printing-pdf');
                window.scrollTo(currentScrollX, currentScrollY);
                btn.innerHTML = originalText;
                btn.style.opacity = "1";
                btn.style.pointerEvents = "auto";
                alert("Failed to generate PDF. Opening standard print window instead.");
                window.print();
            }});
        }}
    </script>

</body>
</html>
"""
    output_path = os.path.join(OUTPUT_DIR, "consolidated_catalog.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(combined_html)
    print(f"Generated Consolidated Catalog: {output_path}")


def generate_dashboard(pages):
    # Sort pages by size (1/4, 3/8, 1/2, 3/4) and then by length (numeric)
    def parse_length(l_str):
        try:
            return int(l_str.replace('"', ''))
        except ValueError:
            return 0
            
    def parse_size(s_str):
        # returns sort weight
        weights = {"1/4\"": 1, "3/8\"": 2, "1/2\"": 3, "3/4\"": 4}
        return weights.get(s_str, 5)

    sorted_pages = sorted(pages, key=lambda p: (parse_size(p["size"]), parse_length(p["length"])))
    
    # Group by size
    grouped = {}
    for p in sorted_pages:
        size = p["size"]
        if size not in grouped:
            grouped[size] = []
        grouped[size].append(p)
        
    # Generate HTML content for index
    groups_html = ""
    for size, items in grouped.items():
        cards_html = ""
        for item in items:
            cards_html += f"""
                <a href="{item['file']}" class="catalog-card">
                    <div class="card-len-badge">{item['length']}</div>
                    <div class="card-title">Coolant Pipe {size} x {item['length']}</div>
                    <div class="card-footer">
                        <span>View Catalog</span>
                        <svg class="arrow-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </div>
                </a>
            """
            
        groups_html += f"""
        <div class="size-group">
            <h2 class="size-group-title">{size} Thread Size Configurations</h2>
            <div class="cards-grid">
                {cards_html}
            </div>
        </div>
        """
        
    files_js_array = ", ".join(f"'{p['file']}'" for p in sorted_pages)

    dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tatvam Tools - Catalog Dashboard</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #00a759;
            --primary-dark: #008847;
            --dark: #1a1a2e;
            --dark-light: #16213e;
            --text-dark: #212529;
            --text-muted: #6c757d;
            --bg-light: #f8f9fa;
            --border-color: #dee2e6;
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --radius-md: 8px;
            --radius-sm: 4px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: #f1f3f5;
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            padding: 40px 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Header Style */
        .dashboard-header {{
            background: linear-gradient(135deg, var(--dark) 0%, var(--dark-light) 100%);
            color: white;
            padding: 30px 40px;
            border-radius: var(--radius-md);
            border-bottom: 5px solid var(--primary);
            box-shadow: var(--shadow-lg);
            margin-bottom: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .brand-section {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}

        .brand-name {{
            font-family: 'Outfit', sans-serif;
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}

        .brand-name span {{
            color: var(--primary);
        }}

        .brand-tagline {{
            font-size: 11px;
            color: #dee2e6;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}

        .dashboard-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 600;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-align: right;
        }}

        /* Size Group & Cards */
        .size-group {{
            margin-bottom: 35px;
        }}

        .size-group-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 15px;
            padding-bottom: 6px;
            border-bottom: 2px solid var(--border-color);
            position: relative;
        }}

        .size-group-title::after {{
            content: "";
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 60px;
            height: 2px;
            background-color: var(--primary);
        }}

        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 20px;
        }}

        .catalog-card {{
            background: white;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 20px;
            text-decoration: none;
            color: var(--text-dark);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
            position: relative;
            box-shadow: var(--shadow-md);
            min-height: 110px;
        }}

        .catalog-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary);
        }}

        .card-len-badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            background-color: var(--primary-light);
            color: var(--primary-dark);
            font-size: 10px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: var(--radius-sm);
            text-transform: uppercase;
        }}

        .card-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 10px;
            margin-top: 10px;
        }}

        .card-footer {{
            border-top: 1px solid var(--border-color);
            padding-top: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
        }}

        .catalog-card:hover .card-footer {{
            color: var(--primary);
        }}

        .catalog-card .arrow-icon {{
            transition: transform 0.2s ease, stroke 0.2s ease;
            stroke: var(--text-muted);
        }}

        .catalog-card:hover .arrow-icon {{
            transform: translateX(4px);
            stroke: var(--primary);
        }}

        .consolidated-btn {{
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 8px 16px;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 13px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            text-decoration: none;
            transition: background-color 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }}

        .consolidated-btn:hover {{
            background-color: var(--primary-dark);
            color: white;
        }}

        footer {{
            text-align: center;
            padding-top: 30px;
            margin-top: 50px;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 13px;
        }}
    </style>
</head>
<body>

    <div class="container">
        <!-- Header -->
        <header class="dashboard-header">
            <div class="brand-section">
                <h1 class="brand-name">Tatvam<span>™</span> Tools</h1>
                <span class="brand-tagline">Quality & Excellence</span>
            </div>
            <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
                <h2 class="dashboard-title">Plastic Coolant Pipe Catalogs</h2>
                <div style="display: flex; gap: 10px;">
                    <a href="consolidated_catalog.html" class="consolidated-btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                        Straight Pipe Catalog (4 Pages)
                    </a>
                    <a href="consolidated_y_catalog.html" class="consolidated-btn" style="background-color: var(--dark-light);">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                        Y-Type Pipe Catalog (3 Pages)
                    </a>
                </div>
            </div>
        </header>

        <!-- Main Cards Section -->
        {groups_html}

        <!-- Footer -->
        <footer>
            <p>Tatvam Tools © 2026. All rights reserved.</p>
        </footer>
    </div>

</body>
</html>
"""
    
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    print(f"Generated Catalog Dashboard: {index_path}")

if __name__ == "__main__":
    print("Starting Multi-page Catalog Generation (Base64 + Direct PDF Download)...")
    pages = generate_catalog_pages()
    generate_consolidated_catalog()
    generate_dashboard(pages)
    print(f"Generation Complete! Total pages generated: {len(pages)}")
