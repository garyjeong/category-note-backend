import { describe, it, expect, beforeEach } from "vitest";
import { useAuthStore } from "./auth";
import type { User, AuthTokens } from "@/types";

describe("Auth Store", () => {
	beforeEach(() => {
		// Reset store before each test
		useAuthStore.getState().clearAuth();
	});

	it("should initialize with default state", () => {
		const state = useAuthStore.getState();

		expect(state.user).toBeNull();
		expect(state.tokens).toBeNull();
		expect(state.isAuthenticated).toBe(false);
		expect(state.isLoading).toBe(false);
	});

	it("should set authentication state", () => {
		const mockUser: User = {
			id: "1",
			email: "test@example.com",
			username: "testuser",
			provider: "github",
			provider_id: "123",
			is_active: true,
			is_verified: true,
			created_at: "2024-01-01T00:00:00Z",
			updated_at: "2024-01-01T00:00:00Z",
		};

		const mockTokens: AuthTokens = {
			access_token: "mock-token",
			token_type: "Bearer",
		};

		useAuthStore.getState().setAuth(mockUser, mockTokens);

		const state = useAuthStore.getState();
		expect(state.user).toEqual(mockUser);
		expect(state.tokens).toEqual(mockTokens);
		expect(state.isAuthenticated).toBe(true);
		expect(state.isLoading).toBe(false);
	});

	it("should clear authentication state", () => {
		const mockUser: User = {
			id: "1",
			email: "test@example.com",
			username: "testuser",
			provider: "github",
			provider_id: "123",
			is_active: true,
			is_verified: true,
			created_at: "2024-01-01T00:00:00Z",
			updated_at: "2024-01-01T00:00:00Z",
		};

		const mockTokens: AuthTokens = {
			access_token: "mock-token",
			token_type: "Bearer",
		};

		// Set auth first
		useAuthStore.getState().setAuth(mockUser, mockTokens);

		// Then clear
		useAuthStore.getState().clearAuth();

		const state = useAuthStore.getState();
		expect(state.user).toBeNull();
		expect(state.tokens).toBeNull();
		expect(state.isAuthenticated).toBe(false);
		expect(state.isLoading).toBe(false);
	});

	it("should set loading state", () => {
		useAuthStore.getState().setLoading(true);
		expect(useAuthStore.getState().isLoading).toBe(true);

		useAuthStore.getState().setLoading(false);
		expect(useAuthStore.getState().isLoading).toBe(false);
	});

	it("should update user information", () => {
		const mockUser: User = {
			id: "1",
			email: "test@example.com",
			username: "testuser",
			provider: "github",
			provider_id: "123",
			is_active: true,
			is_verified: true,
			created_at: "2024-01-01T00:00:00Z",
			updated_at: "2024-01-01T00:00:00Z",
		};

		const mockTokens: AuthTokens = {
			access_token: "mock-token",
			token_type: "Bearer",
		};

		// Set initial auth
		useAuthStore.getState().setAuth(mockUser, mockTokens);

		// Update user
		useAuthStore.getState().updateUser({
			username: "updateduser",
			full_name: "Updated User",
		});

		const state = useAuthStore.getState();
		expect(state.user?.username).toBe("updateduser");
		expect(state.user?.full_name).toBe("Updated User");
		expect(state.user?.email).toBe("test@example.com"); // Should remain unchanged
	});
});
