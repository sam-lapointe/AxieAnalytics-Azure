import "react"
import axios from "axios"
import { useRef, useState, useEffect } from "react"
import { Overview } from "../components/overview.jsx"
import { FilterSection } from "../features/axie_filter/components/filter_section.jsx"
import { ResultSection } from "../features/axie_sales/components/result_section.jsx"
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"


// Temporary data for testing only
const test_parts = {
    "Anemone": {
        "type": "Horn",
        "class": "Aquatic",
        "partsIds": [
            {"id": "anemone", "stage": 1},
            {"id": "anemone-2", "stage": 2}
        ]
    },
    "Arco": {
        "type": "Horn",
        "class": "Beast",
        "partsIds": [
            {"id": "arco", "stage": 1},
            {"id": "arco-2", "stage": 2}
        ]
    },
    "Croc": {
        "type": "Mouth",
        "class": "Reptile",
        "partsIds": [
            {"id": "croc", "stage": 1},
            {"id": "croc-2", "stage": 2}
        ]
    },
    "Nimo": {
        "type": "Tail",
        "class": "Aquatic",
        "partsIds": [
            {"id": "nimo", "stage": 1},
            {"id": "nimo-2", "stage": 2}
        ]
    },
    "Antenna": {
        "type": "Horn",
        "class": "Bug",
        "partsIds": [
            {"id": "antenna", "stage": 1},
            {"id": "antenna-2", "stage": 2}
        ]
    }
}

