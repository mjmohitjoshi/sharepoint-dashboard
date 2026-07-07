import re
import json
import pandas as pd

# Load data
df = pd.read_excel('FF doc report.xlsx')
df = df.fillna('')
records = df.to_dict(orient='records')
json_str = json.dumps(records)

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the upload button and input
html = re.sub(
    r'<div class="filters-bar glass-panel" [^>]*>\s*<label for="ff-upload-input"[^>]*>.*?Upload FF doc report\.xlsx\s*</label>\s*<input type="file" id="ff-upload-input"[^>]*>\s*</div>',
    '',
    html,
    flags=re.DOTALL
)

# 2. Add the JS payload right before <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> or at the top of the JS block.
# Wait, let's just insert it before `function switchMainTab`
js_payload = f"""
        const ffDocsData = {json_str};
        
        // Auto-render when data is loaded
        window.addEventListener('DOMContentLoaded', () => {{
            renderFFTable(ffDocsData);
        }});
"""

html = html.replace('// Tab Switching Logic', js_payload + '\n\n        // Tab Switching Logic')

# 3. Modify `switchMainTab` to render the table if we want, but it's already rendered on load!
# Let's remove the "Awaiting file upload..." text from the HTML body so it doesn't flash.
html = html.replace(
    '<td colspan="8" style="text-align: center; color: var(--text-muted); padding: 3rem 0;"><i class="fa-regular fa-folder-open" style="font-size: 2.5rem; margin-bottom: 1rem; display: block;"></i>Awaiting file upload...</td>',
    '<td colspan="8" style="text-align: center; color: var(--text-muted); padding: 3rem 0;"><i class="fa-solid fa-spinner fa-spin" style="font-size: 2.5rem; margin-bottom: 1rem; display: block;"></i>Loading data...</td>'
)

# 4. Remove the `handleFFFileUpload` function entirely since we don't need it.
html = re.sub(r'// Excel Upload Logic for FF Doc Report.*?function renderFFTable', 'function renderFFTable', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
