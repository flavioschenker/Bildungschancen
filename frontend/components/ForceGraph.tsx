"use client"

import React, { useEffect, useRef } from 'react'
import * as d3 from 'd3'

interface Node extends d3.SimulationNodeDatum {
  id: string;
  img?: string; // Added image property
}

interface Link extends d3.SimulationLinkDatum<Node> {}

const data: { nodes: Node[], links: Link[] } = {
  nodes: [
    { id: "React", img: "https://v2.dev.buildwithfern.com/static/img/react.png" },
    { id: "Next.js", img: "https://assets.vercel.com/image/upload/v1662130559/nextjs/Icon_light_background.png" },
    { id: "Tailwind", img: "https://bourbon-digital.com/wp-content/uploads/2021/05/tail-1.png" },
    // ... add more URLs as needed
  ],
  links: [
    { source: "Next.js", target: "React" },
    { source: "Next.js", target: "Tailwind" },
  ]
}

export default function ForceGraph() {
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    if (!svgRef.current) return

    const width = 800
    const height = 500
    const nodeWidth = 100
    const nodeHeight = 40

    const svg = d3.select(svgRef.current)
      .attr("viewBox", [0, 0, width, height])
      .style("background", "#f8fafc")

    svg.selectAll("*").remove()

    const links = data.links.map(d => ({ ...d }))
    const nodes = data.nodes.map(d => ({ ...d }))

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id((d: any) => d.id).distance(150))
      .force("charge", d3.forceManyBody().strength(-400))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(60)) // Bigger radius for bigger nodes

    const link = svg.append("g")
      .attr("stroke", "#cbd5e1")
      .selectAll("line")
      .data(links)
      .join("line")

    const node = svg.append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("cursor", "grab")
      .call(d3.drag<any, any>()
        .on("start", (e) => { if (!e.active) simulation.alphaTarget(0.3).restart(); e.subject.fx = e.x; e.subject.fy = e.y; })
        .on("drag", (e) => { e.subject.fx = e.x; e.subject.fy = e.y; })
        .on("end", (e) => { if (!e.active) simulation.alphaTarget(0); e.subject.fx = null; e.subject.fy = null; })
      )

    // 1. The Background Rectangle
    node.append("rect")
      .attr("width", nodeWidth)
      .attr("height", nodeHeight)
      .attr("x", -nodeWidth / 2)
      .attr("y", -nodeHeight / 2)
      .attr("rx", 8) // Rounded corners
      .attr("fill", "#ffffff")
      .attr("stroke", "#3b82f6")
      .attr("stroke-width", 2)

    // 2. The Image (Left side)
    node.append("image")
      .attr("xlink:href", d => d.img || "https://via.placeholder.com/20")
      .attr("x", -nodeWidth / 2 + 8)
      .attr("y", -12)
      .attr("width", 24)
      .attr("height", 24)

    // 3. The Text (Right of image)
    node.append("text")
      .text(d => d.id)
      .attr("x", -nodeWidth / 2 + 40)
      .attr("y", 5)
      .style("font-size", "12px")
      .style("font-weight", "600")
      .style("font-family", "sans-serif")
      .style("fill", "#1e293b")

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y)

      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`)
    })

    return () => simulation.stop()
  }, [])

  return (
    <div className="w-full h-full flex justify-center">
      <svg ref={svgRef} className="w-full h-full border border-slate-200" />
    </div>
  )
}