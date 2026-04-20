import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

interface SiteHeaderProps {
    title: string;
}

export default function SiteHeader({ title }: SiteHeaderProps) {
  return (
    <header className="flex w-full items-center gap-4 border-b px-4 py-2">
        <SidebarTrigger className="cursor-pointer" />
        <div className="flex h-4 items-center">
            <Separator orientation="vertical" />
        </div>
        <h1 className="text-base font-medium">{title}</h1>
    </header>
  )
}
