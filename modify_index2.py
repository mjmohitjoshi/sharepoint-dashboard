import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Rename Tabs
html = html.replace('FF Doc Report', 'Version Report Non Excel files')
html = html.replace('tab-ff-report', 'tab-version-report')
html = html.replace("switchMainTab('ff-report')", "switchMainTab('version-report')")
html = html.replace('ff-report-view', 'version-report-view')
html = html.replace('ff-docs-count', 'version-docs-count')
html = html.replace('ff-table-body', 'version-table-body')

# 2. Add Sort Headers
header_replacement = """
                        <tr>
                            <th onclick="handleFFSort('Name')">Document Name <span id="ff-sort-Name"><i class="fa-solid fa-sort"></i></span></th>
                            <th onclick="handleFFSort('Site')">Site <span id="ff-sort-Site"><i class="fa-solid fa-sort"></i></span></th>
                            <th onclick="handleFFSort('List')">List <span id="ff-sort-List"><i class="fa-solid fa-sort"></i></span></th>
                            <th onclick="handleFFSort('Version number')">Version number <span id="ff-sort-Version number"><i class="fa-solid fa-sort"></i></span></th>
                            <th onclick="handleFFSort('Size (MB)')">Size (MB) <span id="ff-sort-Size (MB)"><i class="fa-solid fa-sort"></i></span></th>
                            <th onclick="handleFFSort('Total size for all versions (MB)')">Total size (MB) <span id="ff-sort-Total size for all versions (MB)"><i class="fa-solid fa-sort"></i></span></th>
                        </tr>
"""
html = re.sub(r'<tr>\s*<th>Document Name.*?<th>Total size \(MB\)</th>\s*</tr>', header_replacement.strip(), html, flags=re.DOTALL)

# 3. Add Pagination Controls HTML
footer_html = """
            <!-- Table Pagination and Footer -->
            <div class="table-footer">
                <div>
                    <span>Show </span>
                    <select id="ff-rows-per-page" class="select-filter"
                        style="padding: 0.3rem 0.5rem; min-width: auto; display: inline-block; margin: 0 0.5rem;"
                        onchange="setFFPageSize(this.value)">
                        <option value="10">10</option>
                        <option value="25" selected>25</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                        <option value="all">All</option>
                    </select>
                    <span>rows per page</span>
                </div>
                <div class="pagination" id="ff-pagination-controls">
                    <!-- Pagination buttons generated dynamically -->
                </div>
            </div>
        </div>
"""
html = html.replace('                </table>\n            </div>\n        </div>', '                </table>\n            </div>\n' + footer_html)

