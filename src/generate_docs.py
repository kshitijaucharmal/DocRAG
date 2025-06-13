import importlib
import json
import types
import re

OPERATOR_METHODS = {
    "__add__",
    "__sub__",
    "__mul__",
    "__repr__",
}


import re


def parse_signature_and_description(doc: str):
    if not doc:
        return "No description", {}, "Unknown"

    # Split and clean lines
    lines = [line.strip() for line in doc.strip().splitlines() if line.strip()]
    if not lines:
        return "No description", {}, "Unknown"

    sig_line = lines[0]
    desc_lines = lines[1:]

    # Try to extract parameters and return type
    params = {}
    returns = "Unknown"

    sig_match = re.match(r".*?\((.*?)\)\s*(?:->\s*(.*))?", sig_line)
    if sig_match:
        param_str, return_str = sig_match.groups()
        if return_str:
            returns = return_str.strip()

        for p in param_str.split(","):
            p = p.strip()
            if not p or p == "self":
                continue
            if ":" in p:
                name, type_ = p.split(":", 1)
                params[name.strip()] = type_.strip()
            else:
                params[p] = "Any"

    description = " ".join(desc_lines).strip() if desc_lines else "No description"
    return description, params, returns


def analyze_module_native(module_name: str):
    mod = importlib.import_module(module_name)
    items = []

    for attr_name in dir(mod):
        if attr_name.startswith("_"):
            continue

        attr = getattr(mod, attr_name)

        if isinstance(attr, type):  # is a class
            cls = attr
            for method_name in dir(cls):
                if method_name.startswith("_") and method_name not in OPERATOR_METHODS:
                    continue
                method = getattr(cls, method_name)

                if not callable(method):
                    continue

                doc = getattr(method, "__doc__", "")
                if not doc or doc.strip() == "":
                    continue

                description, parameters, returns = parse_signature_and_description(doc)

                # Skip if no real description
                if description.strip().lower() in {"no description", ""}:
                    continue

                items.append(
                    {
                        "function": f"{cls.__name__}.{method_name}",
                        "description": description,
                        "parameters": parameters,
                        "returns": returns,
                    }
                )

    return items


if __name__ == "__main__":
    import sys

    module_name = sys.argv[1] if len(sys.argv) > 1 else "concept_forge"
    docs = analyze_module_native(module_name)
    print(json.dumps(docs, indent=2))
