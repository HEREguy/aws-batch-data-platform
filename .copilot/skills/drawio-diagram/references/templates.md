# Draw.io Template Examples

Complete examples of common diagram patterns for quick reference.

## Minimal Base Template

```xml
<mxfile host="app.diagrams.net" version="24.0.0" type="device">
  <diagram id="diagram1" name="Page-1">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Add shapes here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Simple Flow Diagram

```xml
<mxfile host="app.diagrams.net" version="24.0.0" type="device">
  <diagram id="flow" name="Simple Flow">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Input -->
        <mxCell id="input" value="Input" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <!-- Process -->
        <mxCell id="process" value="Process" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="300" y="100" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <!-- Output -->
        <mxCell id="output" value="Output" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="500" y="100" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <!-- Connections -->
        <mxCell id="conn1" edge="1" source="input" target="process">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="conn2" edge="1" source="process" target="output">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Status Table

```xml
<mxfile host="app.diagrams.net" version="24.0.0" type="device">
  <diagram id="status_table" name="Status Table">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="850" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Headers -->
        <mxCell id="h1" value="Item" style="fillColor=#4472C4;strokeColor=#2E5FA3;fontStyle=1;fontColor=#FFFFFF;align=center;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="200" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="h2" value="Status" style="fillColor=#4472C4;strokeColor=#2E5FA3;fontStyle=1;fontColor=#FFFFFF;align=center;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="100" width="120" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="h3" value="Notes" style="fillColor=#4472C4;strokeColor=#2E5FA3;fontStyle=1;fontColor=#FFFFFF;align=center;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="100" width="300" height="40" as="geometry"/>
        </mxCell>
        
        <!-- Row 1 -->
        <mxCell id="r1c1" value="Feature A" style="fillColor=#E8F4F8;strokeColor=#4472C4;align=left;spacingLeft=8;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="100" y="140" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="r1c2" value="✅ Done" style="fillColor=#c6e0b4;strokeColor=#70ad47;align=center;fontStyle=1;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="300" y="140" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="r1c3" value="Completed on schedule" style="fillColor=#E8F4F8;strokeColor=#4472C4;align=left;spacingLeft=8;fontSize=10;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="420" y="140" width="300" height="60" as="geometry"/>
        </mxCell>
        
        <!-- Row 2 -->
        <mxCell id="r2c1" value="Feature B" style="fillColor=#F2F2F2;strokeColor=#4472C4;align=left;spacingLeft=8;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="100" y="200" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="r2c2" value="⚪ Pending" style="fillColor=#fff4e6;strokeColor=#f4b183;align=center;fontStyle=1;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="300" y="200" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="r2c3" value="Awaiting review" style="fillColor=#F2F2F2;strokeColor=#4472C4;align=left;spacingLeft=8;fontSize=10;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="420" y="200" width="300" height="60" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Database/Cylinder Shapes

```xml
<!-- Database cylinder -->
<mxCell id="db1" value="Database" style="shape=cylinder;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="140" as="geometry"/>
</mxCell>
```

## Decision Diamond

```xml
<!-- Decision point -->
<mxCell id="decision" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="140" as="geometry"/>
</mxCell>
```

## Swimlane Layout

```xml
<!-- Swimlane container -->
<mxCell id="lane1" value="Actor 1" style="swimlane;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;fontColor=#333333;startSize=40;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="400" height="200" as="geometry"/>
</mxCell>

<!-- Child element in swimlane -->
<mxCell id="task1" value="Task" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;fontSize=11;fontColor=#333333;" vertex="1" parent="lane1">
  <mxGeometry x="20" y="60" width="120" height="60" as="geometry"/>
</mxCell>
```

## Multi-line Text with Formatting

```xml
<!-- Multi-line with breaks -->
<mxCell id="text1" value="Line 1&#xa;Line 2&#xa;Line 3" 
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f2f2f2;strokeColor=#999999;fontSize=11;fontColor=#333333;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;" 
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="100" as="geometry"/>
</mxCell>
```

## Connection with Waypoint

```xml
<!-- Connection with intermediate point -->
<mxCell id="conn_waypoint" edge="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## Legend/Key

```xml
<!-- Legend title -->
<mxCell id="legend_title" value="Legend:" style="text;html=1;strokeColor=none;fillColor=none;align=left;fontStyle=1;fontSize=12;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="100" y="500" width="80" height="30" as="geometry"/>
</mxCell>

<!-- Legend item -->
<mxCell id="legend_done" value="✅ Completed" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#c6e0b4;strokeColor=#70ad47;fontSize=10;fontColor=#333333;align=center;" vertex="1" parent="1">
  <mxGeometry x="180" y="500" width="100" height="30" as="geometry"/>
</mxCell>
```
