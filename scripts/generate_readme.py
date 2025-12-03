import json
import os
from PIL import Image

# Configuration
DATA_FILE = 'data/certificates.json'
README_FILE = 'README.md'
THUMBNAIL_DIR = 'assets/thumbnails'
THUMBNAIL_SIZE = (400, 400) # Max dimension

def load_certificates():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def generate_thumbnail(cert):
    source_path = cert['filename']
    if source_path.lower().endswith('.pdf'):
        print(f"Skipping PDF thumbnail: {source_path}")
        return None
    
    filename = os.path.basename(source_path)
    thumb_path = os.path.join(THUMBNAIL_DIR, filename)
    
    # Ensure thumbnail directory exists
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)
    
    try:
        with Image.open(source_path) as img:
            img.thumbnail(THUMBNAIL_SIZE)
            img.save(thumb_path)
            return thumb_path
    except Exception as e:
        print(f"Error generating thumbnail for {source_path}: {e}")
        return None

def generate_readme(certificates):
    content = []
    
    # Header
    content.append("# Certificates — Sanket Talekar\n")
    content.append("A collection of my professional certificates and course completions from LinkedIn Learning and other providers.\n")
    content.append("![LinkedIn Learning](https://img.shields.io/badge/Platform-LinkedIn%20Learning-blue)\n")
    
    # Contact Info
    content.append("## Contact\n")
    content.append("- **Email**: [sanket.talekar@example.com](mailto:sanket.talekar@example.com)") # Placeholder, user didn't provide email
    content.append("- **LinkedIn**: [Sanket Talekar](https://www.linkedin.com/in/sanket-talekar/)\n") # Placeholder URL if not provided
    
    # Verification Instructions
    content.append("## Verification\n")
    content.append("Click on any certificate thumbnail to view the full-resolution image. For LinkedIn Learning certificates, you can verify the authenticity using the Certificate ID provided in the table (if applicable) or by visiting my LinkedIn profile.\n")

    # Summary Table
    content.append("## Summary\n")
    content.append("| # | Course Title | Provider | Completed On | Duration | Top Skills | Certificate ID | View |")
    content.append("|---|---|---|---|---|---|---|---|")
    
    for i, cert in enumerate(certificates, 1):
        view_link = f"[View]({cert['filename'].replace(' ', '%20')})"
        skills = ", ".join(cert['skills'][:3]) # Top 3 skills
        content.append(f"| {i} | {cert['title']} | {cert['provider']} | {cert['date']} | {cert['duration']} | {skills} | {cert.get('id', 'N/A')} | {view_link} |")
    
    content.append("\n")
    
    # Gallery
    content.append("## Gallery\n")
    content.append("<div align=\"center\">")
    
    for cert in certificates:
        thumb_path = os.path.join(THUMBNAIL_DIR, os.path.basename(cert['filename']))
        if cert['filename'].lower().endswith('.pdf'):
             # For PDFs, use a placeholder or just text if no thumbnail
             continue
        
        # Use relative paths for README
        rel_thumb_path = thumb_path.replace("\\", "/")
        rel_full_path = cert['filename'].replace("\\", "/")
        
        content.append(f'<a href="{rel_full_path}"><img src="{rel_thumb_path}" alt="Certificate: {cert["title"]} — Sanket Talekar — {cert["date"]}" width="200" style="margin: 10px;"></a>')
        
    content.append("</div>\n")
    
    # Generation Info
    content.append("## How this repo is generated\n")
    content.append("This repository is automatically generated using a Python script.\n")
    content.append("- **Data Source**: `data/certificates.json`")
    content.append("- **Script**: `scripts/generate_readme.py`")
    content.append("- **Thumbnails**: Generated using Pillow (PIL)\n")
    
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))

def main():
    print("Loading certificates...")
    certificates = load_certificates()
    
    print("Generating thumbnails...")
    for cert in certificates:
        generate_thumbnail(cert)
        
    print("Generating README...")
    generate_readme(certificates)
    
    print("Done!")

if __name__ == "__main__":
    main()
