import re
import json
import pandas as pd

# 1. Parse Excel data
filename = '260707-8 - Document Info on firstfinancialptyltd_sharepoint_com.xlsx'
df = pd.read_excel(filename)
df = df.fillna('')
records = df.to_dict(orient='records')
json_str = json.dumps(records)

# 2. Read HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 3. Add Tab Button
tab_button = """<button id="tab-version-report" class="main-tab" onclick="switchMainTab('version-report')">Version Report Non Excel files</button>
            <button id="tab-excel-report" class="main-tab" onclick="switchMainTab('excel-report')">Version Report Excel Files</button>"""
html = html.replace('<button id="tab-version-report" class="main-tab" onclick="switchMainTab(\'version-report\')">Version Report Non Excel files</button>', tab_button)

# 4. Update switchMainTab logic
tab_logic_old = """        function switchMainTab(tab) {
            document.getElementById('tab-dashboard').classList.remove('active');
            document.getElementById('tab-version-report').classList.remove('active');
            document.getElementById('dashboard-view').style.display = 'none';
            document.getElementById('version-report-view').style.display = 'none';"""

tab_logic_new = """        function switchMainTab(tab) {
            document.getElementById('tab-dashboard').classList.remove('active');
            document.getElementById('tab-version-report').classList.remove('active');
            document.getElementById('tab-excel-report').classList.remove('active');
            document.getElementById('dashboard-view').style.display = 'none';
            document.getElementById('version-report-view').style.display = 'none';
            document.getElementById('excel-report-view').style.display = 'none';"""

html = html.replace(tab_logic_old, tab_logic_new)

# 5. Extract and duplicate #version-report-view HTML block
view_match = re.search(r'(<!-- Version Report Non Excel files View -->\s*<div id="version-report-view".*?</div>\s*</div>\s*</div>)', html, flags=re.DOTALL)
if view_match:
    ff_view_html = view_match.group(1)
    excel_view_html = ff_view_html.replace('Version Report Non Excel files', 'Version Report Excel Files')
    excel_view_html = excel_view_html.replace('version-report-view', 'excel-report-view')
    excel_view_html = excel_view_html.replace('version-docs-count', 'excel-docs-count')
    excel_view_html = excel_view_html.replace('ff-sort', 'excel-sort')
    excel_view_html = excel_view_html.replace('handleFFSort', 'handleExcelSort')
    excel_view_html = excel_view_html.replace('version-table-body', 'excel-table-body')
    excel_view_html = excel_view_html.replace('ff-rows-per-page', 'excel-rows-per-page')
    excel_view_html = excel_view_html.replace('setFFPageSize', 'setExcelPageSize')
    excel_view_html = excel_view_html.replace('ff-pagination-controls', 'excel-pagination-controls')
    
    html = html.replace(ff_view_html, ff_view_html + '\n\n' + excel_view_html)
else:
    print("Could not find version-report-view block")

# 6. Extract and duplicate JS Logic
js_start_idx = html.find('let ffCurrentPage = 1;')
js_end_idx = html.find('</script>', js_start_idx)
if js_start_idx != -1 and js_end_idx != -1:
    ff_js = html[js_start_idx:js_end_idx]
    
    excel_js = ff_js.replace('ffCurrentPage', 'excelCurrentPage')
    excel_js = excel_js.replace('ffPageSize', 'excelPageSize')
    excel_js = excel_js.replace('ffSortColumn', 'excelSortColumn')
    excel_js = excel_js.replace('ffSortDirection', 'excelSortDirection')
    excel_js = excel_js.replace('ffFilteredData', 'excelFilteredData')
    excel_js = excel_js.replace('ffDocsData', 'excelDocsData')
    excel_js = excel_js.replace('setFFPageSize', 'setExcelPageSize')
    excel_js = excel_js.replace('renderFFTable', 'renderExcelTable')
    excel_js = excel_js.replace('handleFFSort', 'handleExcelSort')
    excel_js = excel_js.replace('ff-sort', 'excel-sort')
    excel_js = excel_js.replace('renderFFPagination', 'renderExcelPagination')
    excel_js = excel_js.replace('ff-pagination-controls', 'excel-pagination-controls')
    excel_js = excel_js.replace('version-table-body', 'excel-table-body')
    excel_js = excel_js.replace('version-docs-count', 'excel-docs-count')
    excel_js = excel_js.replace('Version Report Non Excel files', 'Version Report Excel Files')
    
    # We also need to insert `const excelDocsData = ...` and add auto-render
    auto_render = "renderFFTable(ffDocsData);"
    if auto_render in html:
        html = html.replace(auto_render, auto_render + "\n            renderExcelTable(excelDocsData);")
    else:
        print("Could not find auto_render call")
    
    # Append the js data
    js_payload = f"const excelDocsData = {json_str};\n\n"
    
    html = html[:js_start_idx] + js_payload + ff_js + "\n\n" + excel_js + html[js_end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done editing index.html")
