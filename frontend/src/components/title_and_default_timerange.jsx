import "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";


export function TitleAndDefaultTimerange({title, customTimeframe=[]}) {

    return (
        <div className="flex items-baseline">
                <h1 className="font-bold text-2xl">{title}</h1>

                {
                    customTimeframe.length === 0 ?
                    (
                        <>
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
                        </>
                    ) : (
                        <div className="ml-auto">
                            <p className="font-semibold">{`Last ${customTimeframe[0]} ${customTimeframe[1]}`}</p>
                        </div>
                    )
                }
        </div>
    )
}