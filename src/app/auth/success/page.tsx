'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/lib/api'
import { Loader2, CheckCircle, XCircle } from 'lucide-react'

export default function AuthSuccessPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { setAuth, setLoading } = useAuthStore()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        const token = searchParams.get('token')
        
        if (!token) {
          setStatus('error')
          setMessage('No authentication token received')
          return
        }

        setLoading(true)
        
        // Get user info with the token
        const user = await authApi.getCurrentUser(token)
        
        // Store auth data
        setAuth(user, { access_token: token, token_type: 'Bearer' })
        
        setStatus('success')
        setMessage('Successfully signed in!')
        
        // Redirect to dashboard after a short delay
        setTimeout(() => {
          router.push('/dashboard')
        }, 2000)
        
      } catch (error) {
        setStatus('error')
        setMessage('Authentication failed. Please try again.')
        console.error('Auth callback error:', error)
        
        // Redirect to login after error
        setTimeout(() => {
          router.push('/auth/login')
        }, 3000)
      } finally {
        setLoading(false)
      }
    }

    handleAuthCallback()
  }, [searchParams, setAuth, setLoading, router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-md w-full mx-4">
        <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl p-8 shadow-2xl text-center">
          {status === 'loading' && (
            <>
              <Loader2 className="w-16 h-16 text-blue-400 animate-spin mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-white mb-2">Signing you in...</h1>
              <p className="text-slate-300">Please wait while we complete your authentication.</p>
            </>
          )}
          
          {status === 'success' && (
            <>
              <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-white mb-2">Welcome!</h1>
              <p className="text-slate-300">{message}</p>
              <p className="text-slate-400 text-sm mt-2">Redirecting to your dashboard...</p>
            </>
          )}
          
          {status === 'error' && (
            <>
              <XCircle className="w-16 h-16 text-red-400 mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-white mb-2">Authentication Failed</h1>
              <p className="text-slate-300">{message}</p>
              <p className="text-slate-400 text-sm mt-2">Redirecting to login page...</p>
            </>
          )}
        </div>
      </div>
    </div>
  )
} 