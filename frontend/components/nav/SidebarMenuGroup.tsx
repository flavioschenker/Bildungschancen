import Link from 'next/link';
import { Icon } from '@tabler/icons-react';
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"


interface SidebarMenuGroupItem {
    name: string
    url: string,
    icon: Icon;
}

interface SidebarMenuGroupProps {
    label: string | null;
    items: SidebarMenuGroupItem[]
}

export default function SidebarMenuGroup({ label, items}: SidebarMenuGroupProps) {
    return (
        <SidebarGroup>
            {label ? <SidebarGroupLabel>{label}</SidebarGroupLabel> : null}
            <SidebarGroupContent>
                <SidebarMenu>
                    {items.map(item => (
                        <SidebarMenuItem key={item.url}>
                            <SidebarMenuButton asChild>
                                <Link href={item.url}>
                                    <item.icon/>
                                    <span>{item.name}</span>
                                </Link>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                    ))}
                </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>        
    )
}