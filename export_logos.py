from pathlib import Path
from lxml import etree
from pyprojroot import here
import copy
from cairosvg import svg2png
from dataclasses import dataclass, field
from typing import Literal

ids_always_remove = ["__circle-guide"]
small_remove_ids = ["pandion-text", "background-gradient-large", "white-background-large"]
large_remove_ids = ["background-gradient-small", "white-background-small"]

@dataclass
class LogoVariant:
    filename: str
    ids_remove: list[str] = field(default_factory=list())
    size: Literal["small", "large"] = "large"

    def __post_init__(self):
        self.ids_remove.extend(ids_always_remove)
        if self.size == "large":
            self.ids_remove.extend(large_remove_ids)
        elif self.size == "small":
            self.ids_remove.extend(small_remove_ids)

logo_variants_config: list[LogoVariant] = [
    # Small: no text square shape
    LogoVariant(filename="pandionlabs_logo_small_white.svg", ids_remove=["background-gradient-small"], size="small"),
    LogoVariant(filename="pandionlabs_logo_small_gradient.svg", ids_remove=["white-background-small"], size="small"),
    LogoVariant(filename="pandionlabs_logo_small_transparent.svg", ids_remove=["white-background-small", "background-gradient-small"], size="small"),
    LogoVariant(filename="pandionlabs_logo_small_black.svg", ids_remove=["white-background-small", "background-gradient-small", "background-logo-circle"], size="small"),
    # Large: text on the side, rectangle
    LogoVariant(filename="pandionlabs_logo_text_white.svg", ids_remove=["background-gradient-large"], size="large"),
    LogoVariant(filename="pandionlabs_logo_text_gradient.svg", ids_remove=["white-background-large"], size="large"),
    LogoVariant(filename="pandionlabs_logo_text_transparent.svg", ids_remove=["white-background-large", "background-gradient-large"], size="large"),
    LogoVariant(filename="pandionlabs_logo_text_black.svg", ids_remove=["white-background-large", "background-gradient-large", "background-logo-circle"], size="large"),
]

input_svg_path = here("editable/pandionlabs_logo_editable_simple.svg")
output_dir = here("export")

# IDs of elements to always remove from any generated version


def remove_elements_by_id(tree: etree.ElementTree, ids_to_remove: list[str]):
    """
    Removes elements with the specified IDs from the lxml etree.
    Modifies the tree in-place.
    """
    root = tree.getroot()
    for element_id in ids_to_remove:
        element_found = root.xpath(f"//*[@id='{element_id}']")
        assert len(element_found) == 1 , f"No element with ID '{element_id}' found {element_found}"
        elem = element_found[0]
        parent = elem.getparent()
        parent.remove(elem)


def generate_variant(base_tree: etree.ElementTree, logo_variant: LogoVariant) -> etree.ElementTree:
    """
    Generates a specific variant of the SVG by removing some elements.
    """
    # Create a deep copy so to not modify the original tree
    new_tree = copy.deepcopy(base_tree)
    remove_elements_by_id(new_tree, logo_variant.ids_remove)

    if logo_variant.size == "small":
        root = new_tree.getroot()
        root.set("viewBox", "0 0 1200 1200")
        root.set("width", "1200")
        root.set("height", "1200")

    return new_tree


def main():
    output_dir.mkdir(parents=True, exist_ok=True)

    complete_tree = etree.parse(str(input_svg_path))

    for logo_variant in logo_variants_config:
       variant_tree = generate_variant(complete_tree, logo_variant)
       output_file_path = output_dir / logo_variant.filename
       variant_tree.write(str(output_file_path))
       # Convert to PNG
       png_output_path = output_file_path.with_suffix(".png")
       svg2png(url=str(output_file_path), write_to=str(png_output_path))

if __name__ == "__main__":
    main()
