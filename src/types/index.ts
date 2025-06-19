// User types
export interface User {
	id: string;
	email: string;
	username?: string;
	full_name?: string;
	provider: "github" | "google";
	provider_id: string;
	avatar_url?: string;
	is_active: boolean;
	is_verified: boolean;
	created_at: string;
	updated_at: string;
	last_login?: string;
}

// Auth types
export interface AuthTokens {
	access_token: string;
	token_type: string;
}

export interface AuthResponse {
	user: User;
	tokens: AuthTokens;
}

// URL types
export interface Url {
	id: string;
	url: string;
	title?: string;
	description?: string;
	thumbnail?: string;
	created_at: string;
	updated_at: string;
}

// Bookmark types
export interface Bookmark {
	id: string;
	user_id: string;
	url_id: string;
	url: Url;
	notes?: string;
	tags?: string[];
	created_at: string;
	updated_at: string;
}

// API response types
export interface ApiResponse<T> {
	data?: T;
	message?: string;
	error?: string;
}

export interface PaginatedResponse<T> {
	items: T[];
	total: number;
	page: number;
	size: number;
	pages: number;
	has_next: boolean;
	has_prev: boolean;
}

// Form types
export interface LoginFormData {
	email: string;
	password: string;
	rememberMe?: boolean;
}

export interface SignupFormData {
	email: string;
	password: string;
	confirmPassword: string;
	username?: string;
	full_name?: string;
}

// OAuth provider types
export type OAuthProvider = "github" | "google";

// Component props types
export interface AuthLayoutProps {
	children: any;
	title: string;
	subtitle?: string;
}

export interface SocialLoginButtonProps {
	provider: OAuthProvider;
	isLoading?: boolean;
	onClick: () => void;
}
