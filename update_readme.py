# Automated script to update wallpapers in readme
# AI genrated

import os
import re

def get_filesystem_images(path):
    images = {}
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    
    theme_dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]

    for theme in theme_dirs:
        theme_path = os.path.join(path, theme)
        if theme not in images:
            images[theme] = []
        for root, _, files in os.walk(theme_path):
            for file in files:
                if not file.startswith('.') and any(file.lower().endswith(ext) for ext in valid_extensions):
                    full_path = os.path.relpath(os.path.join(root, file), path)
                    # The key in the dictionary should be the top-level theme folder.
                    theme_key = full_path.split(os.path.sep)[0]
                    if theme_key not in images:
                         images[theme_key] = []
                    images[theme_key].append(full_path)
    return images

def generate_table(theme, images):
    if not images:
        return ""
    
    # Sort images for consistent ordering
    images.sort()
    
    table = f"## {theme}\n\n"
    table += "<table>\n"
    
    # Group images into rows of 3
    for i in range(0, len(images), 3):
        table += "  <tr>\n"
        for j in range(3):
            if i + j < len(images):
                image_path = images[i+j]
                # Alt text is the filename without extension
                alt_text = os.path.splitext(os.path.basename(image_path))[0]
                table += f'    <td><img src="{image_path}" alt="{alt_text}" width="400"/></td>\n'
        table += "  </tr>\n"
    
    table += "</table>\n"
    return table

def main():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        readme_content = ""

    header_match = re.search(r'### Tabular view of all wallpapers', readme_content)
    if header_match:
        header_end_index = header_match.start()
        header = readme_content[:header_end_index]
    else:
        first_table_match = re.search(r'##\s', readme_content)
        if first_table_match:
             header = readme_content[:first_table_match.start()]
        else:
             header = readme_content.split('### Tabular view of all wallpapers')[0] if '### Tabular view of all wallpapers' in readme_content else ""

    fs_images_by_theme = get_filesystem_images('.')

    all_themes = sorted(list(fs_images_by_theme.keys()))

    new_readme_content = header
    new_readme_content += "### Tabular view of all wallpapers\n\n"

    for theme in all_themes:
        new_readme_content += generate_table(theme, fs_images_by_theme.get(theme, [])) + "\n"

    with open('README.md.new', 'w', encoding='utf-8') as f:
        f.write(new_readme_content)

    os.rename('README.md.new', 'README.md')
    print("README.md updated successfully.")

if __name__ == '__main__':
    main()
