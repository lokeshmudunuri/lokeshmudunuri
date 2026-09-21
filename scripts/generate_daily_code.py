"""
Curated Daily Dev Code generator.
Produces a clean, high-contrast SVG showing a daily rotating technical concept/trick
(Python, JavaScript, Java DSA, SQL, Git) based on the day of the year.
"""

import datetime
from pathlib import Path

SNIPPETS = [
    {
        "category": "Python • Performance & Idioms",
        "title": "Decoupling Heavy Computations via Generator Expressions",
        "code": [
            "# Avoid loading millions of database rows or metric streams into memory",
            "def stream_transactions(batch_size=1000):",
            "    for offset in range(0, total_records, batch_size):",
            "        yield fetch_chunk(offset, batch_size)",
            "",
            "# Memory footprint remains O(batch_size) rather than O(N)",
            "active_runways = (calc_runway(tx) for tx in stream_transactions() if tx.is_valid)",
        ],
        "takeaway": "Generators stream items on-demand, preventing memory bloat in high-volume data pipelines.",
    },
    {
        "category": "JavaScript • Robust Async",
        "title": "Safe Async Orchestration with Promise.allSettled()",
        "code": [
            "// Unlike Promise.all(), allSettled() never short-circuits on a single failure",
            "const results = await Promise.allSettled([",
            "  fetchSalesVelocity(storeId),",
            "  fetchStockAnomalies(storeId),",
            "  fetchInventoryRunway(storeId)",
            "]);",
            "",
            "const fulfilled = results.filter(r => r.status === 'fulfilled').map(r => r.value);",
        ],
        "takeaway": "Preserves partial dashboard telemetry even if an individual upstream microservice is degraded.",
    },
    {
        "category": "Java • Data Structures & Algorithms",
        "title": "Fast Sliding Window Anomaly Detection",
        "code": [
            "// Compute rolling max over transaction streams in O(N) using Monotonic Deque",
            "Deque<Integer> deque = new ArrayDeque<>();",
            "for (int i = 0; i < nums.length; i++) {",
            "    while (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();",
            "    while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[i]) deque.pollLast();",
            "    deque.offerLast(i);",
            "    if (i >= k - 1) maxWindow[i - k + 1] = nums[deque.peekFirst()];",
            "}",
        ],
        "takeaway": "Monotonic deques efficiently maintain order in streaming time-series anomaly detection.",
    },
    {
        "category": "FastAPI & Python • Deterministic API",
        "title": "Strict Schema Validation & Pydantic Field Constraints",
        "code": [
            "from pydantic import BaseModel, Field",
            "",
            "class InventoryItem(BaseModel):",
            "    sku: str = Field(..., regex=r'^[A-Z0-9]{8}$')  # Exact canonical pattern",
            "    stock_count: int = Field(..., ge=0)             # Prevents negative stock",
            "    daily_velocity: float = Field(..., gt=0.0)      # Avoids division-by-zero",
        ],
        "takeaway": "Fail-fast input validation prevents bad data from corrupting downstream math or LLM prompts.",
    },
    {
        "category": "SQL & SQLite • Analytical Indexing",
        "title": "Compound Indexes for Fast Range & Aggregation Queries",
        "code": [
            "-- Optimizes queries filtering by store and scanning recent 90-day intervals",
            "CREATE INDEX idx_sales_store_date ",
            "ON sales_records (store_id, transaction_date DESC);",
            "",
            "-- SQLite converts slow linear table scans into targeted index range lookups",
            "SELECT sku, SUM(quantity) FROM sales_records",
            "WHERE store_id = 'S004' AND transaction_date >= '2026-06-01';",
        ],
        "takeaway": "Compound indexes with correct column order drastically cut analytical query execution time.",
    },
    {
        "category": "Git & CI/CD • Clean History",
        "title": "Interactive Rebasing & Atomic Commits",
        "code": [
            "# Keep feature branches auditable and easy for teammates to review",
            "git fetch origin",
            "git rebase -i origin/main",
            "",
            "# Fix a regression in the previous commit without creating 'fix typo' noise",
            "git add src/analytics.py",
            "git commit --amend --no-edit",
        ],
        "takeaway": "Atomic, descriptive commits keep team code reviews effortless and git bisect fast.",
    },
    {
        "category": "AI Systems • Grounded Prompt Engineering",
        "title": "Separating Arithmetic Engines from Generative Reasoning",
        "code": [
            "# Step 1: Deterministic code executes 100% of mathematical calculations",
            "evidence = {'runway_days': 4.2, 'stockout_risk': 'CRITICAL', 'daily_velocity': 18.5}",
            "",
            "# Step 2: Pass only verified JSON numbers to LLM for executive directives",
            "prompt = f'Summarize stock strategy using strictly this payload: {json.dumps(evidence)}'",
            "# Result: Zero math hallucinations. 100% auditable business logic.",
        ],
        "takeaway": "Never rely on LLMs to perform arithmetic; use deterministic code for math and models for reasoning.",
    }
]

