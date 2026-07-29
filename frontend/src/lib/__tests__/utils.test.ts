import { describe, expect, it } from "vitest"
import { cn } from "../utils"

describe("cn", () => {
  it("merges class names", () => {
    expect(cn("foo", "bar")).toBe("foo bar")
  })

  it("handles conditional classes", () => {
    expect(cn("base", false && "hidden", "visible")).toBe("base visible")
  })

  it("merges tailwind classes correctly", () => {
    expect(cn("px-4 py-2", "px-6")).toBe("py-2 px-6")
  })

  it("handles undefined values", () => {
    expect(cn("foo", undefined, "bar")).toBe("foo bar")
  })

  it("handles empty input", () => {
    expect(cn()).toBe("")
  })
})
