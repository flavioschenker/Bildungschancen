import SiteHeader from "@/components/basic/SiteHeader"
import InputForm from "@/features/skills/components/InputForm"

export default function SkillsPage() {
    return (
        <>
            <SiteHeader title="Meine Fähigkeiten"/>
            <main className="p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <InputForm />
            </main>
        </>
    )
}