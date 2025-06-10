import "react"
import { Timeframe } from "./timeframe"
import { SearchParts } from "./search_parts"
import { SelectClass } from "./select_class"
import { SelectLevel } from "./select_level"
import { SelectBreedCount } from "./select_breed_count"
import { SelectCollection } from "./select_collection"
import { Button } from "@/components/ui/button"
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
                <DialogContent
                    className="sm:max-w-[425px] max-h-[90vh] flex flex-col"
                >
                    <DialogHeader className="text-left">
                        <DialogTitle className="text-xl" autoFocus tabIndex={0}>Filter</DialogTitle>
                    </DialogHeader>
                    <DialogDescription className="hidden"/>
                    <div className="grid gap-4 flex-1 overflow-y-auto">
                        <Timeframe />
                        <SearchParts />
                        <SelectClass />
                        <SelectLevel />
                        <SelectBreedCount />
                        <SelectCollection />
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