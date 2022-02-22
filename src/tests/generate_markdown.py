import json
import os
import os.path

with open("src/tests/data/manifest.json", "rb") as f:
    manifest = json.load(f)


markdown = """
# Content Profile / Linked Document Tests
"""

for case in manifest:
    markdown += f"""
## {case['id']}
### {case['type']}

*{case['description']}*

    """
    for attribute in ['raises']:
        if attribute in case:
            markdown += f"\n\n{attribute}: `{case[attribute]}`"

    for loadable in ['input', 'output', 'html_output', 'jsonld_output', 'nquads_output']:
        if loadable in case:
            markdown += f"\n\n {loadable}: [{case[loadable]}](src/tests/data/{case[loadable]})"

with open("documentation.md", "w") as f:
    f.write(markdown)