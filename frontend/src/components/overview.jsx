import "react";
import { useState, useEffect } from "react";
import { ChartOverview } from "./chart_overview";
import { Button } from "@/components/ui/button";
import eth_logo from "../assets/eth_logo.svg"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"


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


export function Overview() {
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
            <div className="flex row-span-2">
                <h1 className="font-bold text-2xl">Overall Axies Stats</h1>

                {/* Buttons for medium and up */}
                <div className="md:flex gap-3 ml-auto hidden">
                    <Button>24H</Button>
                    <Button>7D</Button>
                    <Button>30D</Button>
                </div>

                {/* Dropdown for small screens */}
                <div className="md:hidden ml-auto">
                    <Select defaultValue="24h">
                        <SelectTrigger>
                            <SelectValue placeholder="24H" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                            <SelectItem value="24h">24H</SelectItem>
                            <SelectItem value="7d">7D</SelectItem>
                            <SelectItem value="30d">30D</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 col-span-full">
                <ChartOverview data={chartData} label="Total Sales" keyName="Axies Sold"/>
                <ChartOverview data={chartData} label={insert_eth_logo("Total Volume")} keyName="ETH"/>
                <ChartOverview data={chartData} label={insert_eth_logo("Average Price")} keyName="ETH"/>
            </div>
        </div>
    )
}