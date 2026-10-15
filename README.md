# Tatvam Tools

A responsive commercial website and digital product catalog for an industrial manufacturing company specializing in flexible metal coolant pipes and magnetic bases.

## Features
- Multi-page corporate website including Home, Products Catalog, About Us, and Contact pages
- Comprehensive industrial product catalog with categorized galleries, technical specifications, and application details
- Component-based architecture with reusable navigation header and footer modules
- Interactive client inquiry contact form with client-side form validation
- Fully responsive design optimized across mobile, tablet, and desktop viewports

## Tech Stack
- HTML5 (Semantic elements, meta tags)
- CSS3 (CSS Grid, Flexbox, custom CSS variables)
- Vanilla JavaScript (ES6+, dynamic component loading, mobile menu toggles)
- Google Fonts (Inter & Outfit)

## How to Run
1. Open `index.html` directly in any web browser:
   - Double-click `index.html`, or
   - Right-click and choose your browser of choice.
2. For the best experience (loading modular components cleanly without browser CORS restrictions on `file://`), serve with a local web server:
   - Using Python:
     ```bash
     python -m http.server 8000
     ```
   - Using Node:
     ```bash
     npx serve .
     ```
3. Navigate to `http://localhost:8000`.

## Status
Complete
