import "react"

import { CardCollection } from "./card_collection";
import { Button } from "@/components/ui/button";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
  } from "@/components/ui/carousel"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

export function OverviewByCollection() {
    return (
        <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
            <div className="flex row-span-2">
                <h1 className="font-bold text-2xl">Overall By Collection</h1>

                {/* Buttons for medium and up */}
                <div className="md:flex gap-3 ml-auto hidden">
                    <Button>24H</Button>
                    <Button>7D</Button>
                    <Button>30D</Button>
                </div>

                {/* Dropdown for small screens */}
                <div className="md:hidden ml-auto">
                    <Select defaultValue="24h">
                        <SelectTrigger>
                            <SelectValue placeholder="24H" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                            <SelectItem value="24h">24H</SelectItem>
                            <SelectItem value="7d">7D</SelectItem>
                            <SelectItem value="30d">30D</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
            </div>
            <div className="flex justify-center mt-6 w-full max-w-full relative overflow-hidden">
                <Carousel
                    opts={{
                        align: "start",
                    }}
                    className="w-full"
                    >
                    <CarouselContent>
                        {Array.from({ length: 8 }).map((_, index) => (
                        <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">
                            <div className="p-2">
                                <CardCollection />
                            </div>
                        </CarouselItem>
                        ))}
                    </CarouselContent>
                    <CarouselPrevious className="absolute left-0 top-1/2 -translate-y-1/2 z-10"/>
                    <CarouselNext className="absolute right-0 top-1/2 -translate-y-1/2 z-10"/>
                </Carousel>
            </div>
        </div>
    )
}