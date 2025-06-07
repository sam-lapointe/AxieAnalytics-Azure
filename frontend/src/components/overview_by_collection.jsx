import "react";
import { useState, useEffect } from "react";
import { CardCollection } from "./card_collection";
import { TitleAndDefaultTimerange } from "./title_and_default_timerange";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
  } from "@/components/ui/carousel";

export function OverviewByCollection({data}) {
    const [isLoading, setIsLoading] = useState(false);
    const [timeframe, setTimeframe] =useState("24h")

    // Set the variables for the data of each collection.

    return (
        <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
            <div className="row-span-2">
                <TitleAndDefaultTimerange title="Overall By Collection"/>
            </div>

            <div className="flex justify-center w-full max-w-full relative overflow-hidden">
                <Carousel
                    opts={{
                        align: "start",
                    }}
                    className="w-full"
                    >
                    <CarouselContent>
                        {Array.from({ length: 9 }).map((_, index) => (
                        <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">
                            <CardCollection />
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