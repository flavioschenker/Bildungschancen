"use client"

import React, { useCallback, useEffect, useRef } from "react"
import * as d3 from "d3"
import { RefreshCw } from "lucide-react"

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface Node extends d3.SimulationNodeDatum {
  id: string
  img?: string
}

type Link = d3.SimulationLinkDatum<Node>

const data: { nodes: Node[]; links: Link[] } = {
  nodes: [
    { id: "Anna", img: "/avatars/Anna.jpg" },
    { id: "Beatrice", img: "/avatars/Beatrice.jpg" },
    { id: "Caroline", img: "/avatars/Caroline.jpg" },
    { id: "Doris", img: "/avatars/Doris.jpg" },
    { id: "Etienne", img: "/avatars/Etienne.jpg" },
    { id: "Flavio", img: "/avatars/Flavio.jpg" },
    { id: "Gariel", img: "/avatars/Gariel.jpg" },
    { id: "Iris", img: "/avatars/Iris.jpg" },
    { id: "Jeaninne", img: "/avatars/Jeaninne.jpg" },
    { id: "Kenneth", img: "/avatars/Kenneth.jpg" },
    { id: "Madeleine", img: "/avatars/Madeleine.jpg" },
    { id: "Mario", img: "/avatars/Mario.jpg" },
    { id: "Olivia", img: "/avatars/Olivia.jpg" },
    { id: "Paul", img: "/avatars/Paul.jpg" },
    { id: "Philip", img: "/avatars/Philip.jpg" },
    { id: "Rolf", img: "/avatars/Rolf.jpg" },
    { id: "Sandra", img: "/avatars/Sandra.jpg" },
    { id: "Sara", img: "/avatars/Sara.jpg" },
    { id: "Silvia", img: "/avatars/Silvia.jpg" },
    { id: "Stefan", img: "/avatars/Stefan.jpeg" },
    { id: "Thomas", img: "/avatars/Thomas.jpg" },
    { id: "Vincenzo", img: "/avatars/Vincenzo.jpg" },
  ],
  links: [
    { source: "Flavio", target: "Sara" },
    { source: "Sara", target: "Silvia" },
    { source: "Sara", target: "Vincenzo" },
    { source: "Sara", target: "Mario" },
    { source: "Silvia", target: "Vincenzo" },
    { source: "Silvia", target: "Iris" },
    { source: "Silvia", target: "Mario" },
    { source: "Vincenzo", target: "Mario" },
    { source: "Mario", target: "Sandra" },
    { source: "Sara", target: "Iris" },
    { source: "Sara", target: "Philip" },
    { source: "Iris", target: "Thomas" },
    { source: "Iris", target: "Philip" },
    { source: "Philip", target: "Thomas" },
    { source: "Philip", target: "Anna" },
    { source: "Flavio", target: "Etienne" },
    { source: "Etienne", target: "Olivia" },
    { source: "Etienne", target: "Rolf" },
    { source: "Etienne", target: "Beatrice" },
    { source: "Rolf", target: "Beatrice" },
    { source: "Flavio", target: "Stefan" },
  ],
}

function readThemeColors() {
  const s = getComputedStyle(document.documentElement)
  return {
    background: s.getPropertyValue("--background").trim(),
    border: s.getPropertyValue("--border").trim(),
    card: s.getPropertyValue("--card").trim(),
    mutedForeground: s.getPropertyValue("--muted-foreground").trim(),
    primary: s.getPropertyValue("--primary").trim(),
  }
}

