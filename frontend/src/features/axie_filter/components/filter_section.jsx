import "react"
import { useState } from "react"
import { Timeframe } from "./timeframe"
import { SearchParts } from "./search_parts"
import { SelectClass } from "./select_class"
import { FilterSlider } from "./filter_slider"
import { SelectCollection } from "./select_collection"
import { SelectedFilter } from "./selected_filter"
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


export function FilterSection({timeframe, setTimeframe}) {
    const [parts, setParts] = useState(test_parts)
    const [selectedParts, setSelectedParts] = useState({})
    const [selectedClasses, setSelectedClasses] = useState([])
    const [levelRange, setLevelRange] = useState([1, 60])
    const [breedCountRange, setBreedCountRange] = useState([0, 7])
    const [evolvedPartsRange, setEvolvedPartsRange] = useState([0, 6])
    const [selectedCollections, setSelectedCollections] = useState({})

    console.log(Object.keys(selectedCollections).map((collection) => {
        console.log(selectedCollections[collection])
    }))

    const onSelectPart = (partName, axieParts, action) => {
        if (partName && axieParts && action) {
            for (let p = 0; p < axieParts.length; p++) {
                const displayName = `${partName}-${axieParts[p]["stage"]}`

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

    const onUnselectPart = (displayName, partInfo) => {
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
                            "partsIds": [...prev[partName]["partsIds"], partWithoutAction].sort((a, b) => a.stage - b.stage)
                        }
                    }
                )
            })
        }
    }

    const onClearParts = () => {
        setSelectedParts({})
        setParts(test_parts)
    }

    const clearAll = () => {
        setTimeframe([30, "days"])
        onClearParts()
        setSelectedClasses([])
        setLevelRange([1, 60])
        setBreedCountRange([0, 7])
        setEvolvedPartsRange([0, 6])
        setSelectedCollections({})
    }

    return (
        <div className="flex flex-wrap items-center gap-2">
            <Dialog>
                <form>
                    <DialogTrigger asChild>
                    <Button variant="outline">Filter</Button>
                    </DialogTrigger>
                    <DialogContent
                        className="sm:max-w-[425px] max-h-[90vh] flex flex-col"
                    >
                        <DialogHeader className="text-left">
                            <DialogTitle className="text-xl ml-2" autoFocus tabIndex={0}>Filter</DialogTitle>
                        </DialogHeader>
                        <DialogDescription className="hidden"/>
                        <div className="grid gap-4 flex-1 overflow-y-auto">
                            <Timeframe value={timeframe} onChange={setTimeframe}/>
                            <SearchParts
                                selectedParts={selectedParts}
                                setSelectedParts={setSelectedParts}
                                onSelectPart={(partName, axieParts, action) => onSelectPart(partName, axieParts, action)}
                                onUnselectPart={(displayName, partInfo) => onUnselectPart(displayName, partInfo)}
                                onClearParts={onClearParts}
                                parts={parts}
                                setParts={setParts}
                            />
                            <SelectClass selectedClasses={selectedClasses} setSelectedClasses={setSelectedClasses}/>
                            <FilterSlider
                                title="Level"
                                min={1}
                                max={60}
                                range={levelRange}
                                setRange={setLevelRange}
                            />
                            <FilterSlider
                                title="Breed Count"
                                min={0}
                                max={7}
                                range={breedCountRange}
                                setRange={setBreedCountRange}
                            />
                            <FilterSlider
                                title="Evolved Parts Count"
                                min={0}
                                max={6}
                                range={evolvedPartsRange}
                                setRange={setEvolvedPartsRange}
                            />
                            <SelectCollection collections={selectedCollections} setCollections={setSelectedCollections}/>
                        </div>
                        <DialogFooter>
                            <Button
                                variant="outline"
                                className="hover:border-black"
                                onClick={clearAll}
                            >
                                Clear all
                            </Button>
                            <DialogClose asChild>
                                <Button variant="outline" className="hover:border-black">Apply</Button>
                            </DialogClose>
                        </DialogFooter>
                    </DialogContent>
                </form>
            </Dialog>

            {/* Selected Parts */}
            {Object.keys(selectedParts).map((selectedPart) => {
                return (
                    <SelectedFilter
                        key={selectedPart}
                        text={selectedPart}
                        action={selectedParts[selectedPart]["action"]}
                        removeFilter={() => onUnselectPart(selectedPart, selectedParts[selectedPart])}
                    />
                )
            })}

            {/* Selected Classes */}
            {selectedClasses.map((axieClass) => {
                return (
                    <SelectedFilter
                        key={axieClass}
                        text={axieClass}
                        removeFilter={() => setSelectedClasses(selectedClasses.filter((c) => c !== axieClass))}
                    />
                )
            })}
            
            {/* Selected Level Range */}
            {
                // Does not display if the level range is [1,60].
                (levelRange[0] !== 1 || levelRange[1] !== 60) && (
                <SelectedFilter
                    // If the range is [50,50] the text will be Level 50, else Level 50-55 if the range is [50,55].
                    text={`Level ${levelRange[0]}${levelRange[0] !== levelRange[1] ? `-${levelRange[1]}`: ""}`}
                    removeFilter={() => setLevelRange([1, 60])}
                />
                )
            }

            {/* Selected Breed Count Range */}
            {
                // Does not display if the breed count range is [0,7].
                (breedCountRange[0] !== 0 || breedCountRange[1] !== 7) && (
                <SelectedFilter
                    // If the range is [2,2] the text will be Breed 2, else Breed 2-5 if the range is [2,5].
                    text={`Breed ${breedCountRange[0]}${breedCountRange[0] !== breedCountRange[1] ? `-${breedCountRange[1]}`: ""}`}
                    removeFilter={() => setBreedCountRange([0, 7])}
                />
                )
            }

            {/* Selected Evolved Parts Range */}
            {
                // Does not display if the evolved parts range is [0,6].
                (evolvedPartsRange[0] !== 0 || evolvedPartsRange[1] !== 6) && (
                <SelectedFilter
                    // If the range is [2,2] the text will be Evolved 2, else Evolved 2-5 if the range is [2,5].
                    text={`Evolved ${evolvedPartsRange[0]}${evolvedPartsRange[0] !== evolvedPartsRange[1] ? `-${evolvedPartsRange[1]}`: ""}`}
                    removeFilter={() => setEvolvedPartsRange([0, 6])}
                />
                )
            }

            {/* Selected Collections */}
            {Object.keys(selectedCollections).map((collection) => {
                return (
                    <SelectedFilter
                        text={
                            selectedCollections[collection]["numParts"]
                                ? `${collection} ${selectedCollections[collection]["numParts"][0]}-${selectedCollections[collection]["numParts"][1]}`
                                : `${collection}`
                        }
                        removeFilter={() => Object.fromEntries(
                            Object.entries(selectedCollections).filter(([c]) => c !== collection)
                        )}
                    />
                )
            })}

            <Button
                variant="outline"
                onClick={clearAll}
            >
                Clear All
            </Button>
        </div>
    )
}