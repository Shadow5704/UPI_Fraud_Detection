"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Shield, TrendingUp, Lock, Brain } from "lucide-react";

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.push("/dashboard");
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-full blur-3xl opacity-30 animate-pulse-slow"></div>
                <Shield className="relative h-24 w-24 text-primary-600" />
              </div>
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary-600 via-purple-600 to-pink-600 mb-6 animate-gradient">
              UPI Fraud Detection
            </h1>

            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto">
              Powered by Advanced CNN Machine Learning
            </p>

            <div className="flex gap-4 justify-center flex-wrap">
              <button
                onClick={() => router.push("/login")}
                className="px-8 py-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
              >
                Get Started
              </button>
              <button
                onClick={() => router.push("/register")}
                className="px-8 py-4 bg-white text-primary-600 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 border-2 border-primary-600"
              >
                Create Account
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <h2 className="text-4xl font-bold text-center mb-16 text-gray-800">
          Why Choose Our System?
        </h2>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 border border-gray-100">
            <div className="bg-gradient-to-br from-primary-500 to-primary-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-800">
              CNN-Powered Detection
            </h3>
            <p className="text-gray-600">
              Advanced Convolutional Neural Networks analyze transaction
              patterns to identify fraud with unprecedented accuracy.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 border border-gray-100">
            <div className="bg-gradient-to-br from-purple-500 to-purple-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
              <TrendingUp className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-800">
              Real-Time Analysis
            </h3>
            <p className="text-gray-600">
              Instant fraud detection on every transaction, providing immediate
              alerts for suspicious activities.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 border border-gray-100">
            <div className="bg-gradient-to-br from-pink-500 to-pink-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
              <Lock className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-800">
              Secure & Reliable
            </h3>
            <p className="text-gray-600">
              Bank-grade security with encrypted data transmission and secure
              authentication mechanisms.
            </p>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 text-white text-center">
            <div>
              <div className="text-5xl font-bold mb-2">99.5%</div>
              <div className="text-primary-100">Detection Accuracy</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">&lt;1s</div>
              <div className="text-primary-100">Response Time</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">24/7</div>
              <div className="text-primary-100">Monitoring</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">100%</div>
              <div className="text-primary-100">Secure</div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            © 2025 UPI Fraud Detection System. Powered by Machine Learning & AI.
          </p>
        </div>
      </footer>
    </div>
  );
}
