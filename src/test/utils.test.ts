import { describe, it, expect } from "vitest";
import { cn } from "@/lib/utils";

describe("cn utility function", () => {
	it("should combine class names correctly", () => {
		expect(cn("px-4", "py-2")).toBe("px-4 py-2");
	});

	it("should handle undefined and null values", () => {
		expect(cn("px-4", undefined, "py-2", null)).toBe("px-4 py-2");
	});

	it("should merge conflicting Tailwind classes", () => {
		expect(cn("px-4", "px-6")).toBe("px-6");
	});

	it("should handle conditional classes", () => {
		const isActive = true;
		expect(cn("base", isActive && "active")).toBe("base active");
	});

	it("should handle empty input", () => {
		expect(cn()).toBe("");
	});
});
