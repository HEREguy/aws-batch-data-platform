---
name: drawio-diagram
description: Create professional diagrams in draw.io (.drawio) format. Use for system architecture diagrams, data flow diagrams, tables, timelines, flowcharts, and technical visualizations. Handles XML structure, connection management, styling, and layout best practices.
---

# Draw.io Diagram Creation

Create professional diagrams directly in draw.io XML format for technical documentation, presentations, and system design.

## When to Use This Skill

**USE for:**
- System architecture and data flow diagrams
- Technical tables and status matrices
- Process flowcharts and swimlanes
- Timeline and roadmap visualizations
- Component relationship diagrams
- Infrastructure and network diagrams

**DON'T USE for:**
- Simple markdown tables (use markdown)
- Mermaid-suitable diagrams (use mermaid in markdown)
- Quick sketches (suggest draw.io UI instead)

## File Structure

```xml
<mxfile host="app.diagrams.net" version="24.0.0" type="device">
  <diagram id="unique_id" name="Diagram Name">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" ...>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Shapes here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Core Components

### Shape (mxCell with geometry)

```xml
<mxCell id="unique_id" 
        value="Text Content" 
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;fontColor=#333333;" 
        vertex="1" 
        parent="1">
  <mxGeometry x="100" y="100" width="200" height="80" as="geometry"/>
</mxCell>
```

**Key attributes:**
- `id`: Unique identifier (use descriptive names like "header_check" or "node5")
- `value`: Text content (use `&#xa;` for line breaks)
- `style`: Semicolon-separated CSS-like properties
- `vertex="1"`: Indicates this is a shape (not an edge)
- `parent="1"`: Places in default layer

### Connector (mxCell edge)

**CRITICAL: Connection Best Practices**

For auto-adjusting connections when shapes move:

```xml
<!-- ✅ CORRECT: Minimal connection (auto-adjusts) -->
<mxCell id="edge1" edge="1" source="nodeA" target="nodeB">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**AVOID these patterns that break auto-adjustment:**
```xml
<!-- ❌ Fixed entry/exit points -->
<mxCell ... style="exitX=0.5;exitY=1;entryX=0.5;entryY=0"/>

<!-- ❌ Fixed coordinates -->
<mxGeometry>
  <mxPoint x="190" y="100" as="sourcePoint"/>
</mxGeometry>

<!-- ❌ Overly constrained routing -->
<mxCell ... style="edgeStyle=orthogonalEdgeStyle;exitX=...;entryX=..."/>
```

**Connection patterns:**

```xml
<!-- Simple auto-routing (best for most cases) -->
<mxCell id="conn1" edge="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Orthogonal routing (when needed) -->
<mxCell id="conn2" edge="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200"/>
    </Array>
  </mxGeometry>
</mxCell>
```

**Why connections fail:**
- Draw.io needs minimal constraints to calculate optimal connection points
- Fixed `exitX/exitY/entryX/entryY` lock connections to specific percentages (0.5 = center, 0 = top/left, 1 = bottom/right)
- Fixed `mxPoint` coordinates create floating endpoints
- Let draw.io automatically find the best connection points by only specifying `source` and `target`

### Style Properties

**Common properties:**
```
fillColor=#dae8fc       - Background color
strokeColor=#6c8ebf     - Border color
fontColor=#333333       - Text color (use dark gray, not black)
fontSize=12             - Text size
fontStyle=1             - Bold (0=normal, 1=bold, 2=italic, 3=bold+italic)
fontFamily=FiraGO       - Use FiraGO for a clean, professional look
rounded=1               - Rounded corners
whiteSpace=wrap         - Text wrapping
html=1                  - Enable HTML in text
align=center            - Horizontal alignment (left/center/right)
verticalAlign=middle    - Vertical alignment (top/middle/bottom)
spacingLeft=8           - Internal padding
spacingTop=8            - Internal padding
```

**Shape types:**
```
rounded=1;whiteSpace=wrap;html=1  - Rectangle
ellipse;whiteSpace=wrap;html=1    - Circle/Ellipse
rhombus;whiteSpace=wrap;html=1    - Diamond
shape=cylinder                     - Cylinder (databases)
shape=hexagon                      - Hexagon
```

## Color Schemes

**Professional Palette:**
```
Blue:   fillColor=#dae8fc; strokeColor=#6c8ebf;  - Primary/headers
Gray:   fillColor=#f2f2f2; strokeColor=#999999;  - Secondary/alternating
Green:  fillColor=#d5e8d4; strokeColor=#82b366;  - Success/completed
Orange: fillColor=#ffe6cc; strokeColor=#d79b00;  - Contracts/config
Yellow: fillColor=#fff2cc; strokeColor=#d6b656;  - Data/processing
Purple: fillColor=#e1d5e7; strokeColor=#9673a6;  - Dashboards/UI
Red:    fillColor=#f8cecc; strokeColor=#b85450;  - Notifications/alerts
```

**Status indicators:**
```
Implemented:     fillColor=#c6e0b4; strokeColor=#70ad47;  (green)
Not Implemented: fillColor=#fff4e6; strokeColor=#f4b183;  (orange)
In Progress:     fillColor=#ffe599; strokeColor=#f6b26b;  (yellow)
Blocked:         fillColor=#f4cccc; strokeColor=#cc0000;  (red)
```

## Common Patterns

### Table Diagram
Note that rounded corners should not be used for tables to maintain a clean grid appearance.
```xml
<!-- Header row -->
<mxCell id="header1" value="Column 1" 
        style="fillColor=#4472C4;strokeColor=#2E5FA3;fontStyle=1;fontColor=#FFFFFF;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="40" as="geometry"/>
