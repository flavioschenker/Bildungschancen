import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group"
import { SearchIcon } from "lucide-react"

export default function GraphSearch() {
    return (
        <div className="p-4 flex w-full h-40 border-b z-50 border-gray-100 shadow-sm">
            
        <InputGroup>
            <InputGroupInput id="inline-start-input" placeholder="Search..." />
            <InputGroupAddon align="inline-start">
            <SearchIcon className="text-muted-foreground" />
            </InputGroupAddon>
        </InputGroup>

        </div>
    )
}