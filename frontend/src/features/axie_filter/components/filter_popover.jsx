import "react"
import { Timeframe } from "./timeframe"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog"


  export function FilterPopover() {
    return (
        <Dialog>
            <form>
                <DialogTrigger asChild>
                <Button variant="outline">Filter</Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader className="text-left">
                        <DialogTitle className="text-xl">Filter</DialogTitle>
                    </DialogHeader>
                    <DialogDescription className="hidden"/>
                    <div className="grid gap-4">
                        <Timeframe />
                        <div className="grid gap-3">
                            <Label htmlFor="username-1">Username</Label>
                            <Input id="username-1" name="username" defaultValue="@peduarte" />
                        </div>
                    </div>
                    <DialogFooter>
                        <DialogClose asChild>
                            <Button variant="outline">Apply</Button>
                        </DialogClose>
                    </DialogFooter>
                </DialogContent>
            </form>
        </Dialog>
    )
  }