def generate_svg():
    # Deterministically pick today's concept
    day_of_year = datetime.datetime.now(datetime.timezone.utc).timetuple().tm_yday
    snippet = SNIPPETS[day_of_year % len(SNIPPETS)]

    width = 780
    line_height = 20
    code_start_y = 90
    code_lines = snippet["code"]
    code_block_height = len(code_lines) * line_height + 24
    height = code_start_y + code_block_height + 65

    # Escape XML entities
    def esc(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

    code_elements = []
    for i, line in enumerate(code_lines):
        y = code_start_y + 20 + (i * line_height)
        color = "#8b949e" if line.strip().startswith(("#", "--", "//")) else "#c9d1d9"
        if "def " in line or "class " in line or "const " in line or "CREATE " in line or "from " in line or "import " in line:
            color = "#79c0ff"
        code_elements.append(
            f'    <text x="36" y="{y}" fill="{color}" font-family="Consolas, Fira Code, monospace" font-size="12.5">{esc(line)}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">
  <style>
    .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 15px; fill: #58a6ff; }}
    .category {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 600; fill: #00d4ff; text-transform: uppercase; letter-spacing: 0.8px; }}
    .takeaway {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; fill: #8b949e; font-style: italic; }}
    .badge {{ fill: #161b22; stroke: #30363d; stroke-width: 1; rx: 6; }}
    .header-dot-red {{ fill: #ff5f56; }}
    .header-dot-yellow {{ fill: #ffbd2e; }}
    .header-dot-green {{ fill: #27c93f; }}
  </style>

  <!-- Card Background -->
  <rect width="{width}" height="{height}" rx="10" fill="#0a0e27" stroke="#30363d" stroke-width="1.5"/>

  <!-- Window Header Controls -->
  <circle cx="28" cy="26" r="5" class="header-dot-red" />
  <circle cx="44" cy="26" r="5" class="header-dot-yellow" />
  <circle cx="60" cy="26" r="5" class="header-dot-green" />

  <!-- Badge / Category -->
  <rect x="80" y="16" width="280" height="20" rx="4" fill="#13233a" stroke="#00d4ff" stroke-opacity="0.3" stroke-width="1"/>
  <text x="90" y="30" class="category">⚡ {esc(snippet["category"])}</text>

  <!-- Title -->
  <text x="26" y="66" class="title">{esc(snippet["title"])}</text>

  <!-- Code Container -->
  <rect x="20" y="80" width="{width - 40}" height="{code_block_height}" rx="6" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
{chr(10).join(code_elements)}

  <!-- Takeaway footer -->
  <text x="26" y="{height - 20}" class="takeaway">💡 Takeaway: {esc(snippet["takeaway"])}</text>
</svg>
"""

    out_path = Path("assets/daily-dev-code.svg")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Generated daily dev code SVG: {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    generate_svg()
