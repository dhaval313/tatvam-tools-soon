import os
import base64

# Base paths
BASE_DIR = r"d:\Project\Tatvam Tools"
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "products", "Y-Coolant-Pipe")
OUTPUT_DIR = os.path.join(BASE_DIR, "Catalog pages")

SIZE_LABELS = {
    "1-4": "1/4\"",
    "3-8": "3/8\"",
    "1-2": "1/2\""
}

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

def generate_consolidated_y_catalog():
    print("Generating Consolidated 3-Page Y-Coolant Pipe Catalog...")
    
    # Get Base64 for the logos
    logo_base64 = get_base64_image("../assets/images/logos/logo.png")
    make_in_india_base64 = get_base64_image("../assets/images/logos/make-in-india.png")

    pages_html = ""
    size_dirs = ["1-4", "3-8", "1-2"]
    
    # Pre-defined configurations matching specifications
    configs = {
        "1-4": {
            "lengths": ["6", "12", "12 (6x6x6)", "18"],
            "bending_footnote": "length size 195mm and above",
            "folder_name": "Y - 1-4x12"
        },
        "3-8": {
            "lengths": ["6", "12", "12 (6x6x6)", "18"],
            "bending_footnote": "length size 240mm and above",
            "folder_name": "Y - 3-8x12"
        },
        "1-2": {
            "lengths": ["12", "18"],
            "bending_footnote": "length size 300mm and above",
            "folder_name": "Y - 1-2x12"
        }
    }
    
    for page_idx, size_dir in enumerate(size_dirs):
        size_path = os.path.join(IMAGE_DIR, size_dir)
        if not os.path.exists(size_path):
            continue
            
        size_display = SIZE_LABELS.get(size_dir, size_dir.replace("-", "/"))
        config = configs[size_dir]
        
        # 1. Get first 4 images from the 12" length folder
        len_12_dir = config["folder_name"]
        len_12_path = os.path.join(size_path, len_12_dir)
        
        base64_images = []
        if os.path.exists(len_12_path):
            images = [f for f in os.listdir(len_12_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            images.sort()
            # Select first 4 images
            selected_images = images[:4]
            for img in selected_images:
                img_rel = f"../assets/images/products/Y-Coolant-Pipe/{size_dir}/{len_12_dir}/{img}"
                base64_images.append(get_base64_image(img_rel))
        
        # If we couldn't find 4 images, fill with empty string
        while len(base64_images) < 4:
            base64_images.append("")
            
        # 2. Build specifications and description HTML
        bending_footnote = config["bending_footnote"]
        nozzle_options = "Dual Output (Round / Flat Nozzles)"
            
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
                                Engineered from premium Acetal Copolymer (PP++), KRC® plastic Y-coolant hoses divide a single source stream into two flexible outlets for dual-target precision cooling. The modular segments hold their exact position under pressure with zero springback.
                            </p>
                            <div class="features-box">
                                <ul class="features-list">
                                    <li>Dual output nozzles cool two operations simultaneously.</li>
                                    <li>Targeted dual coolant placement reduces heat and tool wear.</li>
                                    <li>Non-conductive properties are ideal for electrical discharge (EDM) machines.</li>
                                </ul>
                            </div>
        """
        
        # 3. Available lengths table rows HTML
        table_rows_html = ""
        for len_val in config["lengths"]:
            # Handle special length description like "12 (6x6x6)"
            if "(" in len_val:
                mm_val = "~ 300 mm"
            else:
                mm_val = f"~ {int(len_val) * 25} mm"
            table_rows_html += f"""
                                <tr>
                                    <td style="font-weight: 600; color: var(--dark);">{len_val}"</td>
                                    <td>{mm_val}</td>
                                </tr>
            """
            
        # 4. Build A4 page HTML for this thread size
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
                    <h1 class="product-title">PLASTIC Y-COOLANT PIPE</h1>
                    <span class="product-subtitle">CONSOLIDATED CATALOG - {size_display} THREAD SIZE</span>
                </div>

                <!-- Main Content Container (Zig-Zag Rows) -->
                <div class="zigzag-container">
                    <!-- Row 1: Image 1 Left, Specs Table Right -->
                    <div class="zigzag-row">
                        <div class="image-block">
                            <img src="{base64_images[0]}" alt="Model View 1" class="product-image">
                        </div>
                        <div class="info-block">
                            <h3 class="section-header" style="margin-top: 0;">Technical Specifications</h3>
                            {specs_html}
                        </div>
                    </div>

                    <!-- Row 2: Product Description & Features Left, Image 2 Right -->
                    <div class="zigzag-row">
                        <div class="image-block">
                            <img src="{base64_images[1]}" alt="Model View 2" class="product-image">
                        </div>
                        <div class="info-block">
                            <h3 class="section-header" style="margin-top: 0;">Product Description</h3>
                            {desc_html}
                        </div>
                    </div>

                    <!-- Row 3: Image 3 Left, Available Lengths Table Right -->
                    <div class="zigzag-row">
                        <div class="image-block">
                            <img src="{base64_images[2]}" alt="Model View 3" class="product-image">
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
                            <img src="{base64_images[3]}" alt="Model View 4" class="product-image">
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
                <span>Product Family: Plastic Y-Coolant Pipes (KRC®)</span>
                <span>Page {page_idx + 1} of 3</span>
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
            padding: 0 !important;
            margin: 0 !important;
            display: block !important;
            text-align: left !important;
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
            height: 295mm !important;
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
            width: 300px;
            flex-shrink: 0;
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
            width: 250px;
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
            font-family: 'Outfit', sans-serif;
            font-size: 12px;
            font-weight: 600;
            color: var(--primary);
            letter-spacing: 0.5px;
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
                padding: 0 !important;
                margin: 0 !important;
                width: 210mm !important;
            }

            .no-print {
                display: none !important;
            }

            .a4-page {
                box-shadow: none;
                margin: 0 !important;
                padding: 5mm 10mm;
                width: 210mm;
                height: 295mm !important;
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
    <title>Consolidated Catalog - Plastic Y-Coolant Pipes | Tatvam Tools</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    {consolidated_css}
</head>
<body>

    <!-- Utility Bar (Visible on screen, hidden during printing) -->
    <div class="utility-bar no-print">
        <div class="utility-title">
            Consolidated Catalog: <span>3-Page Thread-Size Summary (Y-Type)</span>
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
                Download Consolidated PDF (3 Pages)
            </button>
        </div>
    </div>

    <!-- Printable Catalog Content Wrapper (3 A4 Pages Stacked) -->
    <div id="catalog-content">
        {pages_html}
    </div>

    <!-- html2pdf Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script>
        function downloadPDF() {{
            const btn = document.querySelector('.print-btn');
            const originalText = btn.innerHTML;
            btn.innerHTML = "Generating 3-Page PDF...";
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
                filename:     'tatvam_tools_consolidated_y_catalog.pdf',
                image:        {{ type: 'jpeg', quality: 0.98 }},
                html2canvas:  {{ scale: 2.2, useCORS: true, logging: false, scrollX: 0, scrollY: 0, windowWidth: element.offsetWidth }},
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
    
    output_path = os.path.join(OUTPUT_DIR, "consolidated_y_catalog.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(combined_html)
    print(f"Generated Consolidated Y-Catalog: {output_path}")

if __name__ == "__main__":
    generate_consolidated_y_catalog()
