import "react"
import { useState } from "react"
import * as Slider from "@radix-ui/react-slider"
import { NumberInput } from "./number_input"
import { Input } from "@/components/ui/input"


export function SelectLevel() {
    const [levelRange, setLevelRange] = useState([1, 60])

    const minLevel = 1
    const maxLevel = 60

    return (
        <div>
            <h3 className="text-lg font-medium">Level</h3>

            <Slider.Root
                className="relative flex items-center select-none touch-none w-full h-6"
                min={minLevel}
                max={maxLevel}
                step={1}
                minStepsBetweenThumbs={0}
                value={levelRange}
                onValueChange={(newRange) => {
                    const [newMin, newMax] = newRange;
                    
                    if (newMin !== levelRange[0] && newMin <= levelRange[1]) {
                        setLevelRange([newMin, levelRange[1]])
                    }

                    if (newMax !== levelRange[1] && newMax >= levelRange[0]) {
                        setLevelRange([levelRange[0], newMax])
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
                    value={levelRange[0]}
                    onChange={(newMin) => setLevelRange([newMin, levelRange[1]])}
                    min={minLevel}
                    max={levelRange[1]}
                />
                <p className="text-2xl mx-4">-</p>
                <NumberInput
                    value={levelRange[1]}
                    onChange={(newMax) => setLevelRange([levelRange[0], newMax])}
                    min={levelRange[0]}
                    max={maxLevel}
                />
            </div>
        </div>
    )
}