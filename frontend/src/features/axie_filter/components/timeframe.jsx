import "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
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
    return (
        <div>
            <h3 className="text-lg font-medium">Timeframe</h3>
            
            <div className="flex gap-3">
                <p>Last</p>
                <Input id="timeNum" name="timeNum" type="number" defaultValue={30} min={0}/>
            </div>
        </div>
    )
}