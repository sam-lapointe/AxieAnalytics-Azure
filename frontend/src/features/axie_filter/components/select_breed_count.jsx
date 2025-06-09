import "react"
import { useState } from "react"
import { NumberInput } from "./number_input"
import * as Slider from "@radix-ui/react-slider"


export function SelectBreedCount() {
    const [breedCountRange, setBreedCountRange] = useState([0, 7])

    const minBreedCount = 0
    const maxBreedCount = 7

    return (
        <div>
            <h3 className="text-lg font-medium">Breed Count</h3>

            <Slider.Root
                className="relative flex items-center select-none touch-none w-full h-6"
                min={minBreedCount}
                max={maxBreedCount}
                step={1}
                minStepsBetweenThumbs={0}
                value={breedCountRange}
                onValueChange={(newRange) => {
                    const [newMin, newMax] = newRange;
                    
                    if (newMin !== breedCountRange[0] && newMin <= breedCountRange[1]) {
                        setBreedCountRange([newMin, breedCountRange[1]])
                    }

                    if (newMax !== breedCountRange[1] && newMax >= breedCountRange[0]) {
                        setBreedCountRange([breedCountRange[0], newMax])
                    }
                }}
            >
                <Slider.Track className="bg-gray-300 relative grow rounded-full h-1">
                    <Slider.Range className="absolute bg-black rounded-full h-full" />
                </Slider.Track>
                <Slider.Thumb
                    className="block w-4 h-4 bg-white border-2 border-black rounded-full shadow hover:bg-blue-100 focus:outline-none"
                    aria-label="Minimum"
                />
                <Slider.Thumb
                    className="block w-4 h-4 bg-white border-2 border-black rounded-full shadow hover:bg-blue-100 focus:outline-none"
                    aria-label="Maximum"
                />
            </Slider.Root>
            <div className="flex items-center columns-3 justify-between text-sm text-gray-600">
                <NumberInput
                    value={breedCountRange[0]}
                    onChange={(newMin) => setBreedCountRange([newMin, breedCountRange[1]])}
                    min={minBreedCount}
                    max={breedCountRange[1]}
                />
                <p className="text-2xl mx-4">-</p>
                <NumberInput
                    value={breedCountRange[1]}
                    onChange={(newMax) => setBreedCountRange([breedCountRange[0], newMax])}
                    min={breedCountRange[0]}
                    max={maxBreedCount}
                />
            </div>
        </div>
    )
}