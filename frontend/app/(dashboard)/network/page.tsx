import SiteHeader from "@/components/basic/SiteHeader"
import ForceGraph from "@/components/ForceGraph"

export default function NetworkPage() {
    return (
        <>
            <SiteHeader title="Bildungschance Netzwerk"/>
            <main className="px-4 py-2">
                <ForceGraph/>
            </main>
        </>
    )
}