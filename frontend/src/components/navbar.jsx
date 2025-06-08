import "react"
import { Link } from "react-router-dom"
import { Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"


export function Navbar() {
    return (
        <nav className="w-full m-5 pb-4">
            <div className="relative flex items-center justify-between mx-auto">

                {/* Logo on the left */}
                <h1 className="font-bold text-2xl pl-2">Axie Analytics</h1>

                {/* Desktop Menu Centered */}
                <div className="hidden md:absolute md:flex md:left-1/2 md:transform md:-translate-x-1/2">
                    <NavigationMenu className="flex">
                        <NavigationMenuList className="flex gap-6">
                            <NavigationMenuItem>
                                <NavigationMenuLink className="text-lg font-semibold">
                                    <Link to="/">Home</Link>
                                </NavigationMenuLink>
                            </NavigationMenuItem>
                            <NavigationMenuItem>
                                <NavigationMenuLink className="text-lg font-semibold">
                                    <Link to="/axies">Axies</Link>
                                </NavigationMenuLink>
                            </NavigationMenuItem>
                        </NavigationMenuList>
                    </NavigationMenu>
                </div>

                {/* DropdownMenu for small screens */}
                <div className="md:hidden mr-10 relative">
                    <DropdownMenu modal={false}>
                        <DropdownMenuTrigger asChild>
                            <Button
                                variant="ghost"
                                size="icon"
                            >
                                <Menu className="size-6"/>
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem asChild>
                                <a href="/">Home</a>
                            </DropdownMenuItem>
                            <DropdownMenuItem asChild>
                                <a href="/about">Axies</a>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>
        </nav>
    )
}