export function Axies() {
    const [timeframe, setTimeframe] = useState([1, "days"])
    const [parts, setParts] = useState(test_parts)
    const [selectedParts, setSelectedParts] = useState({})
    const [selectedClasses, setSelectedClasses] = useState([])
    const [levelRange, setLevelRange] = useState([1, 60])
    const [breedCountRange, setBreedCountRange] = useState([0, 7])
    const [evolvedPartsRange, setEvolvedPartsRange] = useState([0, 6])
    const [selectedCollections, setSelectedCollections] = useState({})
    const [overviewData, setOverviewData] = useState({
        "total_sales": 0,
        "total_volume_eth": 0,
        "avg_price_eth": 0,
        "chart": [{"sales": 0, "volume": 0, "avg_price_eth": 0}]
    })
    const [listData, setListData] = useState([])
    const [page, setPage] = useState(1)
    const [isLoading, setIsLoading] = useState({})
    const [error, setError] = useState(null)

    const debounceTimeout = useRef(null)
    const axiesPerPage = 60 // Number of axies per page

    useEffect(() => {
        // Clear previous timeout if it exists
        if (debounceTimeout.current) {
            clearTimeout(debounceTimeout.current)
        }

        // Set a new timeout
        debounceTimeout.current = setTimeout(() => {
            setPage(1) // Reset to first page on filter change
            fetchData()
        }, 2000)  // 2000ms debounce time

        // Cleanup on unmount
        return () => clearTimeout(debounceTimeout.current)
    }, [
        timeframe,
        selectedParts,
        selectedClasses,
        levelRange,
        breedCountRange,
        evolvedPartsRange,
        selectedCollections
    ])

    async function fetchData() {
        try {
            const body_data = {
                "time_unit": timeframe[1],
                        "time_num": timeframe[0],
                        ...formatSelectedParts(selectedParts),
                        "axie_class": selectedClasses,
                        "level": levelRange,
                        "breed_count": breedCountRange,
                        "evolved_parts_count": evolvedPartsRange,
                        "collections": formatSelectedCollections(selectedCollections)
            }
            const headers = {
                "Content-Type": "application/json"
            }

            const [responseOverview, responseList] = await Promise.all([
                axios.post(
                    "https://dev.api.axieanalytics.com/axies/graph/overview",
                    body_data,
                    headers
                ),
                axios.post(
                    "https://dev.api.axieanalytics.com/axies/list",
                    body_data,
                    headers
                )
            ])

            setOverviewData(responseOverview.data)
            setListData(responseList.data)
            setIsLoading(false)
        } catch (err) {
            setError(err.message || "An error occured.")
        }
    }

    function formatSelectedParts(selectedParts) {
        const includeParts = {
            "eyes": [],
            "ears": [],
            "mouth": [],
            "horn": [],
            "back": [],
            "tail": []
        }
        const excludeParts = JSON.parse(JSON.stringify(includeParts))

        for (const part in selectedParts) {
            if (selectedParts[part]["action"] === "include") {
                includeParts[selectedParts[part]["type"]].push(part)
            } else if (selectedParts[part]["action"] === "exclude") {
                excludeParts[part]["type"].push(part)
            }
        }
        return { includeParts, excludeParts }
    }

    function formatSelectedCollections(selectedCollections) {
        const formattedCollections = []
        for (const collection in selectedCollections) {
            if (collection === "Any Collection") {
                formattedCollections.push({"special": "Any Collection"})
                return formattedCollections
            } else if (collection === "No Collection") {
                formattedCollections.push({"special": "No Collection"})
                return formattedCollections
            } else if (selectedCollections[collection]["numParts"]) {
                formattedCollections.push({
                    "partCollection": collection,
                    "numParts": selectedCollections[collection]["numParts"]
                })
            } else if (!selectedCollections[collection]["numParts"]) {
                formattedCollections.push({
                    "title": collection
                })
            }
        }
        return formattedCollections
    }


    return (
        <>
            <Overview
                title="Search Overview"
                data={overviewData}
                timeframe={timeframe}
                setTimeframe={setTimeframe}
                customTimeframe={true}
            />

            <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
                <div className="row-span-2">
                    <FilterSection 
                        timeframe={timeframe}
                        setTimeframe={setTimeframe}
                        parts={parts}
                        setParts={setParts}
                        selectedParts={selectedParts}
                        setSelectedParts={setSelectedParts}
                        selectedClasses={selectedClasses}
                        setSelectedClasses={setSelectedClasses}
                        levelRange={levelRange}
                        setLevelRange={setLevelRange}
                        breedCountRange={breedCountRange}
                        setBreedCountRange={setBreedCountRange}
                        evolvedPartsRange={evolvedPartsRange}
                        setEvolvedPartsRange={setEvolvedPartsRange}
                        selectedCollections={selectedCollections}
                        setSelectedCollections={setSelectedCollections}
                    />
                </div>

                <div className="">
                    <ResultSection 
                        data={listData}
                    />
                </div>
                <div>
                    <Pagination>
                        <PaginationContent>
                            {page > 1 && (
                                <PaginationItem>
                                <PaginationPrevious href="#" onClick={() => setPage(page - 1)}/>
                            </PaginationItem>
                            )}
                            {page > 2 && (
                                <>
                                <PaginationItem>
                                    <PaginationLink href="#" onClick={() => setPage(1)}>
                                        1
                                    </PaginationLink>
                                </PaginationItem>
                                <PaginationItem>
                                    <PaginationEllipsis />
                                </PaginationItem>
                                </>
                            )}
                            <PaginationItem>
                                <PaginationLink
                                    className="rounded-full border-1 pointer-events-none"
                                >
                                    {page}
                                </PaginationLink>
                            </PaginationItem>
                            {page + 1 <= Math.ceil(overviewData["total_sales"] / axiesPerPage) && (
                                <PaginationItem>
                                    <PaginationLink href="#" onClick={() => setPage(page + 1)}>{page + 1}</PaginationLink>
                                </PaginationItem>
                            )}
                            {page + 2 <= Math.ceil(overviewData["total_sales"] / axiesPerPage) && (
                                <PaginationItem>
                                    <PaginationLink href="#" onClick={() => setPage(page + 2)}>{page + 2}</PaginationLink>
                                </PaginationItem>
                            )}
                            {page + 2 < Math.ceil(overviewData["total_sales"] / axiesPerPage) && (
                                <>
                                <PaginationItem>
                                    <PaginationEllipsis />
                                </PaginationItem>
                                <PaginationItem>
                                    <PaginationLink href="#" onClick={() => setPage(Math.ceil(overviewData["total_sales"] / axiesPerPage))}>
                                        {Math.ceil(overviewData["total_sales"] / axiesPerPage)}
                                    </PaginationLink>
                                </PaginationItem>
                                </>
                            )}
                            {page < Math.ceil(overviewData["total_sales"] / axiesPerPage) && (
                                <PaginationItem>
                                    <PaginationNext href="#" onClick={() => setPage(page + 1)}/>
                                </PaginationItem>
                            )}
                        </PaginationContent>
                    </Pagination>
                </div>
            </div>
        </>
    )
}