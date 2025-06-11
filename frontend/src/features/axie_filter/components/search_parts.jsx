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

const partNameButton = "w-14 h-6 text-xs bg-white text-black border-1 border-grey hover:bg-white hover:border-black"
const partStageButton = "w-10 h-4 border-1 bg-white text-black border-grey hover:bg-white hover:border-black"


export function SearchParts() {
    const [parts, setParts] = useState(test_parts)
    const [selectedParts, setSelectedParts] = useState({})
    const [inputValue, setInputValue] = useState("")
    const [isInputFocus, setIsInputFocus] = useState(false)

    const inputRef = useRef(null)

    const handleSelectPart = (partName, axieParts, action) => {
        if (inputRef.current) {
            inputRef.current.focus()
        }

        if (partName && axieParts && action) {
            for (let p = 0; p < axieParts.length; p++) {
                const displayName = `${partName}-${axieParts[p]["stage"]}`

                // Add the part to the selectedParts
                setSelectedParts((prev) => {
                    if (!prev.hasOwnProperty(displayName)) {
                        return (
                            {
                                ...prev,
                                [displayName]: {
                                    ...axieParts[p],
                                    "action": action
                                }
                            }
                        )
                    }
                })

                // Remove the part from the parts[partName][partsIds] list
                setParts((prev) => {
                    return (
                        {
                            ...prev,
                            [partName]: {
                                ...prev[partName],
                                "partsIds": prev[partName]["partsIds"].filter((item) => item.id !== axieParts[p]["id"])
                            }
                        }
                    )
                })
            }
        }
    }

    const handleUnselectPart = (displayName, partInfo) => {
        if (displayName && partInfo) {
            const partName = displayName.split("-")[0]
            const {partAction, ...partWithoutAction} = partInfo

            // Remove the part from the selectedParts
            setSelectedParts((prev) => {
                if (prev.hasOwnProperty(displayName)) {
                    return Object.fromEntries(
                        Object.entries(prev).filter(([p]) => p !== displayName)
                    )
                }
            })

            // Add the part to the parts[partName][partsIds] list
            setParts((prev) => {
                return (
                    {
                        ...prev,
                        [partName]: {
                            ...prev[partName],
                            "partsIds": [...prev[partName]["partsIds"], partWithoutAction]
                        }
                    }
                )
            })
        }
    }

    const clearParts = () => {
        setSelectedParts({})
        setParts(test_parts)
    }

    return (
        <div className="mx-2">
            <div className="flex pb-1">
                <h3 className="text-lg font-medium">Parts</h3>
                <Button
                    size="sm"
                    variant="outline"
                    className="ml-auto w-20 h-7 hover:border-black"
                    onClick={() => clearParts()}
                >
                    Clear Parts
                </Button>
            </div>

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
                        tabIndex={0}
                        onOpenAutoFocus={(e) => e.preventDefault()}
                        onPointerDownOutside={(e) => {
                            const target = e.target
                            if (inputRef.current && inputRef.current.contains(target)) {
                                e.preventDefault
                            } else {
                                setIsInputFocus(false)
                            }
                        }}
                        onWheel={(e) => e.stopPropagation()}
                        onTouchMove={(e) => e.stopPropagation()}
                        className="w-full min-w-[var(--radix-popover-trigger-width)] max-h-90 overflow-y-auto"
                    >
                        <div>
                            {Object.keys(parts).map((part) => {
                                if (
                                    part.toLowerCase().startsWith(inputValue.toLowerCase())
                                    && parts[part]["partsIds"].length > 0
                                ) {
                                    return (
                                        <div className="m-2 bg-gray-100 p-2 rounded-xl mb-4" key={part}>
                                            <div className="flex">
                                                <p className="font-bold">{part}</p>
                                                <div className="ml-auto gap-2 flex">
                                                    <Button
                                                        className={partNameButton}
                                                        size="icon"
                                                        onClick={() => handleSelectPart(part, parts[part]["partsIds"], "include")}
                                                    >
                                                        Include
                                                    </Button>
                                                    <Button
                                                        className={partNameButton}
                                                        size="icon"
                                                        onClick={() => handleSelectPart(part, parts[part]["partsIds"], "exclude")}
                                                    >
                                                        Exclude
                                                    </Button>
                                                </div>
                                            </div>
                                            {
                                                parts[part]["partsIds"].map((item) => {
                                                    return (
                                                        <div className="flex items-center" key={item.id}>
                                                            <p className="text-sm">Stage {item.stage}</p>
                                                                <div className="ml-auto gap-2 flex">
                                                                <Button
                                                                    className={partStageButton}
                                                                    size="icon"
                                                                    onClick={() => handleSelectPart(part, [item], "include")}
                                                                >
                                                                    +
                                                                </Button>
                                                                <Button
                                                                    className={partStageButton}
                                                                    size="icon"
                                                                    onClick={() => handleSelectPart(part, [item], "exclude")}
                                                                >
                                                                    -
                                                                </Button>
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
            <div className="flex flex-wrap gap-2 mt-2">
                {
                    Object.keys(selectedParts).map((selectedPart) => {
                        return (
                            <div key={selectedPart} className="flex items-center align-center border-2 border-gray rounded-lg p-1">
                                <p className="text-xs">{selectedPart}</p>
                                <Button
                                    className="text-xs text-black bg-white shadow-none hover:bg-gray-200 w-4 h-4"
                                    size="icon"
                                    onClick={() => handleUnselectPart(selectedPart, selectedParts[selectedPart])}
                                >
                                    X
                                </Button>
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}