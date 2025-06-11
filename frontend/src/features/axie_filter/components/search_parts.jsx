import "react"
import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Popover,
  PopoverContent,
  PopoverAnchor,
  PopoverTrigger,
} from "@/components/ui/popover"


const test_parts = {
    "Anemone": {
        "class": "Aquatic",
        "partsIds": [
            {"id": "anemone", "stage": 1},
            {"id": "anemone-2", "stage": 2}
        ]
    },
    "Arco": {
        "class": "Beast",
        "partsIds": [
            {"id": "arco", "stage": 1},
            {"id": "arco-2", "stage": 2}
        ]
    },
    "Croc": {
        "class": "Reptile",
        "partsIds": [
            {"id": "croc", "stage": 1},
            {"id": "croc-2", "stage": 2}
        ]
    },
    "Nimo": {
        "class": "Aquatic",
        "partsIds": [
            {"id": "nimo", "stage": 1},
            {"id": "nimo-2", "stage": 2}
        ]
    },
    "Antenna": {
        "class": "Bug",
        "partsIds": [
            {"id": "antenna", "stage": 1},
            {"id": "antenna-2", "stage": 2}
        ]
    }
}


export function SearchParts() {
    const [parts, setParts] = useState(test_parts)
    const [selectedParts, setSelectedParts] = useState({})
    const [inputValue, setInputValue] = useState("")
    const [isInputFocus, setIsInputFocus] = useState(false)

    const inputRef = useRef(null)

    const handleButtonClick = (axieParts, action) => {
        if (inputRef.current) {
            inputRef.current.focus()
        }
        console.log(axieParts, action)
    }

    return (
        <div>
            <h3 className="text-lg font-medium">Parts</h3>
            
            <div className="">
                <Popover open={isInputFocus}>
                    <PopoverAnchor asChild>
                        <Input
                            ref={inputRef}
                            placeholder="Search parts..."
                            onFocus={() => setIsInputFocus(true)}
                            // onBlur={() => setIsInputFocus(false)}
                            onChange={(e) => {setInputValue(e.target.value)}}
                            className = "focus-visible:ring-0 focus-visible:ring-offset-0 focus:outline-none"
                        />
                    </PopoverAnchor>
                    <PopoverContent
                        onOpenAutoFocus={(e) => e.preventDefault()}
                        onPointerDownOutside={(e) => {
                            const target = e.target
                            if (inputRef.current && inputRef.current.contains(target)) {
                                e.preventDefault
                            } else {
                                setIsInputFocus(false)
                            }
                        }}
                        className="w-full min-w-[var(--radix-popover-trigger-width)] max-h-90 overflow-y-auto"
                    >
                        <div>
                            {Object.keys(parts).map((part) => {
                                if (part.toLowerCase().startsWith(inputValue.toLowerCase())) {
                                    return (
                                        <div className="m-2 bg-gray-100 p-2 rounded-xl mb-4" key={part}>
                                            <div className="flex">
                                                <p className="font-bold">{part}</p>
                                                <div className="ml-auto gap-2 flex">
                                                    <Button
                                                        className="w-14 h-6 text-xs"
                                                        size="icon"
                                                        onClick={() => handleButtonClick(parts[part]["partsIds"], "include")}
                                                    >
                                                        Include
                                                    </Button>
                                                    <Button className="w-14 h-6 text-xs" size="icon">Exclude</Button>
                                                </div>
                                            </div>
                                            {
                                                parts[part]["partsIds"].map((item) => {
                                                    return (
                                                        <div className="flex items-center" key={item.id}>
                                                            <p className="text-sm">Stage {item.stage}</p>
                                                                <div className="ml-auto gap-2 flex">
                                                                <Button className="w-10, h-4" size="icon">+</Button>
                                                                <Button className="w-10 h-4" size="icon">-</Button>
                                                            </div>
                                                        </div>
                                                    )
                                                })
                                            }
                                        </div>
                                    )
                                }
                            })}
                        </div>
                    </PopoverContent>
                </Popover>
            </div>
        </div>
    )
}