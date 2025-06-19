import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User, AuthTokens } from "@/types";

interface AuthState {
	user: User | null;
	tokens: AuthTokens | null;
	isAuthenticated: boolean;
	isLoading: boolean;
}

interface AuthActions {
	setAuth: (user: User, tokens: AuthTokens) => void;
	clearAuth: () => void;
	setLoading: (loading: boolean) => void;
	updateUser: (user: Partial<User>) => void;
}

type AuthStore = AuthState & AuthActions;

export const useAuthStore = create<AuthStore>()(
	persist(
		(set, get) => ({
			// State
			user: null,
			tokens: null,
			isAuthenticated: false,
			isLoading: false,

			// Actions
			setAuth: (user, tokens) => {
				set({
					user,
					tokens,
					isAuthenticated: true,
					isLoading: false,
				});
			},

			clearAuth: () => {
				set({
					user: null,
					tokens: null,
					isAuthenticated: false,
					isLoading: false,
				});
			},

			setLoading: (loading) => {
				set({ isLoading: loading });
			},

			updateUser: (userData) => {
				const currentUser = get().user;
				if (currentUser) {
					set({
						user: { ...currentUser, ...userData },
					});
				}
			},
		}),
		{
			name: "auth-storage",
			partialize: (state) => ({
				user: state.user,
				tokens: state.tokens,
				isAuthenticated: state.isAuthenticated,
			}),
		}
	)
);