# 4. Replace JS Logic
js_replacement = """
        let ffCurrentPage = 1;
        let ffPageSize = 25;
        let ffSortColumn = '';
        let ffSortDirection = 'asc';
        let ffFilteredData = [];

        function setFFPageSize(size) {
            ffPageSize = size === 'all' ? ffDocsData.length : parseInt(size);
            ffCurrentPage = 1;
            renderFFTable();
        }

        function handleFFSort(column) {
            if (ffSortColumn === column) {
                ffSortDirection = ffSortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                ffSortColumn = column;
                ffSortDirection = 'asc';
            }

            // Reset sort icons
            document.querySelectorAll('[id^="ff-sort-"]').forEach(el => {
                el.innerHTML = '<i class="fa-solid fa-sort"></i>';
            });

            // Set active sort icon
            const icon = ffSortDirection === 'asc' ? '<i class="fa-solid fa-sort-up"></i>' : '<i class="fa-solid fa-sort-down"></i>';
            const sortSpan = document.getElementById('ff-sort-' + column);
            if(sortSpan) sortSpan.innerHTML = icon;

            ffFilteredData.sort((a, b) => {
                let valA = a[column];
                let valB = b[column];
                
                if (column === 'Site') {
                    valA = a.Site || (a.Location ? (a.Location.match(/\\/sites\\/([^\\/]+)/i) || [])[1] : '') || '';
                    valB = b.Site || (b.Location ? (b.Location.match(/\\/sites\\/([^\\/]+)/i) || [])[1] : '') || '';
                }

                if (valA === undefined || valA === null) valA = '';
                if (valB === undefined || valB === null) valB = '';

                if (typeof valA === 'string') valA = valA.toLowerCase();
                if (typeof valB === 'string') valB = valB.toLowerCase();

                if (valA < valB) return ffSortDirection === 'asc' ? -1 : 1;
                if (valA > valB) return ffSortDirection === 'asc' ? 1 : -1;
                return 0;
            });

            renderFFTable();
        }

        function renderFFPagination() {
            const controls = document.getElementById('ff-pagination-controls');
            controls.innerHTML = '';

            const totalPages = Math.ceil(ffFilteredData.length / ffPageSize);
            if (totalPages <= 1) return;

            const prevBtn = document.createElement('button');
            prevBtn.className = 'page-btn';
            prevBtn.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
            prevBtn.disabled = ffCurrentPage === 1;
            prevBtn.onclick = () => { if (ffCurrentPage > 1) { ffCurrentPage--; renderFFTable(); } };
            controls.appendChild(prevBtn);

            let startPage = Math.max(1, ffCurrentPage - 2);
            let endPage = Math.min(totalPages, startPage + 4);
            if (endPage - startPage < 4) {
                startPage = Math.max(1, endPage - 4);
            }

            if (startPage > 1) {
                const btn = document.createElement('button');
                btn.className = 'page-btn';
                btn.innerText = '1';
                btn.onclick = () => { ffCurrentPage = 1; renderFFTable(); };
                controls.appendChild(btn);
                if (startPage > 2) {
                    const dots = document.createElement('span');
                    dots.innerText = '...';
                    dots.style.padding = '0.5rem';
                    dots.style.color = 'var(--text-muted)';
                    controls.appendChild(dots);
                }
            }

            for (let i = startPage; i <= endPage; i++) {
                const btn = document.createElement('button');
                btn.className = `page-btn ${i === ffCurrentPage ? 'active' : ''}`;
                btn.innerText = i;
                btn.onclick = () => { ffCurrentPage = i; renderFFTable(); };
                controls.appendChild(btn);
            }

            if (endPage < totalPages) {
                if (endPage < totalPages - 1) {
                    const dots = document.createElement('span');
                    dots.innerText = '...';
                    dots.style.padding = '0.5rem';
                    dots.style.color = 'var(--text-muted)';
                    controls.appendChild(dots);
                }
                const btn = document.createElement('button');
                btn.className = 'page-btn';
                btn.innerText = totalPages;
                btn.onclick = () => { ffCurrentPage = totalPages; renderFFTable(); };
                controls.appendChild(btn);
            }

            const nextBtn = document.createElement('button');
            nextBtn.className = 'page-btn';
            nextBtn.innerHTML = '<i class="fa-solid fa-chevron-right"></i>';
            nextBtn.disabled = ffCurrentPage === totalPages;
            nextBtn.onclick = () => { if (ffCurrentPage < totalPages) { ffCurrentPage++; renderFFTable(); } };
            controls.appendChild(nextBtn);
        }

        function renderFFTable(initialData) {
            if (initialData) {
                ffFilteredData = [...initialData];
                ffCurrentPage = 1;
            }

            const tbody = document.getElementById('version-table-body');
            tbody.innerHTML = '';
            
            if (!ffFilteredData || ffFilteredData.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 3rem 0;">No data found in the report.</td></tr>';
                document.getElementById('version-docs-count').innerText = '0 documents';
                return;
            }

            const startIdx = (ffCurrentPage - 1) * ffPageSize;
            const endIdx = Math.min(startIdx + ffPageSize, ffFilteredData.length);
            const pageData = ffFilteredData.slice(startIdx, endIdx);

            document.getElementById('version-docs-count').innerText = `Showing ${ffFilteredData.length} documents from Version Report Non Excel files`;

            pageData.forEach(row => {
                const site = row.Site || (row.Location ? (row.Location.match(/\\/sites\\/([^\\/]+)/i) || [])[1] : 'Unknown') || 'Unknown';
                const totalSize = parseFloat(row['Total size for all versions (MB)'] || 0).toFixed(2);
                const size = parseFloat(row['Size (MB)'] || 0).toFixed(2);

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>
                        <div class="site-name-cell">
                            <span class="site-name">${row.Name || ''}</span>
                            <a href="${row.Location || '#'}" target="_blank" class="site-url">${row.Location || ''}</a>
                        </div>
                    </td>
                    <td>${site}</td>
                    <td>${row.List || ''}</td>
                    <td>${row['Version number'] || ''}</td>
                    <td>${size}</td>
                    <td>${totalSize}</td>
                `;
                tbody.appendChild(tr);
            });
            
            renderFFPagination();
        }
"""
html = re.sub(r'function renderFFTable\(data\) \{.*?(?=</script>)', js_replacement.strip() + '\n    ', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
