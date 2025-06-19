'use client'

import { useState } from 'react'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/lib/api'
import type { OAuthProvider } from '@/types'
import { Github, Chrome, Loader2, Sparkles } from 'lucide-react'
import { cn } from '@/lib/utils'

export function LoginPage() {
  const { isLoading, setLoading } = useAuthStore()
  const [error, setError] = useState<string | null>(null)

  const handleOAuthLogin = async (provider: OAuthProvider) => {
    try {
      setError(null)
      setLoading(true)
      
      // Redirect to backend OAuth endpoint
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/login/${provider}`
    } catch (err) {
      setError('Something went wrong. Please try again.')
      console.error('OAuth login error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div 
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden"
      data-testid="login-container"
    >
      {/* Animated background elements - 2025 trend: subtle animations */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl animate-pulse delay-2000" />
      </div>

      {/* Main login container with glassmorphism effect */}
      <div className="relative z-10 w-full max-w-md mx-4">
        <div 
          className={cn(
            "backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl p-8 shadow-2xl",
            "dark-mode-support", // For testing
            "hover:bg-white/15 transition-all duration-500 ease-out" // Micro-interaction
          )}
        >
          {/* Header with modern typography */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Sparkles className="w-8 h-8 text-blue-400 mr-2 animate-pulse" />
              <h1 className="text-3xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-transparent">
                Welcome Back
              </h1>
            </div>
            <p className="text-slate-300 text-sm">
              Sign in to your account to continue
            </p>
          </div>

          {/* Error message */}
          {error && (
            <div className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-200 text-sm">
              {error}
            </div>
          )}

          {/* Social login buttons - 2025 trend: Social login priority */}
          <div className="space-y-4">
            {/* GitHub - Primary button */}
            <button
              onClick={() => handleOAuthLogin('github')}
              disabled={isLoading}
              className={cn(
                "w-full flex items-center justify-center gap-3 px-6 py-4 rounded-2xl font-medium transition-all duration-300",
                "bg-gradient-to-r from-gray-800 to-gray-900 hover:from-gray-700 hover:to-gray-800",
                "border border-gray-600 hover:border-gray-500",
                "text-white shadow-lg hover:shadow-xl",
                "transform hover:scale-[1.02] active:scale-[0.98]", // Micro-interaction
                "disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none",
                "btn-primary hover-effect" // For testing
              )}
              aria-label="Continue with GitHub"
              tabIndex={0}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" data-testid="loading-spinner" />
              ) : (
                <Github className="w-5 h-5" />
              )}
              <span>Continue with GitHub</span>
            </button>

            {/* Google - Secondary button */}
            <button
              onClick={() => handleOAuthLogin('google')}
              disabled={isLoading}
              className={cn(
                "w-full flex items-center justify-center gap-3 px-6 py-4 rounded-2xl font-medium transition-all duration-300",
                "bg-white/10 hover:bg-white/20 backdrop-blur-sm",
                "border border-white/20 hover:border-white/30",
                "text-white shadow-lg hover:shadow-xl",
                "transform hover:scale-[1.02] active:scale-[0.98]", // Micro-interaction
                "disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none",
                "btn-secondary hover-effect" // For testing
              )}
              aria-label="Continue with Google"
              tabIndex={0}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" data-testid="loading-spinner" />
              ) : (
                <Chrome className="w-5 h-5" />
              )}
              <span>Continue with Google</span>
            </button>
          </div>

          {/* Footer */}
          <div className="mt-8 text-center">
            <p className="text-slate-400 text-xs">
              By continuing, you agree to our{' '}
              <a href="/terms" className="text-blue-400 hover:text-blue-300 transition-colors">
                Terms of Service
              </a>{' '}
              and{' '}
              <a href="/privacy" className="text-blue-400 hover:text-blue-300 transition-colors">
                Privacy Policy
              </a>
            </p>
          </div>
        </div>

        {/* Additional visual elements */}
        <div className="mt-6 text-center">
          <p className="text-slate-500 text-sm">
            New to our platform?{' '}
            <span className="text-blue-400 cursor-pointer hover:text-blue-300 transition-colors">
              Learn more
            </span>
          </p>
        </div>
      </div>
    </div>
  )
} 