export default function ForceGraph({ className }: { className?: string }) {
  const svgRef = useRef<SVGSVGElement>(null)
  const simulationRef = useRef<d3.Simulation<Node, Link> | null>(null)

  useEffect(() => {
    if (!svgRef.current) return

    const colors = readThemeColors()

    const width = 800
    const height = 600
    const imageSize = 50
    const radius = imageSize / 2

    const svg = d3
      .select(svgRef.current)
      .attr("viewBox", [0, 0, width, height])
      .style("background", colors.background)

    svg.selectAll("*").remove()

    const defs = svg.append("defs")
    defs
      .append("clipPath")
      .attr("id", "circle-clip")
      .append("circle")
      .attr("r", radius)
      .attr("cx", 0)
      .attr("cy", 0)

    const links = data.links.map((d) => ({ ...d }))
    const nodes = data.nodes.map((d) => ({ ...d }))

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d: d3.SimulationNodeDatum) => (d as Node).id)
          .distance(120)
      )
      .force("charge", d3.forceManyBody().strength(-500))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(imageSize))

    simulationRef.current = simulation

    const link = svg
      .append("g")
      .attr("stroke", colors.border)
      .attr("stroke-opacity", 0.9)
      .attr("stroke-width", 1.5)
      .selectAll("line")
      .data(links)
      .join("line")

    const node = svg
      .append("g")
      .selectAll<SVGGElement, Node>("g")
      .data(nodes)
      .join("g")
      .attr("cursor", "grab")
      .call(
        d3
          .drag<SVGGElement, Node>()
          .on("start", (event: d3.D3DragEvent<SVGGElement, Node, Node>) => {
            if (!event.active) simulation.alphaTarget(0.3).restart()
            event.subject.fx = event.x
            event.subject.fy = event.y
          })
          .on("drag", (event: d3.D3DragEvent<SVGGElement, Node, Node>) => {
            event.subject.fx = event.x
            event.subject.fy = event.y
          })
          .on("end", (event: d3.D3DragEvent<SVGGElement, Node, Node>) => {
            if (!event.active) simulation.alphaTarget(0)
            event.subject.fx = null
            event.subject.fy = null
          })
      )

    node
      .append("circle")
      .attr("r", radius + 2)
      .attr("fill", colors.card)
      .attr("stroke", colors.primary)
      .attr("stroke-width", 2)

    node
      .append("image")
      .attr("href", (d: Node) => d.img ?? "https://via.placeholder.com/50")
      .attr("x", -radius)
      .attr("y", -radius)
      .attr("width", imageSize)
      .attr("height", imageSize)
      .attr("clip-path", "url(#circle-clip)")

    node
      .append("text")
      .text((d: Node) => d.id)
      .attr("y", radius + 20)
      .attr("text-anchor", "middle")
      .style("font-size", "12px")
      .style("font-weight", "500")
      .style("font-family", "var(--font-sans), ui-sans-serif, system-ui, sans-serif")
      .style("fill", colors.mutedForeground)

    simulation.on("tick", () => {
      link
        .attr("x1", (d: Link) => (d.source as Node).x ?? 0)
        .attr("y1", (d: Link) => (d.source as Node).y ?? 0)
        .attr("x2", (d: Link) => (d.target as Node).x ?? 0)
        .attr("y2", (d: Link) => (d.target as Node).y ?? 0)

      node.attr("transform", (d: Node) => `translate(${d.x ?? 0},${d.y ?? 0})`)
    })

    return () => {
      simulation.stop()
      simulationRef.current = null
    }
  }, [])

  const restartLayout = useCallback(() => {
    simulationRef.current?.alpha(1).restart()
  }, [])

  return (
    <div
      className={cn(
        "flex min-h-screen items-center justify-center bg-background p-4 md:p-8",
        className
      )}
    >
      <Card className="w-full max-w-5xl shadow-sm">
        <CardHeader className="border-b border-border pb-4">
          <CardTitle>Beziehungsnetzwerk</CardTitle>
          <CardDescription>
            Zieh Knoten, um das Layout zu erkunden. Verbindungen folgen den
            Beziehungen im Datensatz.
          </CardDescription>
          <CardAction className="flex flex-wrap items-center justify-end gap-2">
            <Badge variant="secondary">{data.nodes.length} Personen</Badge>
            <Badge variant="outline">{data.links.length} Verbindungen</Badge>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={restartLayout}
            >
              <RefreshCw />
              Layout neu
            </Button>
          </CardAction>
        </CardHeader>

        <CardContent className="pt-2 pb-0">
          <div className="overflow-hidden rounded-lg border border-border bg-muted/30">
            <svg
              ref={svgRef}
              role="img"
              aria-label="Kraftgesteuertes Graphdiagramm der Personen und Verbindungen"
              className="block aspect-[4/3] h-auto w-full max-h-[min(70vh,640px)] min-h-[320px]"
            />
          </div>
        </CardContent>

        <CardFooter className="text-muted-foreground text-xs">
          Kanten nutzen die Rahmenfarbe; Avatare sind mit Primärfarbe umrandet —
          angepasst an dein shadcn-Theme (inkl. Dark Mode).
        </CardFooter>
      </Card>
    </div>
  )
}
