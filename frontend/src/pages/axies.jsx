import "react"
import axios from "axios"
import { useState, useEffect } from "react"
import { Overview } from "../components/overview.jsx"
import { FilterSection } from "../features/axie_filter/components/filter_section.jsx"
import { ResultSection } from "../features/axie_sales/components/result_section.jsx"


// Temporary data for testing only
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
    const [isLoading, setIsLoading] = useState({})

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [responseOverview] = await Promise.all([
                    axios.get(
                        "https://dev.api.axieanalytics.com/axies/graph/overview"
                    ),
                ])

                setOverviewData(responseOverview.data)
                setIsLoading(false)
            } catch (err) {
                setError(err.message || "An error occured.")
            }
        }

        fetchData()
    }, [])

    return (
        <>
            <Overview
                title="Search Overview"
                data={isLoading ? overviewData : overviewData[`${timeframe[0]}${timeframe[1][0]}`]}
                timeframe={timeframe}
                setTimeframe={setTimeframe}
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
                    <ResultSection />
                </div>
            </div>
        </>
    )
}