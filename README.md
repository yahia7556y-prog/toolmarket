# ToolMarket

A live-style dashboard of the most used AI tools, skills and agents. English by default with an Arabic toggle, light and dark themes. Hosted free on GitHub Pages, no server.

## Run locally
    python collector/collect.py --demo   # fake data, no network
    python collector/collect.py          # real data (set GITHUB_TOKEN to avoid rate limits)
    cd web && python -m http.server 8000

## Deploy
Settings > Pages > Source: GitHub Actions, then Actions > update > Run workflow. It refreshes daily.

## Add an item
Add a line to collector/seeds.txt: repo|type|domain|name|npm|pypi|install command|description|arabic description. Types: tool, skill, agent.

## How usage is measured
Daily downloads from npm or PyPI when a package is given, otherwise the star count. 24h change compares with yesterday snapshot in data/history.json.

## Auto-discovery
collector/discover.py finds repos tagged mcp-server, claude-skills, agent-skills, ai-agent (200+ stars, active in 180 days, licensed, not forks).

## Install telemetry (optional)
worker/ is a Cloudflare Worker that counts install-button clicks with no personal data. Deploy it, then set the Actions variable TELEMETRY_URL.
