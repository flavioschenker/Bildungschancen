"use client"
import Link from 'next/link';
import {
  IconDashboard,
  IconUsers,
  IconChartDots3,
  IconAffiliate,
  IconBook,
  IconPlant
} from "@tabler/icons-react"
import { GraduationCap } from "lucide-react"
import { NavUser } from "@/components/nav/User"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import SidebarMenuGroup from '@/components/nav/SidebarMenuGroup';

const data = {
  user: {
    name: "Flavio",
    email: "flavio.schenker@outlook.com",
    avatar: "/avatars/Flavio.jpg",
  }
}

const navPublic = [
  {
    name: "Feed",
    url: "/feed",
    icon: IconDashboard,
  },
  {
    name: "Netzwerk",
    url: "/network",
    icon: IconChartDots3,
  },
  {
    name: "Mitglieder",
    url: "/members",
    icon: IconUsers,
  },
  {
    name: "Bibliothek",
    url: "/library",
    icon: IconBook,
  },
]

const navPrivate = [
  {
    name: "Mein Netzwerk",
    url: "/social",
    icon: IconAffiliate,
  },
  {
    name: "Meine Fähigkeiten",
    url: "/skills",
    icon: IconPlant,
  }
]



export function AppSidebar() {
  return (
    <Sidebar collapsible="icon" variant="inset" >
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:p-1.5!"
            >
              <Link href="/feed">
                <GraduationCap className="size-7!"/>
                <span className="text-xl font-semibold">Bildungschance</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenuGroup label="Der Verein" items={navPublic}/>
        <SidebarMenuGroup label="Persönlich" items={navPrivate}/>
      </SidebarContent>
      <SidebarFooter>
          <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  )
}
