import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { LoginPage } from './LoginPage'

// Mock the auth store
vi.mock('@/stores/auth', () => ({
  useAuthStore: () => ({
    isLoading: false,
    setLoading: vi.fn(),
    setAuth: vi.fn()
  })
}))

// Mock the API
vi.mock('@/lib/api', () => ({
  authApi: {
    initiateOAuth: vi.fn()
  }
}))

describe('LoginPage Component', () => {
  it('should render login page with modern design elements', () => {
    render(<LoginPage />)
    
    // Check for main heading
    expect(screen.getByRole('heading', { name: /welcome back/i })).toBeInTheDocument()
    
    // Check for social login buttons (GitHub and Google)
    expect(screen.getByRole('button', { name: /continue with github/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /continue with google/i })).toBeInTheDocument()
    
    // Check for visual hierarchy elements
    expect(screen.getByText(/sign in to your account/i)).toBeInTheDocument()
  })

  it('should have proper visual hierarchy with primary and secondary actions', () => {
    render(<LoginPage />)
    
    const githubButton = screen.getByRole('button', { name: /continue with github/i })
    const googleButton = screen.getByRole('button', { name: /continue with google/i })
    
    // GitHub should be the primary button (first in order)
    expect(githubButton).toBeInTheDocument()
    expect(googleButton).toBeInTheDocument()
    
    // Check for proper button styling classes (will be added in implementation)
    expect(githubButton).toHaveClass('btn-primary')
    expect(googleButton).toHaveClass('btn-secondary')
  })

  it('should handle OAuth login attempts', async () => {
    const mockInitiateOAuth = vi.fn()
    vi.mocked(require('@/lib/api').authApi.initiateOAuth).mockImplementation(mockInitiateOAuth)
    
    render(<LoginPage />)
    
    const githubButton = screen.getByRole('button', { name: /continue with github/i })
    
    fireEvent.click(githubButton)
    
    await waitFor(() => {
      expect(mockInitiateOAuth).toHaveBeenCalledWith('github')
    })
  })

  it('should show loading state during OAuth process', async () => {
    const mockUseAuthStore = vi.fn()
    mockUseAuthStore.mockReturnValue({
      isLoading: true,
      setLoading: vi.fn(),
      setAuth: vi.fn()
    })
    
    vi.mocked(require('@/stores/auth').useAuthStore).mockImplementation(mockUseAuthStore)
    
    render(<LoginPage />)
    
    // Check for loading indicators
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument()
    
    // Buttons should be disabled during loading
    const githubButton = screen.getByRole('button', { name: /continue with github/i })
    expect(githubButton).toBeDisabled()
  })

  it('should have accessibility features', () => {
    render(<LoginPage />)
    
    // Check for proper ARIA labels
    const githubButton = screen.getByRole('button', { name: /continue with github/i })
    expect(githubButton).toHaveAttribute('aria-label', 'Continue with GitHub')
    
    // Check for keyboard navigation support
    expect(githubButton).toHaveAttribute('tabIndex', '0')
    
    // Check for focus management
    githubButton.focus()
    expect(githubButton).toHaveFocus()
  })

  it('should implement 2025 design trends', () => {
    render(<LoginPage />)
    
    // Check for low-light/dark mode support
    const container = screen.getByTestId('login-container')
    expect(container).toHaveClass('dark-mode-support')
    
    // Check for blur effects and modern styling
    expect(container).toHaveClass('backdrop-blur')
    
    // Check for micro-interactions (hover states will be tested in integration)
    const githubButton = screen.getByRole('button', { name: /continue with github/i })
    expect(githubButton).toHaveClass('hover-effect')
  })

  it('should handle error states gracefully', async () => {
    const mockInitiateOAuth = vi.fn().mockRejectedValue(new Error('OAuth failed'))
    vi.mocked(require('@/lib/api').authApi.initiateOAuth).mockImplementation(mockInitiateOAuth)
    
    render(<LoginPage />)
    
    const githubButton = screen.getByRole('button', { name: /continue with github/i })
    fireEvent.click(githubButton)
    
    await waitFor(() => {
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
    })
  })
}) 