</mxCell>

<!-- Data row (alternating colors) -->
<mxCell id="row1" value="Data" 
        style="fillColor=#E8F4F8;strokeColor=#4472C4;align=left;spacingLeft=8;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="140" width="200" height="60" as="geometry"/>
</mxCell>

<mxCell id="row2" value="Data" 
        style="fillColor=#F2F2F2;strokeColor=#4472C4;align=left;spacingLeft=8;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="200" height="60" as="geometry"/>
</mxCell>
```

### Data Flow Diagram

```xml
<!-- Source -->
<mxCell id="source" value="Data&#xa;Source" 
        style="shape=cylinder;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#333333;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="140" as="geometry"/>
</mxCell>

<!-- Process -->
<mxCell id="process" value="Transform" 
        style="rounded=0;fillColor=#ffe6cc;strokeColor=#d79b00;fontColor=#333333;"
        vertex="1" parent="1">
  <mxGeometry x="340" y="130" width="140" height="80" as="geometry"/>
</mxCell>

<!-- Connection -->
<mxCell id="flow1" edge="1" source="source" target="process">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### Status Matrix with Icons

```xml
<mxCell id="status1" value="✅ Implemented" 
        style="fillColor=#c6e0b4;strokeColor=#70ad47;fontStyle=1;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry"/>
</mxCell>

<mxCell id="status2" value="⚪ Not Implemented" 
        style="fillColor=#fff4e6;strokeColor=#f4b183;fontStyle=1;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="160" width="140" height="60" as="geometry"/>
</mxCell>
```

## Layout Guidelines

**Spacing:**
- Grid: 10px (set `gridSize="10"` in mxGraphModel)
- Minimum gap between shapes: 20-40px
- Table row height: 40-80px depending on content
- Column width: 140-300px depending on content

**Alignment:**
- Snap to 10px grid for professional appearance
- Align related items vertically or horizontally
- Use consistent spacing throughout diagram

**Canvas size:**
- Standard: `pageWidth="1600" pageHeight="1200"`
- Presentation slide: `pageWidth="1400" pageHeight="850"`
- Portrait: `pageWidth="850" pageHeight="1100"`

**Text formatting:**
- Use `&#xa;` for line breaks in value attribute
- Keep font size 10-12 for body text, 14-18 for headers
- Use `fontColor=#333333` (dark gray) instead of black for better readability
- Use `whiteSpace=wrap` for multi-line text
- Use `html=1` to enable formatting

## Multi-Page Diagrams

```xml
<mxfile pages="3">
  <diagram id="page1" name="Overview">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
  <diagram id="page2" name="Detail">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
</mxfile>
```

## Best Practices

1. **IDs**: Use descriptive IDs (`header_name`, `node_source`) not generic (`cell1`, `cell2`)
2. **Connections**: Keep minimal - just `source` and `target` for auto-adjusting behavior
3. **Colors**: Use consistent palette, avoid pure black text (`#333333` is better)
4. **Spacing**: Snap to 10px grid, maintain consistent gaps
5. **Text**: Use `&#xa;` for line breaks, not multiple spaces
6. **Reusability**: Define common styles once, reuse pattern
7. **Accessibility**: Ensure sufficient color contrast, use `fontColor=#333333`

## Troubleshooting

**Connections not adjusting when shapes move:**
- Remove `exitX`, `exitY`, `entryX`, `entryY` from style
- Remove `mxPoint` children from geometry
- Remove `edgeStyle` unless specifically needed
- Keep connection XML minimal: just `source`, `target`, and empty `<mxGeometry relative="1" as="geometry"/>`

**Text not wrapping:**
- Add `whiteSpace=wrap` to style
- Set explicit width in geometry
- Use `&#xa;` for forced line breaks

**Colors not showing:**
- Ensure hex colors start with `#`
- Check strokeColor is different from fillColor for visibility
- Use `html=1` in style for HTML content

**Shape not appearing:**
- Verify `vertex="1"` for shapes (not `edge="1"`)
- Check `parent="1"` is set
- Ensure geometry has x, y, width, height
- Verify unique ID doesn't conflict

## Quick Reference

**Create new diagram:**
1. Copy base XML structure with mxfile/diagram/mxGraphModel
2. Add shapes with unique IDs, geometry, and styles
3. Add connections with source/target only
4. Keep formatting minimal for auto-adjustment
5. Test by opening in draw.io

**File naming:** `descriptive_name.drawio` (use underscores, not spaces)

**Validation:** Open file in draw.io desktop or web app to verify rendering

---

*For advanced patterns, custom shapes, or embedded images, refer to draw.io documentation or examine existing .drawio files in the project.*
