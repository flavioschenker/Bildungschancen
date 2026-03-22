import ForceGraph from "@/components/ForceGraph";
import GraphSearch from "@/components/GraphSearch";

export default async function Dashboard() {
  return (
    <div className="h-screen w-full flex flex-col">
      <GraphSearch/>
      <ForceGraph/>
    </div>
  );
}