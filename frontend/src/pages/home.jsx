import "react"
import { useState, useEffect } from "react"
import { Overview } from "../components/overview.jsx";
import { OverviewByCollection } from "../components/overview_by_collection.jsx";
import { OverviewByBreedCount } from "../components/overview_by_breedcount.jsx";
import axios from "axios"


export function Home() {
    const [overviewData, setOverviewData] = useState({})
    const [overviewTime, setOverviewTime] = useState([1, "days"])
    const [collectionData, setCollectionData] = useState({})
    const [collectionTime, setCollectionTime] = useState([1, "days"])
    const [breedCountData, setBreedCountData] = useState({})
    const [breedCountTime, setBreedCountTime] = useState([1, "days"])
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [responseOverview] = await Promise.all([
                    axios.post(
                        "http://127.0.0.1:8000/axies/graph",
                        {
                            time_unit: overviewTime[1],
                            time_num: overviewTime[0]
                        }
                    )
                ])

                setOverviewData(responseOverview.data)
            } catch (err) {
                setError(err.message || "An error occured.")
            }
        }

        fetchData()
    }, [overviewTime])

    return (
        <>
            <Overview data={overviewData} timeframe={overviewTime} setTimeframe={setOverviewTime}/>
            <OverviewByCollection data={collectionData}/>
            <OverviewByBreedCount data={breedCountData}/>
        </>
    )
}