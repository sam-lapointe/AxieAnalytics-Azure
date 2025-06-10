import "react"
import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Popover,
  PopoverContent,
  PopoverAnchor,
  PopoverTrigger,
} from "@/components/ui/popover"


export function SearchParts() {
    const [parts, setParts] = useState({})
    const [inputValue, setInputValue] = useState("")
    const [isInputFocus, setIsInputFocus] = useState(false)

    return (
        <div>
            <h3 className="text-lg font-medium">Parts</h3>
            
            <div className="">
                <Popover open={isInputFocus}>
                    <PopoverAnchor asChild>
                        <Input 
                            placeholder="Search parts..."
                            onFocus={() => setIsInputFocus(true)}
                            onBlur={() => setIsInputFocus(false)}
                            onChange={(e) => {setInputValue(e.target.value)}}
                            className = "focus-visible:ring-0 focus-visible:ring-offset-0 focus:outline-none"
                        />
                    </PopoverAnchor>
                    <PopoverContent
                        onOpenAutoFocus={(e) => e.preventDefault()}
                        className="w-full min-w-[var(--radix-popover-trigger-width)]"
                    >
                        <div>
                            <p>Hello</p>
                            <p>Hello</p>
                        </div>
                    </PopoverContent>
                </Popover>
            </div>
        </div>
    )
}