#!/usr/bin/env python3

from pathlib import Path
from lxml import etree
from pyprojroot import here
import copy
from cairosvg import svg2png

# Dictionary mapping output filenames to a list of additional element IDs to remove for that variant.
logo_variants = {
    "pandionlabs_logo_color_bg_circle_white.svg": ["background-logo-full"],
    "pandionlabs_logo_color_bg_circle_transparent.svg": ["background-logo-full", "white-background"],
    "pandionlabs_logo_color_bg_full.svg": ["background-logo-circle"],  # Assumes white background is kept by default
    "pandionlabs_logo_black_white.svg": ["background-logo-full", "background-logo-circle"],
    "pandionlabs_logo_black_transparent.svg": ["background-logo-full", "background-logo-circle", "white-background"],
}

input_svg_path = here("editable/pandionlabs_logo_editable_simple.svg")
output_dir = here("export")

# IDs of elements to always remove from any generated version
ids_always_remove = ["__editable-text", "__circle-guide"]


def remove_elements_by_id(tree, ids_to_remove):
    """
    Removes elements with the specified IDs from the lxml etree.
    Modifies the tree in-place.
    """
    root = tree.getroot()
    for element_id in ids_to_remove:
        elements_found = root.xpath(f"//*[@id='{element_id}']")
        for elem in elements_found:
            parent = elem.getparent()
            parent.remove(elem)


def generate_variant(base_tree: etree.ElementTree, ids_remove=[]) -> etree.ElementTree:
    """
    Generates a specific variant of the SVG. by removing some elements
    """
    # Create a deep copy so to not modify the original tree
    new_tree = copy.deepcopy(base_tree)

    ids_remove.extend(ids_always_remove)
    remove_elements_by_id(new_tree, ids_remove)
    return new_tree


def main():
    output_dir.mkdir(parents=True, exist_ok=True)
    complete_tree = etree.parse(input_svg_path)
    for filename, ids_remove in logo_variants.items():
       variant = generate_variant(complete_tree, ids_remove)
       variant.write(output_dir / filename)

    # conver to png
    for filename in logo_variants.keys():
        path = output_dir / filename
        svg2png(url=str(path), write_to=str(path.with_suffix(".png")))

if __name__ == "__main__":
    main()
