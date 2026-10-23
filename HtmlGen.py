import json
import os
import re
import sys

if len(sys.argv) < 2:
    print("Usage: py html_report.py <json_file>")
    sys.exit(1)

json_file = sys.argv[1]

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

output_dir = "Reports"
os.makedirs(output_dir, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>

<style>

* {{
    margin:0;
    padding:0;
    box-sizing:border-box;
}}

body {{
    background:#0f172a;
    color:white;
    font-family:Segoe UI, sans-serif;
    padding:30px;
}}

.container {{
    max-width:1400px;
    margin:auto;
}}

.header {{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(12px);
    border-radius:16px;
    padding:25px;
    margin-bottom:25px;
    animation:fadeIn 0.5s ease;
}}

.card {{
    background:#111827;
    border-radius:16px;
    padding:20px;
    margin-bottom:20px;
    box-shadow:0 4px 12px rgba(0,0,0,.3);
    animation:slideUp 0.4s ease;
}}

.badge {{
    display:inline-block;
    padding:8px 16px;
    border-radius:20px;
    font-weight:bold;
}}

.pass {{
    background:#16a34a;
}}

.fail {{
    background:#dc2626;
}}

.details {{
    display:grid;
    grid-template-columns:200px 1fr;
    gap:10px;
}}

.label {{
    color:#94a3b8;
}}

.section-title {{
    margin-bottom:10px;
    font-size:18px;
}}

.codebox {{
    background:#020617;
    border:1px solid #334155;
    border-radius:10px;
    padding:15px;
    max-height:400px;
    overflow:auto;
    white-space:pre-wrap;
    word-wrap:break-word;
}}

.assertion {{
    padding:10px;
    margin-bottom:8px;
    border-radius:8px;
}}

.assert-pass {{
    background:#14532d;
}}

.assert-fail {{
    background:#7f1d1d;
}}

button {{
    background:#2563eb;
    color:white;
    border:none;
    padding:8px 15px;
    border-radius:8px;
    cursor:pointer;
    margin-bottom:10px;
}}

button:hover {{
    background:#1d4ed8;
}}

details {{
    margin-top:10px;
}}

summary {{
    cursor:pointer;
    font-size:18px;
    margin-bottom:10px;
}}

@keyframes fadeIn {{
    from{{opacity:0}}
    to{{opacity:1}}
}}

@keyframes slideUp {{
    from{{
        opacity:0;
        transform:translateY(20px);
    }}
    to{{
        opacity:1;
        transform:translateY(0);
    }}
}}

</style>

<script>
function copyText(id){{
    navigator.clipboard.writeText(
        document.getElementById(id).innerText
    );
}}
</script>

</head>

<body>

<div class="container">

<div class="header">
<h1>API Test Case Report</h1>
<br>
<h2>{title}</h2>
<br>
{status_badge}
</div>

{content}

</div>

</body>
</html>
"""

for tc in data["testCases"]:

    test_case = tc.get("testCase", "Unknown")

    safe_name = re.sub(
        r'[\\\\/*?:"<>|]',
        "_",
        test_case
    )

    requests = tc.get("requests", [])

    total_pass = 0
    total_fail = 0

    content = ""

    for i, request in enumerate(requests, start=1):

        assertions_html = ""

        for assertion in request.get("assertions", []):

            status = assertion.get("status", "").lower()
            message = assertion.get("message", "")

            if status == "pass":
                total_pass += 1
                css = "assert-pass"
            else:
                total_fail += 1
                css = "assert-fail"

            assertions_html += f"""
            <div class="assertion {css}">
                [{status.upper()}] {message}
            </div>
            """

        request_body = str(
            request.get("requestBody", "")
        ).replace("\\n", "\n")

        response_body = str(
            request.get("responseBody", "")
        )

        response_body = response_body.replace(
            "'Response Body:',",
            ""
        )

        response_body = response_body.replace(
            "\\n",
            "\n"
        )

        content += f"""
        <div class="card">

            <h2>Request #{i}</h2>
            <br>

            <div class="details">
                <div class="label">API Name</div>
                <div>{request.get("apiName","")}</div>

                <div class="label">Method</div>
                <div>{request.get("method","")}</div>

                <div class="label">URL</div>
                <div>{request.get("url","")}</div>

                <div class="label">Status</div>
                <div>{request.get("status","")}</div>

                <div class="label">Response Time</div>
                <div>{request.get("responseTime","")}</div>

                <div class="label">Data Size</div>
                <div>
                    {request.get("dataSize","")}
                    {request.get("dataUnit","")}
                </div>
            </div>

            <br>

            <details>
                <summary>Request Body</summary>

                <button onclick="copyText('req{i}')">
                    Copy
                </button>

                <div class="codebox" id="req{i}">
{request_body}
                </div>
            </details>

            <br>

            <details open>
                <summary>Response Body</summary>

                <button onclick="copyText('res{i}')">
                    Copy
                </button>

                <div class="codebox" id="res{i}">
{response_body}
                </div>
            </details>

            <br>

            <h3>Assertions</h3>
            <br>

            {assertions_html}

        </div>
        """

    status_badge = (
        '<span class="badge pass">PASS</span>'
        if total_fail == 0
        else
        '<span class="badge fail">FAIL</span>'
    )

    html = HTML_TEMPLATE.format(
        title=test_case,
        status_badge=status_badge,
        content=content
    )

    output_file = os.path.join(
        output_dir,
        f"{safe_name}.html"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print("Generated:", output_file)

print("\nAll HTML reports generated successfully.")