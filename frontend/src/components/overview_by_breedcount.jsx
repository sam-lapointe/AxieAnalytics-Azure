import "react"
import { TitleAndDefaultTimerange } from "./title_and_default_timerange"
import { OverviewBarChart } from "./overview_bar_chart"


export function OverviewByBreedCount({data}) {
    return (
        <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
            <div className="row-span-2">
                <TitleAndDefaultTimerange title="Normal Axies Sold By Breed Count"/>
            </div>
            
            <div>
                <OverviewBarChart />
            </div>
        </div>
    )
}