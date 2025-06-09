import "react"
import { useState } from "react"
import { NumberInput } from "./number_input";
import { Input } from "@/components/ui/input"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";


export function Timeframe() {
    const [number, setNumber] = useState(30)

    return (
        <div>
            <h3 className="text-lg font-medium">Timeframe</h3>
            
            <div className="flex gap-3 items-center">
                <p>Last</p>
                {/* <Input
                    id="timeNum"
                    name="timeNum"
                    type="number"
                    defaultValue={30}
                    min={1}
                    className="w-15 h-6"
                /> */}
                <NumberInput
                    value={number}
                    onChange={(newNumber) => setNumber(newNumber)}
                    min={1}
                    max={365}
                    className="!w-15"
                />
                <Select defaultValue="days">
                    <SelectTrigger className="!h-6 py-1 text-sm">
                        <SelectValue placeholder="Days" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                        <SelectItem value="hours">Hours</SelectItem>
                        <SelectItem value="days">Days</SelectItem>
                        </SelectGroup>
                    </SelectContent>
                </Select>
            </div>
        </div>
    )
}