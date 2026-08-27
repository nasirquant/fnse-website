with open('c:/Users/E/Documents/trae_projects/fnse-website/content/docs/api-reference/_index.md', 'r') as f:
    lines = f.readlines()

new_lines = lines[:314]
new_lines.extend([
    '### Get Alerts\n',
    '\n',
    '**GET** `/epochs/{epoch_id}/alerts`\n',
    '\n',
    '**Query Parameters:**\n',
    '- `severity` - Filter by severity (info, warning, critical, emergency)\n',
    '- `limit` - Maximum number of alerts to return (default: 100)\n',
    '\n',
    '**Response** (200 OK):\n',
    '\n',
    '```json\n',
    '[\n',
    '  {\n',
    '    "alert_id": "alt_xyz789",\n',
    '    "timestamp": "2024-01-15T10:40:00Z",\n',
    '    "severity": "warning",\n',
    '    "source": "safeguard_system",\n',
    '    "message": "Divergence score 0.52 exceeds warning threshold",\n',
    '    "details": {"divergence_score": 0.52},\n',
    '    "acknowledged": false,\n',
    '    "resolved": false\n',
    '  }\n',
    ']\n',
    '```\n',
    '\n',
    '### Acknowledge Alert\n',
    '\n',
    '**POST** `/epochs/{epoch_id}/alerts/{alert_id}/acknowledge`\n',
    '\n',
    '**Response** (200 OK):\n',
    '```json\n',
    '{\n',
    '  "status": "acknowledged",\n',
    '  "alert_id": "alt_xyz789"\n',
    '}\n',
    '```\n',
    '\n',
    '## Skills\n'
])
new_lines.extend(lines[361:])

with open('c:/Users/E/Documents/trae_projects/fnse-website/content/docs/api-reference/_index.md', 'w') as f:
    f.writelines(new_lines)
print('Done')