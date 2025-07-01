import "react"
import { useState, useEffect } from "react"
import { Overview } from "../components/overview.jsx";
import { OverviewByCollection } from "../components/overview_by_collection.jsx";
import { OverviewByBreedCount } from "../components/overview_by_breedcount.jsx";
import axios from "axios"


export function Home() {
    const [overviewData, setOverviewData] = useState({
        "total_sales": 0,
        "total_volume_eth": 0,
        "avg_price_eth": 0,
        "chart": [{"sales": 0, "volume": 0, "avg_price_eth": 0}]
    })
    const [overviewTime, setOverviewTime] = useState([1, "days"])
    const [collectionData, setCollectionData] = useState({})
    const [collectionTime, setCollectionTime] = useState([1, "days"])
    const [breedCountData, setBreedCountData] = useState({})
    const [breedCountTime, setBreedCountTime] = useState([1, "days"])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [responseOverview, responseBreedCount] = await Promise.all([
                    axios.get(
                        "http://127.0.0.1:8000/axies/graph/overview"
                    ),
                    axios.get(
                        "http://127.0.0.1:8000/axies/graph/breed_count"
                    )
                ])

                setOverviewData(responseOverview.data)
                setBreedCountData(responseBreedCount.data)
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
                data={isLoading ? overviewData : overviewData[`${overviewTime[0]}${overviewTime[1][0]}`]}
                timeframe={overviewTime}
                setTimeframe={setOverviewTime}
            />
            <OverviewByCollection data={collectionData}/>
            <OverviewByBreedCount
                data={isLoading ? breedCountData : breedCountData[`${breedCountTime[0]}${breedCountTime[1][0]}`]}
                timeframe={breedCountTime}
                setTimeframe={setBreedCountTime}
            />
        </>
    )
}