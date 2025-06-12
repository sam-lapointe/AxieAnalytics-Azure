import "react";
import { useState, useEffect } from "react";
import { OverviewLineChart } from "./overview_line_chart";
import { TitleAndDefaultTimerange } from "./title_and_default_timerange";
import eth_logo from "../assets/eth_logo.svg"


const chartData = [
  { key: "Jan", value: 4000 },
  { key: "Feb", value: 3000 },
  { key: "Mar", value: 2000 },
  { key: "Apr", value: 2780 },
  { key: "May", value: 1890 },
  { key: "Jun", value: 2390 },
  { key: "Jul", value: 3490 },
  { key: "Aug", value: 2000 },
  { key: "Sep", value: 2780 },
  { key: "Oct", value: 1890 },
  { key: "Nov", value: 2390 },
  { key: "Dec", value: 3490 },
];


export function Overview({data, title="Overall Stats", customTimeframe=[]}) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null)

    const insert_eth_logo = (text) => {
        return (
            <div className="flex">
                <p>{text}</p>
                <img src={eth_logo} className="w-4 h-4 ml-2 my-auto"/>
            </div>
        )
    }

    return (
        <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
            <div className="row-span-2">
                <TitleAndDefaultTimerange title={title} customTimeframe={customTimeframe}/>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 col-span-full">
                <OverviewLineChart data={chartData} label="Total Sales" keyName="Axies Sold"/>
                <OverviewLineChart data={chartData} label={insert_eth_logo("Total Volume")} keyName={<img src={eth_logo} className="w-3 h-3 my-auto"/>} />
                <OverviewLineChart data={chartData} label={insert_eth_logo("Average Price")} keyName={<img src={eth_logo} className="w-3 h-3 my-auto"/>} />
            </div>
        </div>
    )
}